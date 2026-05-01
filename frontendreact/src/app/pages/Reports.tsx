import { FileText, Download, Calendar, TrendingUp, BarChart3 } from 'lucide-react';

const reports = [
  {
    title: 'Monthly Performance Report',
    date: 'February 2026',
    type: 'Performance',
    status: 'Ready',
    size: '2.4 MB',
  },
  {
    title: 'Training Effectiveness Analysis',
    date: 'Q1 2026',
    type: 'Analysis',
    status: 'Ready',
    size: '3.1 MB',
  },
  {
    title: 'Team Compliance Report',
    date: 'January 2026',
    type: 'Compliance',
    status: 'Ready',
    size: '1.8 MB',
  },
  {
    title: 'CRM Activity Summary',
    date: 'February 2026',
    type: 'CRM',
    status: 'Ready',
    size: '2.2 MB',
  },
];

export function Reports() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900 mb-2">Reports</h1>
            <p className="text-slate-600">Generate and download comprehensive reports</p>
          </div>
          <button className="px-6 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-teal-500 text-white font-medium shadow-lg hover:shadow-xl transition-all">
            Generate New Report
          </button>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <p className="text-sm text-slate-600">Total Reports</p>
          </div>
          <p className="text-3xl font-bold text-slate-900">127</p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-teal-600" />
            </div>
            <p className="text-sm text-slate-600">This Month</p>
          </div>
          <p className="text-3xl font-bold text-slate-900">24</p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
              <Download className="w-5 h-5 text-purple-600" />
            </div>
            <p className="text-sm text-slate-600">Downloads</p>
          </div>
          <p className="text-3xl font-bold text-slate-900">342</p>
        </div>

        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
            </div>
            <p className="text-sm text-slate-600">Scheduled</p>
          </div>
          <p className="text-3xl font-bold text-slate-900">8</p>
        </div>
      </div>

      {/* Reports List */}
      <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
        <h3 className="text-xl font-semibold text-slate-900 mb-6">Available Reports</h3>

        <div className="space-y-4">
          {reports.map((report, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 rounded-lg bg-slate-50 hover:bg-slate-100 transition-colors"
            >
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-600 to-teal-500 flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h4 className="font-medium text-slate-900">{report.title}</h4>
                  <div className="flex items-center gap-3 text-sm text-slate-500 mt-1">
                    <span>{report.date}</span>
                    <span>•</span>
                    <span>{report.type}</span>
                    <span>•</span>
                    <span>{report.size}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-sm font-medium">
                  {report.status}
                </span>
                <button className="p-2 rounded-lg hover:bg-slate-200 transition-colors">
                  <Download className="w-5 h-5 text-slate-600" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Report Templates */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <FileText className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Performance Report</h3>
          <p className="text-blue-100 text-sm">Detailed analysis of training performance</p>
        </div>

        <div className="bg-gradient-to-br from-teal-600 to-teal-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <FileText className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Compliance Report</h3>
          <p className="text-teal-100 text-sm">Regulatory compliance tracking</p>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-500 rounded-2xl p-6 text-white shadow-lg cursor-pointer hover:shadow-xl transition-all">
          <FileText className="w-8 h-8 mb-3" />
          <h3 className="text-lg font-semibold mb-2">Custom Report</h3>
          <p className="text-purple-100 text-sm">Create your own custom report</p>
        </div>
      </div>
    </div>
  );
}
