# 🚀 Deployment Guide - Streamlit Cloud

## Prerequisites
- GitHub repository with your code
- Perplexity API key

## Step 1: Prepare Your Repository

Your repository is now production-ready with the following structure:
```
saas-signal-miner/
├── app.py                    # Main Streamlit application
├── main.py                   # Core business logic
├── perplexity_client.py      # Perplexity API client
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # Local secrets (not committed)
└── README.md                # Project documentation
```

## Step 2: Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Select your repository**: `bhavayupadhyay/saas-signal-miner`
5. **Set the main file path**: `app.py`
6. **Click "Deploy"**

## Step 3: Configure Secrets

After deployment, configure your API key:

1. **Go to your app's settings** (gear icon)
2. **Navigate to "Secrets"**
3. **Add the following configuration**:

```toml
[API]
PERPLEXITY_API_KEY = "your_actual_perplexity_api_key_here"
```

**Replace `your_actual_perplexity_api_key_here` with your real Perplexity API key.**

## Step 4: Verify Deployment

Your app should now be live at: `https://your-app-name.streamlit.app`

## Environment Variables

The app uses the following priority for API keys:
1. **Streamlit Secrets** (production)
2. **Environment Variables** (local development)
3. **Fallback to dummy data** (if no API key available)

## Troubleshooting

### API Key Issues
- Ensure your Perplexity API key is valid
- Check that the key is properly set in Streamlit secrets
- Verify the key format: `pplx-...`

### Import Errors
- All required dependencies are in `requirements.txt`
- The app will fall back to dummy data if API fails

### Performance
- Data is cached for 5 minutes
- Use the refresh button for latest results

## Security Notes

- ✅ API keys are stored securely in Streamlit secrets
- ✅ `.env` and `.streamlit/secrets.toml` are excluded from Git
- ✅ No sensitive data is committed to the repository

## Local Development

For local development, create a `.env` file:
```
PERPLEXITY_API_KEY=your_api_key_here
```

Then run:
```bash
streamlit run app.py
```

---

**Your SaaS Signal Miner is now ready for production! 🎉** 