import { useEffect, useState } from 'react';
import { Button, Card, CardContent, Grid, TextField, Typography } from '@mui/material';
import { api } from '../api/client';

type Seat = { id: number; seat_name: string; camera_id: number; current_state: string };

export default function Seats() {
  const [seats, setSeats] = useState<Seat[]>([]);
  const [seat_name, setName] = useState('');
  const [camera_id, setCameraId] = useState(1);
  const load = () => api.get('/seats').then((r) => setSeats(r.data));
  useEffect(load, []);
  async function create() { await api.post('/seat', { seat_name, camera_id, region_x1: 100, region_y1: 100, region_x2: 400, region_y2: 400 }); setName(''); load(); }
  return <Grid container spacing={2}><Grid item xs={12} md={4}><Card><CardContent><Typography variant="h6">Add Seat</Typography><TextField fullWidth margin="normal" label="Seat name" value={seat_name} onChange={(e) => setName(e.target.value)} /><TextField fullWidth margin="normal" type="number" label="Camera ID" value={camera_id} onChange={(e) => setCameraId(Number(e.target.value))} /><Button variant="contained" onClick={create}>Save</Button></CardContent></Card></Grid><Grid item xs={12} md={8}>{seats.map((seat) => <Card sx={{ mb: 1 }} key={seat.id}><CardContent><Typography variant="h6">{seat.seat_name}</Typography><Typography>Camera {seat.camera_id} - {seat.current_state}</Typography></CardContent></Card>)}</Grid></Grid>;
}
