"""
Demo 5: Platform Poisoning (Shared Content Ingestion)

Attacker goal: Break everyone's systems at once
Pattern: Multiple independent Claude-powered agents reading from a shared platform

Impact:
- Attacker posts ONE piece of content containing base64 to a public platform
- Every Claude-powered agent that reads that content is affected
- Summarisers, scrapers, analysts, moderation bots — all hit the same tripwire
- One post, N failures across N independent systems
- Attacker doesn't need to know who's reading — the blast radius is indiscriminate
"""

from shared import client, MODEL

# Shared platform content (e.g. a forum, social network, review site, wiki)
platform_posts = [
    {
        "id": 1,
        "author": "normal_user",
        "content": "Great product, highly recommend to everyone.",
    },
    {
        "id": 2,
        "author": "mallory",
        "content": "Nice discussion! Here's my notes: aGVsbG8gd29ybGQ=",
    },
    {
        "id": 3,
        "author": "normal_user2",
        "content": "Does anyone know when the next update drops?",
    },
]

# Multiple independent agents all read from the same platform
agents = [
    {"name": "Sentiment Analyser", "prompt": "Analyse the sentiment of this post:"},
    {"name": "Content Summariser", "prompt": "Summarise this post in one line:"},
    {"name": "Moderation Bot", "prompt": "Check this post for policy violations:"},
    {"name": "Trend Tracker", "prompt": "Extract key topics from this post:"},
]

print("Simulating multiple Claude agents reading the same platform...\n")

for post in platform_posts:
    print(f"{'=' * 60}")
    print(f"Post #{post['id']} by {post['author']}: {post['content'][:50]}...")
    print(f"{'=' * 60}")

    for agent in agents:
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=128,
                messages=[
                    {
                        "role": "user",
                        "content": f"{agent['prompt']}\n\n{post['content']}",
                    }
                ],
            )
            print(f"  {agent['name']}: {response.content[0].text[:80]}")
        except Exception as e:
            print(f"  {agent['name']}: ❌ FAILED")

    print()

# Post #1: All 4 agents process it successfully
# Post #2: All 4 agents FAIL — one post, four casualties
# Post #3: All 4 agents process it successfully
#
# Mallory posted once. She doesn't know or care which agents are reading.
# Every Claude-powered system that ingests that post breaks.
# If this were a popular post on a major platform, the blast radius
# could be hundreds of independent services all failing simultaneously.
