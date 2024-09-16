import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DynamicDashboard = ({ data }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Dynamic Dashboard</CardTitle>
      </CardHeader>
      <CardContent>
        {data.chartData ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              {Object.keys(data.chartData[0]).filter(key => key !== 'name').map((key, index) => (
                <Line key={index} type="monotone" dataKey={key} stroke={`#${Math.floor(Math.random()*16777215).toString(16)}`} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p>No chart data available.</p>
        )}
      </CardContent>
    </Card>
  );
};

export default DynamicDashboard;