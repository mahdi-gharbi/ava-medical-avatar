import {
  FileText,
  Upload,
  CheckCircle2,
  AlertCircle,
  Clock,
  TrendingUp,
  MessageSquare,
} from 'lucide-react';
import { useMemo, useState } from 'react';

const avaDoctorImage = new URL('../../assets/avaDoctor.png', import.meta.url).href;

type Bo5Source = {
  content?: string;
  score?: number;
  source?: string;
  metadata?: Record<string, unknown>;
};

type Bo5Objection = {
  type: string;
  text: string;
  strategy?: string;
  sources?: Bo5Source[];
};

type Bo5Result = {
  type?: string;
  analysis?: string;
  objections?: Bo5Objection[];
  predicted_sentiment?: number;
  predicted_interest?: number;
  predicted_main_objection?: string;
  predicted_objection_score?: number;
  detected_language?: string;
  medical_specialty?: string;
  engagement?: { obtained?: boolean; score?: number; indicators?: string[] };
  detected_needs?: string[];
  client_typology?: { primary?: string; confidence?: number };
  proposed_product?: string;
  recommended_products?: Array<{ name?: string; score?: number; reason?: string } | string>;
  visit_score?: number;
  report_date?: string;
  key_points?: Record<string, number>;
  exchanges?: Array<{ speaker: string; text: string }>;
};

const EXAMPLES: Record<string, string> = {
  '📍 Cardiologie (défaut)': `DÉLÉGUÉ: Bonjour docteur, merci de m'accorder ce moment
MÉDECIN: Bien sûr, que me proposez-vous?
DÉLÉGUÉ: Nous avons lancé un nouveau produit pour la cardiologie
MÉDECIN: Intéressant! Quel est le prix?
DÉLÉGUÉ: 45 euros par boîte, pour un traitement mensuel
MÉDECIN: C'est assez cher, n'avez-vous pas quelque chose de moins onéreux?
DÉLÉGUÉ: Je comprends votre préoccupation. Cependant, les études cliniques montrent 35% d'efficacité supérieure
MÉDECIN: Vous avez les données cliniques?
DÉLÉGUÉ: Absolument, voici les résultats des essais phase 3
MÉDECIN: Et la sécurité? Y a-t-il des effets secondaires?
DÉLÉGUÉ: Le profil de sécurité est excellent, tolérance supérieure aux produits concurrents
MÉDECIN: Bon, et la disponibilité? Avez-vous du stock?
DÉLÉGUÉ: Oui, nous avons en stock chez notre grossiste
MÉDECIN: Et la couverture CNAM?
DÉLÉGUÉ: C'est en cours d'évaluation, mais je vous fournirai la documentation`,
  '🩺 Dermatologie': `DÉLÉGUÉ: Bonjour Dr Martin, comment allez-vous?
MÉDECIN: Bien, je suis occupé. Dites-moi rapidement.
DÉLÉGUÉ: Nous avons une nouvelle crème pour le traitement de l'acné
MÉDECIN: Une crème de plus... Qu'est-ce qui la rend spéciale?
DÉLÉGUÉ: Notre formule combine acide salicylique et probiotiques naturels
MÉDECIN: Les probiotiques dans une crème? C'est quoi, la preuve scientifique?
DÉLÉGUÉ: Nous avons des résultats d'essais sur 500 patients montrant 78% d'amélioration
MÉDECIN: Et les effets secondaires? L'irritation cutanée?
DÉLÉGUÉ: Non, elle est hypoallergénique et testée dermatologiquement
MÉDECIN: Quel est le prix comparé à Duac?
DÉLÉGUÉ: 28 euros par tube, moins cher de 30% mais plus efficace
MÉDECIN: Et l'assurance? Elle rembourse?
DÉLÉGUÉ: Oui, sur prescription médicale`,
};

const REPORT_TYPES = [
  'Analyse Objections',
  'Synthèse Produits',
  'Recommandations',
  'Statistiques',
] as const;

function getApiBaseUrl(): string {
  const fromEnv = (import.meta as any).env?.VITE_AI_BACKEND_URL;
  return (typeof fromEnv === 'string' && fromEnv.trim()) ? fromEnv.trim() : 'http://localhost:8000';
}

async function extractDialogueFromFile(file: File): Promise<string> {
  const apiBase = getApiBaseUrl();
  const formData = new FormData();
  formData.append('file', file);

  const resp = await fetch(`${apiBase}/api/bo5/extract-text`, {
    method: 'POST',
    body: formData,
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `Extract failed (${resp.status})`);
  }

  const data = (await resp.json()) as { dialogue?: string };
  return (data.dialogue || '').trim();
}

async function analyzeBo5(params: {
  dialogue: string;
  rapportType: string;
  topK: number;
}): Promise<Bo5Result> {
  const apiBase = getApiBaseUrl();

  const resp = await fetch(`${apiBase}/api/bo5/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dialogue: params.dialogue,
      rapport_type: params.rapportType,
      top_k: params.topK,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `Analyze failed (${resp.status})`);
  }

  return (await resp.json()) as Bo5Result;
}

function trimResultForPdf(result: Bo5Result): Partial<Bo5Result> {
  return {
    visit_score: result.visit_score,
    predicted_sentiment: result.predicted_sentiment,
    predicted_interest: result.predicted_interest,
    detected_language: result.detected_language,
    medical_specialty: result.medical_specialty,
    analysis: result.analysis,
    predicted_main_objection: result.predicted_main_objection,
    // Keep objections but drop heavy nested sources.
    objections: (result.objections || []).map((o: any) => ({
      type: o?.type,
      text: o?.text,
      strategy: o?.strategy,
    })),
    report_date: result.report_date,
  };
}

function trimResultForCrm(result: Bo5Result): Partial<Bo5Result> {
  return {
    visit_score: result.visit_score,
    predicted_sentiment: result.predicted_sentiment,
    predicted_interest: result.predicted_interest,
    detected_language: result.detected_language,
    medical_specialty: result.medical_specialty,
    engagement: result.engagement,
    detected_needs: result.detected_needs,
    client_typology: result.client_typology,
    proposed_product: result.proposed_product,
    recommended_products: result.recommended_products,
    predicted_main_objection: result.predicted_main_objection,
    predicted_objection_score: result.predicted_objection_score,
    analysis: result.analysis,
    objections: (result.objections || []).map((o: any) => ({
      type: o?.type,
      text: o?.text,
      strategy: o?.strategy,
    })),
    report_date: result.report_date,
  };
}

async function downloadBo5Pdf(params: {
  dialogue: string;
  result: Bo5Result;
  rapportType: string;
  doctorName?: string;
  delegateName?: string;
}): Promise<void> {
  const apiBase = getApiBaseUrl();
  const resultTrimmed = trimResultForPdf(params.result);
  const resp = await fetch(`${apiBase}/api/bo5/pdf`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dialogue: params.dialogue,
      result: resultTrimmed,
      rapport_type: params.rapportType,
      doctor_name: params.doctorName || null,
      delegate_name: params.delegateName || null,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `PDF export failed (${resp.status})`);
  }

  const blob = await resp.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `bo5_report_${new Date().toISOString().replace(/[:.]/g, '-')}.pdf`;
  a.click();
  URL.revokeObjectURL(url);
}

async function saveBo5ToCrm(params: {
  dialogue: string;
  result: Bo5Result;
  doctorName?: string;
  delegateName?: string;
}): Promise<{ success: boolean; message?: string; visit_id?: string; report_id?: string }> {
  const apiBase = getApiBaseUrl();
  const resultTrimmed = trimResultForCrm(params.result);
  const resp = await fetch(`${apiBase}/api/bo5/save-to-crm`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dialogue: params.dialogue,
      result: resultTrimmed,
      doctor_name: params.doctorName || null,
      delegate_name: params.delegateName || null,
    }),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(text || `CRM save failed (${resp.status})`);
  }

  return (await resp.json()) as any;
}

export function BO5() {
  const [selectedExample, setSelectedExample] = useState(Object.keys(EXAMPLES)[0]);
  const [rapportType, setRapportType] = useState<(typeof REPORT_TYPES)[number]>('Analyse Objections');
  const [topK, setTopK] = useState(5);
  const [dialogue, setDialogue] = useState(EXAMPLES[selectedExample]);

  const [isExtracting, setIsExtracting] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isSavingCrm, setIsSavingCrm] = useState(false);
  const [isExportingPdf, setIsExportingPdf] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [result, setResult] = useState<Bo5Result | null>(null);

  const [doctorName, setDoctorName] = useState('');
  const [delegateName, setDelegateName] = useState('');

  const objections = result?.objections || [];

  const keyInsights = useMemo(() => {
    const analysis = (result?.analysis || '').trim();
    if (!analysis) return [] as string[];

    // Heuristic: take first few non-empty lines as insights
    const lines = analysis
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean)
      .slice(0, 4);

    return lines.length ? lines : [analysis.slice(0, 220) + (analysis.length > 220 ? '…' : '')];
  }, [result?.analysis]);

  const timeline = useMemo(() => {
    const exchanges = result?.exchanges || [];
    if (!exchanges.length) return [] as Array<{ time: string; event: string; type: 'info' | 'important' | 'positive' }>;

    const items: Array<{ time: string; event: string; type: 'info' | 'important' | 'positive' }> = [];
    const max = Math.min(exchanges.length, 6);
    for (let i = 0; i < max; i++) {
      const ex = exchanges[i];
      items.push({
        time: String(i + 1).padStart(2, '0') + ':00',
        event: `${ex.speaker}: ${ex.text}`.slice(0, 72) + (ex.text.length > 72 ? '…' : ''),
        type: 'info',
      });
    }

    if ((result?.visit_score ?? 0) >= 80) {
      items.push({ time: '—', event: 'High visit score detected', type: 'positive' });
    }

    if (objections.length > 0) {
      items.push({ time: '—', event: `${objections.length} objection(s) detected`, type: 'important' });
    }

    return items.slice(0, 8);
  }, [result?.exchanges, result?.visit_score, objections.length]);

  const onPickExample = (name: string) => {
    setSelectedExample(name);
    setDialogue(EXAMPLES[name]);
    setResult(null);
    setError(null);
    setSuccess(null);
  };

  const onUpload = async (file: File) => {
    setError(null);
    setSuccess(null);
    setIsExtracting(true);
    try {
      const extracted = await extractDialogueFromFile(file);
      if (!extracted) throw new Error('No text extracted from the uploaded file');
      setDialogue(extracted);
      setResult(null);
    } catch (e: any) {
      setError(e?.message || 'Upload failed');
    } finally {
      setIsExtracting(false);
    }
  };

  const onAnalyze = async () => {
    setError(null);
    setSuccess(null);
    setIsAnalyzing(true);
    try {
      const res = await analyzeBo5({ dialogue, rapportType, topK });
      setResult(res);
    } catch (e: any) {
      setError(e?.message || 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const onExportPdf = async () => {
    if (!result) return;
    setError(null);
    setSuccess(null);
    setIsExportingPdf(true);
    try {
      await downloadBo5Pdf({
        dialogue,
        result,
        rapportType,
        doctorName: doctorName.trim() || undefined,
        delegateName: delegateName.trim() || undefined,
      });
      setSuccess('✅ PDF exported');
    } catch (e: any) {
      setError(e?.message || 'PDF export failed');
    } finally {
      setIsExportingPdf(false);
    }
  };

  const onSaveToCrm = async () => {
    if (!result) return;
    setError(null);
    setSuccess(null);
    setIsSavingCrm(true);
    try {
      const resp = await saveBo5ToCrm({
        dialogue,
        result,
        doctorName: doctorName.trim() || undefined,
        delegateName: delegateName.trim() || undefined,
      });
      if (resp?.success) {
        setSuccess(resp?.message || '✅ Saved to CRM');
      } else {
        setError(resp?.message || 'CRM save failed');
      }
    } catch (e: any) {
      setError(e?.message || 'CRM save failed');
    } finally {
      setIsSavingCrm(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
        <div className="flex items-center justify-between gap-6 flex-wrap">
          <div>
            <h1 className="text-2xl font-semibold text-[#2F748E] mb-2">BO5 – Reporting (Connected)</h1>
            <p className="text-[#20AA99] font-medium">Uses the same LLM+RAG logic as Streamlit BO5</p>
            <p className="text-xs text-[#2F748E]/60 mt-1">API: {getApiBaseUrl()}</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                if (!result) return;
                const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `bo5_report_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
                a.click();
                URL.revokeObjectURL(url);
              }}
              disabled={!result}
              className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FileText className="w-4 h-4" />
              Export JSON
            </button>
            <button
              onClick={onExportPdf}
              disabled={!result || isExportingPdf}
              className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FileText className="w-4 h-4" />
              {isExportingPdf ? 'Exporting…' : 'Export PDF'}
            </button>
            <button
              onClick={onSaveToCrm}
              disabled={!result || isSavingCrm}
              className="px-4 py-2 rounded-lg border border-[#20AA99]/20 text-[#2F748E] hover:bg-[#F4FBFF] transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <CheckCircle2 className="w-4 h-4" />
              {isSavingCrm ? 'Saving…' : 'Save to CRM'}
            </button>
            <button
              onClick={onAnalyze}
              disabled={isAnalyzing || isExtracting || !dialogue.trim()}
              className="px-6 py-3 rounded-lg bg-gradient-to-r from-[#20AA99] to-[#2F748E] text-white font-medium shadow-lg hover:shadow-xl transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <CheckCircle2 className="w-4 h-4" />
              {isAnalyzing ? 'Analyzing…' : 'Generate Report'}
            </button>
          </div>
        </div>

        {success ? (
          <div className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-green-50 border border-green-200">
            <CheckCircle2 className="w-5 h-5 text-green-600 mt-0.5" />
            <p className="text-sm text-green-800 whitespace-pre-wrap">{success}</p>
          </div>
        ) : null}

        {error ? (
          <div className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-red-50 border border-red-200">
            <AlertCircle className="w-5 h-5 text-red-500 mt-0.5" />
            <p className="text-sm text-red-700 whitespace-pre-wrap">{error}</p>
          </div>
        ) : null}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left - Avatar + Inputs */}
        <div className="lg:col-span-1 space-y-6">
          {/* Avatar */}
          <div className="bg-gradient-to-br from-[#2F748E] via-[#20AA99] to-[#8ABFA3] rounded-2xl p-1 shadow-lg">
            <div className="bg-white/80 backdrop-blur-xl rounded-xl p-6">
              <div className="text-center mb-4">
                <div className="w-32 h-32 mx-auto rounded-full bg-gradient-to-br from-[#20AA99] to-[#2F748E] flex items-center justify-center shadow-xl relative overflow-hidden ring-4 ring-white/20">
                  <div className="absolute inset-0 bg-[#20AA99]/20 blur-2xl animate-pulse"></div>
                  <img src={avaDoctorImage} alt="Dr. AVA" className="w-full h-full object-cover object-top" />
                </div>
                <p className="text-[#2F748E] font-semibold mt-3">AVA BO5 Analyzer</p>
                <p className="text-[#20AA99] text-xs">RAG + Groq + ML</p>
              </div>

              <div className="relative bg-[#F4FBFF] rounded-lg p-4 border border-[#20AA99]/20">
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-transparent border-b-[#F4FBFF]"></div>
                <p className="text-sm text-[#2F748E]">"Paste a dialogue or upload a PDF/JSON, then generate the report."</p>
              </div>
            </div>
          </div>

          {/* Inputs */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg space-y-4">
            <h3 className="text-lg font-semibold text-[#2F748E]">Conversation Input</h3>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-[#2F748E]/60">Doctor name</label>
                <input
                  value={doctorName}
                  onChange={(e) => setDoctorName(e.target.value)}
                  placeholder="e.g., Dr. Martinez"
                  className="w-full px-3 py-2 rounded-lg bg-white border border-[#20AA99]/20 text-[#2F748E]"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-[#2F748E]/60">Delegate name</label>
                <input
                  value={delegateName}
                  onChange={(e) => setDelegateName(e.target.value)}
                  placeholder="e.g., Ahmed"
                  className="w-full px-3 py-2 rounded-lg bg-white border border-[#20AA99]/20 text-[#2F748E]"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-[#2F748E]/60">Example</label>
              <select
                value={selectedExample}
                onChange={(e) => onPickExample(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-[#2F748E]"
              >
                {Object.keys(EXAMPLES).map((k) => (
                  <option key={k} value={k}>
                    {k}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-[#2F748E]/60">Report type</label>
                <select
                  value={rapportType}
                  onChange={(e) => setRapportType(e.target.value as any)}
                  className="w-full px-3 py-2 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-[#2F748E]"
                >
                  {REPORT_TYPES.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-[#2F748E]/60">Sources (top_k)</label>
                <input
                  type="number"
                  min={1}
                  max={20}
                  value={topK}
                  onChange={(e) => setTopK(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-[#2F748E]"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-[#2F748E]/60">Dialogue (DÉLÉGUÉ / MÉDECIN)</label>
              <textarea
                value={dialogue}
                onChange={(e) => setDialogue(e.target.value)}
                rows={10}
                className="w-full px-3 py-2 rounded-lg bg-white border border-[#20AA99]/20 text-[#2F748E] focus:outline-none focus:ring-2 focus:ring-[#20AA99]/30"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-[#2F748E]/60">Upload (PDF or JSON)</label>
              <div className="flex items-center gap-3">
                <label className="flex-1 border-2 border-dashed border-[#20AA99]/30 rounded-lg p-3 text-center hover:bg-[#F4FBFF] transition-colors cursor-pointer">
                  <input
                    type="file"
                    accept="application/pdf,application/json,.pdf,.json"
                    className="hidden"
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) void onUpload(f);
                      e.currentTarget.value = '';
                    }}
                  />
                  <div className="flex items-center justify-center gap-2 text-[#2F748E]">
                    <Upload className="w-4 h-4 text-[#20AA99]" />
                    <span className="text-sm font-medium">{isExtracting ? 'Extracting…' : 'Choose file'}</span>
                  </div>
                  <p className="text-xs text-[#2F748E]/60 mt-1">Extracts text server-side</p>
                </label>
              </div>
            </div>
          </div>

          {/* Visit Stats */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Visit Metrics</h3>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Visit score</span>
                <span className="text-sm font-semibold text-[#2F748E]">{result?.visit_score ?? '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Sentiment</span>
                <span className="text-sm font-semibold text-[#2F748E]">{result?.predicted_sentiment ?? '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Interest</span>
                <span className="text-sm font-semibold text-[#2F748E]">{result?.predicted_interest ?? '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Language</span>
                <span className="text-sm font-semibold text-[#2F748E]">{result?.detected_language ?? '—'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-[#2F748E]/70">Specialty</span>
                <span className="text-sm font-semibold text-[#2F748E]">{result?.medical_specialty ?? '—'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right - Report & Insights */}
        <div className="lg:col-span-2 space-y-6">
          {/* Timeline */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">Visit Timeline (from exchanges)</h3>
            </div>

            {timeline.length ? (
              <div className="space-y-3">
                {timeline.map((item, index) => (
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
                      {index < timeline.length - 1 && <div className="w-0.5 h-full bg-[#20AA99]/20 mt-1"></div>}
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
            ) : (
              <div className="p-8 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-center">
                <p className="text-[#2F748E]/60">Generate a report to see the timeline</p>
              </div>
            )}
          </div>

          {/* Report */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-[#20AA99]" />
              <h3 className="text-lg font-semibold text-[#2F748E]">AI-Generated BO5 Report</h3>
            </div>

            {result?.analysis ? (
              <div className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 space-y-4">
                <div>
                  <p className="text-xs font-semibold text-[#2F748E]/60 mb-1">KEY INSIGHTS</p>
                  <ul className="space-y-2">
                    {keyInsights.map((x, idx) => (
                      <li key={idx} className="text-sm text-[#2F748E] leading-relaxed">
                        • {x}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <p className="text-xs font-semibold text-[#2F748E]/60 mb-1">FULL ANALYSIS</p>
                  <p className="text-sm text-[#2F748E] whitespace-pre-wrap leading-relaxed">{result.analysis}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-3 rounded-lg bg-white border border-[#20AA99]/10">
                    <p className="text-xs text-[#2F748E]/60 mb-1">Main objection (ML)</p>
                    <p className="text-sm font-semibold text-[#2F748E]">{result.predicted_main_objection ?? '—'}</p>
                    <p className="text-xs text-[#20AA99]">Score: {result.predicted_objection_score ?? '—'}</p>
                  </div>
                  <div className="p-3 rounded-lg bg-white border border-[#20AA99]/10">
                    <p className="text-xs text-[#2F748E]/60 mb-1">Proposed product</p>
                    <p className="text-sm font-semibold text-[#2F748E]">{result.proposed_product ?? '—'}</p>
                    <p className="text-xs text-[#2F748E]/60">Client typology: {result.client_typology?.primary ?? '—'}</p>
                  </div>
                </div>

                {Array.isArray(result.recommended_products) && result.recommended_products.length ? (
                  <div>
                    <p className="text-xs font-semibold text-[#2F748E]/60 mb-2">RECOMMENDED PRODUCTS</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {result.recommended_products.slice(0, 6).map((p, idx) => {
                        const name = typeof p === 'string' ? p : p?.name;
                        const score = typeof p === 'string' ? undefined : (p as any)?.score;
                        const reason = typeof p === 'string' ? undefined : (p as any)?.reason;
                        return (
                          <div key={idx} className="p-3 rounded-lg bg-white border border-[#20AA99]/10">
                            <p className="text-sm font-semibold text-[#2F748E]">{name || '—'}</p>
                            {score !== undefined ? (
                              <p className="text-xs text-[#20AA99]">Score: {score}</p>
                            ) : null}
                            {reason ? (
                              <p className="text-xs text-[#2F748E]/70 mt-1">{reason}</p>
                            ) : null}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ) : null}
              </div>
            ) : (
              <div className="p-8 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-center">
                <MessageSquare className="w-12 h-12 mx-auto text-[#20AA99]/40 mb-3" />
                <p className="text-[#2F748E]/60">Generate a report to see the BO5 analysis</p>
              </div>
            )}
          </div>

          {/* Objections */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-[#20AA99]/10 shadow-lg">
            <div className="flex items-center justify-between gap-2 mb-4 flex-wrap">
              <h3 className="text-lg font-semibold text-[#2F748E]">Detected Objections & Strategies</h3>
              <p className="text-xs text-[#2F748E]/60">From `detect_objections` + RAG sources</p>
            </div>

            {objections.length ? (
              <div className="space-y-4">
                {objections.map((o, idx) => (
                  <div key={idx} className="p-4 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20">
                    <div className="flex items-start justify-between gap-4 flex-wrap">
                      <div>
                        <p className="text-sm font-semibold text-[#2F748E]">{o.type}</p>
                        <p className="text-xs text-[#2F748E]/70 mt-1">{o.text}</p>
                      </div>
                      <span className="px-3 py-1 rounded-full bg-[#20AA99]/15 text-[#20AA99] text-xs font-medium">
                        {(o.sources?.length ?? 0)} source(s)
                      </span>
                    </div>

                    {o.strategy ? (
                      <div className="mt-3 p-3 rounded-lg bg-white border border-[#20AA99]/10">
                        <p className="text-xs font-semibold text-[#2F748E]/60 mb-1">Suggested strategy</p>
                        <p className="text-sm text-[#2F748E] whitespace-pre-wrap">{o.strategy}</p>
                      </div>
                    ) : null}

                    {o.sources?.length ? (
                      <details className="mt-3">
                        <summary className="cursor-pointer text-sm text-[#2F748E]">Show sources</summary>
                        <div className="mt-2 space-y-2">
                          {o.sources.slice(0, 5).map((s, sidx) => (
                            <div key={sidx} className="p-3 rounded-lg bg-white border border-[#20AA99]/10">
                              <p className="text-xs text-[#20AA99]">Score: {s.score ?? '—'} | {s.source ?? 'source'}</p>
                              <p className="text-xs text-[#2F748E]/70 mt-1 whitespace-pre-wrap">{(s.content || '').slice(0, 450)}{(s.content && s.content.length > 450) ? '…' : ''}</p>
                            </div>
                          ))}
                        </div>
                      </details>
                    ) : null}
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-8 rounded-lg bg-[#F4FBFF] border border-[#20AA99]/20 text-center">
                <p className="text-[#2F748E]/60">No objections yet (generate a report)</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
