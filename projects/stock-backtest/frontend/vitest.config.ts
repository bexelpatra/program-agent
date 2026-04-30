import { defineConfig } from "vitest/config";
import path from "node:path";

/**
 * vitest 설정 — TASK-218 useFormPersistence 단위 테스트 도입,
 * TASK-237 BacktestResultView (.tsx) 컴포넌트 렌더 테스트 확장.
 *
 * - environment: jsdom (localStorage / window 가 필요한 React hook 테스트
 *   + @testing-library/react 의 render).
 * - alias '@/...' → 프런트 루트 (tsconfig paths 와 동기).
 * - globals: false (test/expect 등은 명시 import).
 * - esbuild.jsx='automatic': tsconfig 의 jsx='preserve' 는 Next.js 빌드용
 *   이며 vitest 의 esbuild 변환에는 반영되지 않는다. .tsx 테스트 파일이
 *   `import React` 없이 JSX 를 쓸 수 있도록 React 17+ automatic runtime
 *   을 명시한다.
 */
export default defineConfig({
  test: {
    environment: "jsdom",
    globals: false,
    include: ["**/__tests__/**/*.test.{ts,tsx}"],
    exclude: ["node_modules/**", ".next/**"],
  },
  esbuild: {
    jsx: "automatic",
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./"),
    },
  },
});
