"""
prompt_builder.py
------------------
Pure functions that turn user settings into structured prompts.

No API calls happen here.
This file can be tested completely offline.
"""

from config import LENGTH_GUIDANCE


# ============================================================
# GENERATION MODE INSTRUCTIONS
# ============================================================

MODE_INSTRUCTIONS = {
    "Research Article": """
Structure the output with these exact headings, in order:

1. Title
2. Introduction
3. Background
4. Main Discussion
5. Key Findings / Insights
6. Advantages / Disadvantages (only if relevant)
7. Conclusion
8. Suggested Areas for Further Research

Honesty rules:
- Do NOT invent citations, paper titles, author names, URLs, or statistics.
- Begin the output with:
  "*(AI-generated research-style content — not sourced from verified external references.)*"
""",

    "Literature Review": """
Structure the output as a literature-review-style discussion covering
general themes, common approaches, and open questions in this area.

Do NOT invent specific paper titles, authors, or publication years.
Discuss the topic in terms of general research findings and themes.
""",

    "Abstract": """
Write a single concise abstract paragraph of approximately 150-250 words
summarizing the purpose, approach, and key takeaway in formal academic style.
""",

    "Professional Email": """
Format the output as a complete, ready-to-send email including:

Subject:
Greeting:
Body:
Closing:
Sign-off:
""",

    "Resume Content": """
Use concise, achievement-oriented, action-verb-led bullet points
appropriate for a resume or professional profile.
""",

    "LinkedIn Post": """
Write in a first-person, engaging professional-networking voice.

Start with a strong hook and end with a natural call-to-engagement.
""",

    "Social Media Caption": """
Keep the caption short, punchy, and platform-appropriate.

Include 2-3 relevant hashtags at the end.
""",
}


# ============================================================
# GENERATION PROMPT
# ============================================================

def build_prompt(
    topic: str,
    mode: str,
    length: str,
    tone: str,
    audience: str,
    complexity: str = "Intermediate",
    custom_instructions: str = "",
) -> str:
    """
    Build the complete instruction prompt that will be
    sent to Gemini.
    """

    length_guidance = LENGTH_GUIDANCE.get(
        length,
        "a reasonable length"
    )

    lines = [
        (
            "You are an expert writing assistant. Generate content "
            "based on the following specification. Follow every "
            "instruction precisely and output ONLY the final content "
            "— no meta-commentary about what you are about to do."
        ),

        "",

        f'Topic provided by the user: "{topic.strip()}"',

        "",

        f"Content mode: {mode}",
        f"Target length: {length} ({length_guidance})",
        f"Tone: {tone}",
        f"Target audience: {audience}",
        f"Complexity level: {complexity}",
    ]

    mode_instruction = MODE_INSTRUCTIONS.get(mode)

    if mode_instruction:
        lines.append(mode_instruction)

    if custom_instructions and custom_instructions.strip():
        lines.append(
            "Additional instruction from the user: "
            f"{custom_instructions.strip()}"
        )

    lines.append("")
    lines.append("Now produce the final content only.")

    return "\n".join(lines)


# ============================================================
# TEXT TRANSFORMATION INSTRUCTIONS
# ============================================================

TRANSFORM_INSTRUCTIONS = {
    "Summarize":
        "Summarize the following text, keeping only the most important points.",

    "Expand":
        "Expand the following text with more detail, explanation, and supporting points.",

    "Simplify":
        "Rewrite the following text using simple and easy-to-understand language.",

    "Rewrite":
        "Rewrite the following text using different wording while keeping the same meaning.",

    "Improve Grammar":
        "Correct grammar, spelling, and punctuation without changing the meaning.",

    "Make Professional":
        "Rewrite the following text in a professional and polished tone.",

    "Make Academic":
        "Rewrite the following text in a formal academic tone.",

    "Convert to Bullet Points":
        "Convert the following text into clear, well-organized bullet points.",

    "Change Tone":
        "Rewrite the following text in the requested tone.",
}


# ============================================================
# TRANSFORMATION PROMPT
# ============================================================

def build_transform_prompt(
    text: str,
    transform_type: str,
    target_tone: str = "",
) -> str:
    """
    Build the prompt used when transforming existing text.
    """

    instruction = TRANSFORM_INSTRUCTIONS.get(
        transform_type,
        "Rewrite the following text while preserving its meaning.",
    )

    if transform_type == "Change Tone" and target_tone.strip():
        instruction = (
            f"Rewrite the following text in a "
            f"{target_tone.strip()} tone."
        )

    return (
        f"{instruction}\n\n"
        "Output ONLY the transformed text. "
        "Do not add explanations or commentary.\n\n"
        f'Text:\n"""\n{text.strip()}\n"""'
    )
