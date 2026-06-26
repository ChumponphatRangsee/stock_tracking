# System Architecture Documentation

This document explains the high-level architecture of the Stock Monitor platform (V2), explaining how components interact across different boundaries.

---

## 1. High-Level Architecture Flow

```text
       [React UI Frontend]
               │
               ▼  (HTTP REST)
       [FastAPI Controllers]  (Router endpoints in app/api/routes)
               │
               ▼  (Dependency Injection / DB Session)
      [Domain Service Layer]  (app/services/stock_service, ingestion_service)
         │               │
         │               ▼  (Domain Scoring Engine)
         │       [app/scoring/] (Pure mathematical scoring strategies)
         │
         ▼  (Interfaces / Factory Pattern)
     [app/providers/]
         │
         ├───> [YahooProvider]   ───> Yahoo Finance Scraper
         └───> [FinnhubProvider] ───> Finnhub API (REST)
```

---

## 2. Layer Definitions

### A. The Controller Layer (`app/api/`)
FastAPI handles incoming REST requests and maps inputs and outputs through **Pydantic schemas**.
*   *Separation of Concerns:* The controllers never make raw SQL queries or fetch external APIs. They only talk to the **Domain Service Layer** and return validated JSON.

### B. The Domain Service Layer (`app/services/`)
Coordinates business logic.
*   **`DataIngestionService`:** Orchestrates third-party API data fetching and formats inputs for database snapshot inserts. It uses the `ProviderFactory` layer to fetch data, making it completely vendor-agnostic.
*   **`StockService`:** Computes Quality, Valuation, Discount, Analyst, and Opportunity Scores. It fetches the latest snapshot records from the database, feeds them into the math components, and commits the calculated scores to the `stock_scores` table.
*   **`QuotaService`:** Tracks daily request usage against free limits in the database to prevent API throttling.

### C. The Scoring Engine (`app/scoring/`)
A pure mathematical domain layer containing calculation logic for the 5 different stock scores.
*   *Side-effect free:* These functions do not connect to any database or make HTTP requests. They are pure inputs-to-outputs converters, making them exceptionally easy to unit-test.

### D. The Adapter Layer (`app/providers/`)
Standardizes communication with external vendors.
*   **`MarketDataProvider`, `FinancialDataProvider`, and `AnalystDataProvider`**: Abstract base classes defining the structural interface.
*   **`YahooProvider` & `FinnhubProvider`**: Individual adapters implementing the interfaces. 
*   **`ProviderFactory`**: Instantiates and delivers the correct adapter. If we ever swap Finnhub for Polygon, we *only* change the provider implementation and register it in the Factory.

### E. Database Access & Infrastructure (`app/models/`, `app/core/`)
*   **`app/models/`**: Defines SQLAlchemy ORM structural database models. All snapshot tables utilize composite primary keys (`ticker` + `date`).
*   **`app/core/database.py`**: Configures the PostgreSQL engine pool and session generator.
