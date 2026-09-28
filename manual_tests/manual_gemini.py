from app.services.llm import generate_answer


context = """
FastAPI is a modern Python web framework for building APIs.
It supports asynchronous programming and automatic API documentation.
"""

question = "What is FastAPI?"

answer = generate_answer(question, context)

print("Answer:")
print(answer)