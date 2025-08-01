"""
SaaS Signal Miner - Core Logic
Scans for high-potential early-stage SaaS startups using public signals
"""

import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from perplexity_client import PerplexityClient
from utils import parse_saas_startups_response, format_startup_data, get_fallback_data

# Load environment variables
load_dotenv()

class SaaSSignalMiner:
    """
    Main class for mining SaaS startup signals using Perplexity API
    """
    
    def __init__(self):
        """Initialize the SaaS Signal Miner with API configuration"""
        # Initialize Perplexity client
        self.client = None
        try:
            self.client = PerplexityClient()
            print("✅ PerplexityClient initialized successfully")
        except Exception as e:
            print(f"Error initializing PerplexityClient: {e}")
            self.client = None
    
    def generate_startup_query(self) -> str:
        """
        Generate the query for finding SaaS startups
        
        Returns:
            str: Formatted query for the LLM
        """
        return """Give me 10 early-stage SaaS startups that are likely to experience significant growth based on recent public signals. 

For each startup, provide the following information in JSON format:
- name: Company name
- description: Brief description of what they do
- growth_reason: Specific reason why they show growth potential (funding, partnerships, market trends, etc.)
- source_link: URL or source of the signal
- sector: Industry sector
- funding_stage: Current funding stage
- signal_type: Type of signal (funding, partnership, acquisition, market demand, etc.)

Focus on startups that have shown recent activity like:
- Recent funding rounds
- Strategic partnerships
- Product launches
- Market expansion
- Regulatory changes affecting their sector
- Industry trends favoring their solution

Return the data as a JSON array with these exact field names."""

    def scan_for_startups(self) -> List[Dict[str, Any]]:
        """
        Scan for high-potential SaaS startups using Perplexity API
        
        Returns:
            List[Dict[str, Any]]: List of startup data with growth scores
        """
        if not self.client:
            print("Warning: No API key configured or API initialization failed. Using fallback data.")
            return format_startup_data(get_fallback_data())
        
        try:
            # Generate the query
            query = self.generate_startup_query()
            
            # Make API call
            print("Scanning for SaaS startups using Perplexity API...")
            response = self.client.ask(query)
            
            # Parse the response
            print(f"Received response from API (length: {len(response)})")
            
            # Parse and format the startup data
            startups = parse_saas_startups_response(response)
            formatted_startups = format_startup_data(startups)
            
            print(f"Successfully parsed {len(formatted_startups)} startups")
            return formatted_startups
            
        except Exception as e:
            print(f"Error scanning for startups: {e}")
            print("Falling back to dummy data...")
            return format_startup_data(get_fallback_data())
    
    def filter_startups(self, startups: List[Dict[str, Any]], 
                       sector: Optional[str] = None,
                       funding_stage: Optional[str] = None,
                       signal_type: Optional[str] = None,
                       min_score: int = 0) -> List[Dict[str, Any]]:
        """
        Filter startups based on criteria
        
        Args:
            startups (List[Dict[str, Any]]): List of startups to filter
            sector (Optional[str]): Filter by sector
            funding_stage (Optional[str]): Filter by funding stage
            signal_type (Optional[str]): Filter by signal type
            min_score (int): Minimum growth score
            
        Returns:
            List[Dict[str, Any]]: Filtered list of startups
        """
        filtered_startups = startups.copy()
        
        # Filter by sector
        if sector and sector != "All":
            filtered_startups = [
                s for s in filtered_startups 
                if s.get('sector', '').lower() == sector.lower()
            ]
        
        # Filter by funding stage
        if funding_stage and funding_stage != "All":
            filtered_startups = [
                s for s in filtered_startups 
                if s.get('funding_stage', '').lower() == funding_stage.lower()
            ]
        
        # Filter by signal type
        if signal_type and signal_type != "All":
            filtered_startups = [
                s for s in filtered_startups 
                if s.get('signal_type', '').lower() == signal_type.lower()
            ]
        
        # Filter by minimum score
        filtered_startups = [
            s for s in filtered_startups 
            if s.get('score', 0) >= min_score
        ]
        
        return filtered_startups
    
    def get_unique_values(self, startups: List[Dict[str, Any]], field: str) -> List[str]:
        """
        Get unique values for a specific field from startup data
        
        Args:
            startups (List[Dict[str, Any]]): List of startups
            field (str): Field name to extract unique values from
            
        Returns:
            List[str]: List of unique values
        """
        values = set()
        for startup in startups:
            value = startup.get(field, '')
            if value:
                values.add(value)
        
        return sorted(list(values))

def main():
    """
    Main function for testing the SaaS Signal Miner
    """
    print("🚀 SaaS Signal Miner - Testing Core Logic")
    print("=" * 50)
    
    # Initialize the miner
    miner = SaaSSignalMiner()
    
    # Scan for startups
    startups = miner.scan_for_startups()
    
    # Display results
    print(f"\nFound {len(startups)} startups:")
    print("-" * 50)
    
    for i, startup in enumerate(startups[:5], 1):  # Show top 5
        print(f"{i}. {startup['name']}")
        print(f"   Score: {startup['score']}")
        print(f"   Sector: {startup['sector']}")
        print(f"   Stage: {startup['funding_stage']}")
        print(f"   Signal: {startup['signal_type']}")
        print(f"   Reason: {startup['growth_reason']}")
        print()
    
    # Test filtering
    print("Testing filters...")
    tech_startups = miner.filter_startups(startups, sector="Technology")
    print(f"Technology startups: {len(tech_startups)}")
    
    high_score_startups = miner.filter_startups(startups, min_score=80)
    print(f"High score startups (80+): {len(high_score_startups)}")
    
    print("\n✅ Core logic test completed!")

if __name__ == "__main__":
    main() 