# Personal US Stock Monitoring Platform & Quantitative Trading Cockpit

A high-performance personal stock monitoring web application that tracks US stocks, scores them based on custom quantitative investment rules (Quality, Valuation, 52-Week Discount, and Analyst Sentiment), and highlights "Quality Stocks on Sale" across sectors.

**Tech Stack:**
*   **Backend:** FastAPI (Python 3.12+), SQLAlchemy 2.0 (ORM), APScheduler, `yfinance`, `httpx`
*   **Database:** Supabase PostgreSQL (Time-series / historical snapshot design)
*   **Frontend:** React (Vite, TypeScript), Tailwind CSS, Recharts (Radar/Line charts), Lucide Icons

---

## 🚀 Key Features

*   **Bloomberg-Style Dark Cockpit Dashboard:** Beautiful, high-density quantitative UI showing top opportunities, watchlist metrics, sector rankings, and active system alerts.
*   **No-Overwrite Time-Series Design:** Appends historical data on every ingestion cycle to enable time-series score tracking and backtesting.
*   **API Quota Defense Strategy:** Implements an abstract provider factory layer using Yahoo Finance (`yfinance`) for unlimited fundamentals/targets and Finnhub for recommendations, fully bypassing expensive commercial API key paywalls.
*   **Advanced Quantitative Indicators:** Calculates **ROIC** (Return on Invested Capital - competitive moats) and **EBIT Growth** (core operational momentum) on the fly from raw SEC financial statements.
*   **FastAPI Background Tasks:** Seamless manual refreshes that trigger async ingestion and score recalculations behind the scenes so the UI never blocks.

---

## 🛠️ Installation & Local Setup

### 1. Database Setup (Supabase)
1. Register a free project at [supabase.com](https://supabase.com).
2. Go to your **Project Settings** -> **Database**.
3. Under **Connection String**, select the **URI** tab, toggle **Session / Transaction Pooler** to ON, and copy the connection string:
   `postgresql://postgres.[YOUR_PROJECT_ID]:[PASSWORD]@aws-0-region.pooler.supabase.com:6543/postgres`
4. Store this URL. (Ensure your database password does not contain special characters like `@` or `%` to avoid URL parsing issues).

---

### 2. Backend Setup
1. Open a terminal inside the project root and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your `.env` configuration file:
   Copy `.env.example` to `.env` and update it with your real Supabase Pooler connection string, and your Finnhub free developer API key (register for free at [finnhub.io](https://finnhub.io)):
   ```env
   PROJECT_NAME="Stock Monitor API"
   ENVIRONMENT=development
   SUPABASE_URL=postgresql://postgres.xxx:YOUR_PASSWORD@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres
   FINNHUB_API_KEY=your_free_finnhub_key
   ```
5. Create the database tables automatically:
   ```bash
   $env:PYTHONPATH="."  # For Windows PowerShell
   python create_tables.py
   ```
6. Spin up the local development API server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   The API will launch on `http://127.0.0.1:8000`. You can test endpoints or view the auto-generated documentation at `http://127.0.0.1:8000/docs`.

---

### 3. Frontend Setup
1. Open a *second* terminal window and navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install the node packages:
   ```bash
   npm install
   ```
3. Spin up the local web development client:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser to enter your personal Trading Cockpit!

---

## 📈 Understanding the Scoring Architecture

The cockpit tracks **4 key sub-scores** (each out of 100) to compute the final **Opportunity Score**:

$$OpportunityScore = 40\% \times Quality + 30\% \times Valuation + 20\% \times Discount + 10\% \times Analyst$$

1.  **Quality Score:** Evaluates operational efficiency, pricing power, and profitability stability. Uses **ROIC** (>15% gets max points), **EBIT Margins** (>25%), **Debt-to-Equity** ratios (low leverage rewarded), and YoY **EBIT Growth**.
2.  **Valuation Score:** Checks price relative to fundamental value. Rewards cheap **Forward P/E**, conservative **Price-to-Sales (P/S)**, and low **PEG ratios** (P/E relative to growth).
3.  **Discount Score:** Measures drawdown from 52-week highs. Rewards sweet-spot pullbacks (15%-35%) with **100 points**, while penalizing minor pullbacks (<5%) and potential collapses (>50%).
4.  **Analyst Score:** Evaluates Wall Street targets (rewarding higher upside %) and aggregates bullish vs. bearish consensus ratios.

---

## 📂 File Architecture Map

```text
backend/app/
├── api/routes/          # FastAPI routers (stocks, scores, sectors, watchlists, refresh)
├── clients/             # Master ApiManager (Quota safeguards and Raw JSON delta hashes)
├── core/                # System configuration, database session pool, custom exceptions
├── models/              # SQLAlchemy database snapshots schemas (Composite keys)
├── providers/           # Adapter layer (YahooProvider and FinnhubProvider implementations)
├── scoring/             # Modular scoring calculators (isolated math rules)
├── services/            # Ingestion service and data normalization orchestrators
├── jobs/                # Background APScheduler daily and weekly cron tasks
└── main.py              # Application lifecycle entrypoint

frontend/src/
├── components/          # Layout cards, badges, and navigation bars
├── pages/               # Dashboard, Watchlist, Screener, Alerts, and Stock Detail views
├── lib/                 # Axios clients and TypeScript types
└── index.css            # Custom Bloomberg-style scrollbars and dark slate theme
```

---

## 📝 Future Platform Roadmap
The architecture is completely modular and ready to support:
1.  **Redis & Celery:** To scale queue tasks.
2.  **Docker:** For containerization.
3.  **Multi-user Support:** Through Supabase Auth integration.
4.  **Advanced Alert Systems:** Via Twilio or Discord webhook notifications.
