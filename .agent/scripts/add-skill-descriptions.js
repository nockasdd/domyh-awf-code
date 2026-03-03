#!/usr/bin/env node
/**
 * Batch add 'description' field to SKILL.md files that don't have it.
 * Usage: node add-skill-descriptions.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const SKILLS_DIR = path.resolve(__dirname, '..', 'skills');

const DESCRIPTIONS = {
    'typescript': 'TypeScript development patterns for type-safe web apps, Node.js, and ESM-native projects. Use when working with .ts/.tsx files or tsconfig.json.',
    'javascript': 'JavaScript patterns for modern ES2024+ development. Use when working with .js/.mjs/.cjs files, browser or Node.js projects.',
    'python': 'Python development patterns for web, data science, and automation. Use when working with .py files, pip, poetry, or Python projects.',
    'go': 'Go development patterns for services, CLIs, and cloud-native apps. Use when working with .go files or go.mod projects.',
    'rust': 'Rust development patterns for systems programming and safety-critical code. Use when working with .rs files or Cargo.toml projects.',
    'java': 'Java development patterns for enterprise apps and Spring Boot. Use when working with .java files, Maven, or Gradle projects.',
    'kotlin': 'Kotlin development patterns for Android, JVM, and multiplatform. Use when working with .kt/.kts files.',
    'csharp': 'C# development patterns for .NET, ASP.NET, and cross-platform apps. Use when working with .cs files or .csproj projects.',
    'fsharp': 'F# functional programming patterns for .NET. Use when working with .fs/.fsx files.',
    'swift': 'Swift development patterns for iOS, macOS, and server-side. Use when working with .swift files or Package.swift projects.',
    'ruby': 'Ruby development patterns for Rails and scripting. Use when working with .rb files, Gemfile, or Ruby projects.',
    'php': 'PHP development patterns for web applications and Laravel. Use when working with .php files or composer.json projects.',
    'c': 'C development patterns for systems, embedded, and low-level programming. Use when working with .c/.h files or Makefiles.',
    'cpp': 'C++ development patterns for performance-critical and systems code. Use when working with .cpp/.hpp files or CMake projects.',
    'scala': 'Scala development patterns for JVM and functional programming. Use when working with .scala files or sbt projects.',
    'haskell': 'Haskell functional programming patterns. Use when working with .hs files or Cabal/Stack projects.',
    'elixir': 'Elixir development patterns for concurrent and distributed systems. Use when working with .ex/.exs files or Mix projects.',
    'clojure': 'Clojure functional patterns for JVM. Use when working with .clj/.cljs files or Leiningen projects.',
    'lua': 'Lua scripting patterns for game dev and embedded. Use when working with .lua files.',
    'perl': 'Perl development patterns for text processing and systems. Use when working with .pl/.pm files.',
    'r': 'R statistical computing and data analysis patterns. Use when working with .R/.Rmd files.',
    'julia': 'Julia scientific computing and performance patterns. Use when working with .jl files.',
    'nim': 'Nim systems programming patterns. Use when working with .nim files.',
    'crystal': 'Crystal type-safe Ruby-like language patterns. Use when working with .cr files.',
    'ocaml': 'OCaml functional programming patterns. Use when working with .ml/.mli files.',
    'zig': 'Zig systems programming patterns for safety and performance. Use when working with .zig files.',
    'solidity': 'Solidity smart contract patterns for Ethereum/EVM. Use when working with .sol files or Hardhat/Foundry projects.',
    'asm': 'Assembly language patterns for x86/ARM systems. Use when working with .asm/.s files.',
    'api-design': 'API design patterns for REST, GraphQL, and gRPC. Use when designing endpoints, versioning, pagination, rate limiting, or error responses.',
    'authentication': 'Authentication and authorization patterns. Use when implementing OAuth, JWT, MFA, session management, or access control.',
    'error-handling': 'Error handling patterns for robust applications. Use when implementing error boundaries, recovery strategies, or structured logging.',
    'logging': 'Logging patterns and structured log management. Use when implementing log levels, formatters, transports, or log aggregation.',
    'observability': 'Observability patterns for monitoring, tracing, and alerting. Use when implementing OpenTelemetry, metrics, or distributed tracing.',
    'security': 'Security patterns for application hardening. Use when implementing input validation, OWASP protections, secrets management, or CSP.',
    'react': 'React development patterns for components, hooks, and state management. Use when working with React/JSX/TSX projects.',
    'nextjs': 'Next.js patterns for SSR, ISR, App Router, and full-stack React. Use when working with Next.js projects.',
    'vue': 'Vue.js development patterns for Composition API and SFCs. Use when working with .vue files or Vue projects.',
    'nuxt': 'Nuxt.js patterns for Vue SSR and full-stack development. Use when working with Nuxt projects.',
    'angular': 'Angular development patterns for enterprise SPAs. Use when working with Angular CLI projects or .component.ts files.',
    'svelte': 'Svelte and SvelteKit patterns for reactive UI. Use when working with .svelte files.',
    'react-native': 'React Native patterns for cross-platform mobile apps. Use when working with React Native or Expo projects.',
    'flutter': 'Flutter and Dart patterns for cross-platform mobile/web/desktop. Use when working with .dart files or pubspec.yaml.',
    'streamlit': 'Streamlit patterns for data apps and dashboards. Use when building Python data visualization apps.',
    'docker': 'Docker containerization patterns for builds, security, and deployment. Use when working with Dockerfiles or docker-compose.yml.',
    'kubernetes': 'Kubernetes orchestration patterns for deployments, services, and scaling. Use when working with k8s manifests or Helm charts.',
    'ci-cd': 'CI/CD pipeline patterns for GitHub Actions, GitLab CI, and Jenkins. Use when implementing automated workflows.',
    'terraform': 'Terraform IaC patterns for cloud infrastructure. Use when working with .tf files or managing cloud resources.',
    'aws': 'AWS cloud service patterns. Use when working with EC2, S3, Lambda, ECS, RDS, or other AWS services.',
    'azure': 'Azure cloud service patterns. Use when working with Azure Functions, AKS, Cosmos DB, or other Azure services.',
    'gcp': 'Google Cloud Platform patterns. Use when working with GCP services like Cloud Run, GKE, BigQuery, or Firebase.',
    'accessibility': 'Web accessibility patterns for WCAG compliance. Use when implementing ARIA, keyboard navigation, screen reader support.',
    'audit-pro': 'Professional code audit patterns with 12-expert panel system. Use when performing comprehensive project audits.',
    'bun': 'Bun runtime patterns for fast JavaScript/TypeScript execution. Use when working with bun.lockb or Bun projects.',
    'database': 'Database design patterns for SQL and NoSQL. Use when designing schemas, queries, indexes, or migrations.',
    'deno': 'Deno runtime patterns for secure TypeScript. Use when working with deno.json or Deno projects.',
    'electron': 'Electron desktop app patterns. Use when building cross-platform desktop apps with web technologies.',
    'event-driven': 'Event-driven architecture patterns. Use when implementing pub/sub, event sourcing, CQRS, or message queues.',
    'microservices': 'Microservice architecture patterns. Use when designing service boundaries, communication, or resilience.',
    'monorepo': 'Monorepo management patterns for Nx, Turborepo, or Lerna. Use when organizing multi-package projects.',
    'playwright': 'Playwright E2E testing patterns. Use when writing browser automation or end-to-end tests.',
    'real-time': 'Real-time communication patterns for WebSocket, SSE, and Socket.io. Use when implementing live updates or streaming.',
    'seo': 'SEO optimization patterns for web applications. Use when implementing meta tags, structured data, or performance.',
    'skill-creator': 'SKILL.md creation patterns for the agentskills.io standard. Use when creating new agent skills.',
    'sql': 'SQL patterns for queries, optimization, and database operations. Use when writing SQL or working with relational databases.',
    'tailwind': 'Tailwind CSS patterns for utility-first styling. Use when working with Tailwind configuration or utility classes.',
    'tauri': 'Tauri desktop app patterns for Rust + Web hybrid apps. Use when building lightweight desktop applications.',
    'tdd-workflow': 'Test-Driven Development workflow patterns. Use when practicing Red-Green-Refactor methodology.',
    'testing': 'Testing patterns for unit, integration, and E2E tests. Use when implementing test strategies, mocks, or coverage.',
    'wasm': 'WebAssembly patterns for performance-critical web modules. Use when compiling to Wasm or using Wasm runtimes.',
    'web-perf': 'Web performance optimization patterns. Use when improving Core Web Vitals, bundle size, or load times.',
    'ai-agents': 'AI agent design patterns for autonomous systems. Use when building AI agents, tool-calling, or agent orchestration.',
    'gemini-live': 'Gemini Live API patterns for real-time multimodal AI. Use when implementing live audio/video AI interactions.',
    'gemini-media-gen': 'Gemini media generation patterns. Use when generating images, audio, or video with Gemini.',
    'gemini-tts': 'Gemini Text-to-Speech patterns. Use when implementing AI voice synthesis with Gemini.',
    'ml-pipelines': 'Machine learning pipeline patterns. Use when building ML training, evaluation, or deployment workflows.',
    'prompt-engineering': 'Prompt engineering patterns for LLMs. Use when crafting system prompts, few-shot examples, or chain-of-thought.',
    'rag-patterns': 'Retrieval-Augmented Generation patterns. Use when implementing RAG with vector databases or semantic search.',
    'vector-search': 'Vector search and embedding patterns. Use when implementing similarity search, embeddings, or vector databases.',
    'api-protocols': 'API protocol patterns for HTTP/2, gRPC, WebSocket, and GraphQL transport. Use when choosing or implementing API protocols.',
    'browser-agent': 'Browser automation agent patterns. Use when implementing headless browser control or web scraping.',
    'cli-dev': 'CLI development patterns for Node.js command-line tools. Use when building CLIs with oclif, commander, or yargs.',
    'ide-extension': 'IDE extension development patterns for VS Code and JetBrains. Use when building editor plugins or extensions.',
    'mcp': 'Model Context Protocol patterns for AI-tool integration. Use when implementing MCP servers, tools, or resources.',
};

function findSkillFiles(dir) {
    const results = [];
    try {
        const items = fs.readdirSync(dir, { withFileTypes: true });
        for (const item of items) {
            const fullPath = path.join(dir, item.name);
            if (item.isDirectory()) results.push(...findSkillFiles(fullPath));
            else if (item.name === 'SKILL.md') results.push(fullPath);
        }
    } catch (e) { /* skip inaccessible dirs */ }
    return results;
}

function processSkillFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split(/\r?\n/);
    const lineEnding = content.includes('\r\n') ? '\r\n' : '\n';
    const fmEnd = lines.indexOf('---', 1);
    if (fmEnd === -1) return { skipped: true, reason: 'no-frontmatter' };
    const fm = lines.slice(1, fmEnd).join('\n');
    if (fm.includes('description:')) return { skipped: true, reason: 'has-description' };
    const nameMatch = fm.match(/^name:\s*(.+)$/m);
    if (!nameMatch) return { skipped: true, reason: 'no-name' };
    const name = nameMatch[1].trim().replace(/['"]/g, '');
    const desc = DESCRIPTIONS[name];
    if (!desc) return { skipped: true, reason: 'unmapped', name };
    const nameIdx = lines.findIndex((l, i) => i > 0 && i < fmEnd && /^name:\s/.test(l));
    if (nameIdx === -1) return { skipped: true, reason: 'name-idx-fail' };
    const newLines = [...lines];
    newLines.splice(nameIdx + 1, 0, `description: "${desc}"`);
    if (!DRY_RUN) fs.writeFileSync(filePath, newLines.join(lineEnding), 'utf-8');
    return { modified: true, name, desc };
}

const files = findSkillFiles(SKILLS_DIR);
console.log(`Found ${files.length} SKILL.md files | Mode: ${DRY_RUN ? 'DRY RUN' : 'LIVE'}\n`);
let mod = 0, skip = 0, miss = 0;
const missing = [];
for (const f of files) {
    const r = processSkillFile(f);
    const rel = path.relative(SKILLS_DIR, f);
    if (r.modified) { mod++; console.log(`✅ ${rel}`); }
    else if (r.reason === 'has-description') { skip++; console.log(`⏭️  ${rel} (has desc)`); }
    else if (r.reason === 'unmapped') { miss++; missing.push(r.name); console.log(`❌ ${rel} → ${r.name}`); }
    else console.log(`⚠️  ${rel} (${r.reason})`);
}
console.log(`\n═══ Results ═══\nModified: ${mod}\nAlready had: ${skip}\nUnmapped: ${miss}${missing.length ? '\nMissing: ' + missing.join(', ') : ''}`);
