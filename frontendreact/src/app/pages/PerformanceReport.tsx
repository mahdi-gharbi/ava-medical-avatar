import React from 'react';
import { 
  Radar, 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  ResponsiveContainer 
} from 'recharts';
import { motion } from 'motion/react';
import { 
  Trophy, 
  Target, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Download, 
  Share2,
  FileText,
  BarChart2,
  Brain,
  MessageSquare
} from 'lucide-react';
import { Link } from 'react-router';

// Mock Data for Radar Chart
const radarData = [
  { subject: 'Scientific Knowledge', A: 95, fullMark: 100 },
  { subject: 'Compliance', A: 98, fullMark: 100 },
  { subject: 'Objection Handling', A: 72, fullMark: 100 },
  { subject: 'Communication Clarity', A: 85, fullMark: 100 },
  { subject: 'Persuasion Skills', A: 68, fullMark: 100 },
];

const kpiBreakdown = [
  { id: 1, metric: 'Clinical Data Accuracy', score: 95, status: 'Excellent', comment: 'Perfect recall of Phase 3 primary endpoints.' },
  { id: 2, metric: 'Regulatory Compliance', score: 100, status: 'Perfect', comment: 'Zero off-label claims detected.' },
  { id: 3, metric: 'Empathy & Tone', score: 82, status: 'Good', comment: 'Good active listening, could improve closing speed.' },
  { id: 4, metric: 'Objection Handling', score: 72, status: 'Average', comment: 'Struggled with cost-effectiveness counter-argument.' },
];

export function PerformanceReport() {
  return (
    <div className="min-h-screen bg-background p-8 pb-20">
      <header className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-medium text-foreground flex items-center gap-3">
            <Trophy className="text-yellow-500" />
            Performance Report
          </h1>
          <p className="text-muted-foreground mt-2">Detailed analysis of your recent simulation session.</p>
        </div>
        <div className="flex gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-border bg-white text-foreground rounded-lg hover:bg-muted transition-colors">
            <Download size={18} />
            Export PDF
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20">
            <Share2 size={18} />
            Share Report
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* LEFT COLUMN - Score & Radar */}
        <div className="lg:col-span-4 space-y-8">
          {/* Overall Score Card */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-card rounded-2xl shadow-sm border border-border p-8 flex flex-col items-center justify-center text-center relative overflow-hidden"
          >
            <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-primary to-accent" />
            <h3 className="text-lg font-medium text-muted-foreground mb-6 uppercase tracking-wider">Overall Performance Score</h3>
            
            <div className="relative w-48 h-48 flex items-center justify-center mb-6">
              {/* Custom SVG Circular Progress */}
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="96"
                  cy="96"
                  r="88"
                  stroke="currentColor"
                  strokeWidth="12"
                  fill="transparent"
                  className="text-muted/30"
                />
                <circle
                  cx="96"
                  cy="96"
                  r="88"
                  stroke="currentColor"
                  strokeWidth="12"
                  fill="transparent"
                  strokeDasharray={2 * Math.PI * 88}
                  strokeDashoffset={2 * Math.PI * 88 * (1 - 0.88)}
                  strokeLinecap="round"
                  className="text-primary transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-5xl font-bold text-foreground">88%</span>
                <span className="text-sm font-medium text-primary bg-primary/10 px-2 py-0.5 rounded-full mt-1">Excellent</span>
              </div>
            </div>
            
            <p className="text-sm text-muted-foreground max-w-xs mx-auto">
              You performed better than <span className="font-semibold text-foreground">92%</span> of peers in this scenario.
            </p>
          </motion.div>

          {/* Radar Chart Card */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-card rounded-2xl shadow-sm border border-border p-6 h-[400px]"
          >
            <h3 className="text-lg font-medium text-foreground mb-4 flex items-center gap-2">
              <Target size={20} className="text-accent" />
              Skill Breakdown
            </h3>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar
                  name="My Performance"
                  dataKey="A"
                  stroke="#20AA99"
                  strokeWidth={3}
                  fill="#20AA99"
                  fillOpacity={0.2}
                />
              </RadarChart>
            </ResponsiveContainer>
          </motion.div>
        </div>

        {/* RIGHT COLUMN - Insights & Details */}
        <div className="lg:col-span-8 space-y-8">
          
          {/* Strengths & Weaknesses Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Strengths */}
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-green-50/50 border border-green-100 rounded-2xl p-6"
            >
              <h3 className="text-lg font-semibold text-green-800 mb-4 flex items-center gap-2">
                <TrendingUp size={20} />
                Key Strengths
              </h3>
              <ul className="space-y-3">
                {[
                  "Exceptional knowledge of clinical trial protocols",
                  "Perfect regulatory compliance adherence",
                  "Strong opening statement & engagement"
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <div className="mt-1 p-1 bg-green-200 text-green-700 rounded-full">
                      <CheckCircle size={14} />
                    </div>
                    <span className="text-green-900/80 text-sm font-medium">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>

            {/* Improvements */}
            <motion.div 
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-orange-50/50 border border-orange-100 rounded-2xl p-6"
            >
              <h3 className="text-lg font-semibold text-orange-800 mb-4 flex items-center gap-2">
                <AlertTriangle size={20} />
                Areas for Improvement
              </h3>
              <ul className="space-y-3">
                {[
                  "Handling price/cost objections effectively",
                  "Closing the call with a clear next step",
                  "Asking more open-ended discovery questions"
                ].map((item, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <div className="mt-1 p-1 bg-orange-200 text-orange-700 rounded-full">
                      <TrendingUp size={14} className="rotate-180" />
                    </div>
                    <span className="text-orange-900/80 text-sm font-medium">{item}</span>
                  </li>
                ))}
              </ul>
            </motion.div>
          </div>

          {/* Detailed KPI Table */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-card rounded-2xl shadow-sm border border-border overflow-hidden"
          >
            <div className="p-6 border-b border-border bg-muted/20 flex justify-between items-center">
              <h3 className="text-lg font-medium text-foreground flex items-center gap-2">
                <BarChart2 size={20} className="text-primary" />
                Detailed KPI Breakdown
              </h3>
              <span className="text-xs text-muted-foreground font-medium uppercase tracking-wider">Session ID: #SIM-2024-88A</span>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-muted/30 border-b border-border text-xs uppercase text-muted-foreground tracking-wider font-semibold">
                    <th className="p-4 pl-6">Metric Category</th>
                    <th className="p-4 text-center">Score</th>
                    <th className="p-4">Status</th>
                    <th className="p-4 pr-6">AI Insight</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {kpiBreakdown.map((row) => (
                    <tr key={row.id} className="hover:bg-muted/10 transition-colors">
                      <td className="p-4 pl-6 font-medium text-foreground">{row.metric}</td>
                      <td className="p-4 text-center">
                        <div className="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-muted/50 font-bold text-foreground">
                          {row.score}
                        </div>
                      </td>
                      <td className="p-4">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                          row.status === 'Excellent' || row.status === 'Perfect' ? 'bg-green-100 text-green-800 border-green-200' :
                          row.status === 'Good' ? 'bg-blue-100 text-blue-800 border-blue-200' :
                          'bg-yellow-100 text-yellow-800 border-yellow-200'
                        }`}>
                          {row.status}
                        </span>
                      </td>
                      <td className="p-4 pr-6 text-sm text-muted-foreground max-w-md">
                        <div className="flex items-start gap-2">
                          <MessageSquare size={14} className="mt-1 text-primary shrink-0" />
                          {row.comment}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>

          <div className="flex justify-end gap-4">
            <Link to="/live-simulation" className="text-muted-foreground hover:text-foreground text-sm font-medium py-2 px-4 transition-colors">
              Retry Simulation
            </Link>
            <Link to="/" className="bg-primary text-primary-foreground hover:bg-primary/90 text-sm font-medium py-2 px-6 rounded-lg shadow-lg shadow-primary/20 transition-all flex items-center gap-2">
              Back to Dashboard
              <CheckCircle size={16} />
            </Link>
          </div>

        </div>
      </div>
    </div>
  );
}
