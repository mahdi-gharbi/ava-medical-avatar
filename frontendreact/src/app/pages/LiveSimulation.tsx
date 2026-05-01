import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { useNavigate } from 'react-router';
import { 
  Mic, 
  MicOff, 
  MessageSquare, 
  X, 
  Activity, 
  ShieldCheck, 
  Zap, 
  Brain,
  ChevronRight,
  User,
  Bot
} from 'lucide-react';
                const avaDoctorImage = new URL('../../assets/avaDoctor.pn g', import.meta.url).href;
const DOCTOR_VIDEO_PLACEHOLDER = avaDoctorImage;

// Mock conversation data
const INITIAL_MESSAGES = [
  { id: 1, sender: 'doctor', text: "Hello. I've reviewed the clinical data for CardioVas, but I'm still concerned about the side effect profile in elderly patients." },
  { id: 2, sender: 'rep', text: "I understand your concern, Dr. Smith. The Phase 3 trials specifically addressed this demographic. Would you like to see the safety subgroup analysis?" },
  { id: 3, sender: 'doctor', text: "Yes, show me the data. Specifically for patients over 75 with renal impairment." },
];

export function LiveSimulation() {
  const navigate = useNavigate();
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [isRecording, setIsRecording] = useState(false);
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    
    const newMessage = { id: Date.now(), sender: 'rep', text: inputText };
    setMessages([...messages, newMessage]);
    setInputText('');
    
    // Simulate doctor response
    setTimeout(() => {
      const response = { id: Date.now() + 1, sender: 'doctor', text: "That's a valid point. However, cost is another factor my patients struggle with." };
      setMessages(prev => [...prev, response]);
    }, 1500);
  };

  return (
    <div className="h-screen bg-slate-50 flex flex-col overflow-hidden">
      {/* Top Floating KPI Bar */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-4xl px-4">
        <motion.div 
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="bg-white/90 backdrop-blur-md border border-slate-200 rounded-2xl shadow-xl p-3 flex items-center justify-between gap-4"
        >
          <div className="flex items-center gap-6 px-4">
            <KPIIndicator label="Scientific Accuracy" value={92} color="text-teal-600" />
            <div className="w-px h-8 bg-slate-200" />
            <KPIIndicator label="Sales Argumentation" value={78} color="text-blue-600" />
            <div className="w-px h-8 bg-slate-200" />
            <div className="flex flex-col items-center">
              <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Compliance</span>
              <div className="flex items-center gap-1.5 mt-1">
                <ShieldCheck size={16} className="text-emerald-600" />
                <span className="text-sm font-bold text-emerald-600">Safe</span>
              </div>
            </div>
            <div className="w-px h-8 bg-slate-200" />
            <KPIIndicator label="Engagement" value={85} color="text-purple-600" />
          </div>

          <div className="flex items-center gap-3 pr-2">
            <button 
              onClick={() => navigate('/performance-report')}
              className="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 border border-red-200 rounded-lg text-sm font-medium transition-colors"
            >
              End Session
            </button>
          </div>
        </motion.div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 h-full">
        {/* LEFT SIDE - Doctor Video Interface */}
        <div className="lg:col-span-8 relative bg-slate-900 flex flex-col justify-center items-center overflow-hidden">
          {/* Background Gradient */}
          <div className="absolute inset-0 bg-gradient-to-br from-[#2F748E] via-[#1a4c5e] to-[#0f2e3a]" />
          
          {/* Main Video Container */}
          <div className="relative w-full h-full max-h-[85vh] aspect-video max-w-6xl mx-auto p-8 flex items-center justify-center">
            <div className="relative w-full h-full rounded-2xl overflow-hidden shadow-2xl border border-white/10 ring-1 ring-white/20 group">
              {/* Subtle animated glow frame */}
              <div className="absolute inset-0 z-20 pointer-events-none rounded-2xl ring-1 ring-[#20AA99]/30 animate-pulse" />
              
              {/* Depth blur background effect for image container */}
              <div className="absolute inset-0 bg-black/20 backdrop-blur-[2px] z-10" />

              <img 
                src={DOCTOR_VIDEO_PLACEHOLDER} 
                alt="Doctor Simulation" 
                className="relative z-0 w-full h-full object-cover object-top opacity-95 transform scale-105"
              />
              
              {/* Overlay UI Elements */}
              <div className="absolute top-6 left-6 z-30 flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 bg-red-500/80 backdrop-blur-md text-white rounded-full shadow-lg">
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                  <span className="text-xs font-bold tracking-wider">LIVE</span>
                </div>
                <div className="px-3 py-1.5 bg-black/40 backdrop-blur-md border border-white/10 rounded-full">
                  <span className="text-xs text-white font-medium">Dr. AVA • Cardiologist</span>
                </div>
              </div>

              {/* Waveform Animation (Bottom) */}
              <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black/80 via-black/40 to-transparent flex items-end justify-center pb-8 gap-1 z-30">
                {[...Array(20)].map((_, i) => (
                  <motion.div
                    key={i}
                    animate={{
                      height: [10, Math.random() * 40 + 10, 10],
                      opacity: [0.3, 0.8, 0.3]
                    }}
                    transition={{
                      duration: 0.8,
                      repeat: Infinity,
                      delay: i * 0.05,
                      ease: "easeInOut"
                    }}
                    className="w-1.5 bg-[#20AA99] rounded-full shadow-[0_0_10px_#20AA99]"
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT SIDE - Conversation Panel */}
        <div className="lg:col-span-4 bg-[#F4FBFF] border-l border-slate-200 flex flex-col h-full relative z-10">
          <div className="p-4 border-b border-slate-200 bg-white/80 backdrop-blur shadow-sm">
            <h3 className="font-semibold text-slate-800 flex items-center gap-2">
              <MessageSquare size={18} className="text-[#20AA99]" />
              Conversation Log
            </h3>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
            {messages.map((msg) => (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={msg.id} 
                className={`flex ${msg.sender === 'rep' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] rounded-2xl p-4 shadow-sm ${
                  msg.sender === 'rep' 
                    ? 'bg-[#20AA99] text-white rounded-br-none' 
                    : 'bg-white text-slate-800 rounded-bl-none border border-slate-100'
                }`}>
                  <div className="flex items-center gap-2 mb-1 opacity-80 text-xs">
                    {msg.sender === 'rep' ? <User size={12} /> : <Bot size={12} />}
                    <span className="font-medium">{msg.sender === 'rep' ? 'You' : 'Dr. AVA'}</span>
                  </div>
                  <p className="text-sm leading-relaxed">{msg.text}</p>
                </div>
              </motion.div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 bg-white border-t border-slate-200">
            {/* AI Insight Box */}
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-4 p-3 bg-blue-50 border border-blue-100 rounded-lg flex items-start gap-3"
            >
              <Zap size={16} className="text-[#2F748E] mt-0.5 shrink-0" />
              <div>
                <span className="text-xs font-semibold text-[#2F748E] block mb-0.5">AI Suggestion</span>
                <p className="text-xs text-slate-600">Mention the renal safety profile data from Phase 3 studies to address her concern.</p>
              </div>
            </motion.div>

            <form onSubmit={handleSendMessage} className="relative">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your response..."
                className="w-full bg-slate-50 border border-slate-200 text-slate-800 rounded-xl pl-4 pr-24 py-3.5 focus:ring-2 focus:ring-[#20AA99]/20 focus:border-[#20AA99] outline-none transition-all placeholder:text-slate-400"
              />
              <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
                <button
                  type="button"
                  onClick={() => setIsRecording(!isRecording)}
                  className={`p-2 rounded-lg transition-colors ${
                    isRecording ? 'bg-red-100 text-red-600' : 'hover:bg-slate-200 text-slate-400'
                  }`}
                >
                  {isRecording ? <MicOff size={18} /> : <Mic size={18} />}
                </button>
                <button
                  type="submit"
                  disabled={!inputText.trim()}
                  className="p-2 bg-[#20AA99] text-white rounded-lg hover:bg-[#1b8f80] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <ChevronRight size={18} />
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

function KPIIndicator({ label, value, color }: { label: string, value: number, color: string }) {
  // Calculate stroke dashoffset for circle
  const radius = 18;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-1">
      <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">{label}</span>
      <div className="relative w-12 h-12 flex items-center justify-center">
        {/* Background Circle */}
        <svg className="transform -rotate-90 w-full h-full">
          <circle
            cx="24"
            cy="24"
            r={radius}
            stroke="currentColor"
            strokeWidth="3"
            fill="transparent"
            className="text-slate-200"
          />
          {/* Progress Circle */}
          <circle
            cx="24"
            cy="24"
            r={radius}
            stroke="currentColor"
            strokeWidth="3"
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className={`${color} transition-all duration-1000 ease-out`}
          />
        </svg>
        <span className={`absolute text-xs font-bold ${color}`}>{value}%</span>
      </div>
    </div>
  );
}
