---
library: typescript
version: 5.x
latest: true
category: language
official_docs: https://www.typescriptlang.org/docs
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/microsoft/TypeScript-Handbook/contents/pages
---

# Table of contents

[Intersection Types](#intersection-types)

[Union Types](#union-types)

[Type Guards and Differentiating Types](#type-guards-and-differentiating-types)
* [User-Defined Type Guards](#user-defined-type-guards)
  * [Using type predicates](#using-type-predicates)
  * [Using the `in` operator](#using-the-in-operator)
* [`typeof` type guards](#typeof-type-guards)
* [`instanceof` type guards](#instanceof-type-guards)

[Nullable types](#nullable-types)
* [Optional parameters and properties](#optional-parameters-and-properties)
* [Type guards and type assertions](#type-guards-and-type-assertions)

[Type Aliases](#type-aliases)
* [Interfaces vs. Type Aliases](#interfaces-vs-type-aliases)

[String Literal Types](#string-literal-types)

[Numeric Literal Types](#numeric-literal-types)

[Enum Member Types](#enum-member-types)

[Discriminated Unions](#discriminated-unions)
* [Exhaustiveness checking](#exhaustiveness-checking)

[Polymorphic `this` types](#polymorphic-this-types)

[Index types](#index-types)
* [Index types and index signatures](#index-types-and-index-signatures)

[Mapped types](#mapped-types)
* [Inference from mapped types](#inference-from-mapped-types)

[Conditional Types](#conditional-types)
* [Distributive conditional types](#distributive-conditional-types)
* [Type inference in conditional types](#type-inference-in-conditional-types)
* [Predefined conditional types](#predefined-conditional-types)


## Compiler Options


# Run a compile based on a backwards look through the fs for a tsconfig.json
tsc 


# Transpile any .ts files in the folder src, with the default settings
tsc src/*.ts


# Transpile any .ts files in the folder src, with the compiler settings from tsconfig.json
tsc --project tsconfig.json src/*.ts
```


## Constructor functions are equivalent to classes

Before ES2015, Javascript used constructor functions instead of classes.
The compiler supports this pattern and understands constructor functions as equivalent to ES2015 classes.
The property inference rules described above work exactly the same way.

```js
function C() {
    this.constructorOnly = 0
    this.constructorUnknown = undefined
}
C.prototype.method = function() {
    this.constructorOnly = false // error
    this.constructorUnknown = "plunkbat" // OK, the type is string | undefined
}
```


## Classes, functions, and object literals are namespaces

Classes are namespaces in `.js` files.
This can be used to nest classes, for example:

```js
class C {
}
C.D = class {
}
```

And, for pre-ES2015 code, it can be used to simulate static methods:

```js
function Outer() {
  this.y = 2
}
Outer.Inner = function() {
  this.yy = 2
}
```

It can also be used to create simple namespaces:

```js
var ns = {}
ns.C = class {
}
ns.func = function() {
}
```

Other variants are allowed as well:

```js
// IIFE
var ns = (function (n) {
  return n || {};
})();
ns.CONST = 1

// defaulting to global
var assign = assign || function() {
  // code goes here
}
assign.extra = 1
```


## null, undefined, and empty array initializers are of type any or any[]

Any variable, parameter or property that is initialized with null or undefined will have type any, even if strict null checks is turned on.
Any variable, parameter or property that is initialized with [] will have type any[], even if strict null checks is turned on.
The only exception is for properties that have multiple initializers as described above.

```js
function Foo(i = null) {
    if (!i) i = 1;
    var j = undefined;
    j = 2;
    this.l = [];
}
var foo = new Foo();
foo.l.push(foo.i);
foo.l.push("end");
```


## More examples

```js
var someObj = {
  /**
   * @param {string} param1 - Docs on property assignments work
   */
  x: function(param1){}
};

/**
 * As do docs on variable assignments
 * @return {Window}
 */
let someFunc = function(){};

/**
 * And class methods
 * @param {string} greeting The greeting to use
 */
Foo.prototype.sayHi = (greeting) => console.log("Hi!");

/**
 * And arrow functions expressions
 * @param {number} x - A multiplier
 */
let myArrow = x => x * x;

/**
 * Which means it works for stateless function components in JSX too
 * @param {{a: string, b: number}} test - Some param
 */
var fc = (test) => <div>{test.a.charAt(0)}</div>;

/**
 * A parameter can be a class constructor, using Closure syntax.
 *
 * @param {{new(...args: any[]): object}} C - The class to register
 */
function registerClass(C) {}

/**
 * @param {...string} p1 - A 'rest' arg (array) of strings. (treated as 'any')
 */
function fn10(p1){}

/**
 * @param {...string} p1 - A 'rest' arg (array) of strings. (treated as 'any')
 */
function fn9(p1) {
  return p1.join();
}
```


## Patterns that are known NOT to be supported

Referring to objects in the value space as types doesn't work unless the object also creates a type, like a constructor function.

```js
function aNormalFunction() {

}
/**
 * @type {aNormalFunction}
 */
var wrong;
/**
 * Use 'typeof' instead:
 * @type {typeof aNormalFunction}
 */
var right;
```

Postfix equals on a property type in an object literal type doesn't specify an optional property:

```js
/**
 * @type {{ a: string, b: number= }}
 */
var wrong;
/**
 * Use postfix question on the property name instead:
 * @type {{ a: string, b?: number }}
 */
var right;
```

Nullable types only have meaning if `strictNullChecks` is on:

```js
/**
 * @type {?number}
 * With strictNullChecks: true -- number | null
 * With strictNullChecks: off  -- number
 */
var nullable;
```

Non-nullable types have no meaning and are treated just as their original type:

```js
/**
 * @type {!number}
 * Just has type number
 */
var normal;
```

Unlike JSDoc's type system, Typescript only allows you to mark types as containing null or not.
There is no explicit non-nullability -- if strictNullChecks is on, then `number` is not nullable.
If it is off, then `number` is nullable.


---


## Constructor functions

When you declare a class in TypeScript, you are actually creating multiple declarations at the same time.
The first is the type of the *instance* of the class.

```ts
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        return "Hello, " + this.greeting;
    }
}

let greeter: Greeter;
greeter = new Greeter("world");
console.log(greeter.greet()); // "Hello, world"
```

Here, when we say `let greeter: Greeter`, we're using `Greeter` as the type of instances of the class `Greeter`.
This is almost second nature to programmers from other object-oriented languages.

We're also creating another value that we call the *constructor function*.
This is the function that is called when we `new` up instances of the class.
To see what this looks like in practice, let's take a look at the JavaScript created by the above example:

```ts
let Greeter = (function () {
    function Greeter(message) {
        this.greeting = message;
    }
    Greeter.prototype.greet = function () {
        return "Hello, " + this.greeting;
    };
    return Greeter;
})();

let greeter;
greeter = new Greeter("world");
console.log(greeter.greet()); // "Hello, world"
```

Here, `let Greeter` is going to be assigned the constructor function.
When we call `new` and run this function, we get an instance of the class.
The constructor function also contains all of the static members of the class.
Another way to think of each class is that there is an *instance* side and a *static* side.

Let's modify the example a bit to show this difference:

```ts
class Greeter {
    static standardGreeting = "Hello, there";
    greeting: string;
    greet() {
        if (this.greeting) {
            return "Hello, " + this.greeting;
        }
        else {
            return Greeter.standardGreeting;
        }
    }
}

let greeter1: Greeter;
greeter1 = new Greeter();
console.log(greeter1.greet()); // "Hello, there"

let greeterMaker: typeof Greeter = Greeter;
greeterMaker.standardGreeting = "Hey there!";

let greeter2: Greeter = new greeterMaker();
console.log(greeter2.greet()); // "Hey there!"
```

In this example, `greeter1` works similarly to before.
We instantiate the `Greeter` class, and use this object.
This we have seen before.

Next, we then use the class directly.
Here we create a new variable called `greeterMaker`.
This variable will hold the class itself, or said another way its constructor function.
Here we use `typeof Greeter`, that is "give me the type of the `Greeter` class itself" rather than the instance type.
Or, more precisely, "give me the type of the symbol called `Greeter`," which is the type of the constructor function.
This type will contain all of the static members of Greeter along with the constructor that creates instances of the `Greeter` class.
We show this by using `new` on `greeterMaker`, creating new instances of `Greeter` and invoking them as before.


## Functions


# Functions

To begin, just as in JavaScript, TypeScript functions can be created both as a named function or as an anonymous function.
This allows you to choose the most appropriate approach for your application, whether you're building a list of functions in an API or a one-off function to hand off to another function.

To quickly recap what these two approaches look like in JavaScript:

```ts
// Named function
function add(x, y) {
    return x + y;
}

// Anonymous function
let myAdd = function(x, y) { return x + y; };
```

Just as in JavaScript, functions can refer to variables outside of the function body.
When they do so, they're said to *capture* these variables.
While understanding how this works (and the trade-offs when using this technique) is outside of the scope of this article, having a firm understanding how this mechanic works is an important piece of working with JavaScript and TypeScript.

```ts
let z = 100;

function addToZ(x, y) {
    return x + y + z;
}
```


## `this` and arrow functions

In JavaScript, `this` is a variable that's set when a function is called.
This makes it a very powerful and flexible feature, but it comes at the cost of always having to know about the context that a function is executing in.
This is notoriously confusing, especially when returning a function or passing a function as an argument.

Let's look at an example:

```ts
let deck = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    createCardPicker: function() {
        return function() {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker = deck.createCardPicker();
let pickedCard = cardPicker();

alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

Notice that `createCardPicker` is a function that itself returns a function.
If we tried to run the example, we would get an error instead of the expected alert box.
This is because the `this` being used in the function created by `createCardPicker` will be set to `window` instead of our `deck` object.
That's because we call `cardPicker()` on its own.
A top-level non-method syntax call like this will use `window` for `this`.
(Note: under strict mode, `this` will be `undefined` rather than `window`).

We can fix this by making sure the function is bound to the correct `this` before we return the function to be used later.
This way, regardless of how it's later used, it will still be able to see the original `deck` object.
To do this, we change the function expression to use the ECMAScript 6 arrow syntax.
Arrow functions capture the `this` where the function is created rather than where it is invoked:

```ts
let deck = {
    suits: ["hearts", "spades", "clubs", "diamonds"],
    cards: Array(52),
    createCardPicker: function() {
        // NOTE: the line below is now an arrow function, allowing us to capture 'this' right here
        return () => {
            let pickedCard = Math.floor(Math.random() * 52);
            let pickedSuit = Math.floor(pickedCard / 13);

            return {suit: this.suits[pickedSuit], card: pickedCard % 13};
        }
    }
}

let cardPicker = deck.createCardPicker();
let pickedCard = cardPicker();

alert("card: " + pickedCard.card + " of " + pickedCard.suit);
```

Even better, TypeScript will warn you when you make this mistake if you pass the `--noImplicitThis` flag to the compiler.
It will point out that `this` in `this.suits[pickedSuit]` is of type `any`.


# Basic usage
<b><a href="#table-of-contents">↥ back to top</a></b>

In order to use JSX you must do two things.

1. Name your files with a `.tsx` extension
2. Enable the `jsx` option

TypeScript ships with three JSX modes: `preserve`, `react`, and `react-native`.
These modes only affect the emit stage - type checking is unaffected.
The `preserve` mode will keep the JSX as part of the output to be further consumed by another transform step (e.g. [Babel](https://babeljs.io/)).
Additionally the output will have a `.jsx` file extension.
The `react` mode will emit `React.createElement`, does not need to go through a JSX transformation before use, and the output will have a `.js` file extension.
The `react-native` mode is the equivalent of `preserve` in that it keeps all JSX, but the output will instead have a `.js` file extension.

Mode           | Input     | Output                       | Output File Extension
---------------|-----------|------------------------------|----------------------
`preserve`     | `<div />` | `<div />`                    | `.jsx`
`react`        | `<div />` | `React.createElement("div")` | `.js`
`react-native` | `<div />` | `<div />`                    | `.js`

You can specify this mode using either the `--jsx` command line flag or the corresponding option in your [tsconfig.json](./tsconfig.json.md) file.

> *Note: You can specify the JSX factory function to use when targeting react JSX emit with `--jsxFactory` option (defaults to `React.createElement`)


# Factory Functions
<b><a href="#table-of-contents">↥ back to top</a></b>

The exact factory function used by the `jsx: react` compiler option is configurable. It may be set using either the `jsxFactory` command line option, or an inline `@jsx` comment pragma to set it on a per-file basis. For example, if you set `jsxFactory` to `createElement`, `<div />` will emit as `createElement("div")` instead of `React.createElement("div")`.

The comment pragma version may be used like so (in TypeScript 2.8):

```ts
import preact = require("preact");
/* @jsx preact.h */
const x = <div />;
```

emits as:

```ts
const preact = require("preact");
const x = preact.h("div", null);
```

The factory chosen will also affect where the `JSX` namespace is looked up (for type checking information) before falling back to the global one. If the factory is defined as `React.createElement` (the default), the compiler will check for `React.JSX` before checking for a global `JSX`. If the factory is defined as `h`, it will check for `h.JSX` before a global `JSX`.


---


## More examples

```js
var someObj = {
  /**
   * @param {string} param1 - Docs on property assignments work
   */
  x: function(param1){}
};

/**
 * As do docs on variable assignments
 * @return {Window}
 */
let someFunc = function(){};

/**
 * And class methods
 * @param {string} greeting The greeting to use
 */
Foo.prototype.sayHi = (greeting) => console.log("Hi!");

/**
 * And arrow functions expressions
 * @param {number} x - A multiplier
 */
let myArrow = x => x * x;

/**
 * Which means it works for stateless function components in JSX too
 * @param {{a: string, b: number}} test - Some param
 */
var sfc = (test) => <div>{test.a.charAt(0)}</div>;

/**
 * A parameter can be a class constructor, using Closure syntax.
 *
 * @param {{new(...args: any[]): object}} C - The class to register
 */
function registerClass(C) {}

/**
 * @param {...string} p1 - A 'rest' arg (array) of strings. (treated as 'any')
 */
function fn10(p1){}

/**
 * @param {...string} p1 - A 'rest' arg (array) of strings. (treated as 'any')
 */
function fn9(p1) {
  return p1.join();
}
```


## Patterns that are known NOT to be supported

Referring to objects in the value space as types doesn't work unless the object also creates a type, like a constructor function.

```js
function aNormalFunction() {

}
/**
 * @type {aNormalFunction}
 */
var wrong;
/**
 * Use 'typeof' instead:
 * @type {typeof aNormalFunction}
 */
var right;
```

Postfix equals on a property type in an object literal type doesn't specify an optional property:

```js
/**
 * @type {{ a: string, b: number= }}
 */
var wrong;
/**
 * Use postfix question on the property name instead:
 * @type {{ a: string, b?: number }}
 */
var right;
```

Nullable types only have meaning if `strictNullChecks` is on:

```js
/**
 * @type {?number}
 * With strictNullChecks: true  -- number | null
 * With strictNullChecks: false -- number
 */
var nullable;
```

You can also use a union type:
```js
/**
 * @type {number | null}
 * With strictNullChecks: true  -- number | null
 * With strictNullChecks: false -- number
 */
var unionNullable;
```

Non-nullable types have no meaning and are treated just as their original type:

```js
/**
 * @type {!number}
 * Just has type number
 */
var normal;
```

Unlike JSDoc's type system, Typescript only allows you to mark types as containing null or not.
There is no explicit non-nullability -- if strictNullChecks is on, then `number` is not nullable.
If it is off, then `number` is nullable.


# Hello World of Generics

To start off, let's do the "hello world" of generics: the identity function.
The identity function is a function that will return back whatever is passed in.
You can think of this in a similar way to the `echo` command.

Without generics, we would either have to give the identity function a specific type:

```ts
function identity(arg: number): number {
    return arg;
}
```

Or, we could describe the identity function using the `any` type:

```ts
function identity(arg: any): any {
    return arg;
}
```

While using `any` is certainly generic in that it will cause the function to accept any and all types for the type of `arg`, we actually are losing the information about what that type was when the function returns.
If we passed in a number, the only information we have is that any type could be returned.

Instead, we need a way of capturing the type of the argument in such a way that we can also use it to denote what is being returned.
Here, we will use a *type variable*, a special kind of variable that works on types rather than values.

```ts
function identity<T>(arg: T): T {
    return arg;
}
```

We've now added a type variable `T` to the identity function.
This `T` allows us to capture the type the user provides (e.g. `number`), so that we can use that information later.
Here, we use `T` again as the return type. On inspection, we can now see the same type is used for the argument and the return type.
This allows us to traffic that type information in one side of the function and out the other.

We say that this version of the `identity` function is generic, as it works over a range of types.
Unlike using `any`, it's also just as precise (ie, it doesn't lose any information) as the first `identity` function that used numbers for the argument and return type.

Once we've written the generic identity function, we can call it in one of two ways.
The first way is to pass all of the arguments, including the type argument, to the function:

```ts
let output = identity<string>("myString");  // type of output will be 'string'
```

Here we explicitly set `T` to be `string` as one of the arguments to the function call, denoted using the `<>` around the arguments rather than `()`.

The second way is also perhaps the most common. Here we use *type argument inference* -- that is, we want the compiler to set the value of `T` for us automatically based on the type of the argument we pass in:

```ts
let output = identity("myString");  // type of output will be 'string'
```

Notice that we didn't have to explicitly pass the type in the angle brackets (`<>`); the compiler just looked at the value `"myString"`, and set `T` to its type.
While type argument inference can be a helpful tool to keep code shorter and more readable, you may need to explicitly pass in the type arguments as we did in the previous example when the compiler fails to infer the type, as may happen in more complex examples.


# Merging Namespaces with Classes, Functions, and Enums

Namespaces are flexible enough to also merge with other types of declarations.
To do so, the namespace declaration must follow the declaration it will merge with. The resulting declaration has properties of both declaration types.
TypeScript uses this capability to model some of the patterns in JavaScript as well as other programming languages.


# Caveats for Project References

Project references have a few trade-offs you should be aware of.

Because dependent projects make use of `.d.ts` files that are built from their dependencies, you'll either have to check in certain build outputs *or* build a project after cloning it before you can navigate the project in an editor without seeing spurious errors.
We're working on a behind-the-scenes .d.ts generation process that should be able to mitigate this, but for now we recommend informing developers that they should build after cloning.

Additionally, to preserve compatibility with existing build workflows, `tsc` will *not* automatically build dependencies unless invoked with the `--build` switch.
Let's learn more about `--build`.


# Caveats

Normally, `tsc` will produce outputs (`.js` and `.d.ts`) in the presence of syntax or type errors, unless `noEmitOnError` is on.
Doing this in an incremental build system would be very bad - if one of your out-of-date dependencies had a new error, you'd only see it *once* because a subsequent build would skip building the now up-to-date project.
For this reason, `tsc -b` effectively acts as if `noEmitOnError` is enabled for all projects.

If you check in any build outputs (`.js`, `.d.ts`, `.d.ts.map`, etc.), you may need to run a `--force` build after certain source control operations depending on whether your source control tool preserves timestamps between the local copy and the remote copy.


# Comparing two functions

While comparing primitive types and object types is relatively straightforward, the question of what kinds of functions should be considered compatible is a bit more involved.
Let's start with a basic example of two functions that differ only in their parameter lists:

```ts
let x = (a: number) => 0;
let y = (b: number, s: string) => 0;

y = x; // OK
x = y; // Error
```

To check if `x` is assignable to `y`, we first look at the parameter list.
Each parameter in `x` must have a corresponding parameter in `y` with a compatible type.
Note that the names of the parameters are not considered, only their types.
In this case, every parameter of `x` has a corresponding compatible parameter in `y`, so the assignment is allowed.

The second assignment is an error, because `y` has a required second parameter that `x` does not have, so the assignment is disallowed.

You may be wondering why we allow 'discarding' parameters like in the example `y = x`.
The reason for this assignment to be allowed is that ignoring extra function parameters is actually quite common in JavaScript.
For example, `Array#forEach` provides three parameters to the callback function: the array element, its index, and the containing array.
Nevertheless, it's very useful to provide a callback that only uses the first parameter:

```ts
let items = [1, 2, 3];

// Don't force these extra parameters
items.forEach((item, index, array) => console.log(item));

// Should be OK!
items.forEach(item => console.log(item));
```

Now let's look at how return types are treated, using two functions that differ only by their return type:

```ts
let x = () => ({name: "Alice"});
let y = () => ({name: "Alice", location: "Seattle"});

x = y; // OK
y = x; // Error, because x() lacks a location property
```

The type system enforces that the source function's return type be a subtype of the target type's return type.


## Functions with overloads

When a function has overloads, each overload in the source type must be matched by a compatible signature on the target type.
This ensures that the target function can be called in all the same situations as the source function.


## Compiler Options in MSBuild


# First steps
<b><a href="#table-of-contents">↥ back to top</a></b>

Let's start with the program we'll be using as our example throughout this page.
We've written a small set of simplistic string validators, as you might write to check a user's input on a form in a webpage or check the format of an externally-provided data file.
