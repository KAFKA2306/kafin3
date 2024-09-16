import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const FinancialDataAnalysis = ({ data }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Financial Data Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        {data.financialAnalysis ? (
          <pre>{JSON.stringify(data.financialAnalysis, null, 2)}</pre>
        ) : (
          <p>No financial analysis data available.</p>
        )}
      </CardContent>
    </Card>
  );
};

export default FinancialDataAnalysis;