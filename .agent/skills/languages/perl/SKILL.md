---
name: perl
detect: ["*.pl", "*.pm", "Makefile.PL", "cpanfile"]
version: "6.2.2"
category: scripting
tier: 3
---

# Perl 5 Patterns — DOMYH Awesome Code

> **Version**: Perl 5.40+ (2025-2026)
> **Framework**: Mojolicious, Dancer2
> **Philosophy**: TIMTOWTDI, text processing power

---

## 🎯 When to Use This Skill

Use for: Text processing, regex, system admin, legacy maintenance.
**NOT for**: New web apps (→ python/go), ML (→ python).

---

## 🔄 Modern Perl Patterns

### Strict Mode

```perl
#!/usr/bin/env perl
use v5.40;
use strict;
use warnings;
use feature 'signatures';

# ✅ Modern subroutine signatures
sub greet($name, $greeting = "Hello") {
    say "$greeting, $name!";
}
```

### Data Structures

```perl
# Hash reference
my $user = {
    name  => 'John',
    email => 'john@example.com',
    roles => ['admin', 'user'],
};

# Array of hashes
my @users = (
    { name => 'Alice', age => 30 },
    { name => 'Bob',   age => 25 },
);

# Access
say $user->{name};
say $users[0]->{name};
```

### Regex Mastery

```perl
my $text = "Email: user@example.com, Phone: 123-456-7890";

# ✅ Named captures
if ($text =~ /Email:\s*(?<email>\S+@\S+)/) {
    say "Found: $+{email}";
}

# ✅ Substitution
$text =~ s/\d{3}-\d{3}-\d{4}/[REDACTED]/g;

# ✅ Split and join
my @words = split /\s+/, $text;
my $joined = join ", ", @words;
```

---

## 🌐 Mojolicious Web

```perl
use Mojolicious::Lite -signatures;

get '/' => sub ($c) {
    $c->render(text => 'Hello World!');
};

get '/users/:id' => sub ($c) {
    my $id = $c->param('id');
    $c->render(json => { id => $id });
};

post '/users' => sub ($c) {
    my $data = $c->req->json;
    $c->render(json => { created => $data });
};

app->start;
```

---

## ✅ Production Checklist

- [ ] `use strict; use warnings;`
- [ ] Perl::Critic passing
- [ ] Tests with Test::More
- [ ] perltidy formatting

---

_DOMYH Awesome Code • Perl 5.40+_
