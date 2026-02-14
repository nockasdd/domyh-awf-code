## 🏗️ Data Structures

### Struct Patterns

```c
// ✅ Opaque pointer pattern (information hiding)
// In header file (user.h)
typedef struct User User;
User *user_create(const char *name);
void user_destroy(User *user);
const char *user_get_name(const User *user);

// In implementation file (user.c)
struct User {
    char *name;
    int id;
    // Private implementation details
};

User *user_create(const char *name) {
    User *u = malloc(sizeof(*u));
    if (!u) return NULL;

    u->name = strdup(name);
    if (!u->name) {
        free(u);
        return NULL;
    }
    u->id = generate_id();
    return u;
}

void user_destroy(User *user) {
    if (user) {
        free(user->name);
        free(user);
    }
}
```

### Flexible Array Member (FAM)

```c
// ✅ C99+ pattern for variable-length data
struct Message {
    size_t length;
    uint32_t type;
    char data[];  // Flexible array member (MUST be last)
};

struct Message *create_message(const char *text) {
    size_t len = strlen(text) + 1;
    struct Message *msg = malloc(sizeof(*msg) + len);
    if (!msg) return NULL;

    msg->length = len;
    msg->type = MSG_TYPE_TEXT;
    memcpy(msg->data, text, len);
    return msg;
}
```

---
