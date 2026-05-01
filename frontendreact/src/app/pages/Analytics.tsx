import {
  LineChart,
  Line,
  BarChart,
  Bar,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Download, FileText, TrendingUp } from 'lucide-react';

const performanceOverTime = [
  { month: 'Jan', performance: 75, target: 80 },
  { month: 'Feb', performance: 78, target: 80 },
  { month: 'Mar', performance: 82, target: 80 },
  { month: 'Apr', performance: 85, target: 85 },
  { month: 'May', performance: 88, target: 85 },
  { month: 'Jun', performance: 92, target: 85 },
  { month: 'Jul', performance: 90, target: 90 },
  { month: 'Aug', performance: 94, target: 90 },
];

const teamComparison = [
  { name: 'Sarah J.', score: 94 },
  { name: 'Michael C.', score: 88 },
  { name: 'Emma W.', score: 92 },
  { name: 'David M.', score: 85 },
  { name: 'Lisa K.', score: 90 },
  { name: 'James R.', score: 87 },
];

const skillAnalysis = [
  { skill: 'Product Knowledge', score: 95 },
  { skill: 'Communication', score: 88 },
  { skill: 'Objection Handling', score: 92 },
  { skill: 'Compliance', score: 98 },
  { skill: 'Data Presentation', score: 85 },
  { skill: 'Relationship Building', score: 90 },
];

export function Analytics() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-[#2F748E] mb-2">Performance Analytics</h1>
            <p className="text-[#2F748E]/70">Comprehensive insights into training effectiveness</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Export PDF
            </button>
            <button className="px-4 py-2 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-medium shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
              <Download className="w-4 h-4" />
              Download Report
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-[#2F748E]/70">Overall Score</p>
            <TrendingUp className="w-4 h-4 text-[#8ABFA3]" />
          </div>
          <p className="text-3xl font-bold text-[#2F748E] mb-1">88.5%</p>
          <p className="text-xs text-[#20AA99]">↑ 5.2% from last month</p>
        </div>

        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-[#2F748E]/70">Training Hours</p>
            <TrendingUp className="w-4 h-4 text-[#8ABFA3]" />
          </div>
          <p className="text-3xl font-bold text-[#2F748E] mb-1">342</p>
          <p className="text-xs text-[#20AA99]">↑ 12% from last month</p>
        </div>

        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-[#2F748E]/70">Active Users</p>
            <TrendingUp className="w-4 h-4 text-[#8ABFA3]" />
          </div>
          <p className="text-3xl font-bold text-[#2F748E] mb-1">24</p>
          <p className="text-xs text-[#20AA99]">↑ 3 new this month</p>
        </div>

        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-[#2F748E]/70">Completion Rate</p>
            <TrendingUp className="w-4 h-4 text-[#8ABFA3]" />
          </div>
          <p className="text-3xl font-bold text-[#2F748E] mb-1">96%</p>
          <p className="text-xs text-[#20AA99]">↑ 2% from last month</p>
        </div>
      </div>

      {/* Performance Over Time Chart */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-semibold text-slate-900">Performance Over Time</h3>
            <p className="text-sm text-slate-600">Monthly performance trends vs. targets</p>
          </div>
          <select className="px-4 py-2 rounded-lg border border-slate-200/50 bg-white text-sm text-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/50">
            <option>Last 8 Months</option>
            <option>Last 6 Months</option>
            <option>Last 3 Months</option>
          </select>
        </div>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={performanceOverTime}>
            <defs>
              <linearGradient id="performanceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis dataKey="month" stroke="#64748b" />
            <YAxis stroke="#64748b" domain={[70, 100]} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                backdropFilter: 'blur(10px)',
                border: '1px solid #e2e8f0',
                borderRadius: '12px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="performance"
              stroke="#0ea5e9"
              strokeWidth={3}
              dot={{ fill: '#0ea5e9', r: 6 }}
              activeDot={{ r: 8 }}
              name="Actual Performance"
            />
            <Line
              type="monotone"
              dataKey="target"
              stroke="#14b8a6"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ fill: '#14b8a6', r: 4 }}
              name="Target"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Team Comparison and Skill Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Team Comparison Bar Chart */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-slate-900">Team Comparison</h3>
            <p className="text-sm text-slate-600">Individual performance scores</p>
          </div>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={teamComparison}>
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#0ea5e9" />
                  <stop offset="100%" stopColor="#14b8a6" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" stroke="#64748b" />
              <YAxis stroke="#64748b" domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid #e2e8f0',
                  borderRadius: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                }}
              />
              <Bar
                dataKey="score"
                fill="url(#barGradient)"
                radius={[8, 8, 0, 0]}
                maxBarSize={50}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Skill Analysis Radar Chart */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl p-6 border border-slate-200/50 shadow-lg">
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-slate-900">Skill Analysis</h3>
            <p className="text-sm text-slate-600">Competency breakdown</p>
          </div>
          <ResponsiveContainer width="100%" height={350}>
            <RadarChart data={skillAnalysis}>
              <PolarGrid stroke="#e2e8f0" />
              <PolarAngleAxis dataKey="skill" stroke="#64748b" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#64748b" />
              <Radar
                name="Skills"
                dataKey="score"
                stroke="#0ea5e9"
                fill="#0ea5e9"
                fillOpacity={0.3}
                strokeWidth={2}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid #e2e8f0',
                  borderRadius: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-emerald-600 to-emerald-500 rounded-2xl p-6 text-white shadow-lg">
          <h4 className="text-lg font-semibold mb-2">Top Performer</h4>
          <p className="text-3xl font-bold mb-1">Sarah J.</p>
          <p className="text-sm text-emerald-100">94% average score</p>
        </div>

        <div className="bg-gradient-to-br from-blue-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg">
          <h4 className="text-lg font-semibold mb-2">Strongest Skill</h4>
          <p className="text-3xl font-bold mb-1">Compliance</p>
          <p className="text-sm text-blue-100">98% team average</p>
        </div>

        <div className="bg-gradient-to-br from-purple-600 to-purple-500 rounded-2xl p-6 text-white shadow-lg">
          <h4 className="text-lg font-semibold mb-2">Focus Area</h4>
          <p className="text-3xl font-bold mb-1">Data Presentation</p>
          <p className="text-sm text-purple-100">85% - room for growth</p>
        </div>
      </div>
    </div>
  );
}