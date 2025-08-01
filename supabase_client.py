"""
Supabase Client for SaaS Signal Miner
Optional database persistence for storing startup data and trends
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseClient:
    """
    Supabase client for storing and retrieving SaaS startup data
    """
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        self.client = None
        
        if self.supabase_url and self.supabase_key:
            try:
                from supabase import create_client
                self.client = create_client(self.supabase_url, self.supabase_key)
                print("✅ Supabase client initialized successfully")
            except ImportError:
                print("⚠️ Supabase package not installed. Run: pip install supabase")
            except Exception as e:
                print(f"❌ Error initializing Supabase client: {e}")
        else:
            print("⚠️ Supabase credentials not found in .env file")
    
    def is_connected(self) -> bool:
        """Check if Supabase client is connected"""
        return self.client is not None
    
    def store_startups(self, startups: List[Dict[str, Any]]) -> bool:
        """
        Store startup data in Supabase
        
        Args:
            startups (List[Dict[str, Any]]): List of startup data
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            print("❌ Supabase not connected")
            return False
        
        try:
            # Prepare data for storage
            startup_records = []
            for startup in startups:
                record = {
                    'name': startup.get('name'),
                    'description': startup.get('description'),
                    'growth_reason': startup.get('growth_reason'),
                    'source_link': startup.get('source_link'),
                    'sector': startup.get('sector'),
                    'funding_stage': startup.get('funding_stage'),
                    'signal_type': startup.get('signal_type'),
                    'score': startup.get('score'),
                    'timestamp': datetime.now().isoformat()
                }
                startup_records.append(record)
            
            # Insert data into startups table
            result = self.client.table('startups').insert(startup_records).execute()
            
            print(f"✅ Stored {len(startup_records)} startups in Supabase")
            return True
            
        except Exception as e:
            print(f"❌ Error storing startups: {e}")
            return False
    
    def get_startups(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve startup data from Supabase
        
        Args:
            limit (int): Maximum number of records to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of startup data
        """
        if not self.is_connected():
            print("❌ Supabase not connected")
            return []
        
        try:
            result = self.client.table('startups').select('*').order('timestamp', desc=True).limit(limit).execute()
            return result.data if result.data else []
            
        except Exception as e:
            print(f"❌ Error retrieving startups: {e}")
            return []
    
    def get_startup_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Get startup trends over time
        
        Args:
            days (int): Number of days to analyze
            
        Returns:
            Dict[str, Any]: Trend data
        """
        if not self.is_connected():
            print("❌ Supabase not connected")
            return {}
        
        try:
            # Get startups from the last N days
            from datetime import timedelta
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            result = self.client.table('startups').select('*').gte('timestamp', cutoff_date).execute()
            
            if not result.data:
                return {}
            
            # Calculate trends
            startups = result.data
            
            # Average score trend
            scores = [s.get('score', 0) for s in startups]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            # Sector distribution
            sectors = {}
            for startup in startups:
                sector = startup.get('sector', 'Unknown')
                sectors[sector] = sectors.get(sector, 0) + 1
            
            # Signal type distribution
            signal_types = {}
            for startup in startups:
                signal_type = startup.get('signal_type', 'Unknown')
                signal_types[signal_type] = signal_types.get(signal_type, 0) + 1
            
            return {
                'total_startups': len(startups),
                'average_score': avg_score,
                'sector_distribution': sectors,
                'signal_type_distribution': signal_types,
                'period_days': days
            }
            
        except Exception as e:
            print(f"❌ Error calculating trends: {e}")
            return {}
    
    def create_tables(self) -> bool:
        """
        Create necessary tables in Supabase (for setup)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            print("❌ Supabase not connected")
            return False
        
        try:
            # This would typically be done via SQL migrations
            # For now, we'll just print the schema
            print("📋 Required Supabase table schema:")
            print("""
            CREATE TABLE startups (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                growth_reason TEXT,
                source_link TEXT,
                sector TEXT,
                funding_stage TEXT,
                signal_type TEXT,
                score INTEGER,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            CREATE INDEX idx_startups_timestamp ON startups(timestamp);
            CREATE INDEX idx_startups_sector ON startups(sector);
            CREATE INDEX idx_startups_score ON startups(score);
            """)
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False

# Global instance
supabase_client = SupabaseClient()

def get_supabase_client() -> SupabaseClient:
    """Get the global Supabase client instance"""
    return supabase_client 