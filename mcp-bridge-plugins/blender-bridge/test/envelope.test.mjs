/**
 * envelope.ts, tested on its own.
 *
 * The e2e suite proves the envelope reaches the caller; it cannot prove the
 * arithmetic is right, because a wrong total_items still arrives as a
 * well-formed page. That is exactly the class of bug worth a test here — the
 * defect I already shipped once, when withPage read its total off a Page whose
 * total was the page length.
 *
 * Node strips the types natively, so this needs no test runner installed.
 *
 * Run: node test/envelope.test.mjs
 */

import {
  DEFAULT_BYTE_BUDGET,
  MAX_PAGE_LIMIT,
  byteLength,
  clipText,
  clipToBytes,
  errorEnvelope,
  measure,
  page,
  withPage,
} from '../src/envelope.ts';

let passed = 0;
let failed = 0;

function check(name, condition, detail) {
  if (condition) {
    passed += 1;
    console.log(`  ok   ${name}`);
  } else {
    failed += 1;
    console.log(`  FAIL ${name}${detail !== undefined ? ` — ${JSON.stringify(detail)}` : ''}`);
  }
}

console.log('byteLength');
check('ascii is one byte per char', byteLength('abc') === 3);
check('a 2-byte char counts as 2', byteLength('é') === 2, byteLength('é'));
check('a 4-byte char counts as 4', byteLength('𝄞') === 4, byteLength('𝄞'));

console.log('clipToBytes');
check('text inside the budget is returned whole', clipToBytes('hello', 100) === 'hello');
check('text exactly at the budget is untouched', clipToBytes('hello', 5) === 'hello');
check('over-budget ascii is cut to length', clipToBytes('hello world', 5).length === 5, clipToBytes('hello world', 5));
check('the result never exceeds the budget', byteLength(clipToBytes('y'.repeat(1000), 37)) <= 37);

// The case that produces U+FFFD if the trim is wrong: a 3-byte char straddling
// the boundary, so the byte cut lands mid-sequence.
const wide = 'あ'.repeat(100);
for (const budget of [1, 2, 3, 4, 5, 7, 8, 11, 13]) {
  const clipped = clipToBytes(wide, budget);
  check(
    `a ${budget}-byte cut of a 3-byte string is valid UTF-8`,
    !clipped.includes('�') && byteLength(clipped) <= budget,
    { clipped, bytes: byteLength(clipped) },
  );
}
check('a 4-byte char is dropped whole rather than split', clipToBytes('𝄞𝄞', 3) === '', clipToBytes('𝄞𝄞', 3));
check('a 4-byte char is kept when it fits exactly', clipToBytes('𝄞𝄞', 4) === '𝄞', clipToBytes('𝄞𝄞', 4));

// A cut landing on a character boundary is the case that used to return a lone
// lead byte: 100 3-byte chars clipped to exactly 300 bytes is not a partial
// character, and decoding the lead byte alone costs the caller the whole string.
check('a cut on a character boundary keeps every whole character', clipToBytes(wide, 300) === wide.slice(0, 100), clipToBytes(wide, 300).length);
check('a 2-byte boundary cut keeps every whole character', clipToBytes('é'.repeat(50), 100) === 'é'.repeat(50), clipToBytes('é'.repeat(50), 100).length);
check('a 4-byte boundary cut keeps every whole character', clipToBytes('𝄞'.repeat(25), 100) === '𝄞'.repeat(25), clipToBytes('𝄞'.repeat(25), 100).length);
check('a boundary cut on mixed widths is still valid', !clipToBytes('aあ𝄞'.repeat(40), 401).includes('�'));

console.log('page');
const five = [{ n: 1 }, { n: 2 }, { n: 3 }, { n: 4 }, { n: 5 }];

const first = page(five, 0, 2);
check('the count limit bounds the page', first.items.length === 2, first.items.length);
check('the total is the list length, not the page', first.total === 5, first.total);
check('next_offset points past what was returned', first.nextOffset === 2, first.nextOffset);

// Bounded but not cut. Reporting truncated here would tell the caller its page
// lost data when nothing was lost.
check('a bounded page is not marked truncated', first.truncated === false, first);

const last = page(five, 4, 10);
check('a page running to the end has no next_offset', last.nextOffset === null, last);
check('a page running to the end is not truncated', last.truncated === false, last);
check('a page past the end is empty, not an error', page(five, 99, 10).items.length === 0);

const byBytes = page(five, 0, 5, 10);
check('the byte budget cuts the page', byBytes.truncated === true, byBytes);
check('the byte cut still reports a cursor', byBytes.nextOffset === byBytes.items.length, byBytes);
check('the byte cut stays inside its budget', byteLength(JSON.stringify(byBytes.items)) <= 10, byBytes);

const huge = page([{ blob: 'z'.repeat(10_000) }], 0, 10, 100);
check('a first item over the budget is still returned', huge.items.length === 1, huge.items.length);
check('returning it does not claim it was cut', huge.truncated === false, huge);

check('limit is capped at the maximum', page(five, 0, 10_000).items.length === Math.min(5, MAX_PAGE_LIMIT));
check('a zero limit still yields one item', page(five, 0, 0).items.length === 1);
check('a negative offset is clamped to the start', page(five, -5, 2).items.length === 2);
check('the default budget is a real bound', DEFAULT_BYTE_BUDGET > 0);

console.log('clipText');
const under = clipText('short', 100);
check('text under the cap is whole', under.truncated === false && under.text === 'short');
check('bytes_returned matches the text', under.bytes_returned === 5, under);
check('bytes_total equals bytes_returned when nothing was cut', under.bytes_total === 5, under);

const over = clipText('q'.repeat(1000), 100);
check('text over the cap is cut', over.truncated === true, over);
check('the cut respects the cap', over.bytes_returned <= 100, over);
check('the original size is still reported', over.bytes_total === 1000, over);
check('the dropped size is recoverable', over.bytes_total - over.bytes_returned === 900, over);

console.log('withPage');
// The regression: the scene's real total, not the page length.
const reported = withPage({ objects: five.slice(0, 2) }, 120, 2, 2, measure({ objects: five.slice(0, 2) }));
check('total_items is the caller total, not the page length', reported.meta.total_items === 120, reported.meta);
check('returned_items counts what came back', reported.meta.returned_items === 2, reported.meta);
check('next_offset is the caller cursor', reported.meta.next_offset === 2, reported.meta);
check('status is ok', reported.status === 'ok');
check('bytes_returned is filled in', reported.meta.bytes_returned > 0, reported.meta);

const cut = withPage({ x: 1 }, 10, 1, 1, { bytes: 5, truncated: true, bytes_returned: 5 });
check('a byte cut is carried into the envelope', cut.meta.truncated === true, cut.meta);
check('measure() reports its own byte size', measure({ a: 'bc' }).bytes === 10, measure({ a: 'bc' }));

console.log('errorEnvelope');
const err = errorEnvelope('no add-on on 127.0.0.1:28782');
check('an error is status error', err.status === 'error');
check('an error carries no data', err.data === null);
check('an error is not truncated', err.meta.truncated === false);
check('the reason is the note', err.meta.note === 'no add-on on 127.0.0.1:28782');
check('an error reports no bytes', err.meta.bytes_returned === 0);

console.log(`\n${passed} passed, ${failed} failed`);
// exitCode rather than process.exit(): the latter cuts the process off while
// stdout is still draining, so the summary can be lost and the run reported as
// passing or failing at random depending on how the output was piped.
process.exitCode = failed === 0 ? 0 : 1;
