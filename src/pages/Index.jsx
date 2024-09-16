import React from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-center mb-2">KaFin2: AI-Powered Finance Dashboard 🤖📊</h1>
        <p className="text-xl text-center text-gray-600">Analyze and visualize financial data with natural language commands</p>
      </header>

      <main className="max-w-4xl mx-auto">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Enter Your Financial Analysis Request</CardTitle>
            <CardDescription>Use natural language to describe the analysis you want to perform</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              <Input placeholder="E.g., Compare Toyota and Honda stock prices for the past 3 months" className="flex-grow" />
              <Button>Analyze</Button>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Dashboards</CardTitle>
              <CardDescription>Quick access to your latest analyses</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5">
                <li>GAFA Stock Performance YTD</li>
                <li>USD/JPY vs Nikkei 225 Correlation</li>
                <li>FED Balance Sheet vs 10Y Treasury Yield</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Features</CardTitle>
              <CardDescription>Key capabilities of KaFin2</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="list-disc pl-5">
                <li>AI-driven natural language interface</li>
                <li>Dynamic dashboard generation</li>
                <li>Comprehensive financial data analysis</li>
                <li>Automatic data updates</li>
                <li>Multi-device support</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </main>

      <footer className="mt-12 text-center text-gray-500">
        <p>Powered by OpenAI GPT-4, Streamlit, and various financial data APIs</p>
        <p>© 2024 KaFin2 Project</p>
      </footer>
    </div>
  );
};

export default Index;
