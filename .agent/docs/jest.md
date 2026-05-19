---
library: jest
version: 30.x
latest: true
category: testing
official_docs: https://jestjs.io/docs
last_updated: 2026-03-20
last_checked: 2026-03-21
source: jestjs.io + curated
---

# Jest v29

> Jest — Delightful JavaScript Testing Framework.
> 40M+ npm/week. Built-in mocking, snapshots, code coverage.
> Docs: https://jestjs.io

## Installation

```bash
npm install -D jest @types/jest ts-jest
# OR with TypeScript
npx ts-jest config:init
```

## Configuration

```ts
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
    preset: 'ts-jest',
    testEnvironment: 'node',               // or 'jsdom' for React
    roots: ['<rootDir>/src'],
    testMatch: ['**/*.test.ts', '**/*.spec.ts'],
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1',     // path aliases
    },
    collectCoverage: true,
    coverageThreshold: {
        global: { branches: 80, functions: 80, lines: 80, statements: 80 },
    },
    setupFilesAfterSetup: ['<rootDir>/jest.setup.ts'],
};

export default config;
```

## Test Structure

```ts
describe('UserService', () => {
    let service: UserService;

    beforeAll(async () => { /* one-time setup */ });
    afterAll(async () => { /* one-time cleanup */ });
    beforeEach(() => { service = new UserService(); });
    afterEach(() => { jest.restoreAllMocks(); });

    it('should create a user', async () => {
        const user = await service.create({ name: 'Alice', email: 'alice@test.com' });
        expect(user.id).toBeDefined();
        expect(user.name).toBe('Alice');
    });

    it.each([
        ['alice@test.com', true],
        ['invalid', false],
        ['', false],
    ])('validates email "%s" → %s', (email, expected) => {
        expect(isValidEmail(email)).toBe(expected);
    });

    it.todo('should handle concurrent creates');
    it.skip('known broken test', () => { /* ... */ });
});
```

## Assertions (Matchers)

```ts
// Equality
expect(value).toBe(42);                    // strict ===
expect(obj).toEqual({ a: 1, b: 2 });      // deep equality
expect(obj).toStrictEqual({ a: 1 });       // deep + type check

// Truthiness
expect(val).toBeTruthy();
expect(val).toBeFalsy();
expect(val).toBeNull();
expect(val).toBeUndefined();
expect(val).toBeDefined();

// Numbers
expect(num).toBeGreaterThan(3);
expect(num).toBeGreaterThanOrEqual(3);
expect(num).toBeLessThan(5);
expect(0.1 + 0.2).toBeCloseTo(0.3);       // floating point

// Strings
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');

// Arrays/Iterables
expect(arr).toContain(item);
expect(arr).toContainEqual({ a: 1 });      // deep match
expect(arr).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('nested.key', 'value');
expect(obj).toMatchObject({ a: 1 });       // partial match

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('error message');
expect(() => fn()).toThrow(CustomError);
await expect(asyncFn()).rejects.toThrow();

// Snapshots
expect(component).toMatchSnapshot();
expect(data).toMatchInlineSnapshot(`"expected"`);
```

## Mocking

```ts
// Mock function
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2);
mockFn.mockImplementation((x: number) => x * 2);
mockFn.mockResolvedValue({ id: 1 });       // async mock

expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(3);
expect(mockFn).toHaveBeenCalledWith('arg1', expect.any(Number));
expect(mockFn).toHaveBeenLastCalledWith('final');

// Mock module
jest.mock('./database', () => ({
    query: jest.fn().mockResolvedValue([{ id: 1 }]),
}));

// Spy on existing method
const spy = jest.spyOn(Math, 'random').mockReturnValue(0.5);
// ... test
spy.mockRestore();

// Mock timers
jest.useFakeTimers();
setTimeout(callback, 1000);
jest.advanceTimersByTime(1000);
expect(callback).toHaveBeenCalled();
jest.useRealTimers();
```

## Async Testing

```ts
// async/await
it('fetches data', async () => {
    const data = await fetchData();
    expect(data).toEqual({ id: 1 });
});

// resolves/rejects
it('resolves', async () => {
    await expect(asyncFn()).resolves.toBe(42);
    await expect(failFn()).rejects.toThrow('error');
});
```

## CLI

```bash
npx jest                          # run all tests
npx jest --watch                  # watch mode
npx jest --watchAll               # watch all files
npx jest --coverage               # with coverage
npx jest path/to/test.ts          # specific file
npx jest --testNamePattern="user" # filter by name
npx jest --verbose                # detailed output
npx jest --bail                   # stop on first failure
```

## Gotchas

⚠️ **vs Vitest**: For new Vite/React projects, prefer Vitest (faster, ESM-native). Jest for legacy/CRA.

⚠️ **`toBe` vs `toEqual`**: `toBe` uses `===` (reference). `toEqual` does deep comparison.

⚠️ **Mock auto-clear**: Mocks persist between tests. Use `afterEach(() => jest.restoreAllMocks())`.

⚠️ **`jest.mock()` hoisted**: Module mocks are hoisted to top of file. Can't use variables from test.

⚠️ **Async**: Always `await` assertions. Forgetting makes test pass silently.

⚠️ **ESM**: Jest uses CommonJS by default. For ESM, use `--experimental-vm-modules` or `ts-jest`.

⚠️ **Snapshots**: Review snapshot diffs carefully. Don't blindly update with `--updateSnapshot`.

⚠️ **`testEnvironment`**: Use `'node'` for backend, `'jsdom'` for React component tests.
