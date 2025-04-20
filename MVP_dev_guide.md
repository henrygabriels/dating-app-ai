Dating App MVP Guide

Overview
This project reimagines the classic OKCupid-style compatibility questionnaire for the AI era. Users engage in natural conversation with an AI that intelligently selects and phrases questions from our database. Their responses generate shareable compatibility scores and inform matchmaking.

Core Architecture
[React Frontend] ↔ [FastAPI Backend] ↔ [OpenRouter LLM]
       │                  │
       └── Clerk Auth ────┘

Development Note:
For initial development and testing of the chat flow, Clerk authentication will be temporarily bypassed. 
This allows testing core functionality before implementing proper auth. Steps:
1. Comment out Clerk middleware/guards in backend
2. Skip auth token validation temporarily
3. Use a mock user ID for testing (e.g. "test_user_1")
4. Re-enable auth once core functionality is verified

Essential Components

1. Backend (Python/FastAPI)

Key Features:
Clerk authentication integration
Conversation state management
LLM response orchestration
Basic scoring calculation
Question database from CSV

MVP Endpoints:
# Authentication
POST /auth/clerk-webhook

# Conversation
POST /conversation/start → { "conversation_id": str }
POST /conversation/{id}/response → { "next_question": str, "score_updates": dict }
GET /conversation/{id}/scores → { "scores": dict }

# User Data
GET /profile → { "matches": list, "conversation_history": list }

2. Frontend (React)

Key Features:

Conversational UI flow
Score visualization
Match preview cards
Shareable score links

Critical Integration Points:

// API Client Setup
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  withCredentials: true
});

// Conversation Flow
async function handleResponse(response) {
  await api.post(`/conversation/${convoId}/response`, {
    answer: response,
    question_id: currentQuestion.id
  });
}

3. LLM Integration

MVP Workflow:
1. Load CSV questions into categorized database
Maintain conversation history buffer (last 5 messages)
3. For each interaction:
Use LLM to select next question from CSV
Generate natural phrasing for question
Extract structured data from responses
Update compatibility scores

Simplified Prompt:
You're helping users find romantic matches through conversation.
Your tasks:
1. Select next question from this list: {unasked_questions}
2. Phrase it conversationally
3. Extract key preferences from their response

Current conversation: {history}
Last response: {user_input}

Respond with JSON: {
  "next_question_id": str,
  "phrased_question": str,
  "extracted_data": {key: value}
}

Data Management
Essential Models

class User(BaseModel):
    id: str
    conversation_state: dict
    raw_responses: list
    scores: dict

class Question(BaseModel):
    id: str
    original_text: str
    category: str
    weight: float


Deployment Basics

Backend:
Railway.app with PostgreSQL / SQLite (I'm building on a Mac, sometimes SQLite is easier)
Environment variables for:
CLERK_SECRET_KEY
OPENROUTER_API_KEY
DATABASE_URL

Frontend:
Vercel deployment

Environment variables:
REACT_APP_API_URL
CLERK_PUBLISHABLE_KEY

Critical Path Timeline
1. Week 1: Auth flow + Basic API
2. Week 2: LLM conversation integration
3. Week 3: Scoring system + Frontend UI
4. Week 4: Testing + First launch
MVP Security
1. Clerk authentication only
2. Rate limiting (100 requests/hour/user)
3. Input validation:
   @app.post("/conversation/response")
   async def submit_response(
       response: str = Body(..., max_length=500),
       question_id: str = Body(...)
   ):
Key Technical Decisions
1. Conversation State: Store in Redis with 24h TTL
2. Scoring: Simple weighted average per category
3. LLM Choice: Start with a cheap model via OpenRouter
4. Error Handling: Global error boundary in React + Sentry basic setup