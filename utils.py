"""
Utility functions for SaaS Signal Miner
Handles JSON parsing, data validation, and fallback data
"""

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

def parse_saas_startups_response(response_text: str) -> List[Dict[str, str]]:
    """
    Parse the LLM response into structured startup data
    
    Args:
        response_text (str): Raw response from Perplexity API
        
    Returns:
        List[Dict[str, str]]: List of startup dictionaries
    """
    startups = []
    
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            startups = json.loads(json_str)
        else:
            # Fallback: try to parse structured text
            startups = parse_structured_text(response_text)
            
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing JSON: {e}")
        # Return fallback data if parsing fails
        startups = get_fallback_data()
    
    # Validate and clean the data
    validated_startups = []
    for startup in startups:
        if isinstance(startup, dict):
            validated_startup = {
                'name': startup.get('name', 'Unknown Startup'),
                'description': startup.get('description', 'No description available'),
                'growth_reason': startup.get('growth_reason', 'Growth signals detected'),
                'source_link': startup.get('source_link', 'https://example.com'),
                'sector': startup.get('sector', 'Technology'),
                'funding_stage': startup.get('funding_stage', 'Early Stage'),
                'signal_type': startup.get('signal_type', 'News'),
                'score': startup.get('score', 75)
            }
            validated_startups.append(validated_startup)
    
    return validated_startups

def parse_structured_text(text: str) -> List[Dict[str, str]]:
    """
    Parse structured text response when JSON parsing fails
    
    Args:
        text (str): Structured text response
        
    Returns:
        List[Dict[str, str]]: List of startup dictionaries
    """
    startups = []
    
    # Split by startup entries (look for numbered lists or bullet points)
    entries = re.split(r'\n\d+\.|\n•|\n-', text)
    
    for entry in entries:
        if not entry.strip():
            continue
            
        # Extract startup information using regex patterns
        name_match = re.search(r'Name[:\s]+([^\n]+)', entry, re.IGNORECASE)
        desc_match = re.search(r'Description[:\s]+([^\n]+)', entry, re.IGNORECASE)
        reason_match = re.search(r'Reason[:\s]+([^\n]+)', entry, re.IGNORECASE)
        source_match = re.search(r'Source[:\s]+([^\n]+)', entry, re.IGNORECASE)
        
        if name_match:
            startup = {
                'name': name_match.group(1).strip(),
                'description': desc_match.group(1).strip() if desc_match else 'No description',
                'growth_reason': reason_match.group(1).strip() if reason_match else 'Growth potential detected',
                'source_link': source_match.group(1).strip() if source_match else 'https://example.com',
                'sector': 'Technology',
                'funding_stage': 'Early Stage',
                'signal_type': 'News',
                'score': 75
            }
            startups.append(startup)
    
    return startups

def get_fallback_data() -> List[Dict[str, Any]]:
    """
    Return fallback data when API fails or rate limited
    
    Returns:
        List[Dict[str, Any]]: List of dummy startup data
    """
    return [
        {
            'name': 'TechFlow Analytics',
            'description': 'AI-powered business intelligence platform for SMBs',
            'growth_reason': 'Recent Series A funding of $5M, growing customer base',
            'source_link': 'https://techcrunch.com/techflow-analytics',
            'sector': 'Business Intelligence',
            'funding_stage': 'Series A',
            'signal_type': 'Funding',
            'score': 85
        },
        {
            'name': 'CloudSync Pro',
            'description': 'Enterprise-grade file synchronization solution',
            'growth_reason': 'Major partnership with Microsoft, expanding team',
            'source_link': 'https://venturebeat.com/cloudsync-pro',
            'sector': 'Cloud Computing',
            'funding_stage': 'Seed',
            'signal_type': 'Partnership',
            'score': 78
        },
        {
            'name': 'DataVault Security',
            'description': 'Zero-trust cybersecurity platform for enterprises',
            'growth_reason': 'Increased demand post-cyber attacks, new product launch',
            'source_link': 'https://techcrunch.com/datavault-security',
            'sector': 'Cybersecurity',
            'funding_stage': 'Early Stage',
            'signal_type': 'Market Demand',
            'score': 92
        },
        {
            'name': 'GreenTech Solutions',
            'description': 'Sustainability tracking software for manufacturing',
            'growth_reason': 'Regulatory compliance requirements, ESG focus',
            'source_link': 'https://greenbiz.com/greentech-solutions',
            'sector': 'Sustainability',
            'funding_stage': 'Seed',
            'signal_type': 'Regulatory',
            'score': 80
        },
        {
            'name': 'HealthAI Connect',
            'description': 'AI-powered patient care coordination platform',
            'growth_reason': 'Healthcare digitization trends, pilot with major hospital',
            'source_link': 'https://healthcareitnews.com/healthai-connect',
            'sector': 'Healthcare',
            'funding_stage': 'Series A',
            'signal_type': 'Industry Trend',
            'score': 88
        },
        {
            'name': 'EduTech Pro',
            'description': 'Personalized learning platform for K-12 education',
            'growth_reason': 'Remote learning adoption, government contracts',
            'source_link': 'https://edtechmagazine.com/edutech-pro',
            'sector': 'Education',
            'funding_stage': 'Early Stage',
            'signal_type': 'Government',
            'score': 75
        },
        {
            'name': 'FinFlow Analytics',
            'description': 'Real-time financial data analysis for traders',
            'growth_reason': 'Market volatility, institutional interest',
            'source_link': 'https://fintechnews.com/finflow-analytics',
            'sector': 'Fintech',
            'funding_stage': 'Seed',
            'signal_type': 'Market Opportunity',
            'score': 82
        },
        {
            'name': 'LogiChain Pro',
            'description': 'Supply chain optimization using blockchain',
            'growth_reason': 'Global supply chain disruptions, Fortune 500 pilots',
            'source_link': 'https://supplychaindive.com/logichain-pro',
            'sector': 'Logistics',
            'funding_stage': 'Series A',
            'signal_type': 'Market Disruption',
            'score': 79
        },
        {
            'name': 'RetailAI Insights',
            'description': 'AI-powered retail analytics and customer insights',
            'growth_reason': 'E-commerce growth, major retail partnerships',
            'source_link': 'https://retailwire.com/retailai-insights',
            'sector': 'Retail',
            'funding_stage': 'Early Stage',
            'signal_type': 'Partnership',
            'score': 76
        },
        {
            'name': 'EnergyGrid Optimizer',
            'description': 'Smart grid management and energy optimization',
            'growth_reason': 'Renewable energy transition, government incentives',
            'source_link': 'https://energynews.com/energygrid-optimizer',
            'sector': 'Energy',
            'funding_stage': 'Seed',
            'signal_type': 'Policy',
            'score': 84
        }
    ]

def calculate_growth_score(startup: Dict[str, str]) -> int:
    """
    Calculate a growth score based on startup signals
    
    Args:
        startup (Dict[str, str]): Startup data
        
    Returns:
        int: Growth score (0-100)
    """
    score = 50  # Base score
    
    # Adjust based on funding stage
    funding_stage = startup.get('funding_stage', '').lower()
    if 'seed' in funding_stage:
        score += 10
    elif 'series a' in funding_stage:
        score += 15
    elif 'series b' in funding_stage:
        score += 20
    
    # Adjust based on signal type
    signal_type = startup.get('signal_type', '').lower()
    if 'funding' in signal_type:
        score += 15
    elif 'partnership' in signal_type:
        score += 12
    elif 'acquisition' in signal_type:
        score += 20
    
    # Adjust based on sector
    sector = startup.get('sector', '').lower()
    if 'ai' in sector or 'artificial intelligence' in sector:
        score += 8
    elif 'cybersecurity' in sector:
        score += 10
    elif 'healthcare' in sector:
        score += 7
    
    return min(100, max(0, score))

def format_startup_data(startups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format startup data for display with calculated scores
    
    Args:
        startups (List[Dict[str, Any]]): Raw startup data
        
    Returns:
        List[Dict[str, Any]]: Formatted startup data with scores
    """
    formatted_startups = []
    
    for startup in startups:
        # Calculate growth score if not present
        if 'score' not in startup:
            startup['score'] = calculate_growth_score(startup)
        
        # Add timestamp
        startup['timestamp'] = datetime.now().isoformat()
        
        formatted_startups.append(startup)
    
    # Sort by score (highest first)
    formatted_startups.sort(key=lambda x: x['score'], reverse=True)
    
    return formatted_startups 