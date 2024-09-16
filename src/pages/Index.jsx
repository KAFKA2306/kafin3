import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const dummyChartData = [
  { name: 'Jan', Toyota: 4000, Honda: 2400 },
  { name: 'Feb', Toyota: 3000, Honda: 1398 },
  { name: 'Mar', Toyota: 2000, Honda: 9800 },
  { name: 'Apr', Toyota: 2780, Honda: 3908 },
  { name: 'May', Toyota: 1890, Honda: 4800 },
  { name: 'Jun', Toyota: 2390, Honda: 3800 },
];

const Index = () => {
  const [analysisRequest, setAnalysisRequest] = useState('');

  const handleAnalysis = () => {
    // Here you would integrate with your AI and data processing logic
    console.log("Analyzing:", analysisRequest);
    // For now, we'll just log the request
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-center mb-2">KaFin2: AI-Powered Finance Dashboard 🤖📊</h1>
        <p className="text-xl text-center text-gray-600">Analyze and visualize financial data with natural language commands</p>
      </header>

      <main className="max-w-6xl mx-auto">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Enter Your Financial Analysis Request</CardTitle>
            <CardDescription>Use natural language to describe the analysis you want to perform</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              <Input 
                placeholder="E.g., Compare Toyota and Honda stock prices for the past 3 months" 
                className="flex-grow"
                value={analysisRequest}
                onChange={(e) => setAnalysisRequest(e.target.value)}
              />
              <Button onClick={handleAnalysis}>Analyze</Button>
            </div>
          </CardContent>
        </Card>

        <Tabs defaultValue="dashboard" className="mb-8">
          <TabsList>
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="features">Features</TabsTrigger>
            <TabsTrigger value="examples">Examples</TabsTrigger>
          </TabsList>
          <TabsContent value="dashboard">
            <Card>
              <CardHeader>
                <CardTitle>Sample Dashboard</CardTitle>
                <CardDescription>Toyota vs Honda Stock Comparison (Last 6 Months)</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={dummyChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="Toyota" stroke="#8884d8" />
                    <Line type="monotone" dataKey="Honda" stroke="#82ca9d" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="features">
            <Card>
              <CardHeader>
                <CardTitle>Key Features</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="list-disc pl-5 space-y-2">
                  <li>AI-driven natural language interface</li>
                  <li>Dynamic dashboard generation</li>
                  <li>Comprehensive financial data analysis</li>
                  <li>Automatic data updates</li>
                  <li>Multi-device support</li>
                  <li>Cloud-native architecture</li>
                  <li>Completely free and open-source</li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="examples">
            <Card>
              <CardHeader>
                <CardTitle>Example Queries</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="list-disc pl-5 space-y-2">
                  <li>"Compare Toyota and Honda stock prices for the past 3 months using a line chart."</li>
                  <li>"Show the performance of Nikkei 225 and S&P 500 in 2023 with monthly return bar graphs."</li>
                  <li>"Display the FED balance sheet and 10-year Treasury yield for the last 5 years and explain their correlation."</li>
                  <li>"Create a scatter plot of USD/JPY exchange rate vs Nikkei 225 for the past year."</li>
                  <li>"Compare GAFA (Google, Apple, Facebook, Amazon) stock performance YTD and show their returns in a table."</li>
                </ul>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

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
              <CardTitle>Quick Start</CardTitle>
              <CardDescription>Get started with KaFin2</CardDescription>
            </CardHeader>
            <CardContent>
              <ol className="list-decimal pl-5 space-y-2">
                <li>Enter your financial analysis request in natural language</li>
                <li>Review the AI-generated dashboard</li>
                <li>Explore different visualizations and data points</li>
                <li>Save or share your analysis results</li>
              </ol>
            </CardContent>
          </Card>
        </div>
      </main>

      <footer className="mt-12 text-center text-gray-500">
        <p>Powered by OpenAI GPT-4, Streamlit, and various financial data APIs</p>
        <p>© 2024 KaFin2 Project | <a href="https://github.com/yourusername/kafin2" className="underline">GitHub</a></p>
      </footer>
    </div>
  );
};

export default Index;
