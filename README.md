# TrendForgeAI

TrendForgeAI is a premium, data-driven content marketing optimizer that leverages AI to generate high-performing marketing content based on real-time social media trends and sentiment analysis.

## 🚀 Project Overview

TrendForgeAI combines a powerful FastAPI backend with a modern, sleek Next.js dashboard to provide a comprehensive suite of marketing tools:
- **AI Content Engine**: Uses Gemini 2.0 Flash to craft optimized LinkedIn, Twitter, and Instagram posts.
- **Sentiment & Trend Analysis**: Real-time monitoring of social sentiment across platforms.
- **Performance Metrics**: High-fidelity tracking of engagement, reach, and conversion rates.
- **A/B Testing & Prediction Coach**: Automated testing and AI-powered performance forecasts.

---

## 🏗️ Project Structure

```text
TrendForgeAI/
├── api/             # FastAPI Backend (Routers, Models, DB)
├── dashboard/       # Next.js Frontend (Components, UI)
├── src/             # Core AI Engine & Data Extractors logic
├── tests/           # Unit and Integration tests
├── data/            # Local data storage (CSVs, JSONs)
├── docs/            # Detailed documentation & setup guides
├── run.py           # CLI Control Panel for engine operations
└── README.md        # This file
```

---

## 🚦 Quick Start

### 1. Backend Setup (FastAPI)

#### Prerequisites
- Python 3.11+
- PostgreSQL (Neon DB recommended)
- Google Gemini API Key

#### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create database tables
python -m api.migrations.migrate create

# Start the API server
python -m uvicorn api.main:app --reload --port 8000
```
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Frontend Setup (Next.js)

#### Prerequisites
- Node.js 18+
- npm or yarn

#### Installation
```bash
cd dashboard
npm install
npm run dev
```
- **Dashboard**: [http://localhost:3000](http://localhost:3000)

---

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy 2.0, Pydantic v2
- **Frontend**: Next.js 14, Tailwind CSS, Lucide React
- **AI/ML**: Google Gemini 2.0 Flash, Semantic RAG
- **Database**: PostgreSQL (Neon DB)
- **Task Queue**: Celery & Redis (Planned)

---

## 📖 Documentation

Check out the `docs/` folder for more detailed information:
- **[Redis & Celery Setup](docs/REDIS_CELERY_SETUP.md)**: Guide for asynchronous task processing.
- **[Progress Update](docs/PROGRESS_UPDATE.md)**: Current development status and milestones.
- **[Next Steps](docs/NEXT_STEPS.md)**: Future roadmap and planned features.

## 🧪 Testing

```bash
# Run API tests
pytest tests/
```

## 📄 License

MIT License - See LICENSE file for details.
