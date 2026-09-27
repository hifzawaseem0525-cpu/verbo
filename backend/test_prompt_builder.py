"""
test_prompt_builder.py
-----------------------
Standalone test for Verbo's prompt-generation system.

This does NOT call Gemini.
"""

from prompt_builder import build_prompt


prompt = build_prompt(
    topic="Artificial Intelligence in Education",
    mode="Research Article",
    length="Long",
    tone="Academic",
    audience="Professional",
    complexity="Advanced",
    custom_instructions="Mention both benefits and risks.",
)


print("=" * 70)
print("VERBO PROMPT BUILDER TEST")
print("=" * 70)
print()
print(prompt)
print()
print("=" * 70)
print("PROMPT BUILDER TEST COMPLETED")
print("=" * 70)