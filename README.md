# Saylani Medical Analytical Dashboard

An AI-powered analytics platform designed to provide actionable insights into medical help desk operations. This system processes patient data, generates a structured knowledge base, and provides an interactive dashboard with an intelligent chatbot assistant.

## Key Features

- **Automated Data Pipeline**: robust data cleaning and exploratory data analysis (EDA) to prepare raw patient records for insights.
- **JSON Knowledge Base**: Automatically generates a structured JSON knowledge base from analytics data for efficient querying.
- **AI Analytics Chatbot**: Powered by Google's **Gemini 2.0 Flash**, the chatbot answers questions about disease trends, doctor workloads, and geographic distribution.
- **Smart Query Routing**: The system intelligently distinguishes between analytics queries (answered by data) and medical advice questions (redirected with a safety disclaimer).
- **Interactive Dashboard**: A Streamlit-based UI featuring dynamic charts, metrics, and a chat interface.
- **FastAPI Backend**: A high-performance API server handling data retrieval and LLM interactions.
- **Resilient Architecture**: Implements automatic fallback mechanisms to ensure the system remains operational even if the external AI API is unavailable.

## Technology Stack

- **Language**: Python 3.10+
- **Frontend**: Streamlit
- **Backend**: FastAPI, Uvicorn
- **AI/LLM**: Google Gemini 2.0 Flash
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn

## Project Structure

```text
SaylaniHealthMangementHelpDesk/
├── src/
│   ├── app.py                # Main FastAPI application with query routing
│   ├── dashboard.py          # Streamlit dashboard interface
│   ├── llm.py                # LLM integration (Gemini 2.0) with fallback logic
│   ├── json_kb.py            # Knowledge base loader and query engine
│   ├── json_kb_generator.py  # Script to generate JSON KB from data
│   ├── data_cleaning.py      # Data preprocessing pipeline
│   ├── eda_enhanced.py       # Exploratory Data Analysis generation
│   └── nlp.py                # NLP utilities
├── data/
│   ├── raw/                  # Raw input CSV files
│   ├── cleaned/              # Processed data files
│   ├── knowledge_base/       # Generated analytics_kb.json
│   └── eda_output/           # Generated static charts
├── tests/                    # Unit and integration tests
├── run_pipeline.bat          # One-click startup script
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Installation and Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/MuhammadHanzala-13/SaylaniMedicalAnalyticalDashboard.git
    cd SaylaniMedicalAnalyticalDashboard
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    -   Copy `.env.example` to a new file named `.env`.
    -   Add your Google Gemini API key:
        ```text
        GEMINI_API_KEY=your_api_key_here
        ```

## Usage

### Running the Full Pipeline
The easiest way to start the system is using the provided batch script. This script cleans the data, generates the knowledge base, starts the backend API, and launches the dashboard.

```bash
.\run_pipeline.bat
```

### Manual Startup
If you prefer to run components individually:

1.  **Generate Knowledge Base**:
    ```bash
    python src/json_kb_generator.py
    ```

2.  **Start Backend API**:
    ```bash
    uvicorn src.app:app --reload
    ```

3.  **Start Dashboard**:
    ```bash
    streamlit run src/dashboard.py
    ```

## API Endpoints

The FastAPI backend exposes the following endpoints:

-   `GET /`: System status and version.
-   `POST /chat/query`: Main chatbot endpoint. Handles query classification and response generation.
-   `GET /analytics/disease-trends`: Returns disease statistics.
-   `GET /analytics/doctor-workload`: Returns doctor performance metrics.
-   `GET /analytics/geographic-distribution`: Returns patient distribution by area.
-   `GET /analytics/summary`: Returns executive summary metrics.

## License

This project is intended for educational and demonstration purposes as part of the SMIT Bootcamp.
