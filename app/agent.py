def detect_intent(messages):

    latest = ""

    for msg in reversed(messages):
        if msg.role == "user":
            latest = msg.content.lower()
            break

    if "compare" in latest or "difference" in latest:
        return "compare"

    banned = [
        "salary",
        "visa",
        "legal",
        "politics",
        "cricket",
        "weather",
        "movie"
    ]

    if any(word in latest for word in banned):
        return "refuse"

    vague = [
        "assessment",
        "hire",
        "hiring",
        "test"
    ]

    if len(latest.split()) < 5:
        return "clarify"

    if latest.strip() in vague:
        return "clarify"

    return "recommend"


def needs_clarification(messages):

    text = " ".join(
        m.content.lower()
        for m in messages
        if m.role == "user"
    )

    questions = []

    if not any(word in text for word in [
        "developer", "engineer", "manager",
        "analyst", "sales", "java", "python"
    ]):
        questions.append("What role are you hiring for?")

    if not any(word in text for word in [
        "junior", "mid", "senior", "years"
    ]):
        questions.append("What seniority level is the role?")

    return questions