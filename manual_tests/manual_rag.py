from app.services.retrieval import answer_question


question = "What is FastAPI?"

answer = answer_question(
    question=question,
    namespace="acme",
)

print("\nFinal Answer:")
print(answer)