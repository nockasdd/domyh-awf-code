---
library: nestjs
version: 11.x
latest: true
category: backend
official_docs: https://docs.nestjs.com
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/nestjs/docs.nestjs.com/contents/content
---

### Migration guide

This article offers a comprehensive guide for migrating from NestJS version 10 to version 11. To explore the new features introduced in v11, take a look at [this article](https://trilon.io/blog/announcing-nestjs-11-whats-new). While the update includes a few minor breaking changes, they are unlikely to impact most users. You can review the complete list of changes [here](https://github.com/nestjs/nest/releases/tag/v11.0.0).


#### Config module

If you're using the `ConfigModule` from the `@nestjs/config` package, be aware of several breaking changes introduced in `@nestjs/config@4.0.0`. Most notably, the order in which configuration variables are read by the `ConfigService#get` method has been updated. The new order is:

- Internal configuration (config namespaces and custom config files)
- Validated environment variables (if validation is enabled and a schema is provided)
- The `process.env` object

Previously, validated environment variables and the `process.env` object were read first, preventing them from being overridden by internal configuration. With this update, internal configuration will now always take precedence over environment variables.

Additionally, the `ignoreEnvVars` configuration option, which previously allowed disabling validation of the `process.env` object, has been deprecated. Instead, use the `validatePredefined` option (set to `false` to disable validation of predefined environment variables). Predefined environment variables refer to `process.env` variables that were set before the module was imported. For example, if you start your application with `PORT=3000 node main.js`, the `PORT` variable is considered predefined. However, variables loaded by the `ConfigModule` from a `.env` file are not classified as predefined.

A new `skipProcessEnv` option has also been introduced. This option allows you to prevent the `ConfigService#get` method from accessing the `process.env` object entirely, which can be helpful when you want to restrict the service from reading environment variables directly.


#### Prerequisites

Before deploying your NestJS application, ensure you have:

- A working NestJS application that is ready for deployment.
- Access to a deployment platform or server where you can host your application.
- All necessary environment variables set up for your application.
- Any required services, like a database, set up and ready to go.
- At least an LTS version of Node.js installed on your deployment platform.

> info **Hint** If you are looking for a cloud-based platform to deploy your NestJS application, check out [Mau](https://mau.nestjs.com/ 'Deploy Nest'), our official platform for deploying NestJS applications on AWS. With Mau, deploying your NestJS application is as simple as clicking a few buttons and running a single command:
>
> ```bash
> $ npm install -g @nestjs/mau
> $ mau deploy
> ```
>
> Once the deployment is complete, you'll have your NestJS application up and running on AWS in seconds!


#### Production environment

Your production environment is where your application will be accessible to external users. This could be a cloud-based platform like [AWS](https://aws.amazon.com/) (with EC2, ECS, etc.), [Azure](https://azure.microsoft.com/), or [Google Cloud](https://cloud.google.com/), or even a dedicated server you manage, such as [Hetzner](https://www.hetzner.com/).

To simplify the deployment process and avoid manual setup, you can use a service like [Mau](https://mau.nestjs.com/ 'Deploy Nest'), our official platform for deploying NestJS applications on AWS. For more details, check out [this section](todo).

Some of the pros of using a **cloud-based platform** or service like [Mau](https://mau.nestjs.com/ 'Deploy Nest') include:

- Scalability: Easily scale your application as your user base grows.
- Security: Benefit from built-in security features and compliance certifications.
- Monitoring: Monitor your application's performance and health in real-time.
- Reliability: Ensure your application is always available with high uptime guarantees.

On the other hand, cloud-based platforms are typically more expensive than self-hosting, and you may have less control over the underlying infrastructure. Simple VPS can be a good choice if you're looking for a more cost-effective solution and have the technical expertise to manage the server yourself, but keep in mind that you'll need to handle tasks like server maintenance, security, and backups manually.


#### NODE_ENV=production

While there's technically no difference between development and production in Node.js and NestJS, it's a good practice to set the `NODE_ENV` environment variable to `production` when running your application in a production environment, as some libraries in the ecosystem may behave differently based on this variable (e.g., enabling or disabling debugging output, etc.).

You can set the `NODE_ENV` environment variable when starting your application like so:

```bash
$ NODE_ENV=production node dist/main.js
```

Or just set it in your cloud provider's/Mau dashboard.


# Use the official Node.js image as the base image
FROM node:20


# Install the application dependencies
RUN npm install


## first steps


### First steps

In this set of articles, you'll learn the **core fundamentals** of Nest. To get familiar with the essential building blocks of Nest applications, we'll build a basic CRUD application with features that cover a lot of ground at an introductory level.


#### Prerequisites

Please make sure that [Node.js](https://nodejs.org) (version >= 20) is installed on your operating system.


#### Setup

Setting up a new project is quite simple with the [Nest CLI](/cli/overview). With [npm](https://www.npmjs.com/) installed, you can create a new Nest project with the following commands in your OS terminal:

```bash
$ npm i -g @nestjs/cli
$ nest new project-name
```

> info **Hint** To create a new project with TypeScript's [stricter](https://www.typescriptlang.org/tsconfig#strict) feature set, pass the `--strict` flag to the `nest new` command.

The `project-name` directory will be created, node modules and a few other boilerplate files will be installed, and a `src/` directory will be created and populated with several core files.

<div class="file-tree">
  <div class="item">src</div>
  <div class="children">
    <div class="item">app.controller.spec.ts</div>
    <div class="item">app.controller.ts</div>
    <div class="item">app.module.ts</div>
    <div class="item">app.service.ts</div>
    <div class="item">main.ts</div>
  </div>
</div>

Here's a brief overview of those core files:

|                          |                                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `app.controller.ts`      | A basic controller with a single route.                                                                             |
| `app.controller.spec.ts` | The unit tests for the controller.                                                                                  |
| `app.module.ts`          | The root module of the application.                                                                                 |
| `app.service.ts`         | A basic service with a single method.                                                                               |
| `main.ts`                | The entry file of the application which uses the core function `NestFactory` to create a Nest application instance. |

The `main.ts` includes an async function, which will **bootstrap** our application:

```typescript
@@filename(main)

import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
@@switch
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
```

To create a Nest application instance, we use the core `NestFactory` class. `NestFactory` exposes a few static methods that allow creating an application instance. The `create()` method returns an application object, which fulfills the `INestApplication` interface. This object provides a set of methods which are described in the coming chapters. In the `main.ts` example above, we simply start up our HTTP listener, which lets the application await inbound HTTP requests.

Note that a project scaffolded with the Nest CLI creates an initial project structure that encourages developers to follow the convention of keeping each module in its own dedicated directory.

> info **Hint** By default, if any error happens while creating the application your app will exit with the code `1`. If you want to make it throw an error instead disable the option `abortOnError` (e.g., `NestFactory.create(AppModule, {{ '{' }} abortOnError: false {{ '}' }})`).

<app-banner-courses></app-banner-courses>


#### Getting started

To create a Nest standalone application, use the following construction:

```typescript
@@filename()
async function bootstrap() {
  const app = await NestFactory.createApplicationContext(AppModule);
  // your application logic here ...
}
bootstrap();
```


#### Installation

To get started, you can either scaffold the project with the [Nest CLI](/cli/overview), or [clone a starter project](#alternatives) (both will produce the same outcome).

To scaffold the project with the Nest CLI, run the following commands. This will create a new project directory, and populate the directory with the initial core Nest files and supporting modules, creating a conventional base structure for your project. Creating a new project with the **Nest CLI** is recommended for first-time users. We'll continue with this approach in [First Steps](first-steps).

```bash
$ npm i -g @nestjs/cli
$ nest new project-name
```

> info **Hint** To create a new TypeScript project with stricter feature set, pass the `--strict` flag to the `nest new` command.
