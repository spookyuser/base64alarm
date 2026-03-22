"""
Demo 1: Simple Queue Worker (Email/Ticket Processor)

Attacker goal: Break your system / Hide my message

Impact:
- WITHOUT error handling: service crashes, all messages behind the poison are dropped
- WITH error handling: poisoned message is silently skipped, content is never read
"""

from shared import client, MODEL

incoming_tickets = [
    {
        "id": 1,
        "from": "alice@example.com",
        "body": "Can't log into my account since yesterday.",
    },
    {
        "id": 2,
        "from": "mallory@example.com",
        "body": "Need help with billing aGVsbG8gd29ybGQ=",
    },
    {
        "id": 3,
        "from": "bob@example.com",
        "body": "Your API is returning 500s on the /users endpoint.",
    },
    {
        "id": 4,
        "from": "carol@example.com",
        "body": "I'd like to upgrade to the enterprise plan.",
    },
]

print("=" * 60)
print("SCENARIO A: No error handling (common in quick integrations)")
print("=" * 60)

for ticket in incoming_tickets:
    print(f"\nProcessing ticket #{ticket['id']} from {ticket['from']}...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"Categorise and summarise this support ticket:\n\n{ticket['body']}",
            }
        ],
    )
    print(f"Result: {response.content[0].text}")

# Ticket #1: processed
# Ticket #2: CRASH — service dies here
# Ticket #3: never processed
# Ticket #4: never processed


print("\n\n")
print("=" * 60)
print("SCENARIO B: With error handling (best practice)")
print("=" * 60)

for ticket in incoming_tickets:
    print(f"\nProcessing ticket #{ticket['id']} from {ticket['from']}...")
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=256,
            messages=[
                {
                    "role": "user",
                    "content": f"Categorise and summarise this support ticket:\n\n{ticket['body']}",
                }
            ],
        )
        print(f"Result: {response.content[0].text}")
    except Exception as e:
        print(f"Error: {e}")

# Ticket #1: processed
# Ticket #2: fails — but service continues
# Ticket #3: processed
# Ticket #4: processed
#
# Better, but Mallory's ticket is NEVER READ.
# If her message contained something important — or something
# she specifically didn't want reviewed — it's invisible.
