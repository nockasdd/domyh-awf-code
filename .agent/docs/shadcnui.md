---
library: shadcnui
version: latest
latest: true
category: css
official_docs: https://ui.shadcn.com
last_updated: 2026-03-20
last_checked: 2026-03-21
source: official docs + crawl4ai/trafilatura extraction
---

# shadcn/ui

> shadcn/ui — Beautifully designed components built with Radix UI + Tailwind CSS.
> NOT a package — copy/paste components into your project.
> Docs: https://ui.shadcn.com

## Installation

```bash
# Next.js
npx shadcn@latest init

# Vite + React
npx shadcn@latest init

# Follow prompts: style, color, CSS variables
```

### Add Components

```bash
npx shadcn@latest add button
npx shadcn@latest add card dialog form input
npx shadcn@latest add --all  # add all components
```

## Core Components

```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

// Button variants
<Button variant="default">Primary</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Outline</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button size="icon"><IconSearch /></Button>

// Card
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Content here</p>
  </CardContent>
</Card>

// Input
<Input type="email" placeholder="Email" />
```

### Form + Validation (react-hook-form + zod)

```tsx
"use client"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export function LoginForm() {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: { email: "", password: "" },
  })

  function onSubmit(values: z.infer<typeof schema>) {
    console.log(values)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email</FormLabel>
            <FormControl><Input {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit">Login</Button>
      </form>
    </Form>
  )
}
```

### Dialog / Sheet / Dropdown

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild><Button>Open</Button></DialogTrigger>
  <DialogContent>
    <DialogHeader><DialogTitle>Edit Profile</DialogTitle></DialogHeader>
    <p>Form here</p>
  </DialogContent>
</Dialog>
```

### Data Table

```tsx
import { DataTable } from "@/components/ui/data-table"
import { ColumnDef } from "@tanstack/react-table"

const columns: ColumnDef<User>[] = [
  { accessorKey: "name", header: "Name" },
  { accessorKey: "email", header: "Email" },
  { id: "actions", cell: ({ row }) => <DropdownMenu>...</DropdownMenu> },
]

<DataTable columns={columns} data={users} />
```

## Theming (CSS Variables)

```css
/* OKLCH color format (shadcn/ui default since 2024) */
/* Convention: --{name} = background, --{name}-foreground = text */

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);

  /* Sidebar tokens */
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-border: oklch(0.922 0 0);

  /* Chart tokens */
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
}
```

```tsx
// Usage — bg-{token} text-{token}-foreground
<div className="bg-primary text-primary-foreground">Primary</div>
<div className="bg-muted text-muted-foreground">Muted</div>
<div className="bg-sidebar text-sidebar-foreground">Sidebar</div>
```

## components.json

```jsonc
{
  "style": "new-york",
  "rsc": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

## Component Catalog (60+)

| Category | Components |
|:---------|:----------|
| **Form & Input** | Form, Field, Button, ButtonGroup, Input, InputGroup, InputOTP, Textarea, Checkbox, RadioGroup, Select, Switch, Slider, Calendar, DatePicker, Combobox, Label |
| **Layout & Nav** | Accordion, Breadcrumb, NavigationMenu, Sidebar, Tabs, Separator, ScrollArea, Resizable |
| **Overlays** | Dialog, AlertDialog, Sheet, Drawer, Popover, Tooltip, HoverCard, ContextMenu, DropdownMenu, Menubar, Command |
| **Feedback** | Alert, Toast (Sonner), Progress, Spinner, Skeleton, Badge, Empty |
| **Display** | Avatar, Card, AspectRatio, Carousel, Collapsible, Table, DataTable, Toggle, ToggleGroup |

## MCP Server

```bash
# shadcn/ui MCP Server — AI integration
# Browse, search, install components via AI assistants
npx shadcn@latest mcp

# Works with: Claude Code, Cursor, VS Code Copilot, Codex
```

```jsonc
// Claude Desktop config
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["-y", "shadcn@latest", "mcp"]
    }
  }
}
```

## Registry

```bash
# Create your own component registry
npx shadcn@latest init --registry

# registry/schema.json — defines components, dependencies, files
# Publish to your own domain or npm
```

## Dark Mode Setup

```tsx
// Next.js — use next-themes
import { ThemeProvider } from 'next-themes';

export default function RootLayout({ children }) {
  return (
    <html suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}

// Vite — use vite-plugin-theme
// Astro — use <script> in Layout
// Remix — use remix-themes
```

## Forms Integration

```tsx
// React Hook Form (default)
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

// TanStack Form (alternative)
import { useForm } from '@tanstack/react-form';
// shadcn/ui supports both natively
```

## Gotchas

⚠️ **Not npm package**: Components are copied into `components/ui/`. Edit directly.

⚠️ **cn() util required**: Uses `clsx` + `tailwind-merge` for className merging.

⚠️ **Radix primitives**: Each component wraps Radix — check Radix docs for advanced props.

⚠️ **`"use client"`**: Most interactive components need this directive in Next.js App Router.

⚠️ **OKLCH colors**: Default color format. Use `oklch(lightness chroma hue)` for custom themes.

⚠️ **CSS variables convention**: `--{name}` = background, `--{name}-foreground` = text color.

⚠️ **MCP Server**: `npx shadcn@latest mcp` — AI assistants can browse/install components.

⚠️ **Registry**: Create custom component registries for your team/org.

⚠️ **Tailwind v4**: Supported since shadcn/ui latest. Check migration guide.
