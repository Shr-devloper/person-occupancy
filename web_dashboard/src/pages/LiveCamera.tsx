import { Alert, Card, CardContent, Typography } from '@mui/material';

export default function LiveCamera() {
  return <Card><CardContent><Typography variant="h5" gutterBottom>Live Camera View</Typography><Alert severity="info">For privacy, the production system does not store video. Add an authenticated MJPEG/WebRTC gateway here only when live viewing is legally approved for your office.</Alert></CardContent></Card>;
}
