from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# Point to the local Ollama instance running inside the container
OLLAMA_URL = "http://localhost:11434/api/generate"
VALID_KEYWORDS = ["esg", "sustainability", "carbon", "hvac", "water", "energy", "infrastructure", "waste", "power", "retrofit", "green", "emissions"]

class PromptRequest(BaseModel):
    prompt: str

def is_prompt_valid(prompt_text):
    return any(keyword in prompt_text.lower() for keyword in VALID_KEYWORDS)

@app.post("/generate")
def generate_esg_strategy(request: PromptRequest):
    if not is_prompt_valid(request.prompt):
        raise HTTPException(status_code=400, detail="Prompt rejected by Layer 1 Guardrail. Out of domain.")

    # The payload with your strict JSON instructions included
    full_prompt = f"""
    {request.prompt}
    
    CRITICAL NEGATIVE CONSTRAINTS:
    - DO NOT suggest solar panels, solar-powered devices, BIPV, or wind turbines anywhere on the campus.
    - Instead, use internal load-reduction and off-site energy procurement.

    CRITICAL INSTRUCTION: You must respond ONLY with a valid JSON object using this exact structure:
    {{
      "heritage_hvac_strategy": {{"solution": "...", "estimated_impact": "..."}},
      "electrical_grid_strategy": {{"solution": "...", "estimated_impact": "..."}},
      "waterlogging_strategy": {{"solution": "...", "estimated_impact": "..."}},
      "cloud_infrastructure_strategy": {{"solution": "...", "estimated_impact": "..."}}
    }}
    """

    payload = {
        "model": "vanvikalp-engine",
        "prompt": full_prompt,
        "format": "json",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        # Parse the string into actual JSON before sending it back to the frontend
        return json.loads(response.json()['response'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))