---
name: visualize
trigger: ["/visualize", "ui", "mockup", "thiết kế"]
persona: designer
description: "🖼️ UI/UX Design: mockups, wireframes, component design, visual prototyping"
---

# 🖼️ /visualize — Visualize Pro v5.5

> Multi-Platform Visual Design & Code Generation
> 📚 Web • Desktop • Mobile • 16 Frameworks • Component Mapping

---

## 🔄 VISUALIZE FLOW v5.5

```
User: /visualize [platform] [description]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 0: PLATFORM DETECTION             │
│ ▸ Auto-detect from project files        │
│ ▸ Load platform-specific skill          │
│ ▸ Index existing component library      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: COMPONENT MAPPING (NEW!)       │
│ ▸ Search existing components FIRST      │
│ ▸ Match request to library → 70-90% ↓   │
│ ▸ Generate props only, not full code    │
│ Result: Massive token savings           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: DESIGN                         │
│ ▸ Create wireframes (ASCII/visual)      │
│ ▸ Apply design tokens                   │
│ ▸ Multi-platform code output            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: REVIEW                         │
│ ▸ Present options                       │
│ ⛔ STOP → Confirm design                │
└─────────────────────────────────────────┘
```

---

## 🎯 MULTI-PLATFORM COMMANDS

| Command                       | Platform           | Output               |
| ----------------------------- | ------------------ | -------------------- |
| `/visualize web [page]`       | React/Vue/Svelte   | JSX + Tailwind       |
| `/visualize mobile [screen]`  | Flutter/RN/SwiftUI | Dart/JSX/Swift       |
| `/visualize desktop [window]` | WPF/Qt/Electron    | XAML/QML/HTML        |
| `/visualize component [name]` | Auto-detect        | Component code       |
| `/visualize system`           | All                | Design tokens + docs |
| `/visualize flow [journey]`   | Any                | Mermaid diagram      |
| `/visualize map`              | Current            | Component index      |

---

## 🔍 PLATFORM DETECTION

```yaml
detection:
  package.json:
    react: "Web (React)"
    vue: "Web (Vue)"
    svelte: "Web (Svelte)"
    electron: "Desktop (Electron)"
    react-native: "Mobile (React Native)"

  pubspec.yaml: "Mobile (Flutter)"

  .csproj:
    WPF: "Desktop (WPF)"
    WinUI: "Desktop (WinUI 3)"
    MAUI: "Mobile (.NET MAUI)"
    Avalonia: "Desktop (Avalonia)"

  CMakeLists.txt (Qt): "Desktop (Qt/QML)"
  Cargo.toml (tauri): "Desktop (Tauri)"
  build.gradle.kts (compose): "Mobile (Compose)"
  .xcodeproj: "Mobile (SwiftUI)"
```

---

## 🧩 COMPONENT MAPPING (KEY FEATURE)

### Priority: Map BEFORE Generate

```yaml
component_mapping:
  step_1_index:
    action: "Scan project for existing components"
    paths: ["src/components", "components", "src/ui"]
    result: "Component index file"

  step_2_match:
    action: "Match request to existing components"
    example: '"primary button" → <Button variant="primary">'
    savings: "70-90% token reduction"

  step_3_props:
    action: "Generate props/composition only"
    example: 'size="large" disabled={false}'
    output: "Production-ready usage"

  step_4_gap:
    action: "Only generate missing pieces"
    trigger: "No match found"
    approach: "Use headless + tokens"
```

### Component Decision Matrix

| Need           | → Use            | Token Saved |
| -------------- | ---------------- | ----------- |
| Speed + A11y   | Headless (Radix) | 85-90%      |
| Brand-specific | Custom + tokens  | 60-70%      |
| Data-heavy     | Specialized libs | 70-95%      |
| Standard UI    | shadcn/MUI       | 80-85%      |

---

## 🎨 DESIGN TOKENS (CROSS-PLATFORM)

### Spacing

| Token | Web CSS | Tailwind | WPF | Qt  | Flutter |
| ----- | ------- | -------- | --- | --- | ------- |
| xs    | 4px     | p-1      | 4   | 4   | 4.0     |
| sm    | 8px     | p-2      | 8   | 8   | 8.0     |
| md    | 16px    | p-4      | 16  | 16  | 16.0    |
| lg    | 24px    | p-6      | 24  | 24  | 24.0    |
| xl    | 32px    | p-8      | 32  | 32  | 32.0    |

### Colors

| Token      | Web CSS          | WPF                         | Qt               | Flutter         |
| ---------- | ---------------- | --------------------------- | ---------------- | --------------- |
| primary    | var(--primary)   | {DynamicResource Primary}   | Style.primary    | Theme.primary   |
| secondary  | var(--secondary) | {DynamicResource Secondary} | Style.secondary  | Theme.secondary |
| background | var(--bg)        | {ThemeResource PageBg}      | palette.window() | scaffold.bg     |

### Touch Targets

| Platform | Minimum | Recommended |
| -------- | ------- | ----------- |
| Web      | 44×44px | 48×48px     |
| iOS      | 44×44pt | 48×48pt     |
| Android  | 48×48dp | 56×56dp     |
| Desktop  | 32×32px | 40×40px     |

---

## 📊 DESIGN SPECIFICATION v5.5

```markdown
🖼️ DESIGN: {Component/Page Name}

Platform: {Web/Mobile/Desktop}
Framework: {React/Flutter/WPF/Qt/etc.}
Design System: {Material/Fluent/Custom}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Component Mapping Analysis

✅ EXISTING COMPONENTS:
| Component | Location | Usage |
|-----------|----------|-------|
| Button | @/components/Button | variant="primary" |
| Card | @/components/Card | elevated |

⚠️ NEW COMPONENTS NEEDED:
| Component | Reason | Strategy |
|-----------|--------|----------|
| FilterBar | Not found | Compose from Input + Button |

## Layout (Platform-Specific)

┌─────────────────────────────────────┐
│ <Header /> │
├─────────────────────────────────────┤
│ <FilterBar /> │
├─────────────────────────────────────┤
│ <DataGrid> │
│ {items.map(i => <Card />)} │
│ </DataGrid> │
└─────────────────────────────────────┘

## Code Output

### React (Web)

import { Button, Card } from '@/components';

export function Page() {
return (

<div className="container">
<Header />
<FilterBar />
<DataGrid>{items.map(...)}</DataGrid>
</div>
);
}

### Flutter (Mobile)

import 'package:app/components/components.dart';

class Page extends StatelessWidget {
@override
Widget build(BuildContext context) {
return Scaffold(
appBar: Header(),
body: Column([
FilterBar(),
Expanded(child: DataGrid(...)),
]),
);
}
}

### WPF (Desktop)

<Grid>
  <controls:Header Grid.Row="0"/>
  <controls:FilterBar Grid.Row="1"/>
  <controls:DataGrid Grid.Row="2"/>
</Grid>

## Accessibility Checklist

- [ ] Color contrast ≥ 4.5:1
- [ ] Focus indicators visible
- [ ] Keyboard navigable
- [ ] Touch targets ≥ platform minimum
- [ ] Screen reader labels

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 WIREFRAME TEMPLATES

```yaml
wireframes:
  landing_page:
    sections: [hero, features, cta, footer]
    platform: web

  dashboard:
    sections: [sidebar, header, main, widgets]
    platform: web/desktop

  mobile_app:
    sections: [bottom-nav, content, fab]
    platform: mobile

  settings:
    sections: [nav, content, save]
    platform: all

  auth:
    sections: [logo, form, social, footer]
    platform: all
```

---

## 📱 RESPONSIVE DESIGN

```yaml
breakpoints:
  mobile: "< 640px"
  tablet: "640-1024px"
  desktop: "> 1024px"

patterns:
  mobile_first:
    rule: "Start with mobile, enhance upward"

  platform_adaptive:
    web: "Responsive layout"
    mobile: "Native navigation"
    desktop: "Full keyboard support"
```

---

## 🎨 AI IMAGE GENERATION

```yaml
image_generation:
  commands:
    - "/visualize generate [description]"
    - "/visualize mockup [component]"

  tool: "generate_image"
  formats: ["png", "jpg", "webp"]
  sizes: ["1920x1080", "1280x720", "375x812"]
```

---

## ⚙️ TOKEN OPTIMIZATION v5.5

```yaml
token_saving:
  component_mapping: "70-90% reduction"
  design_tokens: "80-95% consistency"
  platform_detection: "0% overhead (smart routing)"

  strategies:
    - Map to existing components FIRST
    - Generate props, not full code
    - Reference tokens, not hardcode
    - Compose from primitives
```

---

## 📋 NEXT STEPS MENU

```
📋 NEXT STEPS:
1️⃣ Generate code: /code [component]
2️⃣ Create mockup: /visualize generate
3️⃣ Build system: /visualize system
4️⃣ Test design: /test

Enter number or command:
```

---

_DOMYH Awesome Code v5.5 • Visualize Pro v5.5 • Multi-Platform + Component Mapping_
