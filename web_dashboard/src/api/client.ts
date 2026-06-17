import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api'
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export type AnalyticsPoint = { label: string; occupied_seconds: number; occupancy_percentage: number };
export type DashboardAnalytics = {
  total_seats: number;
  occupied_seats: number;
  available_seats: number;
  occupancy_percentage: number;
  camera_status: Record<string, number>;
  daily: AnalyticsPoint[];
  weekly: AnalyticsPoint[];
  monthly: AnalyticsPoint[];
  peak_usage_hours: AnalyticsPoint[];
  most_used_seats: { seat_id: number; seat_name: string; occupied_seconds: number }[];
  least_used_seats: { seat_id: number; seat_name: string; occupied_seconds: number }[];
};
