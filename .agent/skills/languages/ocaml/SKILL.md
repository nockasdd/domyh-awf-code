---
name: ocaml
description: "OCaml functional programming patterns. Use when working with .ml/.mli files."
detect: ["*.ml", "*.mli", "dune", "dune-project", "*.opam"]
category: functional
tier: 3
---

# OCaml Patterns — DOMYH Awesome Code

> **Version**: OCaml 5.1+ (2025-2026)
> **Build**: Dune, opam
> **Philosophy**: Type-safe, efficient, pragmatic FP

---

## 🎯 When to Use

Use for: Compilers, theorem provers, financial systems, type-safe code.
**NOT for**: Rapid prototyping, large web ecosystems.

---

## 🔧 Project Setup

```bash
opam switch create . 5.1.0
dune init project myapp
cd myapp
dune build
dune exec myapp
```

### dune file

```lisp
(executable
 (name main)
 (libraries lwt lwt.unix yojson))
```

---

## 🔄 Core Patterns

### Algebraic Data Types

```ocaml
type user = {
  id: int;
  name: string;
  email: string;
}

type result =
  | Ok of user
  | NotFound of int
  | ValidationError of string

let find_user id =
  match Database.find id with
  | Some user -> Ok user
  | None -> NotFound id

let handle_result = function
  | Ok user -> Printf.printf "Found: %s\n" user.name
  | NotFound id -> Printf.printf "User %d not found\n" id
  | ValidationError msg -> Printf.printf "Error: %s\n" msg
```

### Modules and Functors

```ocaml
module type STORAGE = sig
  type key
  type value
  val get : key -> value option
  val set : key -> value -> unit
end

module MakeCache (S : STORAGE) = struct
  let cache = Hashtbl.create 100

  let get key =
    match Hashtbl.find_opt cache key with
    | Some v -> Some v
    | None ->
      match S.get key with
      | Some v -> Hashtbl.add cache key v; Some v
      | None -> None
end
```

### Async with Lwt

```ocaml
open Lwt.Syntax

let fetch_user id =
  let* response = Http.get (Printf.sprintf "/users/%d" id) in
  let* body = Http.body response in
  Lwt.return (User.of_json body)

let main () =
  let* user = fetch_user 1 in
  print_endline user.name;
  Lwt.return ()

let () = Lwt_main.run (main ())
```

---

## ✅ Production Checklist

- [ ] `dune build` passing
- [ ] Tests with `alcotest`
- [ ] `ocamlformat` applied
- [ ] `.mli` interface files

---
