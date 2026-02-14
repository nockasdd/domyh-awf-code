---
name: haskell
detect: ["*.hs", "*.cabal", "stack.yaml", "cabal.project", "package.yaml"]
version: "6.2.7"
category: functional
tier: 2
---

# Haskell Patterns — DOMYH Awesome Code

> **Version**: GHC 9.8+ (2025-2026)
> **Framework**: Servant, Yesod
> **Philosophy**: Pure functions, strong types, lazy evaluation

---

## 🎯 When to Use This Skill

Use for: Compilers, parsers, formal verification, type-safe APIs.
**NOT for**: Rapid prototyping (→ python), web UI (→ react).

---

## 📦 Recommended Stack

| Library        | Use Case            | Install                    |
| -------------- | ------------------- | -------------------------- |
| **Servant**    | Type-safe APIs 🏆   | `cabal install servant`    |
| **Aeson**      | JSON parsing        | `cabal install aeson`      |
| **Lens**       | Optics              | `cabal install lens`       |
| **Persistent** | Database ORM        | `cabal install persistent` |
| **QuickCheck** | Property testing 🏆 | `cabal install QuickCheck` |

---

## 🔧 Project Setup

```bash
# With cabal
mkdir myproject && cd myproject
cabal init --interactive

# With stack
stack new myproject
cd myproject
stack build
```

### Project Structure

```
myproject/
├── app/
│   └── Main.hs
├── src/
│   ├── Lib.hs
│   └── Types.hs
├── test/
│   └── Spec.hs
├── myproject.cabal
└── cabal.project
```

---

## 🔄 Core Patterns

### Algebraic Data Types

```haskell
-- ✅ Sum type (enum)
data Status = Active | Inactive | Pending
  deriving (Show, Eq)

-- ✅ Product type (record)
data User = User
  { userId    :: Int
  , userName  :: Text
  , userEmail :: Text
  , userStatus :: Status
  } deriving (Show, Eq, Generic)

-- ✅ Parameterized types
data Result e a = Error e | Success a
  deriving (Show, Eq, Functor)

-- ✅ GADT for type safety
data Expr a where
  LitInt  :: Int -> Expr Int
  LitBool :: Bool -> Expr Bool
  Add     :: Expr Int -> Expr Int -> Expr Int
  If      :: Expr Bool -> Expr a -> Expr a -> Expr a
```

### Functor, Applicative, Monad

```haskell
-- ✅ Functor: map over context
data Maybe a = Nothing | Just a

instance Functor Maybe where
  fmap _ Nothing  = Nothing
  fmap f (Just a) = Just (f a)

-- ✅ Applicative: combine contexts
instance Applicative Maybe where
  pure = Just
  Nothing <*> _ = Nothing
  _ <*> Nothing = Nothing
  Just f <*> Just a = Just (f a)

-- Usage: validate multiple fields
data Person = Person { name :: Text, age :: Int }

validatePerson :: Maybe Text -> Maybe Int -> Maybe Person
validatePerson mName mAge = Person <$> mName <*> mAge

-- ✅ Monad: sequence dependent operations
instance Monad Maybe where
  Nothing >>= _ = Nothing
  Just a >>= f = f a

-- Usage: chain operations
findUser :: Int -> Maybe User
getUserPosts :: User -> Maybe [Post]

getUserPostsById :: Int -> Maybe [Post]
getUserPostsById id = do
  user <- findUser id
  posts <- getUserPosts user
  pure posts
```

### Error Handling

```haskell
import Control.Monad.Except

-- ✅ Either for errors
data AppError
  = NotFound Text
  | ValidationError Text
  | DatabaseError Text
  deriving (Show, Eq)

type AppM = ExceptT AppError IO

findUser :: Int -> AppM User
findUser id = do
  mUser <- liftIO $ queryUser id
  case mUser of
    Nothing -> throwError (NotFound "User not found")
    Just user -> pure user

-- Run with error handling
runApp :: AppM a -> IO (Either AppError a)
runApp = runExceptT
```

---

## 🌐 Servant API

```haskell
{-# LANGUAGE DataKinds #-}
{-# LANGUAGE TypeOperators #-}

import Servant

-- ✅ Type-level API definition
type UserAPI =
       "users" :> Get '[JSON] [User]
  :<|> "users" :> Capture "id" Int :> Get '[JSON] User
  :<|> "users" :> ReqBody '[JSON] CreateUser :> Post '[JSON] User
  :<|> "users" :> Capture "id" Int :> Delete '[JSON] NoContent

-- ✅ Handler implementation
server :: Server UserAPI
server = listUsers :<|> getUser :<|> createUser :<|> deleteUser
  where
    listUsers :: Handler [User]
    listUsers = liftIO $ queryAllUsers

    getUser :: Int -> Handler User
    getUser id = do
      mUser <- liftIO $ queryUser id
      maybe (throwError err404) pure mUser

    createUser :: CreateUser -> Handler User
    createUser dto = liftIO $ insertUser dto

    deleteUser :: Int -> Handler NoContent
    deleteUser id = do
      liftIO $ removeUser id
      pure NoContent

-- ✅ Run server
main :: IO ()
main = run 8080 $ serve (Proxy @UserAPI) server
```

---

## 🔍 Lens Patterns

```haskell
{-# LANGUAGE TemplateHaskell #-}

import Control.Lens

data Address = Address
  { _city    :: Text
  , _street  :: Text
  , _zipCode :: Text
  } deriving (Show)

data Person = Person
  { _name    :: Text
  , _age     :: Int
  , _address :: Address
  } deriving (Show)

makeLenses ''Address
makeLenses ''Person

-- ✅ View (get)
getName :: Person -> Text
getName p = p ^. name

-- ✅ Set
setName :: Text -> Person -> Person
setName n p = p & name .~ n

-- ✅ Modify
incrementAge :: Person -> Person
incrementAge = age %~ (+1)

-- ✅ Nested access
getCity :: Person -> Text
getCity p = p ^. address . city

setCity :: Text -> Person -> Person
setCity c = address . city .~ c
```

---

## 🧪 Testing with QuickCheck

```haskell
import Test.QuickCheck
import Test.Hspec

-- ✅ Property-based testing
prop_reverseReverse :: [Int] -> Bool
prop_reverseReverse xs = reverse (reverse xs) == xs

prop_sortIdempotent :: [Int] -> Bool
prop_sortIdempotent xs = sort (sort xs) == sort xs

-- ✅ Custom generators
instance Arbitrary User where
  arbitrary = do
    id <- arbitrary
    name <- elements ["Alice", "Bob", "Carol"]
    email <- arbitrary
    pure $ User id name email

-- ✅ HSpec tests
spec :: Spec
spec = do
  describe "User validation" $ do
    it "rejects empty names" $
      validateUser (User 1 "" "a@b.com") `shouldBe` Left "Name required"

    it "satisfies reverse property" $
      property prop_reverseReverse
```

---

## ✅ Production Checklist

### Code Quality

- [ ] HLint suggestions addressed
- [ ] Ormolu/fourmolu formatting
- [ ] GHC warnings clean (-Wall -Werror)
- [ ] Type signatures on all exports

### Performance

- [ ] Strictness annotations where needed
- [ ] No space leaks (profiling done)
- [ ] Lazy IO avoided

### Testing

- [ ] Property tests with QuickCheck
- [ ] Unit tests with HSpec
- [ ] Coverage > 70%

---

_DOMYH Awesome Code • Haskell GHC 9.8+_
