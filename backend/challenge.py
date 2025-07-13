from langchain_ollama import OllamaLLM
import re

def generate_challenge_questions(text, num=3):
    llm = OllamaLLM(model="mistral")

    prompt = f"""
From the document below, generate {num} logic-based or comprehension-focused questions that test a user's understanding and inference ability.

Document:
{text[:1500]}

Respond with numbered questions only.
"""
    response = llm.invoke(prompt)
    
    raw_lines = re.split(r"\n?\d+[\).] ", response.strip())
    questions = [q.strip() for q in raw_lines if len(q.strip().split()) > 3]

    return questions[:num]

def evaluate_answers(questions, answers, document_text):
    llm = OllamaLLM(model="mistral")
    results = []

    for q, a in zip(questions, answers):
        prompt = f"""
                You are a document-based evaluator.

                Evaluate the user's answer based on the document.

                Question: {q}
                User Answer: {a}

                Document:
                {document_text[:1500]}

                Respond in this format:
                1. Evaluation: (Correct / Partially Correct / Incorrect)
                2. Justification: (with reference to the document)
                """
        response = llm.invoke(prompt)
        results.append(response.strip())

    return results
