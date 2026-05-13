FROM python:3.10-slim

# Install system dependencies for a "Workstation"
RUN apt-get update && apt-get install -y \
    curl git vim nodejs npm sudo procps \
    && rm -rf /var/lib/apt/lists/*

# Set up the Agent user
RUN useradd -m agent
WORKDIR /home/agent/workspace
USER agent

# Initialize Agent Memory System
COPY agent_logic/brain.py /home/agent/brain.py
RUN pip install openai requests chromadb

# Standard Environment Variables
ENV PATH="/home/agent/.local/bin:${PATH}"

# Keep the virtual PC alive
CMD ["tail", "-f", "/dev/null"]