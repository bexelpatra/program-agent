import { defineConfig } from "vitest/config";
import path from "node:path";

/**
 * vitest 설정 — TASK-218 useFormPersistence 단위 테스트 도입.
 *
 * - environment: jsdom (localStorage / window 가 필요한 React hook 테스트).
 * - alias '@/...' → 프런트 루트 (tsconfig paths 와 동기).
 * - globals: false (test/expect 등은 명시 import).
 */
export default defineConfig({
  test: {
    environment: "jsdom",
    globals: false,
    include: ["**/__tests__/**/*.test.{ts,tsx}"],
    exclude: ["node_modules/**", ".next/**"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./"),
    },
  },
});
