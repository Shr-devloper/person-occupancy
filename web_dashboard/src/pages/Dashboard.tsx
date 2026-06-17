import { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api, DashboardAnalytics } from '../api/client';

function Widget({ title, value }: { title: string; value: string | number }) {
  return <Card><CardContent><Typography color="text.secondary">{title}</Typography><Typography variant="h4">{value}</Typography></CardContent></Card>;
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardAnalytics | null>(null);
  useEffect(() => { api.get('/analytics/dashboard').then((r) => setData(r.data)); }, []);
  if (!data) return <Typography>Loading dashboard...</Typography>;
  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(5, 1fr)' }, gap: 2 }}>
      <Widget title="Total Seats" value={data.total_seats} />
      <Widget title="Occupied" value={data.occupied_seats} />
      <Widget title="Available" value={data.available_seats} />
      <Widget title="Occupancy %" value={`${data.occupancy_percentage}%`} />
      <Widget title="Camera Status" value={Object.entries(data.camera_status).map(([k, v]) => `${k}:${v}`).join(' ') || 'none'} />
      <Card sx={{ gridColumn: { xs: '1', md: 'span 3' } }}><CardContent><Typography variant="h6">Weekly occupancy</Typography><ResponsiveContainer width="100%" height={280}><BarChart data={data.weekly}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="label" /><YAxis /><Tooltip /><Bar dataKey="occupancy_percentage" fill="#1565c0" /></BarChart></ResponsiveContainer></CardContent></Card>
      <Card sx={{ gridColumn: { xs: '1', md: 'span 2' } }}><CardContent><Typography variant="h6">Peak usage hours</Typography><ResponsiveContainer width="100%" height={280}><BarChart data={data.peak_usage_hours}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="label" /><YAxis /><Tooltip /><Bar dataKey="occupied_seconds" fill="#2e7d32" /></BarChart></ResponsiveContainer></CardContent></Card>
    </Box>
  );
}
