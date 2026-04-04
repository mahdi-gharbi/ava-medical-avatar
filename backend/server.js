import express from "express";
import mongoose from "mongoose";
import dotenv from "dotenv";
import cors from "cors";

import testRoute from "./routes/testRoute.js";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 5000;

// 🔥 attendre connexion Mongo avant start serveur
mongoose.connect(process.env.MONGO_URI)
  .then(() => {
    console.log("✅ MongoDB connecté");

    app.use("/test", testRoute);

    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
    });

  })
  .catch(err => {
    console.error("❌ Erreur Mongo:", err);
  });