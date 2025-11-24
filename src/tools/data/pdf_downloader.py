"""PDF downloader and text extractor for financial documents."""

from typing import Dict, Any, Optional, List
from pathlib import Path
import requests
from datetime import datetime
import PyPDF2
import pdfplumber
from sec_edgar_downloader import Downloader


class PDFDownloader:
    """Tool for downloading and extracting text from PDFs."""
    
    def __init__(self, cache_dir: str = "pdf_cache"):
        """
        Initialize PDF downloader.
        
        Args:
            cache_dir: Directory to cache downloaded PDFs
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize SEC downloader
        self.sec_downloader = Downloader("MyCompany", "my.email@company.com", self.cache_dir / "sec")
    
    def download_pdf(self, url: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        Download a PDF from URL.
        
        Args:
            url: PDF URL
            filename: Optional filename to save as
            
        Returns:
            Path to downloaded PDF or None
        """
        try:
            if not filename:
                filename = url.split("/")[-1]
                if not filename.endswith(".pdf"):
                    filename += ".pdf"
            
            filepath = self.cache_dir / filename
            
            # Check if already cached
            if filepath.exists():
                print(f"Using cached PDF: {filepath}")
                return filepath
            
            # Download PDF
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded PDF: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error downloading PDF from {url}: {e}")
            return None
    
    def extract_text_pypdf2(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using PyPDF2.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text with PyPDF2: {e}")
            return ""
    
    def extract_text_pdfplumber(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using pdfplumber (better quality).
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
            return ""
    
    def extract_text(self, pdf_path: Path, method: str = "pdfplumber") -> str:
        """
        Extract text from PDF using specified method.
        
        Args:
            pdf_path: Path to PDF file
            method: Extraction method ("pdfplumber" or "pypdf2")
            
        Returns:
            Extracted text
        """
        if method == "pdfplumber":
            text = self.extract_text_pdfplumber(pdf_path)
            if not text:  # Fallback to PyPDF2
                text = self.extract_text_pypdf2(pdf_path)
        else:
            text = self.extract_text_pypdf2(pdf_path)
        
        return text
    
    def download_sec_filing(
        self,
        ticker: str,
        filing_type: str = "10-K",
        limit: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Download SEC filings for a company.
        
        Args:
            ticker: Stock ticker symbol
            filing_type: Type of filing (10-K, 10-Q, 8-K, etc.)
            limit: Number of filings to download
            
        Returns:
            List of filing information
        """
        try:
            # Download filings
            self.sec_downloader.get(filing_type, ticker, limit=limit)
            
            # Find downloaded files
            filing_dir = self.cache_dir / "sec" / "sec-edgar-filings" / ticker / filing_type
            
            if not filing_dir.exists():
                return []
            
            filings = []
            for filing_folder in sorted(filing_dir.iterdir(), reverse=True)[:limit]:
                if filing_folder.is_dir():
                    # Find the filing document
                    for file in filing_folder.iterdir():
                        if file.suffix in ['.txt', '.html']:
                            filings.append({
                                "ticker": ticker,
                                "filing_type": filing_type,
                                "file_path": file,
                                "date": filing_folder.name,
                            })
                            break
            
            return filings
            
        except Exception as e:
            print(f"Error downloading SEC filing for {ticker}: {e}")
            return []
    
    def search_investor_relations_pdfs(self, company_name: str, search_tool) -> List[str]:
        """
        Search for investor relations PDFs using search tool.
        
        Args:
            company_name: Company name
            search_tool: Tavily or other search tool
            
        Returns:
            List of PDF URLs
        """
        queries = [
            f"{company_name} investor presentation PDF",
            f"{company_name} annual report PDF",
            f"{company_name} earnings presentation PDF",
            f"{company_name} investor relations PDF",
        ]
        
        pdf_urls = []
        
        for query in queries:
            try:
                results = search_tool.search(query, max_results=3)
                for result in results.get("results", []):
                    url = result.get("url", "")
                    if url.endswith(".pdf") or "pdf" in url.lower():
                        pdf_urls.append(url)
            except Exception as e:
                print(f"Error searching for PDFs: {e}")
        
        return list(set(pdf_urls))  # Remove duplicates
    
    def extract_financial_data_from_text(self, text: str, company_name: str) -> Dict[str, Any]:
        """
        Extract key financial data from PDF text.
        
        Args:
            text: Extracted PDF text
            company_name: Company name for context
            
        Returns:
            Dictionary with extracted financial data
        """
        # This is a simple extraction - could be enhanced with NLP
        data = {
            "company": company_name,
            "text_length": len(text),
            "contains_revenue": "revenue" in text.lower(),
            "contains_earnings": "earnings" in text.lower() or "ebitda" in text.lower(),
            "contains_balance_sheet": "balance sheet" in text.lower(),
            "contains_cash_flow": "cash flow" in text.lower(),
            "raw_text_sample": text[:1000],  # First 1000 chars
        }
        
        return data
