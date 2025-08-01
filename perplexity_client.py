import os
import requests
from typing import Optional
import streamlit as st


class PerplexityClient:
    """
    A simple client for interacting with the Perplexity AI API using pure requests.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Perplexity client.
        
        Args:
            api_key: Perplexity API key. If not provided, reads from Streamlit secrets or PERPLEXITY_API_KEY env var.
        """
        # Priority: passed api_key > Streamlit secrets > environment variable
        if api_key:
            self.api_key = api_key
        else:
            # Try Streamlit secrets first (for production)
            try:
                self.api_key = st.secrets["API"]["PERPLEXITY_API_KEY"]
            except (KeyError, AttributeError):
                # Fallback to environment variable (for local development)
                self.api_key = os.getenv('PERPLEXITY_API_KEY')
        
        if not self.api_key:
            raise ValueError("Perplexity API key is required. Set PERPLEXITY_API_KEY in Streamlit secrets or environment variable, or pass api_key parameter.")
        
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3-sonar-large-32k"
        
    def ask(self, prompt: str, system_prompt: str = "You are a helpful assistant.") -> str:
        """
        Send a prompt to the Perplexity API and return the response.
        
        Args:
            prompt: The user's question or prompt
            system_prompt: The system message to set context
            
        Returns:
            The model's response as a plain string
            
        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the response is invalid
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4000,
            "temperature": 0.2,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            if 'choices' not in data or not data['choices']:
                raise ValueError("Invalid response format from Perplexity API")
            
            return data['choices'][0]['message']['content']
            
        except requests.RequestException as e:
            raise requests.RequestException(f"API request failed: {str(e)}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid response format: {str(e)}") 