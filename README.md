# 🚀 SaaS Signal Miner

A full-stack MVP for discovering high-potential, early-stage SaaS startups using public signals (news, funding, job posts, etc.) and ranking them by growth potential.

## 🎯 Features

- **AI-Powered Scanning**: Uses Perplexity API with Llama-3-Sonar model to scan for startup signals
- **Smart Ranking**: Automatically calculates growth scores based on multiple factors
- **Interactive Dashboard**: Beautiful Streamlit interface with real-time filtering
- **Data Visualization**: Charts showing score distribution, sector breakdown, and signal types
- **Fallback Data**: Graceful degradation with dummy data when API is unavailable
- **Optional Persistence**: Supabase integration for storing historical data

## 🏗️ Architecture

```
saas-signal-miner/
├── main.py              # Core logic with LangChain + Perplexity API
├── app.py               # Streamlit frontend dashboard
├── utils.py             # JSON parsing and data utilities
├── supabase_client.py   # Optional database persistence
├── requirements.txt     # Python dependencies
├── env_template.txt     # Environment variables template
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd saas-signal-miner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the environment template and add your Perplexity API key:

```bash
# Copy env_template.txt to .env
cp env_template.txt .env

# Edit .env file with your credentials
OPENAI_API_KEY=your_perplexity_key_here
OPENAI_API_BASE=https://api.perplexity.ai
```

### 4. Get Perplexity API Key

1. Visit [Perplexity AI](https://www.perplexity.ai/)
2. Sign up for an account
3. Navigate to API settings
4. Generate an API key
5. Add it to your `.env` file

### 5. Run the Application

#### Option A: Streamlit Dashboard (Recommended)
```bash
streamlit run app.py
```

#### Option B: Test Core Logic
```bash
python main.py
```

## 📊 Dashboard Features

### Main Dashboard
- **Real-time Metrics**: Total startups, average score, high-score count
- **Interactive Charts**: Score distribution, sector breakdown, signal types
- **Startup Cards**: Detailed view of each startup with growth reasons
- **Refresh Button**: Manually update data from API

### Sidebar Filters
- **Sector**: Filter by industry (Technology, Healthcare, Fintech, etc.)
- **Funding Stage**: Filter by stage (Seed, Series A, Early Stage, etc.)
- **Signal Type**: Filter by signal (Funding, Partnership, Market Demand, etc.)
- **Growth Score**: Minimum score threshold (0-100)

### Data Visualization
- **Histogram**: Growth score distribution
- **Pie Chart**: Sector breakdown
- **Bar Chart**: Signal type distribution
- **Color-coded Scores**: Green (80+), Yellow (60-79), Red (<60)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your Perplexity API key | Yes |
| `OPENAI_API_BASE` | Perplexity API base URL | No (defaults to https://api.perplexity.ai) |
| `SUPABASE_URL` | Supabase project URL | No (optional) |
| `SUPABASE_KEY` | Supabase anon key | No (optional) |

### API Configuration

The application uses:
- **Model**: `llama-3-sonar-large-32k-online`
- **Temperature**: 0.2 (for consistent results)
- **Base URL**: `https://api.perplexity.ai`

## 🗄️ Database Setup (Optional)

If you want to enable data persistence with Supabase:

### 1. Create Supabase Project
1. Visit [Supabase](https://supabase.com/)
2. Create a new project
3. Get your project URL and anon key

### 2. Add to Environment
```bash
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
```

### 3. Create Tables
Run the SQL schema provided in `supabase_client.py`:

```sql
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
```

## 📈 Growth Score Algorithm

The application calculates growth scores based on:

- **Base Score**: 50 points
- **Funding Stage Bonus**:
  - Seed: +10 points
  - Series A: +15 points
  - Series B: +20 points
- **Signal Type Bonus**:
  - Funding: +15 points
  - Partnership: +12 points
  - Acquisition: +20 points
- **Sector Bonus**:
  - AI/ML: +8 points
  - Cybersecurity: +10 points
  - Healthcare: +7 points

## 🛠️ Development

### Project Structure

- **`main.py`**: Core business logic with `SaaSSignalMiner` class
- **`app.py`**: Streamlit frontend with caching and error handling
- **`utils.py`**: Data parsing, validation, and fallback utilities
- **`supabase_client.py`**: Database operations and trend analysis

### Key Classes

#### `SaaSSignalMiner`
- `scan_for_startups()`: Main API call to Perplexity
- `filter_startups()`: Apply filters to startup data
- `get_unique_values()`: Extract filter options

#### `SupabaseClient`
- `store_startups()`: Save data to database
- `get_startup_trends()`: Analyze historical trends
- `create_tables()`: Database schema setup

### Error Handling

The application includes comprehensive error handling:
- API rate limiting → Fallback to dummy data
- Network errors → Graceful degradation
- Invalid responses → JSON parsing fallbacks
- Missing credentials → Clear error messages

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Production Deployment
1. Set up environment variables
2. Install dependencies
3. Run with process manager (PM2, Supervisor, etc.)
4. Configure reverse proxy (Nginx, Apache)

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📝 API Response Format

The Perplexity API is prompted to return JSON in this format:

```json
[
  {
    "name": "Startup Name",
    "description": "What they do",
    "growth_reason": "Why they show growth potential",
    "source_link": "https://source.com/article",
    "sector": "Technology",
    "funding_stage": "Series A",
    "signal_type": "Funding"
  }
]
```

## 🔍 Troubleshooting

### Common Issues

1. **"No API key configured"**
   - Check your `.env` file
   - Ensure `OPENAI_API_KEY` is set correctly

2. **"Error initializing LangChain client"**
   - Verify your Perplexity API key is valid
   - Check internet connection

3. **"No startup data available"**
   - API might be rate limited
   - Check Perplexity API status
   - Application will use fallback data

4. **Import errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Perplexity AI](https://www.perplexity.ai/) for the LLM API
- [LangChain](https://langchain.com/) for the AI framework
- [Streamlit](https://streamlit.io/) for the web interface
- [Supabase](https://supabase.com/) for database functionality

---

**Happy Startup Hunting! 🚀**
