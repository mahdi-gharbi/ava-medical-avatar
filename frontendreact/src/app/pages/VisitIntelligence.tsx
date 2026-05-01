import { FileText, Download, Upload, CheckCircle2, AlertCircle, Clock, TrendingUp, MessageSquare } from 'lucide-react';
import { useState } from 'react';
const avaDoctorImage = new URL('../../assets/avaDoctor.png', import.meta.url).href;


const visitTimeline = [
  { time: '00:00', event: 'Visit started', type: 'info' },
  { time: '02:30', event: 'Product presentation begun', type: 'info' },
  { time: '05:15', event: 'Doctor raised pricing concerns', type: 'important' },
  { time: '08:45', event: 'Clinical data discussed', type: 'info' },
  { time: '12:20', event: 'Doctor showed high interest', type: 'positive' },
  { time: '15:00', event: 'Visit concluded', type: 'info' },
];

const keyInsights = [
  'Doctor expressed strong interest in cardiovascular efficacy data',
  'Pricing concerns addressed with cost-effectiveness analysis',
  'Follow-up meeting scheduled for next month',
  'Doctor requested additional clinical study materials',
];

const objections = [
  { objection: 'Product pricing compared to competitors', handled: 'Yes', quality: 'Good' },
  { objection: 'Long-term safety data availability', handled: 'Yes', quality: 'Excellent' },
  { objection: 'Patient compliance concerns', handled: 'Partially', quality: 'Fair' },
];

export function VisitIntelligence() {
  const [hasRecording, setHasRecording] = useState(false);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-[#2F748E] mb-2">Visit Intelligence Mode</h1>
            <p className="text-[#20AA99] font-medium">AVA – Your AI Summarizer & Reporting Assistant</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors flex items-center gap-2">
              <Download className="w-4 h-4" />
              Export PDF
            </button>
            <button className="px-6 py-3 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-medium shadow-lg hover:shadow-xl transition-all flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              Sync to CRM
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left - Avatar Summarizer */}
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
                <p className="text-[#2F748E] font-semibold mt-3">AVA Summarizer</p>
                <p className="text-[#20AA99] text-xs">Report Intelligence</p>
              </div>

              <div className="relative bg-[#F4FBFF] rounded-lg p-4 border border-[#20AA99]/20">
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-transparent border-b-[#F4FBFF]"></div>
                <p className="text-sm text-[#2F748E]">
                  "I'll analyze your visit and generate a comprehensive report with key insights."
                </p>
              </div>
            </div>
          </div>

          {/* Upload Recording */}
          {!hasRecording ? (
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
              <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Upload Visit Recording</h3>
              
              <div className="border-2 border-dashed border-[#20AA99]/30 rounded-lg p-8 text-center hover:bg-[#F4FBFF] transition-colors cursor-pointer">
                <Upload className="w-12 h-12 mx-auto text-[#20AA99] mb-3" />
                <p className="text-[#2F748E] font-medium mb-2">Drop your recording here</p>
                <p className="text-sm text-[#2F748E]/60 mb-4">or click to browse</p>
                <button
                  onClick={() => setHasRecording(true)}
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white text-sm"
                >
                  Select File
                </button>
              </div>

              <p className="text-xs text-[#2F748E]/60 mt-3 text-center">
                Supports: MP3, WAV, M4A (Max 100MB)
              </p>
            </div>
          ) : (
            <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
              <div className="flex items-center gap-3 p-4 rounded-lg bg-[#8ABFA3]/10 border border-[#8ABFA3]/30">
                <CheckCircle2 className="w-8 h-8 text-[#8ABFA3]" />
                <div>
                  <p className="text-sm font-semibold text-[#2F748E]">Recording Uploaded</p>
                  <p className="text-xs text-[#2F748E]/70">visit_recording_021.mp3</p>
                </div>
              </div>
            </div>
          )}

          {/* Performance Tagging */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Performance Tags</h3>
            
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1 rounded-full bg-[#8ABFA3]/20 text-[#8ABFA3] text-xs font-medium">
                High Interest
              </span>
              <span className="px-3 py-1 rounded-full bg-[#20AA99]/20 text-[#20AA99] text-xs font-medium">
                Follow-up Needed
              </span>
              <span className="px-3 py-1 rounded-full bg-[#2F748E]/20 text-[#2F748E] text-xs font-medium">
                Data Requested
              </span>
              <span className="px-3 py-1 rounded-full bg-[#8ABFA3]/20 text-[#8ABFA3] text-xs font-medium">
                Positive Outcome
              </span>
            </div>
          </div>

          {/* Visit Stats */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <h3 className="text-lg font-semibold text-[#2F748E] mb-4">Visit Statistics</h3>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Duration</span>
                <span className="text-sm font-semibold text-[#2F748E]">15:00</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Engagement</span>
                <span className="text-sm font-semibold text-[#20AA99]">High</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Objections</span>
                <span className="text-sm font-semibold text-[#2F748E]">3</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Success Score</span>
                <span className="text-sm font-semibold text-[#8ABFA3]">88%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right - Report & Insights */}
        <div className="lg:col-span-2 space-y-6">
          {/* Visit Timeline */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Visit Timeline</h3>
            </div>

            <div className="space-y-3">
              {visitTimeline.map((item, index) => (
                <div key={index} className="flex gap-4">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-3 h-3 rounded-full ${
                        item.type === 'important'
                          ? 'bg-[#20AA99]'
                          : item.type === 'positive'
                          ? 'bg-[#8ABFA3]'
                          : 'bg-[#2F748E]/40'
                      }`}
                    ></div>
                    {index < visitTimeline.length - 1 && (
                      <div className="w-0.5 h-full bg-[#20AA99]/20 mt-1"></div>
                    )}
                  </div>
                  <div className="flex-1 pb-4">
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-sm font-medium text-[#2F748E]">{item.event}</p>
                      <span className="text-xs text-[#20AA99]">{item.time}</span>
                    </div>
                    {item.type === 'important' && (
                      <div className="flex items-center gap-1 text-xs text-[#20AA99]">
                        <AlertCircle className="w-3 h-3" />
                        <span>Important moment</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI-Generated Report */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">AI-Generated Visit Report</h3>
            </div>

            <div className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 space-y-3">
              <div>
                <p className="text-xs font-semibold text-[#2F748E]/60 mb-1">VISIT SUMMARY</p>
                <p className="text-sm text-[#2F748E] leading-relaxed">
                  Successful 15-minute consultation with Dr. Sarah Martinez (Cardiology). Discussed CardioX Pro with focus on clinical efficacy and safety profile. Doctor showed high engagement and requested additional materials.
                </p>
              </div>

              <div>
                <p className="text-xs font-semibold text-[#2F748E]/60 mb-1">DOCTOR PROFILE</p>
                <p className="text-sm text-[#2F748E]">
                  Dr. Sarah Martinez, Cardiology | 15 years experience | North America
                </p>
              </div>

              <div>
                <p className="text-xs font-semibold text-[#2F748E]/60 mb-1">PRODUCTS DISCUSSED</p>
                <p className="text-sm text-[#2F748E]">
                  CardioX Pro - Cardiovascular treatment | Dosage: 20mg daily
                </p>
              </div>
            </div>
          </div>

          {/* Key Insights */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Key Insights</h3>
            </div>

            <div className="space-y-2">
              {keyInsights.map((insight, index) => (
                <div key={index} className="flex gap-3 p-3 rounded-lg bg-[#F4FBFF]">
                  <CheckCircle2 className="w-5 h-5 text-[#8ABFA3] flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-[#2F748E]">{insight}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Objection Summary */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <MessageSquare className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Objection Summary</h3>
            </div>

            <div className="space-y-3">
              {objections.map((obj, index) => (
                <div key={index} className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/10">
                  <p className="text-sm font-medium text-[#2F748E] mb-2">{obj.objection}</p>
                  <div className="flex gap-4 text-xs">
                    <span className="text-[#2F748E]/60">
                      Handled: <span className="font-medium text-[#2F748E]">{obj.handled}</span>
                    </span>
                    <span className="text-[#2F748E]/60">
                      Quality: <span className={`font-medium ${
                        obj.quality === 'Excellent' ? 'text-[#8ABFA3]' :
                        obj.quality === 'Good' ? 'text-[#20AA99]' : 'text-[#2F748E]'
                      }`}>{obj.quality}</span>
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Follow-up Recommendations */}
          <div className="bg-gradient-to-br from-[#20AA99] to-[#2F748E] rounded-2xl p-6 text-white shadow-lg">
            <h3 className="text-lg font-semibold mb-4">AI Follow-up Recommendations</h3>
            
            <div className="space-y-3">
              <div className="flex items-start gap-3 p-3 rounded-lg bg-white/10 backdrop-blur-sm">
                <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm">Send requested clinical study materials within 48 hours</p>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-white/10 backdrop-blur-sm">
                <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm">Schedule follow-up meeting for next month as agreed</p>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-white/10 backdrop-blur-sm">
                <CheckCircle2 className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <p className="text-sm">Prepare additional cost-effectiveness analysis for next visit</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
