import { CheckCircle2, RefreshCw, Users, TrendingUp, Calendar, MessageSquare } from 'lucide-react';

const crmStatus = {
  connected: true,
  lastSync: '2 minutes ago',
  totalContacts: 1247,
  activeLeads: 89,
  syncRate: 98.5,
};

const recentContacts = [
  {
    name: 'Dr. Emily Richardson',
    specialty: 'Oncology',
    status: 'Hot Lead',
    lastContact: '2024-02-18',
    score: 95,
  },
  {
    name: 'Dr. James Anderson',
    specialty: 'Cardiology',
    status: 'Active',
    lastContact: '2024-02-17',
    score: 88,
  },
  {
    name: 'Dr. Maria Garcia',
    specialty: 'Neurology',
    status: 'Warm Lead',
    lastContact: '2024-02-15',
    score: 76,
  },
  {
    name: 'Dr. Robert Chen',
    specialty: 'Endocrinology',
    status: 'Active',
    lastContact: '2024-02-14',
    score: 82,
  },
  {
    name: 'Dr. Sarah Williams',
    specialty: 'Pediatrics',
    status: 'Hot Lead',
    lastContact: '2024-02-13',
    score: 91,
  },
];

const interactionHistory = [
  {
    contact: 'Dr. Emily Richardson',
    type: 'Product Demo',
    date: '2024-02-18',
    duration: '45 min',
    outcome: 'Positive',
  },
  {
    contact: 'Dr. James Anderson',
    type: 'Follow-up Call',
    date: '2024-02-17',
    duration: '20 min',
    outcome: 'Scheduled Meeting',
  },
  {
    contact: 'Dr. Maria Garcia',
    type: 'Email Campaign',
    date: '2024-02-15',
    duration: 'N/A',
    outcome: 'Opened',
  },
  {
    contact: 'Dr. Robert Chen',
    type: 'Training Session',
    date: '2024-02-14',
    duration: '60 min',
    outcome: 'Completed',
  },
];

export function CRMIntegration() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900 mb-2">CRM Integration</h1>
            <p className="text-slate-600">Seamlessly sync with your customer relationship management system</p>
          </div>
          <button className="px-6 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-teal-500 text-white font-medium shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Sync Now
          </button>
        </div>
      </div>

      {/* Connection Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            </div>
            <div>
              <p className="text-sm text-slate-600">Status</p>
              <p className="font-semibold text-slate-900">Connected</p>
            </div>
          </div>
          <p className="text-xs text-slate-500">Last sync: {crmStatus.lastSync}</p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-slate-600">Total Contacts</p>
              <p className="font-semibold text-slate-900 text-xl">{crmStatus.totalContacts}</p>
            </div>
          </div>
          <p className="text-xs text-emerald-600">↑ 45 new this month</p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-teal-600" />
            </div>
            <div>
              <p className="text-sm text-slate-600">Active Leads</p>
              <p className="font-semibold text-slate-900 text-xl">{crmStatus.activeLeads}</p>
            </div>
          </div>
          <p className="text-xs text-emerald-600">↑ 12% conversion rate</p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <RefreshCw className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-slate-600">Sync Rate</p>
              <p className="font-semibold text-slate-900 text-xl">{crmStatus.syncRate}%</p>
            </div>
          </div>
          <p className="text-xs text-slate-500">Real-time updates</p>
        </div>
      </div>

      {/* Synced Contacts & Interaction History */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Synced Contacts */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-slate-900">Synced Contacts</h3>
            <button className="text-sm text-blue-600 hover:text-blue-700">View All</button>
          </div>

          <div className="space-y-3">
            {recentContacts.map((contact, index) => (
              <div
                key={index}
                className="p-4 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
              >
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <p className="font-medium text-slate-900">{contact.name}</p>
                    <p className="text-xs text-slate-500">{contact.specialty}</p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      contact.status === 'Hot Lead'
                        ? 'bg-red-100 text-red-700'
                        : contact.status === 'Warm Lead'
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-emerald-100 text-emerald-700'
                    }`}
                  >
                    {contact.status}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs text-slate-500">
                  <div className="flex items-center gap-4">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {contact.lastContact}
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="font-medium text-slate-900">{contact.score}</span>
                    <span>Score</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Interaction History */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-slate-900">Interaction History</h3>
            <button className="text-sm text-blue-600 hover:text-blue-700">View All</button>
          </div>

          <div className="space-y-4">
            {interactionHistory.map((interaction, index) => (
              <div key={index} className="flex gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center flex-shrink-0">
                  <MessageSquare className="w-5 h-5 text-white" />
                </div>
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-1">
                    <div>
                      <p className="font-medium text-slate-900">{interaction.contact}</p>
                      <p className="text-xs text-slate-500">{interaction.type}</p>
                    </div>
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        interaction.outcome === 'Positive' || interaction.outcome === 'Completed'
                          ? 'bg-emerald-100 text-emerald-700'
                          : 'bg-blue-100 text-blue-700'
                      }`}
                    >
                      {interaction.outcome}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-500">
                    <span>{interaction.date}</span>
                    <span>•</span>
                    <span>{interaction.duration}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Lead Scoring Panel */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <h3 className="text-xl font-semibold text-slate-900 mb-6">Lead Scoring Overview</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Hot Leads */}
          <div className="p-6 rounded-xl bg-gradient-to-br from-red-50 to-orange-50 border border-red-200/50">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-red-900">Hot Leads</h4>
              <span className="px-3 py-1 rounded-full bg-red-500 text-white text-sm font-bold">
                23
              </span>
            </div>
            <p className="text-sm text-red-700 mb-3">Score: 90-100</p>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-red-700">Ready to convert</span>
                <span className="font-medium text-red-900">78%</span>
              </div>
              <div className="w-full h-2 bg-red-200 rounded-full overflow-hidden">
                <div className="h-full bg-red-500 rounded-full" style={{ width: '78%' }}></div>
              </div>
            </div>
          </div>

          {/* Warm Leads */}
          <div className="p-6 rounded-xl bg-gradient-to-br from-amber-50 to-yellow-50 border border-amber-200/50">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-amber-900">Warm Leads</h4>
              <span className="px-3 py-1 rounded-full bg-amber-500 text-white text-sm font-bold">
                42
              </span>
            </div>
            <p className="text-sm text-amber-700 mb-3">Score: 70-89</p>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-amber-700">Nurturing required</span>
                <span className="font-medium text-amber-900">62%</span>
              </div>
              <div className="w-full h-2 bg-amber-200 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: '62%' }}></div>
              </div>
            </div>
          </div>

          {/* Cold Leads */}
          <div className="p-6 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50 border border-blue-200/50">
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-semibold text-blue-900">Cold Leads</h4>
              <span className="px-3 py-1 rounded-full bg-blue-500 text-white text-sm font-bold">
                24
              </span>
            </div>
            <p className="text-sm text-blue-700 mb-3">Score: Below 70</p>
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-blue-700">Initial contact</span>
                <span className="font-medium text-blue-900">35%</span>
              </div>
              <div className="w-full h-2 bg-blue-200 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: '35%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CRM Integration Settings */}
      <div className="bg-gradient-to-br from-blue-600 to-teal-500 rounded-2xl p-8 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold mb-2">Salesforce Connected</h3>
            <p className="text-blue-100 mb-4">
              Your AVA platform is synchronized with Salesforce CRM
            </p>
            <div className="flex items-center gap-4 text-sm">
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Auto-sync enabled
              </span>
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Real-time updates
              </span>
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                Secure connection
              </span>
            </div>
          </div>
          <button className="px-6 py-3 rounded-lg bg-white text-blue-600 font-medium hover:bg-blue-50 transition-colors">
            Configure Settings
          </button>
        </div>
      </div>
    </div>
  );
}
