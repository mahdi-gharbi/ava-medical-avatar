import express from "express";
import Report from "../models/Report.js";

const router = express.Router();

// 📝 POST - Sauvegarder un rapport
router.post("/", async (req, res) => {
  try {
    console.log("[API] POST /api/reports reçu");
    console.log("[API] Body:", JSON.stringify(req.body).substring(0, 200) + "...");
    
    const {
      doctor_id = "DOC_001", // Statique pour maintenant
      doctor_name,
      delegate_name,
      transcript,
      objections_detected = [],
      main_objection_type,
      strategies = {},
      sentiment = 0,
      interest = 0,
      visit_score = 0,
      json_data = {},
      // 🔥 NOUVEAUX CHAMPS
      detected_language = "FRANÇAIS",
      medical_specialty = "Médecine Générale",
      engagement = null,
      detected_needs = [],
      client_typology = null,
      proposed_product = null,
      report_date = new Date()
    } = req.body;

    console.log(`[API] Création rapport pour Dr: ${doctor_name}`);

    // Créer le rapport
    const report = new Report({
      doctor_id,
      doctor_name,
      delegate_name,
      transcript,
      objections_detected,
      main_objection_type,
      strategies,
      sentiment,
      interest,
      visit_score,
      json_data,
      // 🔥 NOUVEAUX CHAMPS
      detected_language,
      medical_specialty,
      engagement,
      detected_needs,
      client_typology,
      proposed_product,
      report_date
    });

    // Sauvegarder dans MongoDB
    console.log("[API] Tentative de sauvegarde dans MongoDB...");
    await report.save();
    console.log(`[API] ✅ Rapport sauvegardé avec ID: ${report._id}`);

    res.status(201).json({
      message: "✅ Rapport sauvegardé avec succès dans CRM",
      visit_id: report.visit_id,
      report_id: report._id,
      createdAt: report.created_at
    });
  } catch (error) {
    console.error("❌ Erreur lors de la sauvegarde:", error);
    res.status(500).json({
      message: "❌ Erreur lors de la sauvegarde du rapport",
      error: error.message
    });
  }
});

// 📄 GET - Récupérer tous les rapports
router.get("/", async (req, res) => {
  try {
    const reports = await Report.find().sort({ created_at: -1 });
    res.json({
      count: reports.length,
      reports
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 📋 GET - Récupérer rapports d'un médecin
router.get("/doctor/:doctor_id", async (req, res) => {
  try {
    const reports = await Report.find({ doctor_id: req.params.doctor_id }).sort({ created_at: -1 });
    res.json({
      doctor_id: req.params.doctor_id,
      count: reports.length,
      reports
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 🔍 GET - Récupérer un rapport par ID
router.get("/:id", async (req, res) => {
  try {
    const report = await Report.findById(req.params.id);
    if (!report) {
      return res.status(404).json({ message: "Rapport non trouvé" });
    }
    res.json(report);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
