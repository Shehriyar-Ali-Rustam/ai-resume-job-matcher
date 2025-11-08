# Deployment Guide for Streamlit Cloud

## Quick Start

Your app is now ready to deploy on Streamlit Cloud! Follow these steps:

### 1. Streamlit Cloud Deployment Settings

When deploying on Streamlit Cloud, use these settings:

- **Repository**: `shehriyar-ali-rustam/AI-powered-resume-and-job-matcher` (or your actual repo name)
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`
- **App URL**: (optional - customize as you like)

### 2. What Changed

✅ **Created `streamlit_app.py`** - Standalone version that doesn't need FastAPI backend
✅ **Updated `requirements.txt`** - Optimized for Streamlit Cloud (removed unnecessary packages)
✅ **Updated `packages.txt`** - Added system dependencies
✅ **Integrated AI matching** - Everything runs in one app now

### 3. How It Works

The new `streamlit_app.py`:
- Loads the AI model directly (no backend server needed)
- Uses `@st.cache_resource` to cache the model (fast subsequent loads)
- All matching logic integrated into the Streamlit app
- Downloads NLTK data automatically on first run

### 4. Local Testing

To test locally before deploying:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the standalone app
streamlit run streamlit_app.py
```

### 5. Deployment Steps

1. **Push changes to GitHub** (if not already done):
   ```bash
   git add streamlit_app.py requirements.txt packages.txt DEPLOYMENT.md
   git commit -m "Add standalone Streamlit app for cloud deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud** (https://share.streamlit.io/)
   - Sign in with GitHub
   - Click "New app"
   - Fill in the deployment form as shown above
   - Click "Deploy"

3. **Wait for deployment** (usually 5-10 minutes)
   - Streamlit Cloud will install dependencies
   - Download AI models
   - Start your app

### 6. Important Notes

⚠️ **First load will be slow** - The AI model (~90MB) needs to download
✅ **Subsequent loads are fast** - Model is cached
✅ **No backend server needed** - Everything runs in Streamlit
✅ **Privacy-focused** - All processing happens in the app, no external APIs

### 7. Troubleshooting

**If deployment fails:**

1. Check the logs in Streamlit Cloud dashboard
2. Common issues:
   - Repository name might be different
   - Branch name might not be `main` (check `master`)
   - File path must be exactly `streamlit_app.py`

**If the app is slow:**

- First load is always slow (model download)
- Consider using a smaller model in `backend/matcher.py` if needed
- Current model: `all-MiniLM-L6-v2` (good balance of speed/accuracy)

### 8. Architecture Difference

**Old Architecture** (doesn't work on Streamlit Cloud):
```
Frontend (Streamlit) → HTTP Request → Backend (FastAPI) → AI Model
```

**New Architecture** (works on Streamlit Cloud):
```
Streamlit App → AI Model (cached in memory)
```

### 9. Files Overview

- `streamlit_app.py` - Main standalone application
- `requirements.txt` - Python dependencies (optimized)
- `packages.txt` - System-level dependencies
- `backend/matcher.py` - AI matching logic (imported directly)
- `utils/text_processor.py` - Text processing utilities (imported directly)
- `frontend/app.py` - Old version (kept for reference, not used)

---

**Ready to deploy!** 🚀

For questions or issues, visit: https://github.com/Shehriyar-Ali-Rustam/ai-resume-job-matcher/issues
