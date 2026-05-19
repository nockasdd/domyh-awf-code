---
library: rust
version: 2024 edition
latest: true
category: language
official_docs: https://doc.rust-lang.org/book/
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/rust-lang/book/contents/src
---

## ch02 00 guessing game tutorial


# Programming a Guessing Game

Let’s jump into Rust by working through a hands-on project together! This
chapter introduces you to a few common Rust concepts by showing you how to use
them in a real program. You’ll learn about `let`, `match`, methods, associated
functions, external crates, and more! In the following chapters, we’ll explore
these ideas in more detail. In this chapter, you’ll just practice the
fundamentals.

We’ll implement a classic beginner programming problem: a guessing game. Here’s
how it works: The program will generate a random integer between 1 and 100. It
will then prompt the player to enter a guess. After a guess is entered, the
program will indicate whether the guess is too low or too high. If the guess is
correct, the game will print a congratulatory message and exit.


#### Creating a Finite Number of Threads

We want our thread pool to work in a similar, familiar way so that switching
from threads to a thread pool doesn’t require large changes to the code that
uses our API. Listing 21-12 shows the hypothetical interface for a `ThreadPool`
struct we want to use instead of `thread::spawn`.

<Listing number="21-12" file-name="src/main.rs" caption="Our ideal `ThreadPool` interface">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

We use `ThreadPool::new` to create a new thread pool with a configurable number
of threads, in this case four. Then, in the `for` loop, `pool.execute` has a
similar interface as `thread::spawn` in that it takes a closure that the pool
should run for each stream. We need to implement `pool.execute` so that it
takes the closure and gives it to a thread in the pool to run. This code won’t
yet compile, but we’ll try so that the compiler can guide us in how to fix it.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>


### Generic Lifetimes in Functions

We’ll write a function that returns the longer of two string slices. This
function will take two string slices and return a single string slice. After
we’ve implemented the `longest` function, the code in Listing 10-19 should
print `The longest string is abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="A `main` function that calls the `longest` function to find the longer of two string slices">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Note that we want the function to take string slices, which are references,
rather than strings, because we don’t want the `longest` function to take
ownership of its parameters. Refer to [“String Slices as
Parameters”][string-slices-as-parameters]<!-- ignore --> in Chapter 4 for more
discussion about why the parameters we use in Listing 10-19 are the ones we
want.

If we try to implement the `longest` function as shown in Listing 10-20, it
won’t compile.

<Listing number="10-20" file-name="src/main.rs" caption="An implementation of the `longest` function that returns the longer of two string slices but does not yet compile">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Instead, we get the following error that talks about lifetimes:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

The help text reveals that the return type needs a generic lifetime parameter
on it because Rust can’t tell whether the reference being returned refers to
`x` or `y`. Actually, we don’t know either, because the `if` block in the body
of this function returns a reference to `x` and the `else` block returns a
reference to `y`!

When we’re defining this function, we don’t know the concrete values that will
be passed into this function, so we don’t know whether the `if` case or the
`else` case will execute. We also don’t know the concrete lifetimes of the
references that will be passed in, so we can’t look at the scopes as we did in
Listings 10-17 and 10-18 to determine whether the reference we return will
always be valid. The borrow checker can’t determine this either, because it
doesn’t know how the lifetimes of `x` and `y` relate to the lifetime of the
return value. To fix this error, we’ll add generic lifetime parameters that
define the relationship between the references so that the borrow checker can
perform its analysis.


### In Struct Definitions

So far, the structs we’ve defined all hold owned types. We can define structs
to hold references, but in that case, we would need to add a lifetime
annotation on every reference in the struct’s definition. Listing 10-24 has a
struct named `ImportantExcerpt` that holds a string slice.

<Listing number="10-24" file-name="src/main.rs" caption="A struct that holds a reference, requiring a lifetime annotation">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

This struct has the single field `part` that holds a string slice, which is a
reference. As with generic data types, we declare the name of the generic
lifetime parameter inside angle brackets after the name of the struct so that
we can use the lifetime parameter in the body of the struct definition. This
annotation means an instance of `ImportantExcerpt` can’t outlive the reference
it holds in its `part` field.

The `main` function here creates an instance of the `ImportantExcerpt` struct
that holds a reference to the first sentence of the `String` owned by the
variable `novel`. The data in `novel` exists before the `ImportantExcerpt`
instance is created. In addition, `novel` doesn’t go out of scope until after
the `ImportantExcerpt` goes out of scope, so the reference in the
`ImportantExcerpt` instance is valid.


### In Method Definitions

When we implement methods on a struct with lifetimes, we use the same syntax as
that of generic type parameters, as shown in Listing 10-11. Where we declare
and use the lifetime parameters depends on whether they’re related to the
struct fields or the method parameters and return values.

Lifetime names for struct fields always need to be declared after the `impl`
keyword and then used after the struct’s name because those lifetimes are part
of the struct’s type.

In method signatures inside the `impl` block, references might be tied to the
lifetime of references in the struct’s fields, or they might be independent. In
addition, the lifetime elision rules often make it so that lifetime annotations
aren’t necessary in method signatures. Let’s look at some examples using the
struct named `ImportantExcerpt` that we defined in Listing 10-24.

First, we’ll use a method named `level` whose only parameter is a reference to
`self` and whose return value is an `i32`, which is not a reference to anything:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

The lifetime parameter declaration after `impl` and its use after the type name
are required, but because of the first elision rule, we’re not required to
annotate the lifetime of the reference to `self`.

Here is an example where the third lifetime elision rule applies:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

There are two input lifetimes, so Rust applies the first lifetime elision rule
and gives both `&self` and `announcement` their own lifetimes. Then, because
one of the parameters is `&self`, the return type gets the lifetime of `&self`,
and all lifetimes have been accounted for.


#### Using `extern` Functions to Call External Code

Sometimes your Rust code might need to interact with code written in another
language. For this, Rust has the keyword `extern` that facilitates the creation
and use of a _Foreign Function Interface (FFI)_, which is a way for a
programming language to define functions and enable a different (foreign)
programming language to call those functions.

Listing 20-8 demonstrates how to set up an integration with the `abs` function
from the C standard library. Functions declared within `extern` blocks are
generally unsafe to call from Rust code, so `extern` blocks must also be marked
`unsafe`. The reason is that other languages don’t enforce Rust’s rules and
guarantees, and Rust can’t check them, so responsibility falls on the
programmer to ensure safety.

<Listing number="20-8" file-name="src/main.rs" caption="Declaring and calling an `extern` function defined in another language">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Within the `unsafe extern "C"` block, we list the names and signatures of
external functions from another language we want to call. The `"C"` part
defines which _application binary interface (ABI)_ the external function uses:
The ABI defines how to call the function at the assembly level. The `"C"` ABI
is the most common and follows the C programming language’s ABI. Information
about all the ABIs Rust supports is available in [the Rust Reference][ABI].

Every item declared within an `unsafe extern` block is implicitly unsafe.
However, some FFI functions *are* safe to call. For example, the `abs` function
from C’s standard library does not have any memory safety considerations, and we
know it can be called with any `i32`. In cases like this, we can use the `safe`
keyword to say that this specific function is safe to call even though it is in
an `unsafe extern` block. Once we make that change, calling it no longer
requires an `unsafe` block, as shown in Listing 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Explicitly marking a function as `safe` within an `unsafe extern` block and calling it safely">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Marking a function as `safe` does not inherently make it safe! Instead, it is
like a promise you are making to Rust that it is safe. It is still your
responsibility to make sure that promise is kept!


#### Calling Rust Functions from Other Languages

We can also use `extern` to create an interface that allows other languages to
call Rust functions. Instead of creating a whole `extern` block, we add the
`extern` keyword and specify the ABI to use just before the `fn` keyword for
the relevant function. We also need to add an `#[unsafe(no_mangle)]` annotation
to tell the Rust compiler not to mangle the name of this function. _Mangling_
is when a compiler changes the name we’ve given a function to a different name
that contains more information for other parts of the compilation process to
consume but is less human readable. Every programming language compiler mangles
names slightly differently, so for a Rust function to be nameable by other
languages, we must disable the Rust compiler’s name mangling. This is unsafe
because there might be name collisions across libraries without the built-in
mangling, so it is our responsibility to make sure the name we choose is safe
to export without mangling.

In the following example, we make the `call_from_c` function accessible from C
code, after it’s compiled to a shared library and linked from C:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

This usage of `extern` requires `unsafe` only in the attribute, not on the
`extern` block.


## ch18 03 oo design patterns


### Structuring Test Functions

At its simplest, a test in Rust is a function that’s annotated with the `test`
attribute. Attributes are metadata about pieces of Rust code; one example is
the `derive` attribute we used with structs in Chapter 5. To change a function
into a test function, add `#[test]` on the line before `fn`. When you run your
tests with the `cargo test` command, Rust builds a test runner binary that runs
the annotated functions and reports on whether each test function passes or
fails.

Whenever we make a new library project with Cargo, a test module with a test
function in it is automatically generated for us. This module gives you a
template for writing your tests so that you don’t have to look up the exact
structure and syntax every time you start a new project. You can add as many
additional test functions and as many test modules as you want!

We’ll explore some aspects of how tests work by experimenting with the template
test before we actually test any code. Then, we’ll write some real-world tests
that call some code that we’ve written and assert that its behavior is correct.

Let’s create a new library project called `adder` that will add two numbers:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

The contents of the _src/lib.rs_ file in your `adder` library should look like
Listing 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="The code generated automatically by `cargo new`">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

The file starts with an example `add` function so that we have something to
test.

For now, let’s focus solely on the `it_works` function. Note the `#[test]`
annotation: This attribute indicates this is a test function, so the test
runner knows to treat this function as a test. We might also have non-test
functions in the `tests` module to help set up common scenarios or perform
common operations, so we always need to indicate which functions are tests.

The example function body uses the `assert_eq!` macro to assert that `result`,
which contains the result of calling `add` with 2 and 2, equals 4. This
assertion serves as an example of the format for a typical test. Let’s run it
to see that this test passes.

The `cargo test` command runs all tests in our project, as shown in Listing
11-2.

<Listing number="11-2" caption="The output from running the automatically generated test">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo compiled and ran the test. We see the line `running 1 test`. The next
line shows the name of the generated test function, called `tests::it_works`,
and that the result of running that test is `ok`. The overall summary `test
result: ok.` means that all the tests passed, and the portion that reads `1
passed; 0 failed` totals the number of tests that passed or failed.

It’s possible to mark a test as ignored so that it doesn’t run in a particular
instance; we’ll cover that in the [“Ignoring Tests Unless Specifically
Requested”][ignoring]<!-- ignore --> section later in this chapter. Because we
haven’t done that here, the summary shows `0 ignored`. We can also pass an
argument to the `cargo test` command to run only tests whose name matches a
string; this is called _filtering_, and we’ll cover it in the [“Running a
Subset of Tests by Name”][subset]<!-- ignore --> section. Here, we haven’t
filtered the tests being run, so the end of the summary shows `0 filtered out`.

The `0 measured` statistic is for benchmark tests that measure performance.
Benchmark tests are, as of this writing, only available in nightly Rust. See
[the documentation about benchmark tests][bench] to learn more.

The next part of the test output starting at `Doc-tests adder` is for the
results of any documentation tests. We don’t have any documentation tests yet,
but Rust can compile any code examples that appear in our API documentation.
This feature helps keep your docs and your code in sync! We’ll discuss how to
write documentation tests in the [“Documentation Comments as
Tests”][doc-comments]<!-- ignore --> section of Chapter 14. For now, we’ll
ignore the `Doc-tests` output.

Let’s start to customize the test to our own needs. First, change the name of
the `it_works` function to a different name, such as `exploration`, like so:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Then, run `cargo test` again. The output now shows `exploration` instead of
`it_works`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Now we’ll add another test, but this time we’ll make a test that fails! Tests
fail when something in the test function panics. Each test is run in a new
thread, and when the main thread sees that a test thread has died, the test is
marked as failed. In Chapter 9, we talked about how the simplest way to panic
is to call the `panic!` macro. Enter the new test as a function named
`another`, so your _src/lib.rs_ file looks like Listing 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Adding a second test that will fail because we call the `panic!` macro">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Run the tests again using `cargo test`. The output should look like Listing
11-4, which shows that our `exploration` test passed and `another` failed.

<Listing number="11-4" caption="Test results when one test passes and one test fails">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Instead of `ok`, the line `test tests::another` shows `FAILED`. Two new
sections appear between the individual results and the summary: The first
displays the detailed reason for each test failure. In this case, we get the
details that `tests::another` failed because it panicked with the message `Make
this test fail` on line 17 in the _src/lib.rs_ file. The next section lists
just the names of all the failing tests, which is useful when there are lots of
tests and lots of detailed failing test output. We can use the name of a
failing test to run just that test to debug it more easily; we’ll talk more
about ways to run tests in the [“Controlling How Tests Are
Run”][controlling-how-tests-are-run]<!-- ignore --> section.

The summary line displays at the end: Overall, our test result is `FAILED`. We
had one test pass and one test fail.

Now that you’ve seen what the test results look like in different scenarios,
let’s look at some macros other than `panic!` that are useful in tests.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>


#### Creating a Constructor for `Config`

So far, we’ve extracted the logic responsible for parsing the command line
arguments from `main` and placed it in the `parse_config` function. Doing so
helped us see that the `query` and `file_path` values were related, and that
relationship should be conveyed in our code. We then added a `Config` struct to
name the related purpose of `query` and `file_path` and to be able to return the
values’ names as struct field names from the `parse_config` function.

So, now that the purpose of the `parse_config` function is to create a `Config`
instance, we can change `parse_config` from a plain function to a function
named `new` that is associated with the `Config` struct. Making this change
will make the code more idiomatic. We can create instances of types in the
standard library, such as `String`, by calling `String::new`. Similarly, by
changing `parse_config` into a `new` function associated with `Config`, we’ll
be able to create instances of `Config` by calling `Config::new`. Listing 12-7
shows the changes we need to make.

<Listing number="12-7" file-name="src/main.rs" caption="Changing `parse_config` into `Config::new`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

We’ve updated `main` where we were calling `parse_config` to instead call
`Config::new`. We’ve changed the name of `parse_config` to `new` and moved it
within an `impl` block, which associates the `new` function with `Config`. Try
compiling this code again to make sure it works.


### Ownership and Functions

The mechanics of passing a value to a function are similar to those when
assigning a value to a variable. Passing a variable to a function will move or
copy, just as assignment does. Listing 4-3 has an example with some annotations
showing where variables go into and out of scope.

<Listing number="4-3" file-name="src/main.rs" caption="Functions with ownership and scope annotated">

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-03/src/main.rs}}
```

</Listing>

If we tried to use `s` after the call to `takes_ownership`, Rust would throw a
compile-time error. These static checks protect us from mistakes. Try adding
code to `main` that uses `s` and `x` to see where you can use them and where
the ownership rules prevent you from doing so.


### The Difference Between Macros and Functions

Fundamentally, macros are a way of writing code that writes other code, which
is known as _metaprogramming_. In Appendix C, we discuss the `derive`
attribute, which generates an implementation of various traits for you. We’ve
also used the `println!` and `vec!` macros throughout the book. All of these
macros _expand_ to produce more code than the code you’ve written manually.

Metaprogramming is useful for reducing the amount of code you have to write and
maintain, which is also one of the roles of functions. However, macros have
some additional powers that functions don’t have.

A function signature must declare the number and type of parameters the
function has. Macros, on the other hand, can take a variable number of
parameters: We can call `println!("hello")` with one argument or
`println!("hello {}", name)` with two arguments. Also, macros are expanded
before the compiler interprets the meaning of the code, so a macro can, for
example, implement a trait on a given type. A function can’t, because it gets
called at runtime and a trait needs to be implemented at compile time.

The downside to implementing a macro instead of a function is that macro
definitions are more complex than function definitions because you’re writing
Rust code that writes Rust code. Due to this indirection, macro definitions are
generally more difficult to read, understand, and maintain than function
definitions.

Another important difference between macros and functions is that you must
define macros or bring them into scope _before_ you call them in a file, as
opposed to functions you can define anywhere and call anywhere.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>


### Disambiguating Between Identically Named Methods

Nothing in Rust prevents a trait from having a method with the same name as
another trait’s method, nor does Rust prevent you from implementing both traits
on one type. It’s also possible to implement a method directly on the type with
the same name as methods from traits.

When calling methods with the same name, you’ll need to tell Rust which one you
want to use. Consider the code in Listing 20-17 where we’ve defined two traits,
`Pilot` and `Wizard`, that both have a method called `fly`. We then implement
both traits on a type `Human` that already has a method named `fly` implemented
on it. Each `fly` method does something different.

<Listing number="20-17" file-name="src/main.rs" caption="Two traits are defined to have a `fly` method and are implemented on the `Human` type, and a `fly` method is implemented on `Human` directly.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

When we call `fly` on an instance of `Human`, the compiler defaults to calling
the method that is directly implemented on the type, as shown in Listing 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Calling `fly` on an instance of `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Running this code will print `*waving arms furiously*`, showing that Rust
called the `fly` method implemented on `Human` directly.

To call the `fly` methods from either the `Pilot` trait or the `Wizard` trait,
we need to use more explicit syntax to specify which `fly` method we mean.
Listing 20-19 demonstrates this syntax.

<Listing number="20-19" file-name="src/main.rs" caption="Specifying which trait’s `fly` method we want to call">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Specifying the trait name before the method name clarifies to Rust which
implementation of `fly` we want to call. We could also write
`Human::fly(&person)`, which is equivalent to the `person.fly()` that we used
in Listing 20-19, but this is a bit longer to write if we don’t need to
disambiguate.

Running this code prints the following:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Because the `fly` method takes a `self` parameter, if we had two _types_ that
both implement one _trait_, Rust could figure out which implementation of a
trait to use based on the type of `self`.

However, associated functions that are not methods don’t have a `self`
parameter. When there are multiple types or traits that define non-method
functions with the same function name, Rust doesn’t always know which type you
mean unless you use fully qualified syntax. For example, in Listing 20-20, we
create a trait for an animal shelter that wants to name all baby dogs Spot. We
make an `Animal` trait with an associated non-method function `baby_name`. The
`Animal` trait is implemented for the struct `Dog`, on which we also provide an
associated non-method function `baby_name` directly.

<Listing number="20-20" file-name="src/main.rs" caption="A trait with an associated function and a type with an associated function of the same name that also implements the trait">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

We implement the code for naming all puppies Spot in the `baby_name` associated
function that is defined on `Dog`. The `Dog` type also implements the trait
`Animal`, which describes characteristics that all animals have. Baby dogs are
called puppies, and that is expressed in the implementation of the `Animal`
trait on `Dog` in the `baby_name` function associated with the `Animal` trait.

In `main`, we call the `Dog::baby_name` function, which calls the associated
function defined on `Dog` directly. This code prints the following:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

This output isn’t what we wanted. We want to call the `baby_name` function that
is part of the `Animal` trait that we implemented on `Dog` so that the code
prints `A baby dog is called a puppy`. The technique of specifying the trait
name that we used in Listing 20-19 doesn’t help here; if we change `main` to
the code in Listing 20-21, we’ll get a compilation error.

<Listing number="20-21" file-name="src/main.rs" caption="Attempting to call the `baby_name` function from the `Animal` trait, but Rust doesn’t know which implementation to use">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Because `Animal::baby_name` doesn’t have a `self` parameter, and there could be
other types that implement the `Animal` trait, Rust can’t figure out which
implementation of `Animal::baby_name` we want. We’ll get this compiler error:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

To disambiguate and tell Rust that we want to use the implementation of
`Animal` for `Dog` as opposed to the implementation of `Animal` for some other
type, we need to use fully qualified syntax. Listing 20-22 demonstrates how to
use fully qualified syntax.

<Listing number="20-22" file-name="src/main.rs" caption="Using fully qualified syntax to specify that we want to call the `baby_name` function from the `Animal` trait as implemented on `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

We’re providing Rust with a type annotation within the angle brackets, which
indicates we want to call the `baby_name` method from the `Animal` trait as
implemented on `Dog` by saying that we want to treat the `Dog` type as an
`Animal` for this function call. This code will now print what we want:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

In general, fully qualified syntax is defined as follows:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

For associated functions that aren’t methods, there would not be a `receiver`:
There would only be the list of other arguments. You could use fully qualified
syntax everywhere that you call functions or methods. However, you’re allowed
to omit any part of this syntax that Rust can figure out from other information
in the program. You only need to use this more verbose syntax in cases where
there are multiple implementations that use the same name and Rust needs help
to identify which implementation you want to call.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>
