from config import APIModelConfig, initialize_client

SYSTEM_PROMPT = """
You are a synthetic dataset generator.
You create data that looks realistic.
Do not repeat the same data record.
The dataset must be diverse.
Never include or wrap response in markdown, code fences, or any explanation.
The response must be only a valid JSON array.
"""

def generate(
    prompt: str,
    num_records: int,
    model_config: APIModelConfig,
) -> str:
    user_prompt = f"""
    {prompt}
    Generate {num_records} records as a JSON array.
    """
    
    client = initialize_client(model_config)
    response = client.chat.completions.create(
        model = model_config.model_id,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
    )
    return response.choices[0].message.content.strip()