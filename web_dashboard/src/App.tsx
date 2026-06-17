import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material';
import { Link, Navigate, Route, Routes, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Cameras from './pages/Cameras';
import Seats from './pages/Seats';
import LiveCamera from './pages/LiveCamera';
import Analytics from './pages/Analytics';
import Notifications from './pages/Notifications';
import Profile from './pages/Profile';

function PrivateRoute({ children }: { children: React.ReactElement }) {
  return localStorage.getItem('token') ? children : <Navigate to="/login" replace />;
}

function Shell({ children }: { children: React.ReactElement }) {
  const navigate = useNavigate();
  const logout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };
  return (
    <Box>
      <AppBar position="static">
        <Toolbar sx={{ gap: 2 }}>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Smart Seat</Typography>
          {['Dashboard', 'Cameras', 'Seats', 'Live', 'Analytics', 'Notifications', 'Profile'].map((name) => (
            <Button color="inherit" component={Link} to={name === 'Dashboard' ? '/' : `/${name.toLowerCase()}`} key={name}>{name}</Button>
          ))}
          <Button color="inherit" onClick={logout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 3 }}>{children}</Container>
    </Box>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<PrivateRoute><Shell><Dashboard /></Shell></PrivateRoute>} />
      <Route path="/cameras" element={<PrivateRoute><Shell><Cameras /></Shell></PrivateRoute>} />
      <Route path="/seats" element={<PrivateRoute><Shell><Seats /></Shell></PrivateRoute>} />
      <Route path="/live" element={<PrivateRoute><Shell><LiveCamera /></Shell></PrivateRoute>} />
      <Route path="/analytics" element={<PrivateRoute><Shell><Analytics /></Shell></PrivateRoute>} />
      <Route path="/notifications" element={<PrivateRoute><Shell><Notifications /></Shell></PrivateRoute>} />
      <Route path="/profile" element={<PrivateRoute><Shell><Profile /></Shell></PrivateRoute>} />
    </Routes>
  );
}
