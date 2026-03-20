# VanVikalp AI Engine: Environment as a Service (EaaS) 🍃

VanVikalp is an enterprise-grade Environment as a Service (EaaS) platform designed to help corporations transition their physical infrastructure toward sustainability. This repository houses the core **Serverless Generative AI Engine**, which processes complex architectural, electrical, and HVAC constraints to output strict, actionable ESG (Environmental, Social, and Governance) strategies.



## 🏗️ System Architecture

To ensure cost-efficiency during prototyping while maintaining enterprise scalability, the AI engine is completely decoupled from the frontend UI. 

* **Base Model:** Llama-3 (Quantized to 4-bit `.gguf` for memory efficiency)
* **Fine-Tuning:** Custom LoRA adapters (`/lora_adapters`) trained on synthetic ESG compliance and heritage building data.
* **Inference Engine:** [Ollama](https://ollama.com/) running headless inside a Docker container.
* **API Gateway:** FastAPI & Uvicorn routing strict JSON payloads.
* **Deployment:** Google Cloud Run (Serverless, scaled to 0-1 instances, 16GiB RAM constraint).

## 🚀 The Business Logic

The engine is instructed to act as an elite ESG consultant. It accepts multi-constraint scenarios (e.g., "cool this building, but you cannot use solar panels and the grid is overloaded") and returns structured strategies across four key pillars:
1. Heritage/HVAC Strategy
2. Electrical Grid Strategy
3. Waterlogging/Plumbing Strategy
4. Cloud IT Infrastructure Strategy


## 🔌 API Contract & Sample Output

To integrate the VanVikalp Engine into a frontend or external service, use the following specification.

### Sample Request
**Endpoint:** `POST /generate`  
**Headers:** `Authorization: Bearer <ID_TOKEN>`

```json
{
    "prompt": "We are modernizing the Calcutta University heritage campus. The courtyard floods, the grid is overloaded, and we need to cool the old buildings without adding solar panels. Provide an ESG strategy."
}

{
    "heritage_hvac_strategy": {
        "solution": "High-Performance Radiant Cooling System",
        "estimated_impact": "Reduce energy consumption by 30%, improve indoor air quality, and preserve heritage building integrity"
    },
    "electrical_grid_strategy": {
        "solution": "Off-Site Energy Procurement through a nearby data center's waste heat reuse program",
        "estimated_impact": "Reduce peak demand on the grid by 25%, minimize infrastructure upgrades, and achieve cost savings"
    },
    "waterlogging_strategy": {
        "solution": "Rainwater Harvesting with Grey Water Reuse System for irrigation and flushing toilets",
        "estimated_impact": "Reduce stormwater runoff by 50%, conserve potable water, and create a self-sustaining ecosystem"
    },
    "cloud_infrastructure_strategy": {
        "solution": "Migrate campus IT infrastructure to a cloud-based platform with energy-efficient data centers",
        "estimated_impact": "Reduce on-site energy consumption by 40%, minimize e-waste generation, and enhance disaster recovery capabilities"
    }
}