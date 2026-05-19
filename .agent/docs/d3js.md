---
library: d3js
version: 7.x
latest: true
category: data-viz
official_docs: https://d3js.org
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/d3/d3/contents/docs
---

## api

---
next: false
outline: 2
---


# API index

D3 is a collection of modules that are designed to work together; you can use the modules independently, or you can use them together as part of the default build.


## formatLocale(*definition*) {#formatLocale}

```js
const enUs = d3.formatLocale({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
```

[Source](https://github.com/d3/d3-format/blob/main/src/locale.js) · Returns a *locale* object for the specified *definition* with [*locale*.format](#locale_format) and [*locale*.formatPrefix](#locale_formatPrefix) methods. The *definition* must include the following properties:

* `decimal` - the decimal point (e.g., `"."`).
* `thousands` - the group separator (e.g., `","`).
* `grouping` - the array of group sizes (e.g., `[3]`), cycled as needed.
* `currency` - the currency prefix and suffix (e.g., `["$", ""]`).
* `numerals` - optional; an array of ten strings to replace the numerals 0-9.
* `percent` - optional; the percent sign (defaults to `"%"`).
* `minus` - optional; the minus sign (defaults to `"−"`).
* `nan` - optional; the not-a-number value (defaults `"NaN"`).

Note that the *thousands* property is a misnomer, as the grouping definition allows groups other than thousands.


## formatDefaultLocale(*definition*) {#formatDefaultLocale}

```js
const enUs = d3.formatDefaultLocale({
  thousands: ",",
  grouping: [3],
  currency: ["$", ""]
});
```

[Source](https://github.com/d3/d3-format/blob/main/src/defaultLocale.js) · Equivalent to [d3.formatLocale](#formatLocale), except it also redefines [d3.format](#format) and [d3.formatPrefix](#formatPrefix) to the new locale’s [*locale*.format](#locale_format) and [*locale*.formatPrefix](#locale_formatPrefix). If you do not set a default locale, it defaults to [U.S. English](https://github.com/d3/d3-format/blob/main/locale/en-US.json).


## getting started

<script setup>

import ExampleBlankChart from "./components/ExampleBlankChart.vue";

</script>


# Getting started

D3 works in any JavaScript environment.


## Installing from npm

If you’re developing a web application using Node, you can install D3 via yarn, npm, pnpm, or your preferred package manager.

:::code-group

```bash [yarn]
yarn add d3
```

```bash [npm]
npm install d3
```

```bash [pnpm]
pnpm add d3
```

:::

You can then load D3 into your app as:

```js
import * as d3 from "d3";
```

You can instead import specific symbols if you prefer:

```js
import {select, selectAll} from "d3";
```

Alternatively you can install and import from D3 submodules:

```js
import {mean, median} from "d3-array";
```

TypeScript declarations are available via [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped).


## timeFormatLocale(*definition*) {#timeFormatLocale}

```js
const enUs = d3.timeFormatLocale({
  dateTime: "%x, %X",
  date: "%-m/%-d/%Y",
  time: "%-I:%M:%S %p",
  periods: ["AM", "PM"],
  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  shortDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  shortMonths: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
});
```

[Source](https://github.com/d3/d3-time-format/blob/main/src/locale.js) · Returns a *locale* object for the specified *definition* with [*locale*.format](#locale_format), [*locale*.parse](#locale_parse), [*locale*.utcFormat](#locale_utcFormat), [*locale*.utcParse](#locale_utcParse) methods. The *definition* must include the following properties:

* `dateTime` - the date and time (`%c`) format specifier (<i>e.g.</i>, `"%a %b %e %X %Y"`).
* `date` - the date (`%x`) format specifier (<i>e.g.</i>, `"%m/%d/%Y"`).
* `time` - the time (`%X`) format specifier (<i>e.g.</i>, `"%H:%M:%S"`).
* `periods` - the A.M. and P.M. equivalents (<i>e.g.</i>, `["AM", "PM"]`).
* `days` - the full names of the weekdays, starting with Sunday.
* `shortDays` - the abbreviated names of the weekdays, starting with Sunday.
* `months` - the full names of the months (starting with January).
* `shortMonths` - the abbreviated names of the months (starting with January).


## timeFormatDefaultLocale(*definition*) {#timeFormatDefaultLocale}

```js
const enUs = d3.timeFormatDefaultLocale({
  dateTime: "%x, %X",
  date: "%-m/%-d/%Y",
  time: "%-I:%M:%S %p",
  periods: ["AM", "PM"],
  days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
  shortDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  shortMonths: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
});
```

[Source](https://github.com/d3/d3-time-format/blob/main/src/defaultLocale.js) · Equivalent to [d3.timeFormatLocale](#timeFormatLocale), except it also redefines [d3.timeFormat](#timeFormat), [d3.timeParse](#timeParse), [d3.utcFormat](#utcFormat) and [d3.utcParse](#utcParse) to the new locale’s [*locale*.format](#locale_format), [*locale*.parse](#locale_parse), [*locale*.utcFormat](#locale_utcFormat) and [*locale*.utcParse](#locale_utcParse). If you do not set a default locale, it defaults to [U.S. English](https://github.com/d3/d3-time-format/blob/main/locale/en-US.json).


---
