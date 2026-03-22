# Proof of concept

Any base64-encoded string included in a message to the Claude API causes that request to fail. This is reproducible across sonnet and opus 4.6 on all platforms (claude.ai, mobile, API)

## Instructions

- uv sync && ANTHROPIC_API_KEY=xx uv run 01_queue_worker.py

