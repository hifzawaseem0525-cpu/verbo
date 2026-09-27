"""
config.py
----------
Central place for all dropdown options and tunables.
"""

import os

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

MODES = {
    "Basic": [
        "Normal / General",
        "Detailed Explanation",
        "Summary",
    ],
    "Academic": [
        "Research Article",
        "Literature Review",
        "Abstract",
    ],
    "Professional": [
        "Professional Email",
        "Resume Content",
        "LinkedIn Post",
    ],
    "Creative": [
        "Story",
        "Blog",
        "Social Media Caption",
    ],
}

LENGTHS = [
    "Very Short",
    "Short",
    "Medium",
    "Long",
    "Very Long",
]

LENGTH_GUIDANCE = {
    "Very Short": "about 40-60 words",
    "Short": "about 100-150 words",
    "Medium": "about 250-350 words",
    "Long": "about 500-700 words",
    "Very Long": "about 900-1200 words, thorough and detailed",
}

TONES = [
    "Neutral",
    "Professional",
    "Academic",
    "Friendly",
    "Persuasive",
    "Casual",
    "Creative",
]

AUDIENCES = [
    "General Public",
    "School Student",
    "College Student",
    "Professional",
    "Researcher",
    "Customer",
]

COMPLEXITY_LEVELS = [
    "Beginner",
    "Intermediate",
    "Advanced",
]