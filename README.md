# NebulaX API

Exoplanet analysis and light curve detection API backend built with FastAPI.

## Features

- Exoplanet catalog management with NASA data integration
- Light curve analysis for transit detection
- Machine learning classification for exoplanet candidates
- Real-time model training and prediction
- Configurable CORS for development and production
- Automatic database initialization

## Requirements

- Python 3.12+
- FastAPI 0.104.1+
- Uvicorn 0.24.0+
- Scikit-learn 1.3.2+
- Pandas 2.0.3+
- NumPy 1.24.3+

## Installation

1. Clone the repository:
```sh
git clone https://github.com/your-username/nebula-x-backend.git
cd nebula-x-backend
```

2. Install dependencies:
```sh 
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```sh
cp .env.example .env
# Edit .env with your configuration
```

## Running

Start the development server:

```sh
uvicorn app.main:app --reload
```

The server will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /health` - Check API status
- `GET /version` - Get current API version

### Exoplanets
- `GET /exoplanets` - List exoplanets with filters
  - Query parameters: `mission`, `status`, `limit`, `offset`
- `GET /exoplanets/refresh` - Refresh catalog from NASA data

### Analysis
- `POST /analysis/lightcurve` - Analyze light curve data
- `POST /analysis/train` - Train ML classification model
- `POST /analysis/predict` - Predict exoplanet classification

## Project Structure

```
app/
├── api/           # API route handlers
│   ├── analysis.py
│   ├── exoplanets.py
│   └── health.py
├── core/          # Core configuration
│   ├── config.py
│   └── cors.py
├── schemas/       # Pydantic models
│   ├── analysis.py
│   └── exoplanet.py
├── services/      # Business logic
│   ├── analysis.py
│   ├── data_processor.py
│   ├── exoplanets.py
│   ├── ml_service.py
│   └── nasa_api.py
├── utils/         # Utility functions
│   └── responses.py
└── main.py        # FastAPI application
```


## Configuration

Main configuration settings in `app/core/config.py`:

- `API_NAME` - API name
- `API_VERSION` - Current version
- `ALLOWED_ORIGINS` - CORS allowed origins
- `FRONTEND_URL` - Frontend application URL

## Data Models

### Exoplanet
- Mission: Kepler, K2, TESS
- Status: Confirmed, Candidate, False Positive
- Properties: period, radius, temperature, habitable zone

### Light Curve Analysis
- Input: time series flux data points
- Output: transit detection and confidence score

## Machine Learning

The API includes ML capabilities for exoplanet classification:
- Training on NASA exoplanet data
- Real-time prediction with confidence scores
- Model persistence and reloading

## License

MIT