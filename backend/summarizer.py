from langchain_ollama import OllamaLLM

def generate_summary(text, word_limit=150):
    llm = OllamaLLM(model="mistral")
    
    prompt = f"""
You are a helpful assistant. Summarize the following document in under {word_limit} words. 
Focus only on the main ideas and important facts.

Document:
{text[:500]}  # Limit text to avoid model overload
"""
    return llm.invoke(prompt).strip()
