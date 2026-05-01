import { User, MapPin, Languages, FileText, Sparkles, Download, MessageCircle } from 'lucide-react';
import { useState } from 'react';
const avaDoctorImage = new URL("../../assets/avaDoctor.png", import.meta.url).href;
const doctorProfile = {
  name: 'Dr. Sarah Martinez',
  specialty: 'Cardiology',
  region: 'North America',
  language: 'English',
  experience: '15 years',
  preferences: 'Data-driven, Clinical studies focused',
};

const slides = [
  { id: 1, title: 'Product Overview', status: 'completed' },
  { id: 2, title: 'Clinical Efficacy', status: 'completed' },
  { id: 3, title: 'Safety Profile', status: 'current' },
  { id: 4, title: 'Dosing & Administration', status: 'pending' },
  { id: 5, title: 'Cost-Effectiveness', status: 'pending' },
];

const avaRecommendations = [
  'Emphasize the 98.5% safety rate from recent clinical trials',
  'Mention the 24-month follow-up study results',
  'Reference Dr. Martinez\'s previous interest in cardiovascular data',
];

export function CommercialMode() {
  const [selectedLanguage, setSelectedLanguage] = useState('English');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-[#2F748E] mb-2">Commercial Interaction Mode</h1>
            <p className="text-[#20AA99] font-medium">AVA – Your AI Medical Sales Assistant</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors flex items-center gap-2">
              <Download className="w-4 h-4" />
              Export
            </button>
            <button className="px-6 py-3 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-medium shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Generate Presentation
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left - Avatar Assistant */}
        <div className="lg:col-span-1 space-y-6">
          {/* Small 3D Avatar Guiding */}
          <div className="bg-gradient-to-br from-[#2F748E] via-[#20AA99] to-[#8ABFA3] rounded-2xl p-1 shadow-lg">
            <div className="bg-white/80 backdrop-blur-xl rounded-xl p-6">
              <div className="text-center mb-4">
                <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center shadow-xl relative overflow-hidden ring-4 ring-white/20">
                  {/* Glow effect */}
                  <div className="absolute inset-0 bg-[#20AA99]/20 blur-2xl animate-pulse"></div>
                  
                  <img 
                    src={avaDoctorImage} 
                    alt="Dr. AVA" 
                    className="w-full h-full object-cover object-top"
                  />
                </div>
                <p className="text-[#2F748E] font-semibold mt-3">AVA Assistant</p>
                <p className="text-[#20AA99] text-xs">Here to guide you</p>
              </div>

              {/* Speech Bubble */}
              <div className="relative bg-[#F4FBFF] rounded-lg p-4 border border-[#20AA99]/20">
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-transparent border-b-[#F4FBFF]"></div>
                <p className="text-sm text-[#2F748E]">
                  "I recommend focusing on the clinical efficacy data that Dr. Martinez values most."
                </p>
              </div>
            </div>
          </div>

          {/* AVA Recommendations Panel */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <MessageCircle className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">AVA Recommendations</h3>
            </div>

            <div className="space-y-3">
              {avaRecommendations.map((rec, index) => (
                <div
                  key={index}
                  className="flex gap-3 p-3 rounded-lg bg-[#20AA99]/10 border border-[#20AA99]/20"
                >
                  <div className="w-6 h-6 rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center flex-shrink-0">
                    <span className="text-white text-xs font-bold">{index + 1}</span>
                  </div>
                  <p className="text-sm text-[#2F748E]">{rec}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Doctor Profile Card */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-[#2F748E]">{doctorProfile.name}</h3>
                <p className="text-sm text-[#20AA99]">{doctorProfile.specialty}</p>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex items-center gap-3 p-3 rounded-lg bg-[#F4FBFF]">
                <MapPin className="w-4 h-4 text-[#20AA99]" />
                <div>
                  <p className="text-xs text-[#2F748E]/60">Region</p>
                  <p className="text-sm text-[#2F748E]">{doctorProfile.region}</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 rounded-lg bg-[#F4FBFF]">
                <Languages className="w-4 h-4 text-[#20AA99]" />
                <div>
                  <p className="text-xs text-[#2F748E]/60">Language</p>
                  <p className="text-sm text-[#2F748E]">{doctorProfile.language}</p>
                </div>
              </div>

              <div className="flex items-center gap-3 p-3 rounded-lg bg-[#F4FBFF]">
                <FileText className="w-4 h-4 text-[#20AA99]" />
                <div>
                  <p className="text-xs text-[#2F748E]/60">Experience</p>
                  <p className="text-sm text-[#2F748E]">{doctorProfile.experience}</p>
                </div>
              </div>
            </div>

            <div className="mt-4 p-4 rounded-lg bg-gradient-to-br from-[#20AA99]/10 to-[#8ABFA3]/10 border border-[#20AA99]/20">
              <p className="text-xs font-medium text-[#2F748E] mb-2">Key Preferences</p>
              <p className="text-xs text-[#2F748E]/70">{doctorProfile.preferences}</p>
            </div>
          </div>

          {/* Language Toggle */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Language Settings</h3>
            <div className="space-y-2">
              {['English', 'French', 'Arabic'].map((lang) => (
                <button
                  key={lang}
                  onClick={() => setSelectedLanguage(lang)}
                  className={`w-full p-3 rounded-lg text-left transition-all ${
                    selectedLanguage === lang
                      ? 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white shadow-lg'
                      : 'bg-[#F4FBFF] text-[#2F748E] hover:bg-white'
                  }`}
                >
                  {lang}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right - Presentation Preview & Product Recommendations */}
        <div className="lg:col-span-2 space-y-6">
          {/* Adaptive Presentation Preview */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Adaptive Presentation</h3>
            <div className="aspect-video bg-gradient-to-br from-[#F4FBFF] to-white rounded-xl flex items-center justify-center mb-6 relative overflow-hidden border border-[#20AA99]/10">
              <div className="absolute inset-0 bg-gradient-to-br from-[#20AA99]/10 to-[#2F748E]/10"></div>
              <div className="relative z-10 text-center p-8">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center">
                  <FileText className="w-10 h-10 text-white" />
                </div>
                <h4 className="text-xl font-semibold text-[#2F748E] mb-2">Safety Profile</h4>
                <p className="text-[#2F748E]/70 mb-4">Comprehensive safety data from clinical trials</p>
                <div className="flex items-center justify-center gap-8 text-sm">
                  <div>
                    <p className="text-2xl font-bold text-[#20AA99]">98.5%</p>
                    <p className="text-[#2F748E]/70">Safety Rate</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-[#2F748E]">5,000+</p>
                    <p className="text-[#2F748E]/70">Patients</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-[#8ABFA3]">24mo</p>
                    <p className="text-[#2F748E]/70">Follow-up</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Slide Navigation */}
            <div className="flex gap-2 overflow-x-auto pb-2">
              {slides.map((slide) => (
                <div
                  key={slide.id}
                  className={`flex-shrink-0 px-4 py-3 rounded-lg border transition-all cursor-pointer ${
                    slide.status === 'current'
                      ? 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white border-transparent shadow-lg'
                      : slide.status === 'completed'
                      ? 'bg-[#8ABFA3]/20 border-[#8ABFA3]/30 text-[#2F748E]'
                      : 'bg-[#F4FBFF] border-[#20AA99]/20 text-[#2F748E]/60'
                  }`}
                >
                  <p className="text-xs font-medium whitespace-nowrap">
                    {slide.id}. {slide.title}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Product Recommendation Engine */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-[#2F748E]">Product Recommendations</h3>
              <span className="px-3 py-1 rounded-full bg-[#20AA99]/10 text-[#20AA99] text-xs font-medium">
                AI-Powered
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 rounded-lg bg-gradient-to-br from-[#20AA99]/10 to-[#2F748E]/10 border border-[#20AA99]/20">
                <p className="text-sm font-medium text-[#2F748E] mb-2">Recommended Product</p>
                <p className="text-lg font-bold text-[#20AA99]">CardioX Pro</p>
                <p className="text-xs text-[#2F748E]/70 mt-1">Best match for profile</p>
              </div>

              <div className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/10">
                <p className="text-sm font-medium text-[#2F748E] mb-2">Match Score</p>
                <p className="text-lg font-bold text-[#2F748E]">95%</p>
                <p className="text-xs text-[#2F748E]/70 mt-1">Highly relevant</p>
              </div>

              <div className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/10">
                <p className="text-sm font-medium text-[#2F748E] mb-2">Success Rate</p>
                <p className="text-lg font-bold text-[#8ABFA3]">87%</p>
                <p className="text-xs text-[#2F748E]/70 mt-1">Similar profiles</p>
              </div>
            </div>
          </div>

          {/* Automatic CRM Logging */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-[#2F748E]">Automatic CRM Logging</h3>
              <span className="px-3 py-1 rounded-full bg-[#8ABFA3]/20 text-[#8ABFA3] text-xs font-medium">
                Active
              </span>
            </div>

            <div className="space-y-3">
              {[
                { action: 'Profile loaded', time: 'Just now' },
                { action: 'Previous interactions analyzed', time: '2 sec ago' },
                { action: 'Preferences identified', time: '3 sec ago' },
                { action: 'Content personalized', time: '5 sec ago' },
              ].map((activity, index) => (
                <div key={index} className="flex items-center gap-3 p-3 rounded-lg bg-[#F4FBFF]">
                  <div className="w-2 h-2 rounded-full bg-[#8ABFA3]"></div>
                  <div className="flex-1">
                    <p className="text-sm text-[#2F748E]">{activity.action}</p>
                  </div>
                  <p className="text-xs text-[#20AA99]">{activity.time}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
