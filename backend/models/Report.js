import mongoose from "mongoose";

const ReportSchema = new mongoose.Schema({
  // IDs (statiques pour maintenant, pas de login)
  visit_id: {
    type: String,
    default: "VISIT_" + Date.now(),
    required: true
  },
  doctor_id: {
    type: String,
    default: "DOC_001", // À remplacer par doctor_id réel
    required: true
  },

  // Données de conversation
  transcript: {
    type: String,
    required: true
  },
  doctor_name: String,
  delegate_name: String,
  
  // NOUVELLES DONNÉES (AMÉLIORATIONS)
  detected_language: {
    type: String, // "FRANÇAIS", "ANGLAIS", "ARABE", "MIXTE"
    default: "FRANÇAIS"
  },
  medical_specialty: {
    type: String, // "Cardiologie", "Dermatologie", etc.
    default: "Médecine Générale"
  },
  detected_needs: {
    type: [String], // ["Fatigue", "Insomnie", ...]
    default: []
  },
  client_typology: {
    type: {
      primary: String, // "Promouvant", "Facilitant", "Contrôlant", "Analysant"
      confidence: Number, // 0-1
      all_types: {
        Promouvant: Number,
        Facilitant: Number,
        Contrôlant: Number,
        Analysant: Number
      }
    },
    default: null
  },
  engagement: {
    type: {
      obtained: Boolean, // true/false
      score: Number, // 0-1
      indicators: [String] // ["✅ ...", "❌ ..."]
    },
    default: null
  },
  proposed_product: {
    type: String, // Le produit proposé
    default: null
  },
  report_date: {
    type: Date,
    default: Date.now
  },

  // Analyse IA
  objections_detected: {
    type: [String], // Array: ["PRICE_OBJECTION", "SAFETY_CONCERN", ...]
    default: []
  },
  main_objection_type: {
    type: String, // "PRICE_OBJECTION", "SAFETY_CONCERN", etc.
    default: null
  },

  // Stratégies générées
  strategies: {
    type: mongoose.Schema.Types.Mixed, // Object avec clés = type d'objection, valeurs = stratégies
    default: {}
  },

  // Métriques
  sentiment: {
    type: Number, // -1 to 1
    default: 0
  },
  interest: {
    type: Number, // 0-100
    default: 0
  },
  visit_score: {
    type: Number, // 0-100
    default: 0
  },

  // Rapports
  pdf_url: String,
  json_data: {
    type: mongoose.Schema.Types.Mixed, // Contient le rapport complet en JSON
    default: {}
  },

  // Timestamps
  created_at: {
    type: Date,
    default: Date.now
  },
  updated_at: {
    type: Date,
    default: Date.now
  }
});

export default mongoose.model("Report", ReportSchema);
