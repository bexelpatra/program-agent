import Link from "next/link";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ko } from "@/lib/i18n/ko";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">{ko.app.title}</h1>
          <p className="mt-2 text-lg text-gray-600">{ko.app.subtitle}</p>
        </header>

        <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>{ko.nav.backtests}</CardTitle>
              <CardDescription>{ko.backtest.create}</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/backtests/new">
                <Button>{ko.backtest.create}</Button>
              </Link>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{ko.nav.assets}</CardTitle>
              <CardDescription>{ko.asset.add}</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/assets">
                <Button variant="secondary">자산 카탈로그 보기</Button>
              </Link>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{ko.nav.history}</CardTitle>
              <CardDescription>백테스트 결과 이력</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/backtests">
                <Button variant="secondary">이력 보기</Button>
              </Link>
            </CardContent>
          </Card>
        </section>
      </div>
    </main>
  );
}
