import 'package:dio/dio.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

final apiProvider = Provider((ref) => ApiClient());
final tokenProvider = StateProvider<String?>((ref) => null);

class ApiClient {
  final Dio dio = Dio(BaseOptions(baseUrl: const String.fromEnvironment('API_URL', defaultValue: 'http://localhost:8000')));

  void setToken(String? token) {
    dio.options.headers['Authorization'] = token == null ? null : 'Bearer $token';
  }
}

Future<void> firebaseBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
}

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    await Firebase.initializeApp();
    FirebaseMessaging.onBackgroundMessage(firebaseBackgroundHandler);
  } catch (_) {
    // Firebase config is optional for local development.
  }
  runApp(const ProviderScope(child: SmartSeatApp()));
}

class SmartSeatApp extends ConsumerWidget {
  const SmartSeatApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp(
      title: 'Smart Seat',
      theme: ThemeData(colorSchemeSeed: Colors.blue, useMaterial3: true),
      routes: {
        '/': (_) => const SplashScreen(),
        '/login': (_) => const LoginScreen(),
        '/dashboard': (_) => const DashboardScreen(),
        '/live': (_) => const LiveCameraScreen(),
        '/analytics': (_) => const AnalyticsScreen(),
        '/notifications': (_) => const NotificationsScreen(),
        '/settings': (_) => const SettingsScreen(),
      },
    );
  }
}

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() async {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('token');
      ref.read(tokenProvider.notifier).state = token;
      ref.read(apiProvider).setToken(token);
      if (mounted) Navigator.pushReplacementNamed(context, token == null ? '/login' : '/dashboard');
    });
  }

  @override
  Widget build(BuildContext context) => const Scaffold(body: Center(child: CircularProgressIndicator()));
}

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final email = TextEditingController();
  final password = TextEditingController();
  String? error;

  Future<void> login() async {
    try {
      final api = ref.read(apiProvider);
      final response = await api.dio.post('/login', data: {'email': email.text, 'password': password.text});
      final token = response.data['access_token'] as String;
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', token);
      api.setToken(token);
      ref.read(tokenProvider.notifier).state = token;
      if (mounted) Navigator.pushReplacementNamed(context, '/dashboard');
    } catch (_) {
      setState(() => error = 'Login failed. Check email and password.');
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        body: Center(
          child: SizedBox(
            width: 360,
            child: Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Text('Smart Seat Login', style: TextStyle(fontSize: 24)),
                  if (error != null) Text(error!, style: const TextStyle(color: Colors.red)),
                  TextField(controller: email, decoration: const InputDecoration(labelText: 'Email')),
                  TextField(controller: password, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
                  const SizedBox(height: 16),
                  FilledButton(onPressed: login, child: const Text('Login')),
                ]),
              ),
            ),
          ),
        ),
      );
}

class AppScaffold extends StatelessWidget {
  const AppScaffold({super.key, required this.title, required this.child});
  final String title;
  final Widget child;

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: Text(title)),
        drawer: Drawer(
          child: ListView(children: [
            const DrawerHeader(child: Text('Smart Seat')),
            ListTile(title: const Text('Dashboard'), onTap: () => Navigator.pushReplacementNamed(context, '/dashboard')),
            ListTile(title: const Text('Live Camera'), onTap: () => Navigator.pushReplacementNamed(context, '/live')),
            ListTile(title: const Text('Analytics'), onTap: () => Navigator.pushReplacementNamed(context, '/analytics')),
            ListTile(title: const Text('Notifications'), onTap: () => Navigator.pushReplacementNamed(context, '/notifications')),
            ListTile(title: const Text('Settings'), onTap: () => Navigator.pushReplacementNamed(context, '/settings')),
          ]),
        ),
        body: child,
      );
}

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  Map<String, dynamic>? data;

  @override
  void initState() {
    super.initState();
    ref.read(apiProvider).dio.get('/analytics/dashboard').then((value) => setState(() => data = Map<String, dynamic>.from(value.data)));
  }

  @override
  Widget build(BuildContext context) {
    final d = data;
    return AppScaffold(
      title: 'Dashboard',
      child: d == null
          ? const Center(child: CircularProgressIndicator())
          : GridView.count(
              padding: const EdgeInsets.all(16),
              crossAxisCount: 2,
              children: [
                MetricCard('Total Seats', '${d['total_seats']}'),
                MetricCard('Occupied', '${d['occupied_seats']}'),
                MetricCard('Available', '${d['available_seats']}'),
                MetricCard('Occupancy', '${d['occupancy_percentage']}%'),
              ],
            ),
    );
  }
}

class MetricCard extends StatelessWidget {
  const MetricCard(this.title, this.value, {super.key});
  final String title;
  final String value;

  @override
  Widget build(BuildContext context) => Card(child: Center(child: Column(mainAxisSize: MainAxisSize.min, children: [Text(title), Text(value, style: Theme.of(context).textTheme.headlineMedium)])));
}

class LiveCameraScreen extends StatelessWidget {
  const LiveCameraScreen({super.key});

  @override
  Widget build(BuildContext context) => const AppScaffold(title: 'Live Camera', child: Center(child: Text('Live stream placeholder. Use an approved secure stream gateway.')));
}

class AnalyticsScreen extends StatelessWidget {
  const AnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context) => AppScaffold(
        title: 'Analytics',
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: LineChart(LineChartData(lineBarsData: [LineChartBarData(spots: const [FlSpot(0, 10), FlSpot(1, 35), FlSpot(2, 22)])])),
        ),
      );
}

class NotificationsScreen extends ConsumerStatefulWidget {
  const NotificationsScreen({super.key});

  @override
  ConsumerState<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends ConsumerState<NotificationsScreen> {
  List<dynamic> items = [];

  @override
  void initState() {
    super.initState();
    ref.read(apiProvider).dio.get('/notifications').then((value) => setState(() => items = value.data as List<dynamic>));
  }

  @override
  Widget build(BuildContext context) => AppScaffold(title: 'Notifications', child: ListView(children: items.map((item) => ListTile(title: Text(item['title']), subtitle: Text(item['message']))).toList()));
}

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) => const AppScaffold(title: 'Settings', child: Center(child: Text('Notification preferences and API URL settings.')));
}
