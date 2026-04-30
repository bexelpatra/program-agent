/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // VPN 사용자 브라우저는 :3001 만 접근. backend(8001) 는 내부에서 frontend 가 프록시.
  // → 외부 노출 포트는 3001 하나뿐, backend 는 localhost 유지 (보안 ↑).
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:8001/api/:path*",
      },
    ];
  },
};

export default nextConfig;
