import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const AIAnalysis = ({ data }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>AI-Powered Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{data.aiAnalysis || "AI analysis not available for this data."}</p>
      </CardContent>
    </Card>
  );
};

export default AIAnalysis;