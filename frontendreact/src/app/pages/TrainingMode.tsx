import { Mic, MicOff, Pause, Play, RotateCcw, Radio, Clock } from 'lucide-react';
import { useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
// @ts-expect-error CSS is resolved by the bundler at runtime
import 'react-circular-progressbar/dist/styles.css';
const avaDoctorImage = new URL('../../assets/avaDoctor.png', import.meta.url).href;

const kpiMetrics = [
  { label: 'Confidence', value: 88, color: '#20AA99' },
  { label: 'Accuracy', value: 92, color: '#2F748E' },
  { label: 'Empathy', value: 85, color: '#8ABFA3' },
];

const coachingSuggestions = [
  {
    type: 'positive',
    message: 'Excellent product knowledge demonstration',
    time: '00:45',
  },
  {
    type: 'improvement',
    message: 'Consider addressing the pricing objection earlier',
    time: '01:20',
  },
  {
    type: 'positive',
    message: 'Great empathy shown in response',
    time: '02:15',
  },
];

export function TrainingMode() {
  const [isRecording, setIsRecording] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [sessionTime, setSessionTime] = useState('05:42');
  const globalScore = 88;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-[#2F748E] mb-2">Training & Simulation Mode</h1>
            <p className="text-[#2F748E]/70">AVA – Your AI Training Coach</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#20AA99]/10 border border-[#20AA99]/20">
              <Clock className="w-4 h-4 text-[#20AA99]" />
              <span className="text-[#2F748E] font-medium">{sessionTime}</span>
            </div>
            <button className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors">
              <RotateCcw className="w-4 h-4 inline mr-2" />
              Reset
            </button>
          </div>
        </div>
      </div>

      {/* Main Training Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left - Large Immersive Avatar */}
        <div className="lg:col-span-2 space-y-6">
          {/* 3D Avatar Display */}
          <div className="bg-gradient-to-br from-[#2F748E] via-[#20AA99] to-[#8ABFA3] rounded-2xl p-1 shadow-2xl">
            <div className="bg-[#1a2942] rounded-xl overflow-hidden relative" style={{ height: '500px' }}>
              {/* LIVE CONNECTION Badge */}
              <div className="absolute top-4 left-4 z-10 flex items-center gap-2 px-4 py-2 rounded-lg bg-[#20AA99]/90 backdrop-blur-sm">
                <Radio className="w-4 h-4 text-white animate-pulse" />
                <span className="text-white text-sm font-medium">LIVE CONNECTION</span>
              </div>

              {/* Global Score */}
              <div className="absolute top-4 right-4 z-10 px-4 py-2 rounded-lg bg-white/90 backdrop-blur-sm">
                <p className="text-xs text-[#2F748E]/70">Global Score</p>
                <p className="text-2xl font-bold text-[#20AA99]">{globalScore}%</p>
              </div>

              {/* Avatar Container */}
              <div className="absolute inset-0 flex items-center justify-center">
                {/* Animated background glow */}
                <div className="absolute inset-0 bg-gradient-to-br from-[#20AA99]/20 via-[#2F748E]/20 to-[#8ABFA3]/20 animate-pulse"></div>
                
                {/* 3D Avatar Representation */}
                <div className="relative z-10">
                  <div className="relative">
                    {/* Avatar circle with glow */}
                    <div className="w-64 h-64 rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center shadow-2xl relative overflow-hidden ring-4 ring-white/20">
                      {/* Glow effect */}
                      <div className="absolute inset-0 bg-[#20AA99]/30 blur-3xl animate-pulse"></div>
                      
                      {/* Avatar Image */}
                      <img 
                        src={avaDoctorImage} 
                        alt="Dr. AVA" 
                        className="w-full h-full object-cover object-top"
                      />
                    </div>

                    {/* Listening waveform */}
                    {isRecording && (
                      <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 flex gap-1">
                        {[...Array(7)].map((_, i) => (
                          <div
                            key={i}
                            className="w-2 bg-[#20AA99] rounded-full animate-pulse"
                            style={{
                              height: `${20 + Math.random() * 30}px`,
                              animationDelay: `${i * 0.1}s`,
                            }}
                          ></div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Voice Input Indicator */}
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4">
                <button
                  onClick={() => setIsMuted(!isMuted)}
                  className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-lg hover:bg-white/30 flex items-center justify-center transition-colors border border-white/30"
                >
                  {isMuted ? (
                    <MicOff className="w-5 h-5 text-white" />
                  ) : (
                    <Mic className="w-5 h-5 text-white" />
                  )}
                </button>

                <button
                  onClick={() => setIsRecording(!isRecording)}
                  className={`w-20 h-20 rounded-full flex items-center justify-center transition-all shadow-2xl ${
                    isRecording
                      ? 'bg-red-500 hover:bg-red-600'
                      : 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] hover:shadow-[#20AA99]/50'
                  }`}
                >
                  {isRecording ? (
                    <Pause className="w-8 h-8 text-white" />
                  ) : (
                    <Play className="w-8 h-8 text-white ml-1" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Live Conversation */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Live Conversation</h3>
            <div className="space-y-4 h-48 overflow-y-auto">
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex-shrink-0"></div>
                <div className="flex-1 bg-[#F4FBFF] rounded-lg p-3 border border-[#20AA99]/10">
                  <p className="text-sm text-[#2F748E]">
                    Hello! I'm Dr. AVA, your AI training coach. Let's practice your medical presentation.
                  </p>
                </div>
              </div>

              <div className="flex gap-3 justify-end">
                <div className="flex-1 bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white rounded-lg p-3 max-w-md">
                  <p className="text-sm">
                    Our product is a breakthrough treatment with proven clinical efficacy...
                  </p>
                </div>
                <div className="w-8 h-8 rounded-full bg-[#8ABFA3] flex-shrink-0"></div>
              </div>
            </div>
          </div>
        </div>

        {/* Right - Performance Metrics */}
        <div className="space-y-6">
          {/* Performance Score Gauge */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-6 text-center">
              Performance Score
            </h3>
            <div className="w-48 h-48 mx-auto">
              <CircularProgressbar
                value={globalScore}
                text={`${globalScore}%`}
                styles={buildStyles({
                  textColor: '#2F748E',
                  pathColor: '#20AA99',
                  trailColor: '#e2f2f8',
                  textSize: '20px',
                })}
              />
            </div>
            <p className="text-center text-[#20AA99] mt-4 font-medium">
              Excellent performance!
            </p>
          </div>

          {/* KPI Rings */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Key Metrics</h3>
            <div className="space-y-4">
              {kpiMetrics.map((metric, index) => (
                <div key={index}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-[#2F748E]/70">{metric.label}</span>
                    <span className="text-sm font-semibold text-[#2F748E]">{metric.value}%</span>
                  </div>
                  <div className="w-full h-3 bg-[#F4FBFF] rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${metric.value}%`,
                        backgroundColor: metric.color,
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Real-time Coaching */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Real-time Coaching</h3>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {coachingSuggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg border ${
                    suggestion.type === 'positive'
                      ? 'bg-[#8ABFA3]/10 border-[#8ABFA3]/30'
                      : 'bg-[#2F748E]/10 border-[#2F748E]/30'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <div
                      className={`w-2 h-2 rounded-full mt-1.5 ${
                        suggestion.type === 'positive' ? 'bg-[#8ABFA3]' : 'bg-[#2F748E]'
                      }`}
                    ></div>
                    <div className="flex-1">
                      <p className="text-sm text-[#2F748E]">{suggestion.message}</p>
                      <p className="text-xs text-[#20AA99] mt-1">{suggestion.time}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Action Button */}
      <div className="flex justify-center">
        <button className="px-8 py-4 rounded-xl bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
          Start New Simulation
        </button>
      </div>
    </div>
  );
}
