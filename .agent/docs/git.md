---
library: git
version: latest
latest: true
category: dev-knowledge
official_docs: https://git-scm.com/doc
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/git/git-scm.com/contents/external/book/content/book/en/v2
---

# Simple Git

[![NPM version](https://img.shields.io/npm/v/simple-git.svg)](https://www.npmjs.com/package/simple-git)

A lightweight interface for running `git` commands in any [node.js](https://nodejs.org) application.


# Installation

Use your favourite package manager:

-  [npm](https://npmjs.org): `npm install simple-git`
-  [yarn](https://yarnpkg.com/): `yarn add simple-git`


# Usage

Include into your JavaScript app using common js:

```javascript
// require the library, main export is a function
const simpleGit = require('simple-git');
simpleGit().clean(simpleGit.CleanOptions.FORCE);

// or use named properties
const { simpleGit, CleanOptions } = require('simple-git');
simpleGit().clean(CleanOptions.FORCE);
```

Include into your JavaScript app as an ES Module:

```javascript
import { simpleGit, CleanOptions } from 'simple-git';

simpleGit().clean(CleanOptions.FORCE);
```

Include in a TypeScript app using the bundled type definitions:

```typescript
import { simpleGit, SimpleGit, CleanOptions } from 'simple-git';

const git: SimpleGit = simpleGit().clean(CleanOptions.FORCE);
```


## Configuration

Configure each `simple-git` instance with a properties object passed to the main `simpleGit` function:

```typescript
import { simpleGit, SimpleGit, SimpleGitOptions } from 'simple-git';

const options: Partial<SimpleGitOptions> = {
   baseDir: process.cwd(),
   binary: 'git',
   maxConcurrentProcesses: 6,
   trimmed: false,
};

// when setting all options in a single object
const git: SimpleGit = simpleGit(options);

// or split out the baseDir, supported for backward compatibility
const git: SimpleGit = simpleGit('/some/path', { binary: 'git' });
```

The first argument can be either a string (representing the working directory for `git` commands to run in),
`SimpleGitOptions` object or `undefined`, the second parameter is an optional `SimpleGitOptions` object.

All configuration properties are optional, the default values are shown in the example above.


## Per-command Configuration

To prefix the commands run by `simple-git` with custom configuration not saved in the git config (ie: using the
`-c` command) supply a `config` option to the instance builder:

```typescript
// configure the instance with a custom configuration property
const git: SimpleGit = simpleGit('/some/path', { config: ['http.proxy=someproxy'] });

// any command executed will be prefixed with this config
// runs: git -c http.proxy=someproxy pull
await git.pull();
```


## Configuring Plugins

- [AbortController](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-ABORT-CONTROLLER.md)
   Terminate pending and future tasks in a `simple-git` instance (requires node >= 16).

- [Custom Binary](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-CUSTOM-BINARY.md)
   Customise the `git` binary `simple-git` uses when spawning `git` child processes. 

- [Completion Detection](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-COMPLETION-DETECTION.md)
   Customise how `simple-git` detects the end of a `git` process.

- [Error Detection](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-ERRORS.md)
   Customise the detection of errors from the underlying `git` process.

- [Progress Events](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-PROGRESS-EVENTS.md)
   Receive progress events as `git` works through long-running processes.

- [Spawned Process Ownership](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-SPAWN-OPTIONS.md)
   Configure the system `uid` / `gid` to use for spawned `git` processes.

- [Timeout](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-TIMEOUT.md)
   Automatically kill the wrapped `git` process after a rolling timeout.

- [Unsafe](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-UNSAFE-ACTIONS.md)
   Selectively opt out of `simple-git` safety precautions - for advanced users and use cases.


# API

| API                                                  | What it does                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `.add([fileA, ...], handlerFn)`                      | adds one or more files to be under source control                                                                                                                                                                                                                                                                                                                                                                            |
| `.addAnnotatedTag(tagName, tagMessage, handlerFn)`   | adds an annotated tag to the head of the current branch                                                                                                                                                                                                                                                                                                                                                                      |
| `.addTag(name, handlerFn)`                           | adds a lightweight tag to the head of the current branch                                                                                                                                                                                                                                                                                                                                                                     |
| `.catFile(options, [handlerFn])`                     | generate `cat-file` detail, `options` should be an array of strings as supported arguments to the [cat-file](https://git-scm.com/docs/git-cat-file) command                                                                                                                                                                                                                                                                  |
| `.checkIgnore([filepath, ...], handlerFn)`           | checks if filepath excluded by .gitignore rules                                                                                                                                                                                                                                                                                                                                                                              |
| `.commit(message, handlerFn)`                        | commits changes in the current working directory with the supplied message where the message can be either a single string or array of strings to be passed as separate arguments (the `git` command line interface converts these to be separated by double line breaks)                                                                                                                                                    |
| `.commit(message, [fileA, ...], options, handlerFn)` | commits changes on the named files with the supplied message, when supplied, the optional options object can contain any other parameters to pass to the commit command, setting the value of the property to be a string will add `name=value` to the command string, setting any other type of value will result in just the key from the object being passed (ie: just `name`), an example of setting the author is below |
| `.customBinary(gitPath)`                             | sets the command to use to reference git, allows for using a git binary not available on the path environment variable [docs](https://github.com/steveukx/git-js/blob/main/docs/PLUGIN-CUSTOM-BINARY.md)                                                                                                                                                                                                                     |
| `.env(name, value)`                                  | Set environment variables to be passed to the spawned child processes, [see usage in detail below](#environment-variables).                                                                                                                                                                                                                                                                                                  |
| `.exec(handlerFn)`                                   | calls a simple function in the current step                                                                                                                                                                                                                                                                                                                                                                                  |
| `.fetch([options, ] handlerFn)`                      | update the local working copy database with changes from the default remote repo and branch, when supplied the options argument can be a standard [options object](#how-to-specify-options) either an array of string commands as supported by the [git fetch](https://git-scm.com/docs/git-fetch).                                                                                                                          |
| `.fetch(remote, branch, handlerFn)`                  | update the local working copy database with changes from a remote repo                                                                                                                                                                                                                                                                                                                                                       |
| `.fetch(handlerFn)`                                  | update the local working copy database with changes from the default remote repo and branch                                                                                                                                                                                                                                                                                                                                  |
| `.outputHandler(handlerFn)`                          | attaches a handler that will be called with the name of the command being run and the `stdout` and `stderr` [readable streams](https://nodejs.org/api/stream.html#stream_class_stream_readable) created by the [child process](https://nodejs.org/api/child_process.html#child_process_class_childprocess) running that command, see [examples](https://github.com/steveukx/git-js/blob/main/examples/git-output-handler.md) |
| `.raw(args, [handlerFn])`                            | Execute any arbitrary array of commands supported by the underlying git binary. When the git process returns a non-zero signal on exit and it printed something to `stderr`, the command will be treated as an error, otherwise treated as a success.                                                                                                                                                                        |
| `.rebase([options,] handlerFn)`                      | Rebases the repo, `options` should be supplied as an array of string parameters supported by the [git rebase](https://git-scm.com/docs/git-rebase) command, or an object of options (see details below for option formats).                                                                                                                                                                                                  |
| `.revert(commit , [options , [handlerFn]])`          | reverts one or more commits in the working copy. The commit can be any regular commit-ish value (hash, name or offset such as `HEAD~2`) or a range of commits (eg: `master~5..master~2`). When supplied the [options](#how-to-specify-options) argument contain any options accepted by [git-revert](https://git-scm.com/docs/git-revert).                                                                                   |
| `.rm([fileA, ...], handlerFn)`                       | removes any number of files from source control                                                                                                                                                                                                                                                                                                                                                                              |
| `.rmKeepLocal([fileA, ...], handlerFn)`              | removes files from source control but leaves them on disk                                                                                                                                                                                                                                                                                                                                                                    |
| `.tag(args[], handlerFn)`                            | Runs any supported [git tag](https://git-scm.com/docs/git-tag) commands with arguments passed as an array of strings .                                                                                                                                                                                                                                                                                                       |
| `.tags([options, ] handlerFn)`                       | list all tags, use the optional [options](#how-to-specify-options) object to set any options allows by the [git tag](https://git-scm.com/docs/git-tag) command. Tags will be sorted by semantic version number by default, for git versions 2.7 and above, use the `--sort` option to set a custom sort.                                                                                                                     |


## git config

-  `.addConfig(key, value, append = false, scope = 'local')` add a local configuration property, when `append` is set to
   `true` the configuration setting is appended to rather than overwritten in the local config. Use the `scope` argument
   to pick where to save the new configuration setting (use the exported `GitConfigScope` enum, or equivalent string
   values - `worktree | local | global | system`).
-  `.getConfig(key)` get the value(s) for a named key as a [ConfigGetResult](https://github.com/steveukx/git-js/blob/main/simple-git/typings/response.d.ts)
-  `.getConfig(key, scope)` get the value(s) for a named key as a [ConfigGetResult](https://github.com/steveukx/git-js/blob/main/simple-git/typings/response.d.ts) but limit the
   scope of the properties searched to a single specified scope (use the exported `GitConfigScope` enum, or equivalent
   string values - `worktree | local | global | system`)

-  `.listConfig()` reads the current configuration and returns a [ConfigListSummary](https://github.com/steveukx/git-js/blob/main/simple-git/src/lib/responses/ConfigList.ts)
-  `.listConfig(scope: GitConfigScope)` as with `listConfig` but returns only those items in a specified scope (note that configuration values are overlaid on top of each other to build the config `git` will actually use - to resolve the configuration you are using use `(await listConfig()).all` without the scope argument)


## git grep [examples](https://github.com/steveukx/git-js/blob/main/examples/git-grep.md)

-  `.grep(searchTerm)` searches for a single search term across all files in the working tree, optionally passing a standard [options](#how-to-specify-options) object of additional arguments
-  `.grep(grepQueryBuilder(...))` use the `grepQueryBuilder` to create a complex query to search for, optionally passing a standard [options](#how-to-specify-options) object of additional arguments


## git init

-  `.init(bare , [options])` initialize a repository using the boolean `bare` parameter to intialise a bare repository.
   Any number of other arguments supported by [git init](https://git-scm.com/docs/git-init) can be supplied as an
   [options](#how-to-specify-options) object/array.

-  `.init([options])` initialize a repository using any arguments supported by
   [git init](https://git-scm.com/docs/git-init) supplied as an [options](#how-to-specify-options) object/array.


## git version [examples](https://github.com/steveukx/git-js/blob/main/examples/git-version.md)

- `.version()` retrieve the major, minor and patch for the currently installed `git`. Use the `.installed` property of the result to determine whether `git` is accessible on the path.


## How to Specify Options

Where the task accepts custom options (eg: `pull` or `commit`), these can be supplied as an object, the keys of which
will all be merged as trailing arguments in the command string, or as a simple array of strings.


### Options as an Object

When the value of the property in the options object is a `string`, that name value
pair will be included in the command string as `name=value`. For example:

```javascript
// results in 'git pull origin master --no-rebase'
git.pull('origin', 'master', { '--no-rebase': null });

// results in 'git pull origin master --rebase=true'
git.pull('origin', 'master', { '--rebase': 'true' });
```

When the value of the property is an array of `string`s or `number`s, each element will be 
included as separate `name=value` pairs:

```javascript
// results in 'git log --grep=bug --grep=fix --grep=feature'
git.log({ '--grep': ['bug', 'fix', 'feature'] });
```


### Options as an Array

Options can also be supplied as an array of strings to be merged into the task's commands
in the same way as when an object is used:

```javascript
// results in 'git pull origin master --no-rebase'
git.pull('origin', 'master', ['--no-rebase']);
```


# Environment Variables

Pass one or more environment variables to the child processes spawned by `simple-git` with the `.env` method which
supports passing either an object of name=value pairs or setting a single variable at a time:

```javascript
const GIT_SSH_COMMAND = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no';

simpleGit()
   .env('GIT_SSH_COMMAND', GIT_SSH_COMMAND)
   .status((err, status) => {
      /*  */
   });

simpleGit()
   .env({ ...process.env, GIT_SSH_COMMAND })
   .status()
   .then((status) => {})
   .catch((err) => {});
```

Note - when passing environment variables into the child process, these will replace the standard `process.env`
variables, the example above creates a new object based on `process.env` but with the `GIT_SSH_COMMAND` property added.


# Troubleshooting / FAQ


# Examples


### Initialise a git repo if necessary

```javascript
const git = simpleGit(__dirname);

git.checkIsRepo()
   .then((isRepo) => !isRepo && initialiseRepo(git))
   .then(() => git.fetch());

function initialiseRepo(git) {
   return git.init().then(() => git.addRemote('origin', 'https://some.git.repo'));
}
```


### Set the local configuration for author, then author for an individual commit

```javascript
simpleGit()
   .addConfig('user.name', 'Some One')
   .addConfig('user.email', 'some@one.com')
   .commit('committed as "Some One"', 'file-one')
   .commit('committed as "Another Person"', 'file-two', {
      '--author': '"Another Person <another@person.com>"',
   });
```
