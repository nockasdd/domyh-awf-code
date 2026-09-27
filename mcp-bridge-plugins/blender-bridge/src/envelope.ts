/**
 * Bounded responses.
 *
 * A response that was cut and did not say so is worse than a large one: the
 * caller reads "10 objects" as the scene, and every later decision is built on
 * a scene that was never observed. So a truncation is not a shorter string, it
 * is a different shape — `truncated: true` beside the counts that explain what
 * is missing and a cursor that fetches the rest.
 *
 * `items()` is the single funnel every listing goes through, so a new tool
 * cannot accidentally invent a fourth way to truncate.
 */

export const DEFAULT_BYTE_BUDGET = 24_000;
export const DEFAULT_PAGE_LIMIT = 50;
export const MAX_PAGE_LIMIT = 500;

export interface Budget {
  bytes: number;
  truncated: boolean;
  bytes_returned: number;
}

export interface Envelope<T> {
  status: 'ok' | 'error';
  data: T;
  meta: {
    truncated: boolean;
    total_items?: number;
    returned_items?: number;
    next_offset?: number | null;
    bytes_returned: number;
    note?: string;
  };
}

export interface Page {
  items: unknown[];
  total: number;
  nextOffset: number | null;
  truncated: boolean;
}

/** UTF-8 byte length, without allocating a Buffer per call site. */
export function byteLength(text: string): number {
  return Buffer.byteLength(text, 'utf8');
}

/**
 * Slice to a byte budget without splitting a character.
 *
 * `slice` on a code-unit boundary can leave a lone surrogate at the end, which
 * serializes as U+FFFD and silently corrupts the last character. Trimming back
 * to a well-formed boundary costs at most 3 bytes and keeps the output valid.
 */
export function clipToBytes(text: string, maxBytes: number): string {
  if (byteLength(text) <= maxBytes) return text;

  // A generous upper bound: a char is at most 4 bytes, and surrogate pairs are
  // 2 code units, so 2*maxBytes chars can never exceed 4*maxBytes bytes.
  const slice = text.slice(0, maxBytes);
  const buf = Buffer.from(slice, 'utf8').subarray(0, maxBytes);

  let end = buf.length;
  // Walk back to the start of the last character (continuation bytes are
  // 10xxxxxx).
  while (end > 0 && (buf[end - 1] & 0xc0) === 0x80) end--;
  if (end > 0) {
    const lead = buf[end - 1];
    const expected = lead < 0x80 ? 1 : lead >= 0xf0 ? 4 : lead >= 0xe0 ? 3 : lead >= 0xc0 ? 2 : 1;
    // The walk-back lands just past the last lead byte whether or not that
    // character's bytes all fit, so completeness has to be decided here. Without
    // the else, a cut landing exactly on a character boundary keeps the lead
    // byte alone and decodes it to U+FFFD — a 300-byte budget over 3-byte
    // characters would return one replacement char instead of all of them.
    if (end - 1 + expected > buf.length) end--;
    else end = end - 1 + expected;
  }
  return buf.subarray(0, end).toString('utf8');
}

/**
 * One page of a listing, chosen by count and then by byte budget.
 *
 * The count limit bounds the work; the byte limit bounds what the model pays.
 * Both matter, and they fail differently: 50 objects is cheap until one of them
 * has a 4k-character custom property.
 */
export function page<T>(
  all: T[],
  offset: number,
  limit: number,
  budgetBytes: number = DEFAULT_BYTE_BUDGET,
): Page {
  const start = Math.max(0, Math.floor(offset));
  const take = Math.min(Math.max(1, Math.floor(limit)), MAX_PAGE_LIMIT);
  const slice = all.slice(start, start + take);

  const items: unknown[] = [];
  let bytes = 0;
  let truncated = false;

  for (let i = 0; i < slice.length; i++) {
    const size = byteLength(JSON.stringify(slice[i]) ?? '');
    if (bytes + size > budgetBytes && items.length > 0) {
      truncated = true;
      break;
    }
    bytes += size;
    items.push(slice[i]);
  }

  const returned = items.length;
  const nextOffset = start + returned < all.length ? start + returned : null;

  return { items, total: all.length, nextOffset, truncated };
}

/**
 * Cap a free-form string (stdout, a text block) and say what was dropped.
 *
 * The count of dropped bytes is the whole point: without it a caller cannot
 * tell "the script printed nothing" from "we cut it off after 24k".
 */
export function clipText(text: string, maxBytes: number): { text: string; truncated: boolean; bytes_returned: number; bytes_total: number } {
  const total = byteLength(text);
  if (total <= maxBytes) {
    return { text, truncated: false, bytes_returned: total, bytes_total: total };
  }
  const clipped = clipToBytes(text, maxBytes);
  return {
    text: clipped,
    truncated: true,
    bytes_returned: byteLength(clipped),
    bytes_total: total,
  };
}

export function envelope<T>(
  data: T,
  budget: Budget,
  extra: Partial<Envelope<T>['meta']> = {},
): Envelope<T> {
  return {
    status: 'ok',
    data,
    meta: {
      truncated: budget.truncated,
      bytes_returned: budget.bytes_returned,
      ...extra,
    },
  };
}

export function measure<T>(data: T): Budget {
  return { bytes: byteLength(JSON.stringify(data) ?? ''), truncated: false, bytes_returned: byteLength(JSON.stringify(data) ?? '') };
}

export function errorEnvelope(message: string): Envelope<never> {
  return { status: 'error', data: null as never, meta: { truncated: false, bytes_returned: 0, note: message } };
}

/**
 * Merge a listing's page facts into the envelope's meta.
 *
 * The counts are passed explicitly rather than read off a Page because a
 * listing is often paged twice — once inside the generated script and once
 * against the byte budget — and the envelope has to report the scene's real
 * total, not the size of whatever survived the budget.
 */
export function withPage<T>(
  data: T,
  total: number,
  returned: number,
  nextOffset: number | null,
  budget: Budget,
): Envelope<T> {
  return envelope(data, budget, {
    total_items: total,
    returned_items: returned,
    next_offset: nextOffset,
  });
}
