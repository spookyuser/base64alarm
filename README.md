# Proof of concept

Any base64-encoded string included in a message to the Claude API causes that request to fail. This is reproducible across all models (onnet, Opus) and all platforms (claude.ai, mobile, API)

## Instructions


- uv sync && ANTHROPIC_API_KEY=xx uv run 01_queue_worker.py

