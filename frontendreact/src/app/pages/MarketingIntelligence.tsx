import { Sparkles, Image as ImageIcon, Users, CheckCircle2, Globe, FileText } from 'lucide-react';
import { useState } from 'react';
const avaDoctorImage = new URL('../../assets/avaDoctor.png', import.meta.url).href;

const campaignTargets = ['Doctor', 'Pharmacist', 'Specialist', 'Hospital Administrator'];
const languages = ['English', 'French', 'Arabic'];

export function MarketingIntelligence() {
  const [selectedTarget, setSelectedTarget] = useState('Doctor');
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [generatedCaption, setGeneratedCaption] = useState('');

  const handleGenerate = () => {
    setGeneratedCaption(
      `🏥 Revolutionary breakthrough in cardiovascular care! Our latest innovation delivers 98.5% safety rate with proven clinical efficacy. Join 5,000+ healthcare professionals already using CardioX Pro. #MedicalExcellence #CardiovascularCare #Innovation`
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-[#2F748E] mb-2">Marketing Intelligence Mode</h1>
            <p className="text-[#20AA99] font-medium">AVA – Your AI Content Advisor</p>
          </div>
          <div className="px-4 py-2 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white">
            <Sparkles className="w-5 h-5 inline mr-2" />
            <span className="font-medium">AI-Powered</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left - Avatar Content Advisor */}
        <div className="lg:col-span-1 space-y-6">
          {/* Avatar */}
          <div className="bg-gradient-to-br from-[#2F748E] via-[#20AA99] to-[#8ABFA3] rounded-2xl p-1 shadow-lg">
            <div className="bg-white/80 backdrop-blur-xl rounded-xl p-6">
              <div className="text-center mb-4">
                <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center shadow-xl relative overflow-hidden ring-4 ring-white/20">
                  <div className="absolute inset-0 bg-[#20AA99]/20 blur-2xl animate-pulse"></div>
                  <img 
                    src={avaDoctorImage} 
                    alt="Dr. AVA" 
                    className="w-full h-full object-cover object-top"
                  />
                </div>
                <p className="text-[#2F748E] font-semibold mt-3">AVA Content Advisor</p>
                <p className="text-[#20AA99] text-xs">Marketing AI Expert</p>
              </div>

              <div className="relative bg-[#F4FBFF] rounded-lg p-4 border border-[#20AA99]/20">
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-transparent border-b-[#F4FBFF]"></div>
                <p className="text-sm text-[#2F748E]">
                  "I'll help you create compliant, engaging marketing content for your target audience."
                </p>
              </div>
            </div>
          </div>

          {/* Campaign Target Selection */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <Users className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Campaign Target</h3>
            </div>

            <div className="space-y-2">
              {campaignTargets.map((target) => (
                <button
                  key={target}
                  onClick={() => setSelectedTarget(target)}
                  className={`w-full p-3 rounded-lg text-left transition-all ${
                    selectedTarget === target
                      ? 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white shadow-lg'
                      : 'bg-[#F4FBFF] text-[#2F748E] hover:bg-white'
                  }`}
                >
                  <span className="font-medium">{target}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Language Selection */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <Globe className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Language</h3>
            </div>

            <div className="space-y-2">
              {languages.map((lang) => (
                <button
                  key={lang}
                  onClick={() => setSelectedLanguage(lang)}
                  className={`w-full p-3 rounded-lg text-left transition-all ${
                    selectedLanguage === lang
                      ? 'bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white shadow-lg'
                      : 'bg-[#F4FBFF] text-[#2F748E] hover:bg-white'
                  }`}
                >
                  <span className="font-medium">{lang}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Compliance Badge */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-3 p-4 rounded-lg bg-[#8ABFA3]/10 border border-[#8ABFA3]/30">
              <CheckCircle2 className="w-8 h-8 text-[#8ABFA3]" />
              <div>
                <p className="text-sm font-semibold text-[#2F748E]">Compliance Validated</p>
                <p className="text-xs text-[#2F748E]/70">All content meets regulatory standards</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right - Content Generation & Preview */}
        <div className="lg:col-span-2 space-y-6">
          {/* AI Caption Generator */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">AI-Generated Caption</h3>
            </div>

            {generatedCaption ? (
              <div className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 mb-4">
                <p className="text-[#2F748E] leading-relaxed">{generatedCaption}</p>
              </div>
            ) : (
              <div className="p-8 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 mb-4 text-center">
                <Sparkles className="w-12 h-12 mx-auto text-[#20AA99]/40 mb-3" />
                <p className="text-[#2F748E]/60">Click "Generate" to create compliant marketing content</p>
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={handleGenerate}
                className="flex-1 px-6 py-3 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-medium shadow-lg hover:shadow-xl transition-all"
              >
                <Sparkles className="w-4 h-4 inline mr-2" />
                Generate Caption
              </button>
              {generatedCaption && (
                <button className="px-6 py-3 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors">
                  Copy
                </button>
              )}
            </div>
          </div>

          {/* AI Visual Suggestions */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <ImageIcon className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">AI Visual Suggestions</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[1, 2, 3].map((i) => (
                <div
                  key={i}
                  className="aspect-square rounded-lg bg-gradient-to-br from-[#F4FBFF] to-white border border-[#20AA99]/10 flex items-center justify-center cursor-pointer hover:shadow-lg transition-all"
                >
                  <div className="text-center">
                    <ImageIcon className="w-12 h-12 mx-auto text-[#20AA99]/40 mb-2" />
                    <p className="text-xs text-[#2F748E]/60">Suggested Visual {i}</p>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full mt-4 px-6 py-3 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-[#2F748E] hover:bg-white transition-colors font-medium">
              <ImageIcon className="w-4 h-4 inline mr-2" />
              Generate Visuals
            </button>
          </div>

          {/* Campaign Preview */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Campaign Preview</h3>

            <div className="bg-gradient-to-br from-[#F4FBFF] to-white rounded-lg p-6 border border-[#20AA99]/10">
              <div className="aspect-video bg-white rounded-lg mb-4 flex items-center justify-center border border-[#20AA99]/10">
                <div className="text-center p-8">
                  <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center">
                    <ImageIcon className="w-8 h-8 text-white" />
                  </div>
                  <p className="text-[#2F748E]/60">Your campaign visual will appear here</p>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <p className="text-xs text-[#2F748E]/60 mb-1">Target Audience</p>
                  <p className="text-sm font-medium text-[#2F748E]">{selectedTarget}</p>
                </div>
                <div>
                  <p className="text-xs text-[#2F748E]/60 mb-1">Language</p>
                  <p className="text-sm font-medium text-[#2F748E]">{selectedLanguage}</p>
                </div>
                <div>
                  <p className="text-xs text-[#2F748E]/60 mb-1">Compliance Status</p>
                  <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-[#8ABFA3]/20 text-[#8ABFA3] text-xs font-medium">
                    <CheckCircle2 className="w-3 h-3" />
                    Approved
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-[#20AA99] to-[#2F748E] rounded-xl p-6 text-white shadow-lg">
              <p className="text-sm text-white/80 mb-2">Engagement Rate</p>
              <p className="text-3xl font-bold">85%</p>
              <p className="text-xs text-white/70 mt-2">↑ 15% from average</p>
            </div>

            <div className="bg-gradient-to-br from-[#2F748E] to-[#8ABFA3] rounded-xl p-6 text-white shadow-lg">
              <p className="text-sm text-white/80 mb-2">Reach</p>
              <p className="text-3xl font-bold">12.5K</p>
              <p className="text-xs text-white/70 mt-2">Target audience</p>
            </div>

            <div className="bg-gradient-to-br from-[#8ABFA3] to-[#20AA99] rounded-xl p-6 text-white shadow-lg">
              <p className="text-sm text-white/80 mb-2">Compliance</p>
              <p className="text-3xl font-bold">100%</p>
              <p className="text-xs text-white/70 mt-2">Fully validated</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
