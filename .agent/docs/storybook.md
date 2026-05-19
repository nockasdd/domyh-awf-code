---
library: storybook
version: 9.x
latest: true
category: testing
official_docs: https://storybook.js.org/docs
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/storybookjs/storybook/contents/docs/writing-stories
---

# How to write stories


<IfRenderer renderer="svelte">

  With Svelte, stories can be defined as objects using standard CSF or with Svelte CSF's `Story` component. Both methods describe how to render a component. You can have multiple stories per component, and those stories can build upon one another. For example, we can add Secondary and Tertiary stories based on our Primary story above.

</IfRenderer>

<If notRenderer="svelte">

  A story is an object that describes how to render a component. You can have multiple stories per component, and those stories can build upon one another. For example, we can add Secondary and Tertiary stories based on our Primary story from above.

</If>

{/* prettier-ignore-start */}

<CodeSnippets path="button-story-using-args.md" />

{/* prettier-ignore-end */}

What’s more, you can import `args` to reuse when writing stories for other components, and it's helpful when you’re building composite components. For example, if we make a `ButtonGroup` story, we might remix two stories from its child component `Button`.

{/* prettier-ignore-start */}

<CodeSnippets path="button-group-story.md" />

{/* prettier-ignore-end */}

When Button’s signature changes, you only need to change Button’s stories to reflect the new schema, and ButtonGroup’s stories will automatically be updated. This pattern allows you to reuse your data definitions across the component hierarchy, making your stories more maintainable.

That’s not all! Each of the args from the story function are live editable using Storybook’s [Controls](../essentials/controls.mdx) panel. It means your team can dynamically change components in Storybook to stress test and find edge cases.

<Video src="../_assets/writing-stories/addon-controls-demo-optimized.mp4" />

You can also use the Controls panel to edit or save a new story after adjusting its control values.

<Video src="../_assets/get-started/edit-story-from-controls-optimized.mp4" />

<If renderer="svelte">

  <Callout variant="info">

    This feature is not supported with the Svelte CSF. To opt-in to this feature with Svelte, you must use Storybook's [Component Story Format](../api/csf/index.mdx).
  
  </Callout>
  
</If>

Addons can enhance args. For instance, [Actions](../essentials/actions.mdx) auto-detects which args are callbacks and appends a logging function to them. That way, interactions (like clicks) get logged in the actions panel.

<Video src="../_assets/writing-stories/addon-actions-demo-optimized.mp4" />


## [Mocking API Services](./mocking-data-and-modules/mocking-network-requests.mdx)

For components that make network requests (e.g., fetching data from a REST or GraphQL API), you can mock those requests in your stories.


# Recipes


## Preview API hooks

The same applies to Storybook hooks you want to call in your decorator. For instance, this decorator increments a counter used by its decorated story.

{/* prettier-ignore-start */}

<CodeSnippets path="decorator-with-updateArgs.md" />

{/* prettier-ignore-end */}

</IfRenderer>


# Reusing story definitions

We can also reduce repetition in our stories by reusing story definitions. Here, we can reuse the `ListItem` stories' args in the story for `List`:

{/* prettier-ignore-start */}

<CodeSnippets path="list-story-reuse-data.md" />

{/* prettier-ignore-end */}

By rendering the `Unchecked` story with its args, we are able to reuse the input data from the `ListItem` stories in the `List`.

<If renderer="react">
  However, we still aren’t using args to control the `ListItem` stories, which means we cannot change them with controls and we cannot reuse them in other, more complex component stories.

  ## Using children as an arg

  One way we improve that situation is by pulling the rendered subcomponent out into a `children` arg:

  {/* prettier-ignore-start */}

  <CodeSnippets path="list-story-with-unchecked-children.md" />

  {/* prettier-ignore-end */}

  Now that `children` is an arg, we can potentially reuse it in another story.

  However, there are some caveats when using this approach that you should be aware of.

  The `children` arg, just like all args, needs to be JSON serializable. To avoid errors with your Storybook, you should:

  * Avoid using empty values
  * Use [mapping](../essentials/controls.mdx#dealing-with-complex-values) if you want to adjust the value with [controls](../essentials/controls.mdx)
  * Use caution with components that include third party libraries

  <Callout variant="info">
    We're currently working on improving the overall experience for the children arg and allow you to edit children arg in a control and allow you to use other types of components in the near future. But for now you need to factor in this caveat when you're implementing your stories.
  </Callout>

  {/* End if react */}
</If>


# Fetching API data

Stories are isolated component examples that render internal data defined as part of the story or alongside the story as [args](./args.mdx).

Loaders are helpful when you need to load story data externally (e.g., from a remote API). Consider the following example that fetches a todo item to display in a todo list:

{/* prettier-ignore-start */}

<CodeSnippets path="loader-story.md" />

{/* prettier-ignore-end */}

The response obtained from the remote API call is combined into a `loaded` field on the story context, which is the second argument to a story function. For example, in React, the story's args were spread first to prioritize them over the static data provided by the loader. With other frameworks (e.g., Angular), you can write your stories as you'd usually do.
