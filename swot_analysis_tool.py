from langchain.tools import tool
import PyPDF2
from typing import Dict, List
import os
import re

class SWOTAnalysisGuideTool:
    def __init__(self, pdf_path: str = "./SWOTAnalysis.pdf"):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The SWOT Analysis PDF file was not found at {pdf_path}")
        self.pdf_path = pdf_path
        self.content = self._extract_text_from_pdf()
        self.sections = self._parse_sections()

    def _extract_text_from_pdf(self) -> str:
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _parse_sections(self) -> Dict[str, str]:
        sections = {}
        current_section = "introduction"
        sections[current_section] = ""
        
        for line in self.content.split('\n'):
            if re.match(r'^[A-Z][a-z]+:', line):  # Detect section headers
                current_section = line.split(':')[0].lower()
                sections[current_section] = ""
            else:
                sections[current_section] += line + "\n"
        
        return sections

    @tool("Get SWOT Analysis Structure")
    def get_structure_guide(self) -> str:
        """Provides a guide on the structure of the SWOT analysis based on the PDF content."""
        structure = "The SWOT analysis in the provided PDF follows this structure:\n\n"
        for section, content in self.sections.items():
            word_count = len(content.split())
            structure += f"{section.capitalize()}: {word_count} words\n"
        
        total_words = sum(len(section.split()) for section in self.sections.values())
        structure += f"\nTotal length: {total_words} words\n"
        structure += "\nEach section should be well-developed with specific examples and analysis."
        return structure

    @tool("Get SWOT Section Example")
    def get_section_example(self, section: str) -> str:
        """Provides an example of a specific section from the SWOT analysis."""
        section_lower = section.lower()
        if section_lower in self.sections:
            return f"Example of {section.capitalize()} section:\n\n{self.sections[section_lower][:500]}..."
        else:
            available_sections = ", ".join(self.sections.keys())
            return f"Section not found. Available sections are: {available_sections}"

    @tool("Get SWOT Writing Style Tips")
    def get_writing_style_tips(self) -> List[str]:
        """Extracts and provides writing style tips based on the SWOT analysis content."""
        tips = [
            "Use clear and concise language throughout the analysis.",
            "Back up each point with specific examples or data when possible.",
            "Maintain a professional tone, avoiding casual language."
        ]
        
        # Analyze the content to extract more specific tips
        full_text = " ".join(self.sections.values()).lower()
        if re.search(r'\b(bullet|numbered)\s+(?:point|list)', full_text):
            tips.append("Use bullet points or numbered lists to organize information within each section.")
        
        if re.search(r'\b(transition|flow)\b', full_text):
            tips.append("Ensure a logical flow between sections, with smooth transitions.")
        
        if re.search(r'\b(conclude|summary)\b', full_text):
            tips.append("Conclude with a summary that ties together the key points from each section.")
        
        return tips