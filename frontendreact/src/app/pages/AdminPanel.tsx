import { Users, Shield, Activity, Database, Settings, AlertTriangle } from 'lucide-react';

const systemStats = [
  { label: 'Active Users', value: '24', change: '+3', icon: Users, color: 'blue' },
  { label: 'System Uptime', value: '99.9%', change: '0.0%', icon: Activity, color: 'emerald' },
  { label: 'Storage Used', value: '67%', change: '+5%', icon: Database, color: 'purple' },
  { label: 'Security Score', value: '95', change: '+2', icon: Shield, color: 'teal' },
];

const users = [
  {
    name: 'Sarah Johnson',
    role: 'Medical Rep',
    email: 'sarah.j@company.com',
    status: 'Active',
    lastLogin: '2 hours ago',
  },
  {
    name: 'Michael Chen',
    role: 'Medical Rep',
    email: 'michael.c@company.com',
    status: 'Active',
    lastLogin: '5 hours ago',
  },
  {
    name: 'Emma Williams',
    role: 'Team Lead',
    email: 'emma.w@company.com',
    status: 'Active',
    lastLogin: '1 hour ago',
  },
  {
    name: 'David Martinez',
    role: 'Medical Rep',
    email: 'david.m@company.com',
    status: 'Inactive',
    lastLogin: '2 days ago',
  },
];

const systemLogs = [
  { event: 'User login', user: 'sarah.j@company.com', time: '10 minutes ago', status: 'success' },
  { event: 'CRM sync completed', user: 'System', time: '15 minutes ago', status: 'success' },
  { event: 'Report generated', user: 'emma.w@company.com', time: '1 hour ago', status: 'success' },
  { event: 'Failed login attempt', user: 'unknown', time: '2 hours ago', status: 'warning' },
];

export function AdminPanel() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900 mb-2">Admin Panel</h1>
            <p className="text-slate-600">System administration and user management</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-sm font-medium flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              System Healthy
            </span>
          </div>
        </div>
      </div>

      {/* System Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {systemStats.map((stat, index) => {
          const Icon = stat.icon;
          const colorMap = {
            blue: 'from-blue-600 to-blue-500',
            emerald: 'from-emerald-600 to-emerald-500',
            purple: 'from-purple-600 to-purple-500',
            teal: 'from-teal-600 to-teal-500',
          };
          return (
            <div
              key={index}
              className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg"
            >
              <div className="flex items-start justify-between mb-4">
                <div
                  className={`w-12 h-12 rounded-xl bg-gradient-to-br ${
                    colorMap[stat.color as keyof typeof colorMap]
                  } flex items-center justify-center shadow-lg`}
                >
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <span className="text-emerald-600 text-sm font-medium bg-emerald-50 px-3 py-1 rounded-lg">
                  {stat.change}
                </span>
              </div>
              <h3 className="text-slate-600 text-sm mb-2">{stat.label}</h3>
              <p className="text-3xl font-bold text-slate-900">{stat.value}</p>
            </div>
          );
        })}
      </div>

      {/* User Management & System Logs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* User Management */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-slate-900">User Management</h3>
            <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-teal-500 text-white font-medium text-sm shadow-lg hover:shadow-xl transition-all">
              Add User
            </button>
          </div>

          <div className="space-y-3">
            {users.map((user, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user.name
                        .split(' ')
                        .map((n) => n[0])
                        .join('')}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-slate-900 text-sm">{user.name}</p>
                    <p className="text-xs text-slate-500">{user.email}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${
                      user.status === 'Active'
                        ? 'bg-emerald-100 text-emerald-700'
                        : 'bg-slate-200 text-slate-600'
                    }`}
                  >
                    {user.status}
                  </span>
                  <button className="p-1 hover:bg-slate-200 rounded transition-colors">
                    <Settings className="w-4 h-4 text-slate-600" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Logs */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-slate-900">System Logs</h3>
            <button className="text-sm text-blue-600 hover:text-blue-700">View All</button>
          </div>

          <div className="space-y-3">
            {systemLogs.map((log, index) => (
              <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-slate-50">
                <div
                  className={`w-2 h-2 rounded-full mt-1.5 ${
                    log.status === 'success'
                      ? 'bg-emerald-500'
                      : log.status === 'warning'
                      ? 'bg-amber-500'
                      : 'bg-red-500'
                  }`}
                ></div>
                <div className="flex-1">
                  <p className="text-sm text-slate-900 font-medium">{log.event}</p>
                  <p className="text-xs text-slate-500 mt-1">
                    {log.user} • {log.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <Users className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Manage Users</h3>
          <p className="text-blue-100 text-sm">Add, edit, or remove users</p>
        </div>

        <div className="bg-gradient-to-br from-teal-600 to-teal-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <Shield className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Security</h3>
          <p className="text-teal-100 text-sm">Configure security settings</p>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <Database className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Database</h3>
          <p className="text-purple-100 text-sm">Manage data and backups</p>
        </div>

        <div className="bg-gradient-to-br from-red-600 to-red-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <AlertTriangle className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Alerts</h3>
          <p className="text-red-100 text-sm">View system alerts</p>
        </div>
      </div>

      {/* System Configuration */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <h3 className="text-xl font-semibold text-slate-900 mb-6">System Configuration</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
              <div>
                <p className="font-medium text-slate-900 text-sm">Auto-backup</p>
                <p className="text-xs text-slate-500">Daily automated backups</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
              <div>
                <p className="font-medium text-slate-900 text-sm">Two-factor Authentication</p>
                <p className="text-xs text-slate-500">Required for all users</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
              <div>
                <p className="font-medium text-slate-900 text-sm">Email Notifications</p>
                <p className="text-xs text-slate-500">System alerts via email</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
              <div>
                <p className="font-medium text-slate-900 text-sm">Maintenance Mode</p>
                <p className="text-xs text-slate-500">Restrict access during updates</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" />
                <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
