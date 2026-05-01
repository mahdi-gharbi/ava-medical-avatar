import { TrendingUp, Target, MessageSquare, CheckCircle2, Activity, Sparkles, FileText } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const performanceData = [
  { name: 'Jan', performance: 75, target: 80 },
  { name: 'Feb', performance: 78, target: 80 },
  { name: 'Mar', performance: 82, target: 80 },
  { name: 'Apr', performance: 85, target: 85 },
  { name: 'May', performance: 88, target: 85 },
  { name: 'Jun', performance: 92, target: 85 },
];

const teamComparison = [
  { name: 'Sarah J.', score: 94 },
  { name: 'Michael C.', score: 88 },
  { name: 'Emma W.', score: 92 },
  { name: 'David M.', score: 85 },
  { name: 'Lisa K.', score: 90 },
];

const skillAnalysis = [
  { skill: 'Product Knowledge', score: 95 },
  { skill: 'Communication', score: 88 },
  { skill: 'Objection Handling', score: 92 },
  { skill: 'Compliance', score: 98 },
  { skill: 'Data Presentation', score: 85 },
];

const kpiCards = [
  {
    title: 'Training Sessions Completed',
    value: '127',
    change: '+12%',
    icon: Target,
    color: 'from-[#20AA99] to-[#2F748E]',
  },
  {
    title: 'Average Performance Score',
    value: '88.5%',
    change: '+5.2%',
    icon: TrendingUp,
    color: 'from-[#2F748E] to-[#8ABFA3]',
  },
  {
    title: 'Objection Handling Accuracy',
    value: '92%',
    change: '+8%',
    icon: MessageSquare,
    color: 'from-[#8ABFA3] to-[#20AA99]',
  },
  {
    title: 'Compliance Rate',
    value: '98.7%',
    change: '+2.1%',
    icon: CheckCircle2,
    color: 'from-[#20AA99] to-[#2F748E]',
  },
  {
    title: 'Marketing Campaign Engagement',
    value: '85%',
    change: '+15%',
    icon: Sparkles,
    color: 'from-[#2F748E] to-[#8ABFA3]',
  },
  {
    title: 'Visit Reports Generated',
    value: '342',
    change: '+24%',
    icon: FileText,
    color: 'from-[#8ABFA3] to-[#20AA99]',
  },
];

const recentActivity = [
  { user: 'Sarah Johnson', action: 'Completed Advanced Training Module', time: '2 hours ago' },
  { user: 'Michael Chen', action: 'Generated Marketing Campaign', time: '4 hours ago' },
  { user: 'Emma Williams', action: 'Submitted Visit Report with AI', time: '5 hours ago' },
  { user: 'David Martinez', action: 'Commercial Presentation Completed', time: '6 hours ago' },
];

export function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-semibold text-[#2F748E] mb-2">
              Welcome back, Medical Manager 👋
            </h1>
            <p className="text-[#2F748E]/70">
              Here's your AI-powered pharmaceutical performance overview
            </p>
          </div>
          <div className="px-6 py-3 rounded-xl bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-medium shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
            Start AI Training
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {kpiCards.map((kpi, index) => {
          const Icon = kpi.icon;
          return (
            <div
              key={index}
              className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
            >
              <div className="flex items-start justify-between mb-4">
                <div
                  className={`w-12 h-12 rounded-xl bg-gradient-to-br ${kpi.color} flex items-center justify-center shadow-lg`}
                >
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <span className="text-[#20AA99] text-sm font-medium bg-[#20AA99]/10 px-3 py-1 rounded-lg">
                  {kpi.change}
                </span>
              </div>
              <h3 className="text-[#2F748E]/70 text-sm mb-2">{kpi.title}</h3>
              <p className="text-3xl font-bold text-[#2F748E]">{kpi.value}</p>
              <div className="mt-4 pt-4 border-t border-[#20AA99]/10">
                <ResponsiveContainer width="100%" height={40}>
                  <AreaChart data={performanceData}>
                    <defs>
                      <linearGradient id={`gradient-${index}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#20AA99" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#20AA99" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <Area
                      type="monotone"
                      dataKey="performance"
                      stroke="#20AA99"
                      strokeWidth={2}
                      fill={`url(#gradient-${index})`}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Over Time */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-semibold text-[#2F748E]">Performance Over Time</h3>
              <p className="text-[#2F748E]/60 text-sm">Monthly performance trends</p>
            </div>
            <Activity className="w-5 h-5 text-[#20AA99]" />
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={performanceData}>
              <defs>
                <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#20AA99" />
                  <stop offset="100%" stopColor="#2F748E" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#20AA99" opacity={0.1} />
              <XAxis dataKey="name" stroke="#2F748E" />
              <YAxis stroke="#2F748E" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(32, 170, 153, 0.2)',
                  borderRadius: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="performance"
                stroke="url(#lineGradient)"
                strokeWidth={3}
                dot={{ fill: '#20AA99', r: 6 }}
                activeDot={{ r: 8 }}
                name="Performance"
              />
              <Line
                type="monotone"
                dataKey="target"
                stroke="#8ABFA3"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ fill: '#8ABFA3', r: 4 }}
                name="Target"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Team Comparison */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-semibold text-[#2F748E]">Team Comparison</h3>
              <p className="text-[#2F748E]/60 text-sm">Individual performance scores</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={teamComparison}>
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#20AA99" />
                  <stop offset="100%" stopColor="#2F748E" />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#20AA99" opacity={0.1} />
              <XAxis dataKey="name" stroke="#2F748E" />
              <YAxis stroke="#2F748E" domain={[0, 100]} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(32, 170, 153, 0.2)',
                  borderRadius: '12px',
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
      </div>

      {/* Skill Analysis & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Skill Analysis Radar */}
        <div className="lg:col-span-2 bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-[#2F748E]">Skill Analysis</h3>
            <p className="text-[#2F748E]/60 text-sm">Competency breakdown</p>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={skillAnalysis}>
              <PolarGrid stroke="#20AA99" opacity={0.2} />
              <PolarAngleAxis dataKey="skill" stroke="#2F748E" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="#2F748E" />
              <Radar
                name="Skills"
                dataKey="score"
                stroke="#20AA99"
                fill="#20AA99"
                fillOpacity={0.3}
                strokeWidth={2}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(32, 170, 153, 0.2)',
                  borderRadius: '12px',
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Recent Activity */}
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
          <h3 className="text-xl font-semibold text-[#2F748E] mb-6">Recent Activity</h3>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex gap-3">
                <div className="w-2 h-2 rounded-full bg-gradient-to-r from-[#20AA99] to-[#2F748E] mt-2"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-[#2F748E]">{activity.user}</p>
                  <p className="text-xs text-[#2F748E]/70">{activity.action}</p>
                  <p className="text-xs text-[#20AA99] mt-1">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-[#20AA99] to-[#2F748E] rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer">
          <h3 className="text-lg font-semibold mb-2">AI Training</h3>
          <p className="text-white/80 text-sm">Start simulation</p>
        </div>
        <div className="bg-gradient-to-br from-[#2F748E] to-[#8ABFA3] rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer">
          <h3 className="text-lg font-semibold mb-2">Marketing AI</h3>
          <p className="text-white/80 text-sm">Generate campaign</p>
        </div>
        <div className="bg-gradient-to-br from-[#8ABFA3] to-[#20AA99] rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer">
          <h3 className="text-lg font-semibold mb-2">Visit Report</h3>
          <p className="text-white/80 text-sm">AI-powered insights</p>
        </div>
        <div className="bg-gradient-to-br from-[#20AA99] to-[#2F748E] rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer">
          <h3 className="text-lg font-semibold mb-2">View Analytics</h3>
          <p className="text-white/80 text-sm">Deep dive metrics</p>
        </div>
      </div>
    </div>
  );
}
