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

## 🔌 API Contract

The engine exposes a single `POST` endpoint at `/generate`. It is secured via Google Cloud IAM Identity Tokens.

**Request Payload:**
```json
{
    "prompt": "We are modernizing a heritage campus. The courtyard floods, the grid is overloaded, and we need to cool the old buildings without adding solar panels. Provide an ESG strategy."
}
