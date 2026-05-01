import { User, Bell, Lock, Globe, Palette, Database, Mail } from 'lucide-react';

export function Settings() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <h1 className="text-2xl font-semibold text-slate-900 mb-2">Settings</h1>
        <p className="text-slate-600">Manage your account preferences and configurations</p>
      </div>

      {/* Settings Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Profile Settings */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <User className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900">Profile Settings</h3>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-600 mb-2">Full Name</label>
              <input
                type="text"
                defaultValue="Medical Manager"
                className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-2">Email Address</label>
              <input
                type="email"
                defaultValue="manager@ava-medical.com"
                className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-2">Role</label>
              <input
                type="text"
                defaultValue="Medical Manager"
                className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>
            <button className="w-full px-4 py-2 rounded-lg bg-gradient-to-r from-blue-600 to-teal-500 text-white font-medium shadow-lg hover:shadow-xl transition-all">
              Update Profile
            </button>
          </div>
        </div>

        {/* Notification Settings */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Bell className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900">Notifications</h3>
          </div>

          <div className="space-y-4">
            {[
              { label: 'Email Notifications', description: 'Receive updates via email' },
              { label: 'Training Reminders', description: 'Get notified about training sessions' },
              { label: 'Performance Alerts', description: 'Alerts for performance metrics' },
              { label: 'CRM Updates', description: 'Notifications for CRM changes' },
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                <div>
                  <p className="font-medium text-slate-900 text-sm">{item.label}</p>
                  <p className="text-xs text-slate-500">{item.description}</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" className="sr-only peer" defaultChecked />
                  <div className="w-11 h-6 bg-slate-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            ))}
          </div>
        </div>

        {/* Security Settings */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
              <Lock className="w-5 h-5 text-red-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900">Security</h3>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-600 mb-2">Current Password</label>
              <input
                type="password"
                placeholder="Enter current password"
                className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-2">New Password</label>
              <input
                type="password"
                placeholder="Enter new password"
                className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-2">Confirm Password</label>
              <input
                type="password"
                placeholder="Confirm new password"
                className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              />
            </div>
            <button className="w-full px-4 py-2 rounded-lg bg-red-600 text-white font-medium hover:bg-red-700 transition-colors">
              Change Password
            </button>
          </div>
        </div>

        {/* Language & Region */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
              <Globe className="w-5 h-5 text-teal-600" />
            </div>
            <h3 className="text-xl font-semibold text-slate-900">Language & Region</h3>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm text-slate-600 mb-2">Language</label>
              <select className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                <option>English</option>
                <option>French</option>
                <option>Arabic</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-2">Time Zone</label>
              <select className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                <option>UTC-5 (Eastern Time)</option>
                <option>UTC+0 (GMT)</option>
                <option>UTC+1 (Central European)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm text-slate-600 mb-2">Date Format</label>
              <select className="w-full px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                <option>MM/DD/YYYY</option>
                <option>DD/MM/YYYY</option>
                <option>YYYY-MM-DD</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Settings Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <Palette className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Theme</h3>
          <p className="text-blue-100 text-sm">Customize appearance</p>
        </div>

        <div className="bg-gradient-to-br from-teal-600 to-teal-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <Database className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Data & Privacy</h3>
          <p className="text-teal-100 text-sm">Manage your data</p>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <Mail className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Integrations</h3>
          <p className="text-purple-100 text-sm">Connect external tools</p>
        </div>
      </div>
    </div>
  );
}
