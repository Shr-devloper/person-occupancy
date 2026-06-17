import { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { api, AnalyticsPoint } from '../api/client';

export default function Analytics() {
  const [daily, setDaily] = useState<AnalyticsPoint[]>([]);
  const [weekly, setWeekly] = useState<AnalyticsPoint[]>([]);
  const [monthly, setMonthly] = useState<AnalyticsPoint[]>([]);
  useEffect(() => { api.get('/occupancy/daily').then((r) => setDaily([r.data])); api.get('/occupancy/weekly').then((r) => setWeekly(r.data)); api.get('/occupancy/monthly').then((r) => setMonthly(r.data)); }, []);
  const chart = (title: string, data: AnalyticsPoint[]) => <Card><CardContent><Typography variant="h6">{title}</Typography><ResponsiveContainer width="100%" height={260}><LineChart data={data}><XAxis dataKey="label" /><YAxis /><Tooltip /><Line dataKey="occupancy_percentage" stroke="#1565c0" /></LineChart></ResponsiveContainer></CardContent></Card>;
  return <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}><Box sx={{ gridColumn: { xs: '1', md: '1 / -1' } }}>{chart('Daily occupancy', daily)}</Box>{chart('Weekly occupancy', weekly)}{chart('Monthly occupancy heatmap source data', monthly)}</Box>;
}
