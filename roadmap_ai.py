import ollama

def generate_roadmap(goal, duration, level):
    prompt = f"""
    Create a detailed learning roadmap.

    Goal: {goal}
    Duration: {duration}
    Level: {level}

    Include:
    - Weekly plan
    - Resources
    - Tools
    - Projects
    - Interview tips
    """

    response = ollama.chat(model="llama3.2", messages=[
        {"role":"user","content":prompt}
    ])

    return response["message"]["content"]
