---
name: clojure
description: "Clojure functional patterns for JVM. Use when working with .clj/.cljs files or Leiningen projects."
detect: ["*.clj", "*.cljs", "*.cljc", "deps.edn", "project.clj"]
category: functional
tier: 3
---

# Clojure Patterns — DOMYH Awesome Code

> **Version**: Clojure 1.11+ (2025-2026)
> **Framework**: Ring, Pedestal, Reagent
> **Philosophy**: Simple, data-oriented, REPL-driven

---

## 🎯 When to Use

Use for: Data processing, concurrent systems, REPL prototyping.
**NOT for**: Beginners (steep curve), strict typing needs.

---

## 🔧 Project Setup (deps.edn)

```clojure
{:deps {org.clojure/clojure {:mvn/version "1.11.1"}
        ring/ring-core {:mvn/version "1.10.0"}
        ring/ring-jetty-adapter {:mvn/version "1.10.0"}
        metosin/reitit {:mvn/version "0.7.0"}}
 :paths ["src"]
 :aliases {:dev {:extra-paths ["dev"]
                 :extra-deps {nrepl/nrepl {:mvn/version "1.0.0"}}}
           :test {:extra-paths ["test"]
                  :extra-deps {lambdaisland/kaocha {:mvn/version "1.87.1366"}}}}}
```

---

## 🔄 Core Patterns

### Data Transformations

```clojure
;; Threading macros for clarity
(->> users
     (filter :active)
     (map :email)
     (take 10))

;; Transform data with reduce
(defn group-by-status [orders]
  (reduce
    (fn [acc order]
      (update acc (:status order) (fnil conj []) order))
    {}
    orders))

;; Transducers for efficiency
(def xf
  (comp
    (filter :active)
    (map :name)
    (take 10)))

(into [] xf users)
```

### HTTP Server with Ring

```clojure
(ns myapp.core
  (:require [ring.adapter.jetty :refer [run-jetty]]
            [ring.util.response :as response]
            [reitit.ring :as reitit]))

(defn handler [request]
  (response/response "Hello, World!"))

(def app
  (reitit/ring-handler
    (reitit/router
      [["/" {:get handler}]
       ["/api/users" {:get list-users
                      :post create-user}]
       ["/api/users/:id" {:get get-user}]])))

(defn -main []
  (run-jetty app {:port 3000}))
```

### Concurrency with Atoms

```clojure
;; Atom for shared state
(def counter (atom 0))

(swap! counter inc)     ; Increment
(reset! counter 0)      ; Reset
@counter               ; Deref to read

;; Agent for async updates
(def logger (agent []))
(send logger conj "Log message")

;; Core.async channels
(require '[clojure.core.async :as async])

(let [ch (async/chan 10)]
  (async/go
    (async/>! ch "Hello")
    (async/>! ch "World"))
  (async/go-loop []
    (when-let [msg (async/<! ch)]
      (println msg)
      (recur))))
```

---

## ✅ Production Checklist

- [ ] `clj-kondo` linting
- [ ] Tests with `kaocha`
- [ ] REPL workflow established
- [ ] Spec validations

---
