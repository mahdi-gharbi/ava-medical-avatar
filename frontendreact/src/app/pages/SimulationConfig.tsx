import React, { useState } from 'react';
import { motion } from 'motion/react';
import { useNavigate } from 'react-router';
import { 
  Heart, 
  Brain, 
  Activity, 
  Zap, 
  Shield, 
  User, 
  Play, 
  CheckCircle2,
  Stethoscope,
  Microscope,
  Dna,
  Syringe,
  Pill,
  BriefcaseMedical,
  AlertCircle,
  Clock,
  Settings2
} from 'lucide-react';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';
const avaDoctorImage = new URL('../../assets/avaDoctor.png', import.meta.url).href;

// Doctor Avatar URL - Using the new AVA image
const DOCTOR_AVATAR = avaDoctorImage;

export function SimulationConfig() {
  const navigate = useNavigate();
  const [config, setConfig] = useState({
    specialty: 'Cardiology',
    profile: 'Analytical',
    difficulty: 'Intermediate',
    productName: 'CardioVas 500mg',
    regulatoryFocus: true
  });

  const specialties = [
    { id: 'Cardiology', icon: Heart, color: 'text-red-500' },
    { id: 'Oncology', icon: Microscope, color: 'text-purple-500' },
    { id: 'Immunology', icon: Shield, color: 'text-blue-500' },
    { id: 'Diabetes', icon: Activity, color: 'text-orange-500' },
    { id: 'Neurology', icon: Brain, color: 'text-pink-500' },
  ];

  const profiles = [
    { id: 'Skeptical', icon: AlertCircle, desc: 'Requires strong evidence' },
    { id: 'Analytical', icon: Activity, desc: 'Focuses on data & stats' },
    { id: 'Friendly', icon: User, desc: 'Open to discussion' },
    { id: 'Busy', icon: Clock, desc: 'Short, concise interaction' },
    { id: 'Specialist', icon: BriefcaseMedical, desc: 'Deep technical questions' },
  ];

  const difficulties = ['Beginner', 'Intermediate', 'Advanced'];

  return (
    <div className="min-h-screen bg-background p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-medium text-foreground">Simulation Configuration</h1>
        <p className="text-muted-foreground mt-2">Configure your AI simulation parameters before starting the session.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* LEFT SIDE - Configuration Panel */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-7 xl:col-span-8"
        >
          <div className="bg-card/50 backdrop-blur-xl border border-white/20 shadow-lg rounded-2xl p-8 h-full">
            <div className="space-y-8">
              
              {/* Medical Specialty */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-3">Medical Specialty</label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {specialties.map((spec) => (
                    <button
                      key={spec.id}
                      onClick={() => setConfig({ ...config, specialty: spec.id })}
                      className={`flex items-center gap-3 p-3 rounded-xl border transition-all duration-200 ${
                        config.specialty === spec.id
                          ? 'bg-primary/10 border-primary text-primary shadow-sm'
                          : 'bg-white/50 border-transparent hover:border-border hover:bg-white'
                      }`}
                    >
                      <spec.icon size={20} className={config.specialty === spec.id ? 'text-primary' : spec.color} />
                      <span className="font-medium">{spec.id}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Doctor Profile */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-3">Doctor Profile</label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {profiles.map((profile) => (
                    <button
                      key={profile.id}
                      onClick={() => setConfig({ ...config, profile: profile.id })}
                      className={`flex items-start gap-3 p-4 rounded-xl border text-left transition-all duration-200 ${
                        config.profile === profile.id
                          ? 'bg-primary/10 border-primary shadow-sm'
                          : 'bg-white/50 border-transparent hover:border-border hover:bg-white'
                      }`}
                    >
                      <div className={`mt-0.5 p-1.5 rounded-lg ${config.profile === profile.id ? 'bg-primary text-white' : 'bg-muted text-muted-foreground'}`}>
                        <profile.icon size={16} />
                      </div>
                      <div>
                        <div className={`font-medium ${config.profile === profile.id ? 'text-primary' : 'text-foreground'}`}>
                          {profile.id}
                        </div>
                        <div className="text-xs text-muted-foreground mt-0.5">{profile.desc}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Difficulty Level */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-3">Difficulty Level</label>
                <div className="flex bg-muted/50 p-1 rounded-xl">
                  {difficulties.map((level) => (
                    <button
                      key={level}
                      onClick={() => setConfig({ ...config, difficulty: level })}
                      className={`flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200 ${
                        config.difficulty === level
                          ? 'bg-white text-primary shadow-sm'
                          : 'text-muted-foreground hover:text-foreground'
                      }`}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>

              {/* Product & Regulatory */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-3">Product Name</label>
                  <div className="relative">
                    <Pill className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
                    <input
                      type="text"
                      value={config.productName}
                      onChange={(e) => setConfig({ ...config, productName: e.target.value })}
                      className="w-full pl-10 pr-4 py-3 bg-white/50 border border-transparent hover:border-border focus:border-primary focus:ring-1 focus:ring-primary rounded-xl outline-none transition-all"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between bg-white/50 p-4 rounded-xl border border-transparent">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-accent/10 rounded-lg text-accent">
                      <Shield size={18} />
                    </div>
                    <div>
                      <div className="font-medium text-foreground">Regulatory Focus</div>
                      <div className="text-xs text-muted-foreground">Strict compliance mode</div>
                    </div>
                  </div>
                  <button
                    onClick={() => setConfig({ ...config, regulatoryFocus: !config.regulatoryFocus })}
                    className={`w-12 h-6 rounded-full p-1 transition-colors duration-200 ${
                      config.regulatoryFocus ? 'bg-primary' : 'bg-muted'
                    }`}
                  >
                    <div className={`w-4 h-4 rounded-full bg-white shadow-sm transition-transform duration-200 ${
                      config.regulatoryFocus ? 'translate-x-6' : 'translate-x-0'
                    }`} />
                  </button>
                </div>
              </div>

              {/* Action Button */}
              <div className="pt-4">
                <button
                  onClick={() => navigate('/live-simulation')}
                  className="w-full py-4 px-6 bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-white rounded-xl font-medium shadow-lg hover:shadow-xl hover:shadow-primary/20 transition-all duration-300 flex items-center justify-center gap-2 group"
                >
                  <Play size={20} className="fill-current group-hover:scale-110 transition-transform" />
                  Start Simulation
                </button>
              </div>

            </div>
          </div>
        </motion.div>

        {/* RIGHT SIDE - Preview Card */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:col-span-5 xl:col-span-4"
        >
          <div className="sticky top-8">
            <div className="relative bg-card rounded-2xl overflow-hidden shadow-2xl border border-primary/20 group hover:shadow-primary/30 transition-all duration-500">
              {/* Soft Teal Glow around frame */}
              <div className="absolute inset-0 rounded-2xl ring-1 ring-[#20AA99]/30 z-40 pointer-events-none" />
              
              {/* Glowing Border Effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-transparent to-accent/20 opacity-50 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
              
              {/* Avatar Image - Enhanced Size & Crop */}
              <div className="relative h-[400px] w-full bg-gradient-to-b from-sky-50 to-white overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-white/40 via-transparent to-transparent z-10" />
                <img 
                  src={DOCTOR_AVATAR} 
                  alt="AI Doctor Avatar" 
                  className="w-full h-full object-cover object-top transform group-hover:scale-105 transition-transform duration-700 contrast-105"
                />
                
                {/* Subtle glass overlay at bottom for Simulation Preview text */}
                <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black/60 to-transparent z-20 backdrop-blur-[2px]" />
                
                {/* Live Badge */}
                <div className="absolute top-4 left-4 z-30 bg-white/90 backdrop-blur-md px-3 py-1.5 rounded-full flex items-center gap-2 shadow-sm border border-white/50">
                  <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-xs font-semibold text-foreground tracking-wide">AVA ENGINE READY</span>
                </div>
              </div>

              {/* Preview Content */}
              <div className="relative z-30 px-6 pb-8 -mt-16 space-y-6">
                <div className="bg-white/90 backdrop-blur-xl border border-white/50 rounded-xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-bold text-foreground">Simulation Preview</h3>
                    <Settings2 size={18} className="text-muted-foreground" />
                  </div>

                  <p className="text-sm text-muted-foreground leading-relaxed mb-6">
                    You will be interacting with a <span className="text-primary font-medium">{config.profile.toLowerCase()}</span> doctor specializing in <span className="text-primary font-medium">{config.specialty}</span>. 
                    The session will focus on <span className="text-primary font-medium">{config.productName}</span> with <span className="text-primary font-medium">{config.difficulty.toLowerCase()}</span> objection handling.
                  </p>

                  <div className="flex flex-wrap gap-2">
                    <div className="px-3 py-1 bg-primary/10 text-primary text-xs font-medium rounded-full border border-primary/20">
                      {config.specialty}
                    </div>
                    <div className="px-3 py-1 bg-accent/10 text-accent text-xs font-medium rounded-full border border-accent/20">
                      {config.profile} Mode
                    </div>
                    <div className="px-3 py-1 bg-secondary/20 text-secondary-foreground text-xs font-medium rounded-full border border-secondary/30">
                      {config.difficulty}
                    </div>
                    {config.regulatoryFocus && (
                      <div className="px-3 py-1 bg-orange-50 text-orange-600 text-xs font-medium rounded-full border border-orange-200">
                        Regulatory+
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-4 text-xs text-muted-foreground px-2">
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 size={14} className="text-green-500" />
                    <span>AI Model Loaded</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 size={14} className="text-green-500" />
                    <span>Voice Synth Ready</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
