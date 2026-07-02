from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import detect_intent, needs_clarification
from rag.retrieve import retrieve
from app.llm import generate_reply
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("SHL Assessment Recommendation Agent")
    logger.info("=" * 60)
    logger.info("A conversational AI agent that recommends SHL Individual")
    logger.info("Test Solutions based on hiring requirements.")
    logger.info("")
    logger.info("Available Endpoints:")
    logger.info("GET  /health   -> Health check")
    logger.info("POST /chat     -> Chat with the recommendation agent")
    logger.info("")
    logger.info("Swagger UI: http://127.0.0.1:8000/docs")
    logger.info("=" * 60)
    yield


app = FastAPI(lifespan=lifespan)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


def build_search_query(messages):
    user_messages = []

    for msg in messages:
        if msg.role == "user":
            user_messages.append(msg.content)

    return " ".join(user_messages)


@app.get("/")
def root():
    return {
        "app": "SHL Assessment Recommendation Agent",
        "endpoints": {
            "health": "GET /health",
            "chat": "POST /chat",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):

    latest_user_message = ""

    for msg in reversed(req.messages):
        if msg.role == "user":
            latest_user_message = msg.content
            break

    intent = detect_intent(req.messages)
    if intent == "clarify":
        return {
            "reply": (
                "I'd be happy to help. "
                "Could you tell me:\n"
                "- Which role are you hiring for?\n"
                "- Seniority level?\n"
                "- Any specific technical or behavioural skills?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }
    if intent == "refuse":
        return {
            "reply": (
                "I'm designed to help only with SHL assessment "
                "recommendations and comparisons."
            ),
            "recommendations": [],
            "end_of_conversation": True
        }

    search_query = build_search_query(req.messages)
    docs = retrieve(search_query)
    logger.info(f"Intent: {intent}")
    logger.info(f"Query: {search_query}")
    logger.info(f"Retrieved: {len(docs)} documents")

    intent = detect_intent(req.messages)
    answer = generate_reply(latest_user_message, docs)
    questions = needs_clarification(req.messages)

    if questions:
        return {
            "reply": "\n".join(questions),
            "recommendations": [],
            "end_of_conversation": False
        }

    recommendations = []

    for d in docs:
        recommendations.append(
            {
                "name": d["title"],
                "url": d["url"],
                "test_type": "Assessment"
            }
        )

    return {
        "reply": answer,
        "recommendations": recommendations,
        "end_of_conversation": False
    }