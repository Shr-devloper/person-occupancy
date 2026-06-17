import { Card, CardContent, Typography } from '@mui/material';

export default function Profile() {
  return <Card><CardContent><Typography variant="h5">User Profile</Typography><Typography>JWT-authenticated profile settings can be extended here for name, role, password reset, and notification preferences.</Typography></CardContent></Card>;
}
