# Dating App

A modern dating app that uses AI-driven conversations to create meaningful matches.

## Project Structure

```
dating_app/
├── backend/             # FastAPI backend
│   ├── app/            # Application code
│   │   ├── __init__.py
│   │   ├── main.py    # FastAPI application
│   │   ├── models.py  # Database models
│   │   ├── routes.py  # Conversation endpoints
│   │   ├── discovery_routes.py  # User discovery & messaging
│   │   ├── auth.py    # Authentication
│   │   ├── database.py # Database configuration
│   │   └── conversation.py # LLM conversation handling
│   ├── Questions Sheet1.csv  # Question database
│   ├── requirements.txt
│   ├── .env           # Environment variables
│   └── .env.example   # Environment template
│
└── frontend/          # React frontend (coming soon)
```

## Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 with documentation at http://localhost:8000/docs

## Frontend Setup

Coming soon!