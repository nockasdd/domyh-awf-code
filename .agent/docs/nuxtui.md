---
library: nuxtui
version: 3.x
latest: true
category: frontend
official_docs: https://ui.nuxt.com
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://ui.nuxt.com/llms-full.txt
---

# Installation

\> \[!NOTE]
\> See: /docs/getting-started/installation/vue
\> Looking for the Vue version?


## Setup


# Installation

\> \[!NOTE]
\> See: /docs/getting-started/installation/nuxt
\> Looking for the Nuxt version?


## Setup


# Installation

\> \[!NOTE]
\> See: /docs/getting-started/installation/vue
\> Looking for the Vue version?


## Setup


# Installation

\> \[!NOTE]
\> See: /docs/getting-started/installation/nuxt
\> Looking for the Nuxt version?


## Setup


### IDE Setup

We recommend using VSCode alongside the [ESLint extension](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint){rel="&#x22;nofollow&#x22;"}. You can enable auto-fix and formatting when saving your code. Here's how:

```json [.vscode/settings.json]
{
  "editor.codeActionsOnSave": {
    "source.fixAll": "never",
    "source.fixAll.eslint": "explicit"
  },
  "prettier.enable": false
}
```

\> \[!WARNING]
\> Since ESLint is already configured to format the code, there's no need for duplicating functionality with Prettier. If you have it installed in your editor, we recommend disabling it to avoid conflicts.


## Usage


## Installation

To get started, you can follow the official [guide](https://content.nuxt.com/docs/getting-started/installation){rel="&#x22;nofollow&#x22;"} or in summary:

\`\`\`bash
pnpm add @nuxt/content
\`\`\`
\`\`\`bash
yarn add @nuxt/content
\`\`\`
\`\`\`bash
npm install @nuxt/content
\`\`\`
\`\`\`bash
bun add @nuxt/content
\`\`\`

Then, add the `@nuxt/content` module in your `nuxt.config.ts`:

```ts [nuxt.config.ts] {4}
export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@nuxt/content'
  ],
  css: ['~/assets/css/main.css']
})
```

\> \[!CAUTION]
\> You need to register \`@nuxt/content\` after \`@nuxt/ui\` in the \`modules\` array, otherwise the prose components will not be available.


#### Setup Instructions:

1. Open Claude Desktop and navigate to "Settings" > "Developer".
2. Click on "Edit Config". This will open the local Claude directory.
3. Modify the `claude_desktop_config.json` file with your custom MCP server configuration.

```json [claude_desktop_config.json]
{
  "mcpServers": {
    "nuxt-ui": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://ui.nuxt.com/mcp"
      ]
    }
  }
}
```

4. Restart Claude Desktop app. The Nuxt UI MCP server should now be registered.


#### Quick Install

Click the button below to install the Nuxt UI MCP server directly in Cursor:

\[Install MCP Server]\(cursor://anysphere.cursor-deeplink/mcp/install?name=nuxt-ui\&config=eyJ0eXBlIjoiaHR0cCIsInVybCI6Imh0dHBzOi8vdWkubnV4dC5jb20vbWNwIn0%3D)


#### Manual Setup Instructions:

1. Open Cursor and go to "Settings" > "Tools & MCP"
2. Add the Nuxt UI MCP server configuration

Or manually create/update `.cursor/mcp.json` in your project root:

```json [.cursor/mcp.json]
{
  "mcpServers": {
    "nuxt-ui": {
      "type": "http",
      "url": "https://ui.nuxt.com/mcp"
    }
  }
}
```


#### Setup Instructions:

1. Open the MCP store via the "..." dropdown at the top of the editor's agent panel.
2. Click on "Manage MCP Servers"
3. Click on "View raw config"
4. Modify the `mcp_config.json` with your custom MCP server configuration:

```json
{
  "mcpServers": {
    "nuxt-ui": {
      "serverUrl": "https://ui.nuxt.com/mcp"
    }
  }
}
```

5. Return to the "Manage MCP Servers" tab and click "Refresh". The Nuxt UI MCP server should now appear.


#### Setup Instructions:

1. Locate your Gemini CLI configuration file (usually \~/.gemini/settings.json or as specified in your environment).
2. Add the following configuration to your mcpServers object:

```json
{
  "mcpServers": {
    "nuxt-ui": {
      "url": "https://ui.nuxt.com/mcp"
    }
  }
}
```

3. Restart your terminal session or reload the CLI. The Nuxt UI MCP server tools will now be available for use.


#### Setup Instructions:

1. Navigate to "Intelligence" > "Connectors"
2. Click on "Add Connector" button, then select "Custom MCP Connector"
3. Create your Custom MCP Connector:
   - Connector Name: `NuxtUI`
   - Connector Server: `https://ui.nuxt.com/mcp`


#### Setup Instructions:

1. Open VS Code and access the Command Palette (Ctrl/Cmd + Shift + P)
2. Type "Preferences: Open Workspace Settings (JSON)" and select it
3. Navigate to your project's `.vscode` folder or create one if it doesn't exist
4. Create or edit the `mcp.json` file with the following configuration:

```json [.vscode/mcp.json]
{
  "servers": {
    "nuxt-ui": {
      "type": "http",
      "url": "https://ui.nuxt.com/mcp"
    }
  }
}
```


#### Setup Instructions:

1. Open Windsurf and navigate to "Settings" > "Windsurf Settings" > "Cascade"
2. Click the "Manage MCPs" button, then select the "View raw config" option
3. Add the following configuration to your MCP settings:

```json [.codeium/windsurf/mcp_config.json]
{
  "mcpServers": {
    "nuxt-ui": {
      "type": "http",
      "url": "https://ui.nuxt.com/mcp"
    }
  }
}
```


#### Setup Instructions:

1. Open Zed and go to "Settings" > "Open Settings"
2. Navigate to the JSON settings file
3. Add the following context server configuration to your settings:

```json [.config/zed/settings.json]
{
  "context_servers": {
    "nuxt-ui": {
      "source": "custom",
      "command": "npx",
      "args": ["mcp-remote", "https://ui.nuxt.com/mcp"],
      "env": {}
    }
  }
}
```


#### Setup Instructions:

1. In your project root, create `opencode.json`
2. Add the following configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "nuxt-ui": {
      "type": "remote",
      "url": "https://ui.nuxt.com/mcp",
      "enabled": true
    }
  }
}
```


#### Setup Instructions:

1. Navigate to your GitHub repository
2. Go to **Settings** > **Code & automation** > **Copilot** > **Coding agent**
3. In the **MCP configuration** section, add the following configuration:

```json
{
  "mcpServers": {
    "nuxt-ui": {
      "type": "http",
      "url": "https://ui.nuxt.com/mcp",
      "tools": ["*"]
    }
  }
}
```

4. Click Save


#### Quick Install

Click the button below to install the Nuxt UI skill directly in Cursor:

\[Install Skill]\(cursor://anysphere.cursor-deeplink/install-skill?url=https\://github.com/nuxt/ui/tree/v4/skills/nuxt-ui)


#### Manual Setup

1. Open Cursor and go to "Settings" > "Skills"
2. Click "Add skill" and enter the following URL:

```text
https://github.com/nuxt/ui/tree/v4/skills/nuxt-ui
```


## API


## Usage


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## Installation

The Chat components are designed to be used with the [Vercel AI SDK](https://ai-sdk.dev/){rel="&#x22;nofollow&#x22;"}, specifically the [`Chat`](https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-chat){rel="&#x22;nofollow&#x22;"} class for managing chat state and streaming responses.

Install the required dependencies:

\`\`\`bash
pnpm add ai @ai-sdk/gateway @ai-sdk/vue
\`\`\`
\`\`\`bash
yarn add ai @ai-sdk/gateway @ai-sdk/vue
\`\`\`
\`\`\`bash
npm install ai @ai-sdk/gateway @ai-sdk/vue
\`\`\`
\`\`\`bash
bun add ai @ai-sdk/gateway @ai-sdk/vue
\`\`\`


## Server Setup

Create a server API endpoint to handle chat requests using [`streamText`](https://ai-sdk.dev/docs/reference/ai-sdk-core/stream-text){rel="&#x22;nofollow&#x22;"}. You can use the [Vercel AI Gateway](https://vercel.com/ai-gateway){rel="&#x22;nofollow&#x22;"} to access AI models through a centralized endpoint:

```ts [server/api/chat.post.ts]
import { streamText, convertToModelMessages } from 'ai'
import { gateway } from '@ai-sdk/gateway'

export default defineEventHandler(async (event) => {
  const { messages } = await readBody(event)

  return streamText({
    model: gateway('anthropic/claude-sonnet-4.6'),
    maxOutputTokens: 10000,
    system: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages)
  }).toUIMessageStreamResponse()
})
```


## Client Setup

Use the `Chat` class from `@ai-sdk/vue` to manage chat state and connect to your server endpoint:

```vue
<script setup lang="ts">
import type { UIMessage } from 'ai'
import { isReasoningUIPart, isTextUIPart, isToolUIPart, getToolName } from 'ai'
import { Chat } from '@ai-sdk/vue'
import { isReasoningStreaming, isToolStreaming } from '@nuxt/ui/utils/ai'

const input = ref('')

const chat = new Chat({
  onError(error) {
    console.error(error)
  }
})

function onSubmit() {
  chat.sendMessage({ text: input.value })

  input.value = ''
}
</script>

<template>
  <UChatMessages
    :messages="chat.messages"
    :status="chat.status"
  >
    <template #content="{ message }">
      <template
        v-for="(part, index) in message.parts"
        :key="`${message.id}-${part.type}-${index}`"
      >
        <UChatReasoning
          v-if="isReasoningUIPart(part)"
          :text="part.text"
          :streaming="isReasoningStreaming(message, index, chat)"
        >
          <MDC
            :value="part.text"
            :cache-key="`reasoning-${message.id}-${index}`"
            class="*:first:mt-0 *:last:mb-0"
          />
        </UChatReasoning>

        <UChatTool
          v-else-if="isToolUIPart(part)"
          :text="getToolName(part)"
          :streaming="isToolStreaming(part)"
        />

        <MDC
          v-else-if="isTextUIPart(part)"
          :value="part.text"
          :cache-key="`${message.id}-${index}`"
          class="*:first:mt-0 *:last:mb-0"
        />
      </template>
    </template>
  </UChatMessages>

  <UChatPrompt
    v-model="input"
    :error="chat.error"
    @submit="onSubmit"
  >
    <UChatPromptSubmit
      :status="chat.status"
      @stop="chat.stop()"
      @reload="chat.regenerate()"
    />
  </UChatPrompt>
</template>
```

\> \[!NOTE]
\> In this example, we use the \`MDC\` component from \[\`@nuxtjs/mdc\`]\(https\://github.com/nuxt-modules/mdc) to render messages as Markdown. As Nuxt UI provides pre-styled prose components, your content will be automatically styled.

\> \[!TIP]
\> See: /blog/how-to-build-an-ai-chat
\> Read the full Build an AI Chatbot tutorial for a step-by-step guide.



## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


### With infinite scroll `4.4+`

You can use the [`useInfiniteScroll`](https://vueuse.org/core/useInfiniteScroll/){rel="&#x22;nofollow&#x22;"} composable to load more data as the user scrolls.

```vue [InputMenuInfiniteScrollExample.vue]
<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core'

type User = {
  firstName: string
}

type UserResponse = {
  users: User[]
  total: number
  skip: number
  limit: number
}

const skip = ref(0)

const { data, status, execute } = await useLazyFetch('https://dummyjson.com/users?limit=10&select=firstName', {
  key: 'input-menu-users-infinite-scroll',
  params: { skip },
  transform: (data?: UserResponse) => {
    return data?.users.map(user => user.firstName)
  },
  immediate: false
})

const users = ref<string[]>([])

watch(data, () => {
  users.value = [
    ...users.value,
    ...(data.value || [])
  ]
})

function onOpen() {
  if (!users.value?.length) {
    execute()
  }
}

const inputMenu = useTemplateRef('inputMenu')

onMounted(() => {
  useInfiniteScroll(() => inputMenu.value?.viewportRef, () => {
    skip.value += 10
  }, {
    canLoadMore: () => {
      return status.value !== 'pending'
    }
  })
})
</script>

<template>
  <UInputMenu
    ref="inputMenu"
    placeholder="Select user"
    :items="users"
    @update:open="onOpen"
  />
</template>
```

\> \[!NOTE]
\> This example uses \`useLazyFetch\` with \`immediate: false\` so data is only loaded as the user scrolls.


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API


### With infinite scroll

You can use the [`useInfiniteScroll`](https://vueuse.org/core/useInfiniteScroll/){rel="&#x22;nofollow&#x22;"} composable to load more data as the user scrolls.

```vue [ScrollAreaInfiniteScrollExample.vue]
<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core'

type User = {
  id: number
  firstName: string
  lastName: string
  username: string
  email: string
  image: string
}

type UserResponse = {
  users: User[]
  total: number
  skip: number
  limit: number
}

const skip = ref(0)

const { data, status } = useLazyFetch('https://dummyjson.com/users?limit=10&select=firstName,lastName,username,email,image', {
  key: 'scroll-area-users-infinite-scroll',
  params: { skip },
  transform: (data?: UserResponse) => {
    return data?.users
  },
  server: false
})

const users = ref<User[]>([])

watch(data, () => {
  users.value = [
    ...users.value,
    ...(data.value || [])
  ]
})

const scrollArea = useTemplateRef('scrollArea')

onMounted(() => {
  useInfiniteScroll(scrollArea.value?.$el, () => {
    skip.value += 10
  }, {
    distance: 200,
    canLoadMore: () => {
      return status.value !== 'pending'
    }
  })
})
</script>

<template>
  <UScrollArea
    ref="scrollArea"
    v-slot="{ item }"
    :items="users"
    :virtualize="{
      estimateSize: 88,
      skipMeasurement: true
    }"
    class="h-96 w-full"
  >
    <UPageCard
      orientation="horizontal"
      class="rounded-none"
    >
      <UUser
        :name="`${item.firstName} ${item.lastName}`"
        :description="item.email"
        :avatar="{ src: item.image, alt: item.firstName, loading: 'lazy' as const }"
        size="lg"
      />
    </UPageCard>
  </UScrollArea>

  <UProgress
    v-if="status === 'pending' || status === 'idle'"
    indeterminate
    size="xs"
    class="absolute top-0 inset-x-0 z-1"
    :ui="{ base: 'bg-default' }"
  />
</template>
```

\> \[!NOTE]
\> This example uses \`useLazyFetch\` with \`server: false\` to fetch data on the client without blocking the initial render. The loading state checks for both \`pending\` and \`idle\` status to display a loading indicator before and during the fetch. Additional pages are loaded as the user scrolls.


## API


### With infinite scroll `4.4+`

You can use the [`useInfiniteScroll`](https://vueuse.org/core/useInfiniteScroll/){rel="&#x22;nofollow&#x22;"} composable to load more data as the user scrolls.

```vue [SelectInfiniteScrollExample.vue]
<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core'

type User = {
  firstName: string
}

type UserResponse = {
  users: User[]
  total: number
  skip: number
  limit: number
}

const skip = ref(0)

const { data, status, execute } = await useLazyFetch('https://dummyjson.com/users?limit=10&select=firstName', {
  key: 'select-users-infinite-scroll',
  params: { skip },
  transform: (data?: UserResponse) => {
    return data?.users.map(user => user.firstName)
  },
  immediate: false
})

const users = ref<string[]>([])

watch(data, () => {
  users.value = [
    ...users.value,
    ...(data.value || [])
  ]
})

function onOpen() {
  if (!users.value?.length) {
    execute()
  }
}

const select = useTemplateRef('select')

onMounted(() => {
  useInfiniteScroll(() => select.value?.viewportRef, () => {
    skip.value += 10
  }, {
    canLoadMore: () => {
      return status.value !== 'pending'
    }
  })
})
</script>

<template>
  <USelect
    ref="select"
    placeholder="Select user"
    :items="users"
    @update:open="onOpen"
  />
</template>
```

\> \[!NOTE]
\> This example uses \`useLazyFetch\` with \`immediate: false\` so data is only loaded as the user scrolls.


## API


### With infinite scroll `4.4+`

You can use the [`useInfiniteScroll`](https://vueuse.org/core/useInfiniteScroll/){rel="&#x22;nofollow&#x22;"} composable to load more data as the user scrolls.

```vue [SelectMenuInfiniteScrollExample.vue]
<script setup lang="ts">
import { useInfiniteScroll } from '@vueuse/core'

type User = {
  firstName: string
}

type UserResponse = {
  users: User[]
  total: number
  skip: number
  limit: number
}

const skip = ref(0)

const { data, status, execute } = await useLazyFetch('https://dummyjson.com/users?limit=10&select=firstName', {
  key: 'select-menu-users-infinite-scroll',
  params: { skip },
  transform: (data?: UserResponse) => {
    return data?.users.map(user => user.firstName)
  },
  immediate: false
})

const users = ref<string[]>([])

watch(data, () => {
  users.value = [
    ...users.value,
    ...(data.value || [])
  ]
})

function onOpen() {
  if (!users.value?.length) {
    execute()
  }
}

const selectMenu = useTemplateRef('selectMenu')

onMounted(() => {
  useInfiniteScroll(() => selectMenu.value?.viewportRef, () => {
    skip.value += 10
  }, {
    canLoadMore: () => {
      return status.value !== 'pending'
    }
  })
})
</script>

<template>
  <USelectMenu
    ref="selectMenu"
    placeholder="Select user"
    :items="users"
    @update:open="onOpen"
  />
</template>
```

\> \[!NOTE]
\> This example uses \`useLazyFetch\` with \`immediate: false\` so data is only loaded as the user scrolls.


## API


## API


## API


## API


## API


## API


## API


## API


### With infinite scroll

If you use server-side pagination, you can use the [`useInfiniteScroll`](https://vueuse.org/core/useInfiniteScroll/#useinfinitescroll){rel="&#x22;nofollow&#x22;"} composable to load more data as the user scrolls.

```vue [TableInfiniteScrollExample.vue]
<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { useInfiniteScroll } from '@vueuse/core'

const UAvatar = resolveComponent('UAvatar')

type User = {
  id: number
  firstName: string
  username: string
  email: string
  image: string
}

type UserResponse = {
  users: User[]
  total: number
  skip: number
  limit: number
}

const skip = ref(0)

const { data, status } = useLazyFetch('https://dummyjson.com/users?limit=10&select=firstName,username,email,image', {
  key: 'table-users-infinite-scroll',
  params: { skip },
  transform: (data?: UserResponse) => {
    return data?.users
  },
  server: false
})

const columns: TableColumn<User>[] = [{
  accessorKey: 'id',
  header: 'ID'
}, {
  accessorKey: 'image',
  header: 'Avatar',
  cell: ({ row }) => h(UAvatar, { src: row.original.image, loading: 'lazy' })
}, {
  accessorKey: 'firstName',
  header: 'First name'
}, {
  accessorKey: 'email',
  header: 'Email'
}, {
  accessorKey: 'username',
  header: 'Username'
}]

const users = ref<User[]>([])

watch(data, () => {
  users.value = [
    ...users.value,
    ...(data.value || [])
  ]
})

const table = useTemplateRef('table')

onMounted(() => {
  useInfiniteScroll(table.value?.$el, () => {
    skip.value += 10
  }, {
    distance: 200,
    canLoadMore: () => {
      return status.value !== 'pending'
    }
  })
})
</script>

<template>
  <UTable
    ref="table"
    :data="users"
    :columns="columns"
    :loading="status === 'pending' || status === 'idle'"
    sticky
    class="flex-1 h-80"
  />
</template>
```

\> \[!NOTE]
\> This example uses \`useLazyFetch\` with \`server: false\` to fetch data on the client without blocking the initial render. The loading state checks for both \`pending\` and \`idle\` status to display a loading indicator before and during the fetch. Additional pages are loaded as the user scrolls.


## API


## API


## API


## API


## API


## API


## API


## API


## API


## API

`defineLocale<M>(options: DefineLocaleOptions<M>): Locale<M>`{.shiki,shiki-themes,material-theme-lighter,material-theme,material-theme-palenight lang="ts-type"}

Creates a new locale object with the provided options.


## API

`defineShortcuts(config: ShortcutsConfig, options?: ShortcutsOptions): void`{.shiki,shiki-themes,material-theme-lighter,material-theme,material-theme-palenight lang="ts-type"}

Define keyboard shortcuts for your application.


#### Shortcut definition

Shortcuts are defined using the following format:

- Single key: `'a'`, `'b'`, `'1'`, `'?'`, etc.
- Key combinations: Use `_` to separate keys, e.g., `'meta_k'`, `'ctrl_shift_f'`
- Key sequences: Use `-` to define a sequence, e.g., `'g-d'`


## Instance API


## API

`useScrollShadow(element, options?)`{.shiki,shiki-themes,material-theme-lighter,material-theme,material-theme-palenight lang="ts-type"}
