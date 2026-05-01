from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

import requests
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field


class BO5AnalyzeRequest(BaseModel):
	dialogue: str = Field(..., min_length=1)
	rapport_type: str = Field(default="Analyse Objections")
	top_k: int = Field(default=5, ge=1, le=20)
	use_finetuned: bool = Field(default=False)


class BO5PdfRequest(BaseModel):
	dialogue: str = Field(..., min_length=1)
	result: dict[str, Any]
	rapport_type: str = Field(default="Analyse Objections")
	doctor_name: str | None = None
	delegate_name: str | None = None


class BO5SaveToCrmRequest(BaseModel):
	dialogue: str = Field(..., min_length=1)
	result: dict[str, Any]
	doctor_name: str | None = None
	delegate_name: str | None = None


app = FastAPI(title="AVA AI Backend", version="0.1.0")


allowed_origins = [
	os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173"),
	"http://127.0.0.1:5173",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok"}


@app.post("/api/bo5/analyze")
def bo5_analyze(payload: BO5AnalyzeRequest) -> dict[str, Any]:
	try:
		from ai_backend.rag.query.query_bo5_medical import analyze_conversation

		return analyze_conversation(
			dialogue=payload.dialogue,
			rapport_type=payload.rapport_type,
			top_k=payload.top_k,
			use_finetuned=payload.use_finetuned,
		)
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"BO5 analyze failed: {exc}") from exc


def _get_crm_api_url() -> str:
	return os.environ.get("CRM_API_URL") or "http://localhost:5000/api/reports"


def _pdf_bytes_from_bo5(
	dialogue: str,
	result: dict[str, Any],
	rapport_type: str,
	doctor_name: str | None = None,
	delegate_name: str | None = None,
) -> bytes:
	from fpdf import FPDF
	import re

	pdf = FPDF(format="A4", unit="mm")
	pdf.set_margins(8, 8, 8)
	pdf.set_auto_page_break(auto=True, margin=10)
	pdf.add_page()

	font_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts"))
	regular = os.path.join(font_dir, "DejaVuSans.ttf")
	bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
	has_fonts = os.path.exists(regular) and os.path.exists(bold)

	if has_fonts:
		pdf.add_font("DejaVu", "", regular, uni=True)
		pdf.add_font("DejaVu", "B", bold, uni=True)
		font_regular = ("DejaVu", "", 10)
		font_bold = ("DejaVu", "B", 12)
		font_small = ("DejaVu", "", 8)
	else:
		font_regular = ("Helvetica", "", 10)
		font_bold = ("Helvetica", "B", 12)
		font_small = ("Helvetica", "", 8)

	def set_font(f: tuple[str, str, int]) -> None:
		family, style, size = f
		pdf.set_font(family, style, size)

	def safe_text(text: str) -> str:
		"""Make text safe for fpdf2 layout.

		fpdf2 can raise `Not enough horizontal space to render a single character`
		when encountering very long unbroken tokens (e.g. JSON blobs, URLs).
		We proactively insert line breaks into such tokens.
		"""
		if text is None:
			return ""
		text = str(text)
		text = text.replace("\r\n", "\n").replace("\r", "\n")
		text = text.replace("\t", " ")
		text = text.replace("\x00", "")

		max_token_len = 80

		def _break_token(match: re.Match[str]) -> str:
			token = match.group(0)
			return "\n".join(token[i : i + max_token_len] for i in range(0, len(token), max_token_len))

		# Break long sequences with no whitespace to avoid overflow.
		return re.sub(rf"\S{{{max_token_len + 1},}}", _break_token, text)

	def h2(title: str) -> None:
		set_font(font_bold)
		pdf.set_text_color(47, 116, 142)
		pdf.set_x(pdf.l_margin)
		pdf.multi_cell(0, 6, safe_text(title))
		pdf.set_text_color(0, 0, 0)

	def p(text: str) -> None:
		set_font(font_regular)
		pdf.set_x(pdf.l_margin)
		pdf.multi_cell(0, 5, safe_text(text))

	def small(text: str) -> None:
		set_font(font_small)
		pdf.set_text_color(32, 170, 153)
		pdf.set_x(pdf.l_margin)
		pdf.multi_cell(0, 4, safe_text(text))
		pdf.set_text_color(0, 0, 0)

	h2("RAPPORT BO5")
	small("Analyse intelligente de visite médicale (React + API)")
	set_font(font_small)
	pdf.set_x(pdf.l_margin)
	pdf.multi_cell(
		0,
		4,
		safe_text(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Type: {rapport_type}"),
	)
	if doctor_name or delegate_name:
		pdf.set_x(pdf.l_margin)
		pdf.multi_cell(
			0,
			4,
			safe_text(
				f"Médecin: {doctor_name or '-'} | Délégué: {delegate_name or '-'}"
			),
		)
	pdf.ln(2)

	visit_score = result.get("visit_score")
	sentiment = result.get("predicted_sentiment")
	interest = result.get("predicted_interest")
	lang = result.get("detected_language")
	spec = result.get("medical_specialty")

	h2("Métriques")
	p(
		"\n".join(
			[
				f"Score visite: {visit_score}",
				f"Sentiment: {sentiment}",
				f"Intérêt: {interest}",
				f"Langue: {lang}",
				f"Spécialité: {spec}",
			]
		)
	)
	pdf.ln(2)

	h2("Dialogue")
	p(dialogue)
	pdf.ln(2)

	h2("Analyse")
	analysis = str(result.get("analysis") or "")
	if analysis.strip():
		p(analysis)
	else:
		p("(Aucune analyse générée)")
	pdf.ln(2)

	h2("Objections & stratégies")
	objections = result.get("objections") or []
	if isinstance(objections, list) and objections:
		for idx, obj in enumerate(objections[:8], start=1):
			if not isinstance(obj, dict):
				continue
			obj_type = str(obj.get("type") or "Objection")
			obj_text = str(obj.get("text") or "")
			strategy = str(obj.get("strategy") or "")
			set_font(font_bold)
			pdf.set_x(pdf.l_margin)
			pdf.multi_cell(0, 5, safe_text(f"{idx}. {obj_type}"))
			set_font(font_regular)
			if obj_text:
				pdf.set_x(pdf.l_margin)
				pdf.multi_cell(0, 5, safe_text(obj_text))
			if strategy:
				pdf.set_x(pdf.l_margin)
				pdf.multi_cell(0, 5, safe_text("Stratégie:"))
				pdf.set_x(pdf.l_margin)
				pdf.multi_cell(0, 5, safe_text(strategy))
			pdf.ln(1)
	else:
		p("Aucune objection détectée.")

	return bytes(pdf.output(dest="S"))


@app.post("/api/bo5/pdf")
def bo5_pdf(payload: BO5PdfRequest) -> Response:
	try:
		pdf_bytes = _pdf_bytes_from_bo5(
			payload.dialogue,
			payload.result,
			payload.rapport_type,
			doctor_name=payload.doctor_name,
			delegate_name=payload.delegate_name,
		)
		filename = f"bo5_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
		return Response(
			content=pdf_bytes,
			media_type="application/pdf",
			headers={"Content-Disposition": f"attachment; filename={filename}"},
		)
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"PDF generation failed: {exc}") from exc


@app.post("/api/bo5/save-to-crm")
def bo5_save_to_crm(payload: BO5SaveToCrmRequest) -> dict[str, Any]:
	try:
		result = payload.result or {}
		objections = result.get("objections") or []
		strategies: list[str] = []
		if isinstance(objections, list):
			for obj in objections:
				if isinstance(obj, dict) and obj.get("strategy"):
					strategies.append(str(obj.get("strategy")))

		crm_payload = {
			"doctor_id": "DOC_001",
			"doctor_name": payload.doctor_name or "Médecin",
			"delegate_name": payload.delegate_name or "Délégué",
			"transcript": payload.dialogue,
			"objections_detected": bool(objections),
			"main_objection_type": result.get("predicted_main_objection"),
			"strategies": strategies,
			"sentiment": float(result.get("predicted_sentiment") or 0),
			"interest": float(result.get("predicted_interest") or 0),
			"visit_score": float(result.get("visit_score") or 0),
			"json_data": result,
			"detected_language": result.get("detected_language"),
			"medical_specialty": result.get("medical_specialty"),
			"engagement": result.get("engagement"),
			"detected_needs": result.get("detected_needs"),
			"client_typology": result.get("client_typology"),
			"proposed_product": result.get("proposed_product"),
			"report_date": result.get("report_date"),
		}

		resp = requests.post(_get_crm_api_url(), json=crm_payload, timeout=15)
		if resp.status_code == 201:
			data = resp.json() if resp.content else {}
			return {
				"success": True,
				"message": data.get("message", "✅ Rapport sauvegardé"),
				"visit_id": data.get("visit_id"),
				"report_id": data.get("report_id"),
			}
		return {"success": False, "message": f"CRM error {resp.status_code}: {resp.text}"}
	except requests.exceptions.ConnectionError as exc:
		return {
			"success": False,
			"message": f"❌ Impossible de se connecter au CRM: {_get_crm_api_url()} ({exc})",
		}
	except Exception as exc:
		raise HTTPException(status_code=500, detail=f"Save to CRM failed: {exc}") from exc


@app.post("/api/bo5/extract-text")
async def bo5_extract_text(file: UploadFile = File(...)) -> dict[str, str]:
	"""Extract dialogue text from an uploaded PDF or JSON file.

	Matches the Streamlit helpers in `frontendstreamlit/pages/5_BO5_reporting.py`.
	"""

	content_type = (file.content_type or "").lower()
	filename = (file.filename or "").lower()

	try:
		raw = await file.read()
	except Exception as exc:
		raise HTTPException(status_code=400, detail=f"Failed to read upload: {exc}") from exc

	try:
		if content_type == "application/pdf" or filename.endswith(".pdf"):
			from pypdf import PdfReader

			import io

			reader = PdfReader(io.BytesIO(raw))
			text_parts: list[str] = []
			for page in reader.pages:
				page_text = page.extract_text() or ""
				if page_text:
					text_parts.append(page_text)
			return {"dialogue": "\n".join(text_parts).strip()}

		if content_type in {"application/json", "text/json"} or filename.endswith(".json"):
			data = json.loads(raw.decode("utf-8"))
			if isinstance(data, dict):
				return {"dialogue": str(data.get("dialogue", data)).strip()}
			if isinstance(data, list):
				return {"dialogue": "\n".join(str(item) for item in data).strip()}
			return {"dialogue": str(data).strip()}

		raise HTTPException(status_code=415, detail="Only PDF or JSON supported")
	except HTTPException:
		raise
	except Exception as exc:
		raise HTTPException(status_code=400, detail=f"Failed to extract text: {exc}") from exc

