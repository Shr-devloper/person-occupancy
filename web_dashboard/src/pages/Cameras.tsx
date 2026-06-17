import { useEffect, useState } from 'react';
import { Button, Card, CardContent, Grid, TextField, Typography } from '@mui/material';
import { api } from '../api/client';

type Camera = { id: number; camera_name: string; location: string; ip_address?: string; status: string };

export default function Cameras() {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [camera_name, setName] = useState('');
  const [location, setLocation] = useState('');
  const load = () => api.get('/cameras').then((r) => setCameras(r.data));
  useEffect(load, []);
  async function create() { await api.post('/camera', { camera_name, location, status: 'offline' }); setName(''); setLocation(''); load(); }
  return <Grid container spacing={2}><Grid item xs={12} md={4}><Card><CardContent><Typography variant="h6">Add Camera</Typography><TextField fullWidth margin="normal" label="Name" value={camera_name} onChange={(e) => setName(e.target.value)} /><TextField fullWidth margin="normal" label="Location" value={location} onChange={(e) => setLocation(e.target.value)} /><Button variant="contained" onClick={create}>Save</Button></CardContent></Card></Grid><Grid item xs={12} md={8}>{cameras.map((camera) => <Card sx={{ mb: 1 }} key={camera.id}><CardContent><Typography variant="h6">{camera.camera_name}</Typography><Typography>{camera.location} - {camera.status}</Typography></CardContent></Card>)}</Grid></Grid>;
}
