import { useEffect, useState } from 'react';
import { Card, CardContent, Grid, Typography } from '@mui/material';
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
    <Grid container spacing={2}>
      <Grid item xs={12} md={2.4}><Widget title="Total Seats" value={data.total_seats} /></Grid>
      <Grid item xs={12} md={2.4}><Widget title="Occupied" value={data.occupied_seats} /></Grid>
      <Grid item xs={12} md={2.4}><Widget title="Available" value={data.available_seats} /></Grid>
      <Grid item xs={12} md={2.4}><Widget title="Occupancy %" value={`${data.occupancy_percentage}%`} /></Grid>
      <Grid item xs={12} md={2.4}><Widget title="Camera Status" value={Object.entries(data.camera_status).map(([k, v]) => `${k}:${v}`).join(' ') || 'none'} /></Grid>
      <Grid item xs={12} md={6}><Card><CardContent><Typography variant="h6">Weekly occupancy</Typography><ResponsiveContainer width="100%" height={280}><BarChart data={data.weekly}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="label" /><YAxis /><Tooltip /><Bar dataKey="occupancy_percentage" fill="#1565c0" /></BarChart></ResponsiveContainer></CardContent></Card></Grid>
      <Grid item xs={12} md={6}><Card><CardContent><Typography variant="h6">Peak usage hours</Typography><ResponsiveContainer width="100%" height={280}><BarChart data={data.peak_usage_hours}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="label" /><YAxis /><Tooltip /><Bar dataKey="occupied_seconds" fill="#2e7d32" /></BarChart></ResponsiveContainer></CardContent></Card></Grid>
    </Grid>
  );
}
