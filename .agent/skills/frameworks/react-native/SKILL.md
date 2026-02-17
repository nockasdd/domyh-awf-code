---
name: react-native
detect: ["metro.config.js", "app.json:expo", "react-native.config.js"]
version: "6.3.1"
category: mobile
tier: 1
---

# React Native Patterns — DOMYH Awesome Code

> **Version**: React Native 0.76+ (2025-2026)
> **Philosophy**: New Architecture, Fabric, Turbo Modules, Expo

---

## 🎯 When to Use This Skill

Use for: Cross-platform mobile apps (iOS/Android), React teams.
**NOT for**: Web (→ react), native-only (→ swift/kotlin).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Tool                   | Use Case            |
| ---------------------- | ------------------- |
| **React Native 0.76+** | New Architecture 🏆 |
| **Expo**               | Managed workflow 🏆 |
| **Hermes**             | JS engine           |

### Navigation

| Library              | Use Case                |
| -------------------- | ----------------------- |
| **React Navigation** | Stack/Tab navigation 🏆 |
| **Expo Router**      | File-based routing      |

### State

| Library            | Use Case         |
| ------------------ | ---------------- |
| **Zustand**        | Minimal state 🏆 |
| **TanStack Query** | Server state     |
| **Jotai**          | Atomic state     |

### IDE Support

| IDE                | Features              |
| ------------------ | --------------------- |
| **VS Code**        | React Native Tools 🏆 |
| **Xcode**          | iOS debugging         |
| **Android Studio** | Android debugging     |

---

## 🆕 New Architecture (Required 2026)

### Overview

```
┌─────────────────────────────────────────────────────┐
│                  JavaScript                          │
├─────────────────────────────────────────────────────┤
│                      JSI                             │
│        (Direct JS ↔ Native Communication)           │
├─────────────────────────────────────────────────────┤
│    Fabric (UI)     │     Turbo Modules (Native)     │
├─────────────────────────────────────────────────────┤
│                 Native (iOS/Android)                 │
└─────────────────────────────────────────────────────┘
```

### Enable New Architecture

```javascript
// app.json (Expo)
{
  "expo": {
    "newArchEnabled": true
  }
}

// android/gradle.properties (Bare)
newArchEnabled=true

// ios/Podfile (Bare)
ENV['RCT_NEW_ARCH_ENABLED'] = '1'
```

---

## 🔧 Core Patterns

### Component Structure

```tsx
import React from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";

interface UserCardProps {
  user: User;
  onPress: (user: User) => void;
}

export function UserCard({ user, onPress }: UserCardProps) {
  return (
    <Pressable
      style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
      onPress={() => onPress(user)}
    >
      <Text style={styles.name}>{user.name}</Text>
      <Text style={styles.email}>{user.email}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 16,
    backgroundColor: "#fff",
    borderRadius: 8,
    marginVertical: 4,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  cardPressed: {
    opacity: 0.8,
  },
  name: {
    fontSize: 16,
    fontWeight: "600",
  },
  email: {
    fontSize: 14,
    color: "#666",
    marginTop: 4,
  },
});
```

### List Rendering (FlashList)

```tsx
import { FlashList } from "@shopify/flash-list";

function UserList() {
  const { data, isLoading, refetch } = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
  });

  return (
    <FlashList
      data={data}
      renderItem={({ item }) => <UserCard user={item} onPress={handlePress} />}
      estimatedItemSize={80}
      refreshing={isLoading}
      onRefresh={refetch}
      keyExtractor={(item) => item.id.toString()}
      ListEmptyComponent={<EmptyState />}
    />
  );
}
```

### Navigation (React Navigation)

```tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

type RootStackParamList = {
  Home: undefined;
  Profile: { userId: string };
  Settings: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen
          name="Profile"
          component={ProfileScreen}
          options={{ title: "User Profile" }}
        />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Expo Features

```tsx
// Camera with Expo
import { CameraView, useCameraPermissions } from "expo-camera";

function Scanner() {
  const [permission, requestPermission] = useCameraPermissions();

  if (!permission?.granted) {
    return <Button title="Grant Permission" onPress={requestPermission} />;
  }

  return (
    <CameraView
      style={StyleSheet.absoluteFill}
      onBarcodeScanned={({ data }) => console.log(data)}
      barcodeScannerSettings={{
        barcodeTypes: ["qr"],
      }}
    />
  );
}
```

---

## ⚡ Performance Patterns

### Animations with Reanimated

```tsx
import Animated, {
  useAnimatedStyle,
  withSpring,
  useSharedValue,
} from "react-native-reanimated";

function AnimatedButton() {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: withSpring(scale.value) }],
  }));

  return (
    <Animated.View style={animatedStyle}>
      <Pressable
        onPressIn={() => (scale.value = 0.95)}
        onPressOut={() => (scale.value = 1)}
      >
        <Text>Press Me</Text>
      </Pressable>
    </Animated.View>
  );
}
```

### Memoization

```tsx
// ✅ Memoize expensive components
const MemoizedCard = React.memo(UserCard);

// ✅ Memoize callbacks
const handlePress = useCallback(
  (user: User) => {
    navigation.navigate("Profile", { userId: user.id });
  },
  [navigation],
);
```

---

## ✅ Best Practices Checklist

### Architecture

- [ ] New Architecture enabled
- [ ] Fabric components used
- [ ] Turbo Modules for native code
- [ ] Hermes engine

### Performance

- [ ] FlashList over FlatList
- [ ] React.memo for lists
- [ ] Reanimated for animations
- [ ] Avoid inline styles

### Expo

- [ ] EAS Build for production
- [ ] OTA updates configured
- [ ] Development client for testing

---

_DOMYH Awesome Code • React Native 0.76+_
