import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { useQuery } from '@tanstack/react-query';
import AIAnalysis from '../components/AIAnalysis';
import DynamicDashboard from '../components/DynamicDashboard';
import FinancialDataAnalysis from '../components/FinancialDataAnalysis';

const fetchFinancialData = async (query, useGoogleDrive) => {
  const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, use_google_drive: useGoogleDrive }),
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

const Index = () => {
  const [analysisRequest, setAnalysisRequest] = useState('');
  const [useGoogleDrive, setUseGoogleDrive] = useState(false);
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['financialData', analysisRequest, useGoogleDrive],
    queryFn: () => fetchFinancialData(analysisRequest, useGoogleDrive),
    enabled: false,
  });

  const handleAnalysis = () => {
    refetch();
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
            <div className="flex space-x-2 mb-4">
              <Input 
                placeholder="E.g., Compare Toyota and Honda stock prices for the past 3 months" 
                className="flex-grow"
                value={analysisRequest}
                onChange={(e) => setAnalysisRequest(e.target.value)}
              />
              <Button onClick={handleAnalysis} disabled={isLoading}>
                {isLoading ? 'Analyzing...' : 'Analyze'}
              </Button>
            </div>
            <div className="flex items-center space-x-2">
              <Switch
                id="google-drive"
                checked={useGoogleDrive}
                onCheckedChange={setUseGoogleDrive}
              />
              <label htmlFor="google-drive">Save results to Google Drive</label>
            </div>
          </CardContent>
        </Card>

        {error && (
          <Card className="mb-8 bg-red-50">
            <CardContent>
              <p className="text-red-500">Error: {error.message}</p>
            </CardContent>
          </Card>
        )}

        {data && (
          <>
            <Tabs defaultValue="dashboard" className="mb-8">
              <TabsList>
                <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
                <TabsTrigger value="aiAnalysis">AI Analysis</TabsTrigger>
                <TabsTrigger value="financialData">Financial Data</TabsTrigger>
              </TabsList>
              <TabsContent value="dashboard">
                <DynamicDashboard data={data} />
              </TabsContent>
              <TabsContent value="aiAnalysis">
                <AIAnalysis data={data} />
              </TabsContent>
              <TabsContent value="financialData">
                <FinancialDataAnalysis data={data} />
              </TabsContent>
            </Tabs>
            
            {data.google_drive_link && (
              <Card className="mb-8">
                <CardContent>
                  <p>Data saved to Google Drive: <a href={data.google_drive_link} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">View File</a></p>
                </CardContent>
              </Card>
            )}
          </>
        )}
      </main>

      <footer className="mt-12 text-center text-gray-500">
        <p>Powered by OpenAI GPT-4, FastAPI, and various financial data APIs</p>
        <p>© 2024 KaFin2 Project | <a href="https://github.com/yourusername/kafin2" className="underline">GitHub</a></p>
      </footer>
    </div>
  );
};

export default Index;
