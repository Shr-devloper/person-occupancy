import { useEffect, useState } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { api } from '../api/client';

type Notification = { id: number; title: string; message: string; severity: string; created_at: string };

export default function Notifications() {
  const [items, setItems] = useState<Notification[]>([]);
  useEffect(() => { api.get('/notifications').then((r) => setItems(r.data)); }, []);
  return <>{items.map((item) => <Card sx={{ mb: 1 }} key={item.id}><CardContent><Typography variant="h6">{item.title}</Typography><Typography>{item.message}</Typography><Typography color="text.secondary">{item.severity} - {new Date(item.created_at).toLocaleString()}</Typography></CardContent></Card>)}</>;
}
