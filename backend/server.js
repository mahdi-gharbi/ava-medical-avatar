import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import cors from "cors";

import testRoute from "./routes/testRoute.js";
import reportRoute from "./routes/reportRoute.js";

dotenv.config();

const app = express();
app.use(cors());
// Augmenter la limite de payload pour les gros rapports JSON
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

const PORT = process.env.PORT || 5000;

// 🔥 attendre connexion Mongo avant start serveur
mongoose.connect(process.env.MONGO_URI)
  .then(() => {
    console.log("✅ MongoDB connecté");

    app.use("/test", testRoute);
    app.use("/api/reports", reportRoute);

    console.log("📝 Routes enregistrées:");
    console.log("  - GET  /test/all");
    console.log("  - GET  /test/add");
    console.log("  - POST /api/reports");
    console.log("  - GET  /api/reports");
    console.log("  - GET  /api/reports/doctor/:doctor_id");
    console.log("  - GET  /api/reports/:id");

    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
      console.log(`📍 Testez: http://localhost:${PORT}/api/reports`);
    });

  })
  .catch(err => {
    console.error("❌ Erreur Mongo:", err);
  });