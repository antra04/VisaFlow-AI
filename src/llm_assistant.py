"""LLM Assistant for Visa Queries"""
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class VisaAssistant:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        self.system_prompt = """You are a visa and immigration expert assistant. 
        You help people understand visa requirements, application processes, and documentation needs.
        
        Key responsibilities:
        - Provide accurate visa requirement information
        - Explain application processes step-by-step
        - Suggest required documents
        - Answer questions about visa eligibility
        
        Always be helpful, accurate, and ask clarifying questions if needed."""
        
    def get_visa_requirements(self, from_country, to_country, purpose):
        """Get visa requirements for travel between countries"""
        prompt = f"""{self.system_prompt}

Question: What are the visa requirements for a {purpose} trip from {from_country} to {to_country}?

Provide:
1. Visa type needed
2. Key requirements
3. Processing time estimate
4. Required documents
5. Important notes

Be concise but comprehensive."""

        response = self.model.generate_content(prompt)
        return response.text
    
    def analyze_document(self, extracted_text, document_type="passport"):
        """Analyze extracted document text for completeness"""
        text_summary = "\n".join([item['text'] for item in extracted_text['full_text'][:10]])
        
        prompt = f"""{self.system_prompt}

I've extracted the following text from a {document_type}:

{text_summary}

Please analyze:
1. What information is present?
2. What critical information might be missing?
3. Is this sufficient for visa applications?
4. Any concerns or recommendations?

Be specific and practical."""

        response = self.model.generate_content(prompt)
        return response.text
    
    def chat(self, user_message, context=""):
        """General chat about visa/immigration queries"""
        prompt = f"""{self.system_prompt}

{context}

User question: {user_message}

Provide a helpful, accurate response."""

        response = self.model.generate_content(prompt)
        return response.text
