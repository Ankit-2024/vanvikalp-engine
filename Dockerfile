FROM python:3.10-slim

# Install curl and the new zstd unzipper, then download and extract the updated archive
RUN apt-get update && apt-get install -y curl zstd && \
    curl -L https://ollama.com/download/ollama-linux-amd64.tar.zst -o ollama.tar.zst && \
    tar -I zstd -xf ollama.tar.zst -C /usr && \
    rm ollama.tar.zst

WORKDIR /app

# Copy the weights (downloaded by cloudbuild.yaml) and the Modelfile
COPY esg-eaas-model-001.gguf .
COPY Modelfile .

# Bake the model into the Ollama registry so it is ready on boot
RUN nohup bash -c "ollama serve &" && \
    sleep 5 && \
    ollama create vanvikalp-engine -f Modelfile

# Install Python API dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API gateway code and startup script
COPY app.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]