---
library: expo
version: latest
latest: true
category: mobile
official_docs: https://docs.expo.dev
last_updated: 2026-03-21
source: auto-fetched from llms-full
source_url: https://docs.expo.dev/llms-full.txt
---

# Expo Documentation

Expo is an open-source React Native framework for apps that run natively on Android, iOS, and the web. Expo brings together the best of mobile and the web and enables many important features for building and scaling an app such as live updates, instantly sharing your app, and web support. The company behind Expo also offers Expo Application Services (EAS), which are deeply integrated cloud services for Expo and React Native apps.

---
modificationDate: March 10, 2026
title: Create a project
description: Learn how to create a new Expo project.
---


#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```


#### Install the development build on your device

After the build is complete, scan the QR code in your terminal or open the link on your device. Tap **Install** to download the build on your device, then tap **Open** to install it.

---


### Install Watchman and JDK

##### macOS

##### Prerequisites

Use a package manager such as [Homebrew](https://brew.sh/) to install the following dependency.

##### Install dependencies

[Install Watchman](https://facebook.github.io/watchman/docs/install#macos) using a tool such as Homebrew:

```sh
brew install watchman
```

Install OpenJDK distribution called Azul Zulu using Homebrew. This distribution offers JDKs for both Apple Silicon and Intel Macs.

Run the following commands in a terminal:

```sh
brew install --cask zulu@17
```

After you install the JDK, add the `JAVA_HOME` environment variable in **~/.bash_profile** (or **~/.zshrc** if you use Zsh):

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
```

##### Windows

##### Prerequisites

Use a package manager such as [Chocolatey](https://chocolatey.org/) to install the following dependencies.

##### Install dependencies

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

```sh
choco install -y microsoft-openjdk17
```

##### Linux

##### Install dependencies

Follow [instructions from the Watchman documentation](https://facebook.github.io/watchman/docs/install#linux) to compile and install it from the source.

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

You can download and install [OpenJDK@17](http://openjdk.java.net/) from [AdoptOpenJDK](https://adoptopenjdk.net/) or your system packager.


#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```


### Install Expo Go

When you start a development server with `npx expo start` on the [start developing](/get-started/start-developing) page, press <kbd>a</kbd> to open the Android Emulator. Expo CLI will install Expo Go automatically.

---


#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```


#### Install the development build on your emulator

After the build is complete, the CLI will prompt you to automatically download and install it on the Android Emulator. When prompted, press <kbd>Y</kbd> to directly install it on the emulator.

If you miss this prompt, you can download the build from the link provided in the terminal and drag and drop it onto the Android Emulator to install it.

---


### Install Watchman and JDK

##### macOS

##### Prerequisites

Use a package manager such as [Homebrew](https://brew.sh/) to install the following dependency.

##### Install dependencies

[Install Watchman](https://facebook.github.io/watchman/docs/install#macos) using a tool such as Homebrew:

```sh
brew install watchman
```

Install OpenJDK distribution called Azul Zulu using Homebrew. This distribution offers JDKs for both Apple Silicon and Intel Macs.

Run the following commands in a terminal:

```sh
brew install --cask zulu@17
```

After you install the JDK, add the `JAVA_HOME` environment variable in **~/.bash_profile** (or **~/.zshrc** if you use Zsh):

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
```

##### Windows

##### Prerequisites

Use a package manager such as [Chocolatey](https://chocolatey.org/) to install the following dependencies.

##### Install dependencies

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

```sh
choco install -y microsoft-openjdk17
```

##### Linux

##### Install dependencies

Follow [instructions from the Watchman documentation](https://facebook.github.io/watchman/docs/install#linux) to compile and install it from the source.

Install [Java SE Development Kit (JDK)](https://openjdk.org/):

You can download and install [OpenJDK@17](http://openjdk.java.net/) from [AdoptOpenJDK](https://adoptopenjdk.net/) or your system packager.


#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```

Run the following from your terminal:

```sh
npx expo run:android
```

> This command runs a development server after building your app. You can skip running `npx expo start` on the next page.

---


#### Install TestFlight

Download and install the [TestFlight app](https://apps.apple.com/us/app/testflight/id899247664). You can also scan the QR code below on your iOS device:

Download link: [https://apps.apple.com/us/app/testflight/id899247664](https://apps.apple.com/us/app/testflight/id899247664)


#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```


#### Install the development build on your device

After the build is complete, scan the QR code in your terminal and tap **Open with iTunes** when it appears inside the Camera app. Alternatively, open the link displayed in the terminal on your device.

After confirming the installation, the app will appear in your device's app library.


#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).


#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.


#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.


#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```


#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```


#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).


#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.


#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.


#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```


### Install Expo Go

When you start a development server with `npx expo start` on the [start developing](/get-started/start-developing) page, press <kbd>i</kbd> to open the iOS Simulator. Expo CLI will install Expo Go automatically.

---


#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).


#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.


#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.


#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```


#### Install EAS CLI

To build your app, you will need to install EAS CLI. You can do this by running the following command in your terminal:

```sh
npm install -g eas-cli
```


#### Install the development build on your simulator

After the build is complete, the CLI will prompt you to automatically download and install it on the iOS Simulator. When prompted, press <kbd>Y</kbd> to directly install it on the simulator.

If you miss this prompt, you can download the build from the link provided in the terminal and drag and drop it onto the iOS Simulator to install it.

---


#### Install Xcode

Open up the Mac App Store, search for [Xcode](https://apps.apple.com/us/app/xcode/id497799835), and click **Install** (or **Update** if you have it already).


#### Install Xcode Command Line Tools

Open Xcode, choose **Settings...** from the Xcode menu (or press <kbd>cmd ⌘</kbd> + <kbd>,</kbd>). Go to the **Locations** and install the tools by selecting the most recent version in the **Command Line Tools** dropdown.


#### Install an iOS Simulator in Xcode

To install an iOS Simulator, open **Xcode > Settings... > Components**, and under **Platform Support > iOS ...**, click **Get**.


#### Install Watchman

[Watchman](https://facebook.github.io/watchman/docs/install#macos) is a tool for watching changes in the filesystem. Installing it will result in better performance. You can install it with:

```sh
brew update
brew install watchman
```


#### Install expo-dev-client

Run the following command in your project's root directory:

```sh
npx expo install expo-dev-client
```

Run the following from your terminal:

```sh
npx expo run:ios
```

> This command runs a development server after building your app. You can skip running `npx expo start` on the next page.


## Install Expo Skills

Run the following commands to add and install Expo Skills from the plugin marketplace:

```sh
/plugin marketplace add expo/skills
/plugin install expo
```


## Quick start

Pick the method that matches your tool:

| Method | Best for | How |
| --- | --- | --- |
| Per-page markdown | Chat interfaces (ChatGPT, Claude.ai) and coding agents | Append `/index.md` to any documentation page URL. |
| Copy Markdown dropdown | Quick prompts with a single page | Click **Copy page** > **Copy Markdown** at the top of any documentation page. |
| Section bundles | Project rules and coding agents | Add a section-level `llms-*.txt` URL to your AI tool configuration or the general-purpose index (`/llms.txt`). |


### Installation

You can download Orbit with Homebrew for macOS, or directly from the [GitHub releases](https://github.com/expo/orbit/releases).

```sh
brew install expo-orbit
```

If you want Orbit to start when you log in automatically, click on the Orbit icon in the menu bar, then **Settings** and select the **Launch on Login** option.

> Orbit relies on the Android SDK on both macOS and Windows and `xcrun` for device management only on macOS, which requires setting up both [Android Studio](/workflow/android-studio-emulator) and [Xcode](/workflow/ios-simulator).


### Installation

You can skip installing `react-native-safe-area-context` if you have created a project using [the default template](/get-started/create-a-project). This library is installed as peer dependency for Expo Router library. Otherwise, install it by running the following command:

```sh
npx expo install react-native-safe-area-context
```


### Handle `@expo/vector-icons` initial load

When the icons from `@expo/vector-icons` library load for the first time, they appear as invisible icons in your app. Once they load, they're cached for all the app's subsequent usage. To avoid showing invisible icons on your app's first load, preload during the initial loading screen with [`useFonts`](/versions/latest/sdk/font#usefontsmap). For example:

```tsx
import { useFonts } from 'expo-font';
import Ionicons from '@expo/vector-icons/Ionicons';

export default function RootLayout() {
  useFonts([require('./assets/fonts/Inter-Black.otf', Ionicons.font)]);

  return (
    ... 
  )
}
```

Now, you can use any icon from the `Ionicons` library in a React component:

```tsx
<Ionicons name="checkmark-circle" size={32} color="green" />
```

[Icons](/guides/icons) — Learn how to use various types of icons in your Expo app, including vector icons, custom icon fonts, icon images, and icon buttons.


## Installation

You can skip installing `react-native-reanimated` if you have created a project using [the default template](/get-started/create-a-project). This library is already installed. Otherwise, install it by running the following command:

```sh
npx expo install react-native-reanimated
```


## Install the `expo-dev-client`

The Expo Dev Client library includes the launcher UI (shown in the screenshots below), dev menu, extensions to test over-the-air updates, and more. The Expo Go app has the dev menu built in, and that's why you need to install it separately for a development build.

```sh
npx expo install expo-dev-client
```

When you run a development build it will look like this, only with your app name and icon included rather than "Microfoam". The launcher UI is pictured in iOS on the left and Android on the right. In between, you can see an app running inside of the development build, with the customizable developer menu open.

> We recommend using the `expo-dev-client` for the best development experience, but it is possible to use development builds without installing this library. If not using the dev client, in [Step 3](/develop/development-builds/expo-go-to-dev-build#start-the-dev-client), start the bundler with `--dev-client`. Otherwise, it will default to opening in Expo Go.


## Prerequisites

The instructions assume you already have an existing Expo project that runs on Expo Go.

The requirements for building the native app depend on which platform you are using, which platform you are building for, and whether you want to build on EAS or on your local machine.

Build on EAS

This is the easiest way to build your native app, as it requires no native build tools on your side. The builds happen on the EAS servers, which makes it possible to trigger iOS builds from non-macOS platforms.

|  | Android | iOS Simulator | iPhone device |
| --- | --- | --- | --- |
| **macOS** | ✓ | ✓ | ✓ (\*) |
| **Windows** | ✓ | ✓ | ✓ (\*) |
| **Linux** | ✓ | ✓ | ✓ (\*) |

(\*) All builds that run on an iPhone device require a paid [Apple Developer](https://developer.apple.com) account for build signing.

Build locally using the EAS CLI

Any EAS CLI command can be built on your local machine with the `--local` flag. This requires your local [development environment](https://reactnative.dev/docs/set-up-your-environment?os=macos&platform=ios) to be set up with native build tools. Read more about [local app development](/build-reference/local-builds).

|  | Android | iOS Simulator | iPhone device |
| --- | --- | --- | --- |
| **macOS** | ✓ | ✓ | ✓ (\*) |
| **Windows** | ✓ (\*\*) | ✗ | ✗ |
| **Linux** | ✓ | ✗ | ✗ |

(\*) All builds that run on an iPhone device require a paid [Apple Developer](https://developer.apple.com) account for build signing.

(\*\*) No first-class support, but possible with [WSL](http://expo.fyi/wsl.md).

Build locally without EAS

To build locally without EAS requires your local [development environment](https://reactnative.dev/docs/set-up-your-environment?os=macos&platform=ios) to be set up with native build tools. This is the only way to test your iOS build on an iPhone device without a paid Apple Developer Account (only possible on macOS). Read more about [local app compilation](/guides/local-app-development#local-app-compilation) and see the [Expo Go to Development Build](/develop/development-builds/expo-go-to-dev-build) guide.

|  | Android | iOS Simulator | iPhone device |
| --- | --- | --- | --- |
| **macOS** | ✓ | ✓ | ✓ |
| **Windows** | ✓ | ✗ | ✗ |
| **Linux** | ✓ | ✗ | ✗ |


### Install expo-dev-client

```sh
npx expo install expo-dev-client
```

Are you using this library in a existing (bare) React Native apps?

Apps that don't use [Continuous Native Generation](/workflow/continuous-native-generation) or are created with `npx react-native`, require further configuration after installing this library. See steps 1 and 2 from [Install `expo-dev-client` in an existing React Native app](/bare/install-dev-builds-in-bare).


### Install the app

You'll need to install the native app on your device, emulator, or simulator.


## Installation and configuration for development

The most straightforward approach to leverage Expo's tooling is to use `expo` and [`expo-module-scripts`](https://www.npmjs.com/package/expo-module-scripts).

-   `expo` provides a config plugin API and types that your plugin will use.
-   `expo-module-scripts` provides build tooling specifically designed for Expo modules and config plugins. It also handles TypeScript compilation.

```sh
npx expo install package
```

When using `expo-module-scripts`, it requires the following **package.json** configuration. For any already existing script with the same script name, replace it.

```json
{
  "scripts": {
    "build": "expo-module build",
    "build:plugin": "expo-module build plugin",
    "clean": "expo-module clean",
    "test": "expo-module test",
    "prepare": "expo-module prepare",
    "prepublishOnly": "expo-module prepublishOnly"
  },
  "devDependencies": {
    "expo": "^54.0.0"
  },
  "peerDependencies": {
    "expo": ">=54.0.0"
  },
  "peerDependenciesMeta": {
    "expo": {
      "optional": true
    }
  }
}
```

The next step is to add TypeScript support within the **plugins** directory. Open **plugins/tsconfig.json** file and add the following:

```json
{
  "extends": "expo-module-scripts/tsconfig.plugin",
  "compilerOptions": {
    "outDir": "build",
    "rootDir": "src"
  },
  "include": ["./src"],
  "exclude": ["**/__mocks__/*", "**/__tests__/*"]
}
```

You also need to define the main entry point for your config plugin in the **app.plugin.js** file, which exports the compiled plugin code from the **plugin/build** directory:

```js
module.exports = require('./plugin/build');
```

The above configuration is essential because when the Expo CLI looks for a plugin, it checks for this file in the project root of your library. The **plugin/build** directory contains the JavaScript files generated from your config plugin's TypeScript source code.


### Install dependencies

Use the following dependencies in a library that provides a config plugin:

```json
{
  "dependencies": {},
  "devDependencies": {
    "expo": "^54.0.0"
  },
  "peerDependencies": {
    "expo": ">=54.0.0"
  },
  "peerDependenciesMeta": {
    "expo": {
      "optional": true
    }
  }
}
```

-   You may update the exact version of `expo` to build against a specific version.
-   For simple config plugins that depend on core, stable APIs, such as a plugin that only modifies **AndroidManifest.xml** or **Info.plist**, you can use a loose dependency such as in the example above.
-   You may also want to install [`expo-module-scripts`](https://github.com/expo/expo/blob/main/packages/expo-module-scripts/README.md) as a development dependency, but it's not required.


## Prerequisites

Before you begin, in your project's **app.json** file, ensure that the [`expo.web.output`](/versions/latest/config/app#output) property is either `static` or `server`.


## Initialize a development build


## Getting started


## Setup
