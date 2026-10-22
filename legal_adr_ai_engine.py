import os
import json
import logging
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GlobalLegalADREngine:
    """
    Open-Source Global Legal & ADR Engine powered by Google Gemini AI.
    Handles jurisdiction analysis, contract/dispute risk assessment, 
    and ADR suitability evaluation for local and international law practices.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logging.warning("GEMINI_API_KEY not found. Please set the environment variable.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.5-flash"

    def analyze_dispute_for_adr(self, case_description: str, jurisdiction: str) -> Dict[str, Any]:
        """
        Analyzes a legal dispute to determine suitability for Alternative Dispute Resolution (ADR)
        versus traditional court litigation under the specified local jurisdiction.
        """
        if not self.client:
            return {"error": "Gemini API client not initialized. Check API Key."}

        system_instruction = (
            "You are an expert AI Legal Consultant and Mediator for a global law firm. "
            "Analyze legal disputes objectively according to the specified national jurisdiction "
            "and jurisprudence. Output your assessment in strict JSON format."
        )

        prompt = f"""
        Jurisdiction: {jurisdiction}
        Case Description: {case_description}

        Provide a structured JSON output with the following keys:
        1. "adr_suitability_score": Integer from 1 to 100 (100 being perfectly suited for mediation/ADR).
        2. "recommended_path": String ("Mediation", "Arbitration", "Litigation", or "Hybrid ADR").
        3. "key_legal_risks": List of strings detailing key statutory or procedural risks under local law.
        4. "mediation_strategy": String summarizing the recommended negotiation posture.
        5. "jurisprudence_notes": Brief notes regarding local court stance on similar disputes.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logging.error(f"Error executing Gemini API call: {e}")
            return {"error": str(e)}

    def audit_contract_clauses(self, contract_text: str, jurisdiction: str) -> Dict[str, Any]:
        """
        Audits contract text for dispute resolution clauses, jurisdiction compliance, 
        and potential liability risks.
        """
        if not self.client:
            return {"error": "Gemini API client not initialized."}

        system_instruction = (
            "You are a senior contract attorney auditing commercial agreements. "
            "Identify risk clauses, check jurisdiction validity, and ensure proper ADR/Mediation clauses."
        )

        prompt = f"""
        Target Jurisdiction: {jurisdiction}
        Contract Excerpt:
        {contract_text}

        Analyze the text and return a JSON object with:
        1. "has_adr_clause": Boolean.
        2. "jurisdiction_clause_valid": Boolean.
        3. "risk_level": String ("Low", "Medium", "High").
        4. "suggested_improvements": List of recommended edits to protect the client under local laws.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            return json.loads(response.text)
        except Exception as e:
            logging.error(f"Error auditing contract: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    # Example usage for testing
    print("=== Global Legal & ADR Gemini AI Engine ===")
