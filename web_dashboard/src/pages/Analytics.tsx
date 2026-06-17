import { useEffect, useState } from 'react';
import { Card, CardContent, Grid, Typography } from '@mui/material';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api, AnalyticsPoint } from '../api/client';

export default function Analytics() {
  const [daily, setDaily] = useState<AnalyticsPoint[]>([]);
  const [weekly, setWeekly] = useState<AnalyticsPoint[]>([]);
  const [monthly, setMonthly] = useState<AnalyticsPoint[]>([]);
  useEffect(() => { api.get('/occupancy/daily').then((r) => setDaily([r.data])); api.get('/occupancy/weekly').then((r) => setWeekly(r.data)); api.get('/occupancy/monthly').then((r) => setMonthly(r.data)); }, []);
  const chart = (title: string, data: AnalyticsPoint[]) => <Card><CardContent><Typography variant="h6">{title}</Typography><ResponsiveContainer width="100%" height={260}><LineChart data={data}><XAxis dataKey="label" /><YAxis /><Tooltip /><Line dataKey="occupancy_percentage" stroke="#1565c0" /></LineChart></ResponsiveContainer></CardContent></Card>;
  return <Grid container spacing={2}><Grid item xs={12}>{chart('Daily occupancy', daily)}</Grid><Grid item xs={12} md={6}>{chart('Weekly occupancy', weekly)}</Grid><Grid item xs={12} md={6}>{chart('Monthly occupancy heatmap source data', monthly)}</Grid></Grid>;
}
