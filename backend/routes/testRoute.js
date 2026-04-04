import express from "express";
import Test from "../models/Test.js";

const router = express.Router();

// 👉 TEST INSERT
router.get("/add", async (req, res) => {
  try {
    const doc = new Test({
      name: "hajaokhra",
      message: "MongoDB is working 🚀"
    });

    await doc.save();

    res.json({
      message: "Document ajouté avec succès",
      data: doc
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 👉 VOIR DATA
router.get("/all", async (req, res) => {
  try {
    const docs = await Test.find();
    res.json(docs);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;