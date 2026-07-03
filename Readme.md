# SHL Assessment Recommendation Agent

A conversational AI agent that recommends SHL Individual Test Solutions based on user hiring requirements.

## Features

- Conversational assessment recommendation
- Clarifies vague hiring requests
- Recommends relevant SHL assessments
- Compares SHL assessments
- Refuses off-topic queries
- FastAPI REST API

## Project Structure

```
SHL-ASSIGNMENT/
│
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── llm.py
│   └── scraper.py
│
├── rag/
│   └── retrieval.py
│
├── data/
│   └── catalog.json
│
├── requirements.txt
└── README.md
```

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

### Chat

```
POST /chat
```

Example request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I want to hire a Java developer."
    }
  ]
}
```

## Workflow

1. Load the SHL catalog.
2. Build embeddings for assessments.
3. Retrieve relevant assessments using semantic search.
4. Generate responses using Gemini.
5. Return assessment recommendations in the required format.
