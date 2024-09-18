import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const Tutorial = () => {
  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle>How to Use KaFin2</CardTitle>
      </CardHeader>
      <CardContent>
        <ol className="list-decimal list-inside space-y-2">
          <li>Enter your financial analysis request in natural language.</li>
          <li>You can ask for stock price comparisons, economic indicator analysis, or custom financial queries.</li>
          <li>Examples:
            <ul className="list-disc list-inside ml-4">
              <li>"Compare Apple and Microsoft stock prices for the last 6 months"</li>
              <li>"Show me the trend of US GDP growth rate over the past 5 years"</li>
              <li>"Analyze the correlation between S&P 500 and oil prices"</li>
            </ul>
          </li>
          <li>Click the "Analyze" button to process your request.</li>
          <li>View the generated charts, AI analysis, and financial data on the dashboard.</li>
          <li>Use the tabs to switch between different views of the analysis.</li>
          <li>Optionally, save your results to Google Drive for future reference.</li>
        </ol>
      </CardContent>
    </Card>
  );
};

export default Tutorial;