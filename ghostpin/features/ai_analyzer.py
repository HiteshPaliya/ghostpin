"""
GhostPin Enterprise v5 - AI Analyzer Module
Handles LLM integration for automatically explaining vulnerabilities and providing mitigation code.
Uses Google's Gemini API if configured, otherwise falls back to a locally hosted LLM or returns a generic analysis.
"""
import os
import json
import urllib.request
from typing import Dict, Any

class AIAnalyzer:
    def __init__(self):
        # Allow user to set their API key via env var, or provide a default demo behavior
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.api_key}"

    def analyze_finding(self, finding_title: str, finding_details: str, context: str = "SAST") -> Dict[str, str]:
        """
        Takes a raw technical finding and returns a structured AI analysis containing:
        1. Explanation of the risk
        2. Real-world impact
        3. Exact remediation code (Java/Kotlin/Swift)
        """
        prompt = f"""
You are an expert mobile application penetration tester. Analyze the following security finding.
Context: {context} testing of a mobile app.
Finding Title: {finding_title}
Details: {finding_details}

Provide your response in exactly the following JSON format (no markdown blocks, just raw JSON):
{{
  "explanation": "A clear, concise explanation of why this is a vulnerability.",
  "impact": "The real-world business and technical impact if exploited.",
  "remediation": "Specific steps to fix the issue.",
  "code_snippet": "Provide a secure code example in Java/Kotlin or Swift demonstrating the fix."
}}
"""

        if not self.api_key:
            # Fallback if no API key is set - provide a simulated "AI" response for demo purposes
            return {
                "explanation": f"Simulated AI Analysis for: {finding_title}. This finding indicates a deviation from mobile security best practices.",
                "impact": "Depending on the context, this could lead to data leakage, unauthorized access, or app tampering. A live API key is required for deep, context-aware analysis.",
                "remediation": "Review the relevant code paths and ensure sensitive data is removed from the codebase and proper encryption/pinning is enforced.",
                "code_snippet": "// Set GEMINI_API_KEY environment variable to enable full AI code generation\n// Example secure storage:\n// EncryptedSharedPreferences prefs = EncryptedSharedPreferences.create(...);"
            }

        try:
            data = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2}
            }).encode('utf-8')
            
            req = urllib.request.Request(self.endpoint, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                
                # Clean up any potential markdown formatting the LLM might have ignored instructions on
                if text_response.startswith('```json'):
                    text_response = text_response.split('```json')[1].split('```')[0].strip()
                elif text_response.startswith('```'):
                    text_response = text_response.split('```')[1].split('```')[0].strip()
                    
                return json.loads(text_response)
        except Exception as e:
            return {
                "explanation": f"AI Analysis failed: {str(e)}",
                "impact": "N/A",
                "remediation": "Manually investigate the finding.",
                "code_snippet": ""
            }

# Singleton instance
analyzer = AIAnalyzer()

def analyze_vulnerability(title: str, details: str, context: str = "SAST"):
    return analyzer.analyze_finding(title, details, context)
