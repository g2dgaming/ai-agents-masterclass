# Use the official n8n image as the base
FROM n8nio/n8n:latest

# Switch to root user to install system packages
USER root

# Install necessary packages using apk
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    curl \
    pnpm

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"


# Set the working directory
WORKDIR /app

# Clone the spotify_mcp project
RUN git clone https://github.com/varunneal/spotify-mcp.git

RUN git clone https://github.com/g2dgaming/mcp-media-manager

WORKDIR /app/mcp-media-manager

RUN pnpm install

RUN pnpm run build

COPY .env.mcp_sonarr_radarr .env


WORKDIR /app/spotify-mcp

COPY .cache.spotify_mcp .cache

WORKDIR /app


# Create n8n custom nodes directory and install n8n-nodes-mcp
RUN mkdir -p /root/.n8n/nodes && \
    cd /root/.n8n/nodes && \
    npm install n8n-nodes-mcp

