---
library: graphql
version: Oct 2021
latest: true
category: api-spec
official_docs: https://graphql.org
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/graphql/graphql-spec/contents/spec
---

# Type System

The GraphQL Type system describes the capabilities of a GraphQL service and is
used to determine if a requested operation is valid, to guarantee the type of
response results, and describes the input types of variables to determine if
values provided at request time are valid.

TypeSystemDocument : TypeSystemDefinition+

TypeSystemDefinition :

- SchemaDefinition
- TypeDefinition
- DirectiveDefinition

The GraphQL language includes an
[IDL](https://en.wikipedia.org/wiki/Interface_description_language) used to
describe a GraphQL service's type system. Tools may use this definition language
to provide utilities such as client code generation or service bootstrapping.

GraphQL tools or services which only seek to execute GraphQL requests and not
construct a new GraphQL schema may choose not to allow {TypeSystemDefinition}.
Tools which only seek to produce schema and not execute requests may choose to
only allow {TypeSystemDocument} and not allow {ExecutableDefinition} or
{TypeSystemExtension} but should provide a descriptive error if present.

Note: The type system definition language is used throughout the remainder of
this specification document when illustrating example type systems.


### Executable Definitions

**Formal Specification**

- For each definition {definition} in the document:
  - {definition} must be {ExecutableDefinition} (it must not be
    {TypeSystemDefinitionOrExtension}).

**Explanatory Text**

GraphQL execution will only consider the executable definitions Operation and
Fragment. Type system definitions and extensions are not executable, and are not
considered during execution.

To avoid ambiguity, a document containing {TypeSystemDefinitionOrExtension} is
invalid for execution.

GraphQL documents not intended to be directly executed may include
{TypeSystemDefinitionOrExtension}.

For example, the following document is invalid for execution since the original
executing schema may not know about the provided type extension:

```graphql counter-example
query getDogName {
  dog {
    name
    color
  }
}

extend type Dog {
  color: String
}
```


### All Operation Definitions


### Named Operation Definitions


### Anonymous Operation Definitions


### Subscription Operation Definitions


### All Variable Usages Are Allowed

**Formal Specification**

- For each {operation} in {document}:
  - Let {variableUsages} be all usages transitively included in the {operation}.
  - For each {variableUsage} in {variableUsages}:
    - Let {variableName} be the name of {variableUsage}.
    - Let {variableDefinition} be the {VariableDefinition} named {variableName}
      defined within {operation}.
    - {IsVariableUsageAllowed(variableDefinition, variableUsage)} must be
      {true}.

IsVariableUsageAllowed(variableDefinition, variableUsage):

- Let {variableType} be the expected type of {variableDefinition}.
- Let {locationType} be the expected type of the {Argument}, {ObjectField}, or
  {ListValue} entry where {variableUsage} is located.
- If {IsNonNullPosition(locationType, variableUsage)} AND {variableType} is NOT
  a non-null type:
  - Let {hasNonNullVariableDefaultValue} be {true} if a default value exists for
    {variableDefinition} and is not the value {null}.
  - Let {hasLocationDefaultValue} be {true} if a default value exists for the
    {Argument} or {ObjectField} where {variableUsage} is located.
  - If {hasNonNullVariableDefaultValue} is NOT {true} AND
    {hasLocationDefaultValue} is NOT {true}, return {false}.
  - Let {nullableLocationType} be the unwrapped nullable type of {locationType}.
  - Return {AreTypesCompatible(variableType, nullableLocationType)}.
- Return {AreTypesCompatible(variableType, locationType)}.

IsNonNullPosition(locationType, variableUsage):

- If {locationType} is a non-null type, return {true}.
- If the location of {variableUsage} is an {ObjectField}:
  - Let {parentObjectValue} be the {ObjectValue} containing {ObjectField}.
  - Let {parentLocationType} be the expected type of {ObjectValue}.
  - If {parentLocationType} is a _OneOf Input Object_ type, return {true}.
- Return {false}.

AreTypesCompatible(variableType, locationType):

- If {locationType} is a non-null type:
  - If {variableType} is NOT a non-null type, return {false}.
  - Let {nullableLocationType} be the unwrapped nullable type of {locationType}.
  - Let {nullableVariableType} be the unwrapped nullable type of {variableType}.
  - Return {AreTypesCompatible(nullableVariableType, nullableLocationType)}.
- Otherwise, if {variableType} is a non-null type:
  - Let {nullableVariableType} be the nullable type of {variableType}.
  - Return {AreTypesCompatible(nullableVariableType, locationType)}.
- Otherwise, if {locationType} is a list type:
  - If {variableType} is NOT a list type, return {false}.
  - Let {itemLocationType} be the unwrapped item type of {locationType}.
  - Let {itemVariableType} be the unwrapped item type of {variableType}.
  - Return {AreTypesCompatible(itemVariableType, itemLocationType)}.
- Otherwise, if {variableType} is a list type, return {false}.
- Return {true} if {variableType} and {locationType} are identical, otherwise
  {false}.

**Explanatory Text**

Variable usages must be compatible with the arguments they are passed to.

Validation failures occur when variables are used in the context of types that
are complete mismatches, or if a nullable type in a variable is passed to a
non-null argument type.

Types must match:

```graphql counter-example
query intCannotGoIntoBoolean($intArg: Int) {
  arguments {
    booleanArgField(booleanArg: $intArg)
  }
}
```

${intArg} typed as {Int} cannot be used as an argument to {booleanArg}, typed as
{Boolean}.

List cardinality must also be the same. For example, lists cannot be passed into
singular values.

```graphql counter-example
query booleanListCannotGoIntoBoolean($booleanListArg: [Boolean]) {
  arguments {
    booleanArgField(booleanArg: $booleanListArg)
  }
}
```

Nullability must also be respected. In general a nullable variable cannot be
passed to a non-null argument.

```graphql counter-example
query booleanArgQuery($booleanArg: Boolean) {
  arguments {
    nonNullBooleanArgField(nonNullBooleanArg: $booleanArg)
  }
}
```

For list types, the same rules around nullability apply to both outer types and
inner types. A nullable list cannot be passed to a non-null list, and a list of
nullable values cannot be passed to a list of non-null values. The following is
valid:

```graphql example
query nonNullListToList($nonNullBooleanList: [Boolean]!) {
  arguments {
    booleanListArgField(booleanListArg: $nonNullBooleanList)
  }
}
```

However, a nullable list cannot be passed to a non-null list:

```graphql counter-example
query listToNonNullList($booleanList: [Boolean]) {
  arguments {
    nonNullBooleanListField(nonNullBooleanListArg: $booleanList)
  }
}
```

This would fail validation because a `[T]` cannot be passed to a `[T]!`.
Similarly a `[T]` cannot be passed to a `[T!]`.

Variables used for OneOf Input Object fields must be non-nullable.

```graphql example
mutation addCat($cat: CatInput!) {
  addPet(pet: { cat: $cat }) {
    name
  }
}

mutation addCatWithDefault($cat: CatInput! = { name: "Brontie" }) {
  addPet(pet: { cat: $cat }) {
    name
  }
}
```

```graphql counter-example
mutation addNullableCat($cat: CatInput) {
  addPet(pet: { cat: $cat }) {
    name
  }
}
```

**Allowing Optional Variables When Default Values Exist**

A notable exception to typical variable type compatibility is allowing a
variable definition with a nullable type to be provided to a non-null location
as long as either that variable or that location provides a default value.

In the example below, an optional variable `$booleanArg` is allowed to be used
in the non-null argument `optionalBooleanArg` because the field argument is
optional since it provides a default value in the schema.

```graphql example
query booleanArgQueryWithDefault($booleanArg: Boolean) {
  arguments {
    optionalNonNullBooleanArgField(optionalBooleanArg: $booleanArg)
  }
}
```

In the example below, an optional variable `$booleanArg` is allowed to be used
in the non-null argument (`nonNullBooleanArg`) because the variable provides a
default value in the operation. This behavior is explicitly supported for
compatibility with earlier editions of this specification. GraphQL authoring
tools may wish to report this as a warning with the suggestion to replace
`Boolean` with `Boolean!` to avoid ambiguity.

```graphql example
query booleanArgQueryWithDefault($booleanArg: Boolean = true) {
  arguments {
    nonNullBooleanArgField(nonNullBooleanArg: $booleanArg)
  }
}
```

Note: The value {null} could still be provided to such a variable at runtime. A
non-null argument must raise an _execution error_ if provided a {null} value.


---
