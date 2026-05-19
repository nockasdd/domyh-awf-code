---
library: cypress
version: latest
latest: true
category: testing
official_docs: https://docs.cypress.io
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/cypress-io/cypress-documentation/contents/docs/app
---

# Frequently Asked Questions


### <Icon name="angle-right" /> Can I write API tests using Cypress?

Cypress is mainly designed to run end-to-end and component tests, but if you
need to write a few tests that call the backend API using the
[`cy.request()`](/api/commands/request) command ... who can stop you?

```js
it('adds a todo', () => {
  cy.request({
    url: '/todos',
    method: 'POST',
    body: {
      title: 'Write REST API',
    },
  })
    .its('body')
    .should('deep.contain', {
      title: 'Write REST API',
      completed: false,
    })
})
```

Take a look at our <Icon name="github" inline="true" contentType="rwa" /> that
uses quite a few such tests to verify the backend APIs.

You can verify the responses using the built-in assertions and perform multiple
calls. You can even write E2E tests that combine UI commands with API testing as
needed:

```js
it('adds todos', () => {
  // drive the application through its UI
  cy.visit('/')
  cy.get('.new-todo')
    .type('write E2E tests{enter}')
    .type('add API tests as needed{enter}')
  // now confirm the server has 2 todo items
  cy.request('/todos')
    .its('body')
    .should('have.length', 2)
    .and((items) => {
      // confirm the returned items
    })
})
```

A good strategy for writing targeted API tests is to use them to reach the
hard-to-test code not covered by other tests. You can find such places in the
code using the [code coverage](/app/tooling/code-coverage) as a guide. Watch
the


### <Icon name="angle-right" /> Can I override environment variables or create configuration for different environments?

Yes, you can pass configuration to Cypress via environment variables, CLI
arguments and other means.

[Read the Environment Variables & Secrets guide.](/app/guides/environment-variables)


### <Icon name="angle-right" /> What is the right balance between custom commands and utility functions?

There is already a great section in
[Custom Commands](/api/cypress-api/custom-commands#Best-Practices) guide that
talks about trade-offs between custom commands and utility functions. We feel
reusable functions in general are a way to go. Plus they do not confuse
[IntelliSense like custom commands do](https://github.com/cypress-io/cypress/issues/1065).


### <Icon name="angle-right" /> I tried to install Cypress in my CI, but I get the error: `EACCES: permission denied`.

First, make sure you have [Node](https://nodejs.org) installed on your system.
`npm` is a Node package that is installed globally by default when you install
Node and is required to install our
[`cypress` npm package](/app/references/command-line).

Next, you'd want to check that you have the proper permissions for installing on
your system or you may need to run `sudo npm install cypress`.


### <Icon name="angle-right" /> How does Cypress component testing compare to other options?

When Cypress mounts a component, it does so in an actual browser and not a
simulated environment like jsdom. This allows you to visually see and interact
with the component as you work on it. You can use the same browser-based
developer tools that you are used to when building web applications, such as
element inspectors, modifying CSS, and source debugging.

Cypress Component Testing is built around the same tools and APIs that
end-to-end testing uses. Anyone familiar with Cypress can immediately hop in and
feel productive writing component tests without a large learning curve.
Component tests can also use the vast Cypress ecosystem, plugins, and services
(like [Cypress Cloud](https://www.cypress.io/cloud)) already available to
complement your component tests.
