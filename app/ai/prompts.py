# File: app/ai/prompts.py
"""
Prompt templates for content generation.
"""

# System prompt for all educational content generation
SYSTEM_PROMPT = """You are an expert educational content creator and professor's assistant. 
Your role is to help create high-quality educational materials based on lecture transcripts and course materials.

Guidelines:
- Create clear, well-structured content appropriate for university students
- Focus on key concepts and learning objectives
- Use academic but accessible language
- Ensure accuracy based on the provided source material
- Output all responses in valid JSON format as specified"""


# Notes generation prompt
NOTES_PROMPT = """Based on the following lecture transcript and course context, generate comprehensive lecture notes.

LECTURE TRANSCRIPT:
{transcript}

RELEVANT COURSE CONTEXT:
{context}

LECTURE TITLE: {lecture_title}

Generate structured notes in the following JSON format:
{{
    "title": "Lecture Notes: [Topic]",
    "summary": "A 2-3 sentence summary of the lecture content",
    "sections": [
        {{
            "heading": "Section heading",
            "content": "Detailed content for this section (2-4 paragraphs)",
            "key_points": ["Key point 1", "Key point 2", "Key point 3"]
        }}
    ],
    "key_takeaways": ["Main takeaway 1", "Main takeaway 2", "Main takeaway 3"],
    "vocabulary": [
        {{"term": "Technical term", "definition": "Clear definition"}}
    ],
    "further_reading": ["Topic to explore further"]
}}

Create 3-5 sections covering the main topics discussed. Each section should have 2-4 key points.
Ensure the notes are comprehensive yet concise, suitable for exam preparation."""


# Assignment generation prompt
ASSIGNMENT_PROMPT = """Based on the following lecture content and course context, generate a practice assignment.

LECTURE TRANSCRIPT:
{transcript}

RELEVANT COURSE CONTEXT:
{context}

LECTURE TITLE: {lecture_title}

Generate an assignment in the following JSON format:
{{
    "title": "Practice Questions: [Topic]",
    "description": "Brief description of what this assignment covers",
    "total_points": 100,
    "questions": [
        {{
            "type": "mcq",
            "question": "Multiple choice question text",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct_answer": "A",
            "explanation": "Why this is the correct answer",
            "points": 10,
            "difficulty": "easy"
        }},
        {{
            "type": "short_answer",
            "question": "Short answer question text",
            "expected_answer": "Expected answer content",
            "keywords": ["key", "words", "to", "look", "for"],
            "points": 15,
            "difficulty": "medium"
        }},
        {{
            "type": "long_answer",
            "question": "Essay or long answer question",
            "rubric": "What should be included for full marks",
            "points": 25,
            "difficulty": "hard"
        }}
    ]
}}

Generate a balanced mix of:
- 3-4 MCQ questions (testing recall and understanding)
- 2-3 Short answer questions (testing application)
- 1-2 Long answer questions (testing analysis and synthesis)

Ensure questions progress from easier to harder and cover key topics from the lecture."""


# Flashcard generation prompt
FLASHCARDS_PROMPT = """Based on the following lecture content and course context, generate study flashcards.

LECTURE TRANSCRIPT:
{transcript}

RELEVANT COURSE CONTEXT:
{context}

LECTURE TITLE: {lecture_title}

Generate flashcards in the following JSON format:
{{
    "title": "Flashcards: [Topic]",
    "description": "Flashcards for studying [topic]",
    "cards": [
        {{
            "front": "Question or term (keep concise)",
            "back": "Answer or definition (clear and complete)",
            "difficulty": "easy"
        }},
        {{
            "front": "What is [concept]?",
            "back": "Definition and key characteristics",
            "difficulty": "medium"
        }}
    ]
}}

Generate 10-15 flashcards that:
- Cover all major concepts from the lecture
- Include definitions, formulas, processes, and key facts
- Progress from basic recall to more complex concepts
- Use clear, concise language on both sides
- Include a mix of easy (40%), medium (40%), and hard (20%) cards"""


def get_notes_prompt(transcript: str, context: str, lecture_title: str) -> str:
    """Format the notes generation prompt."""
    return NOTES_PROMPT.format(
        transcript=transcript[:8000],  # Limit transcript length
        context=context[:4000],  # Limit context length
        lecture_title=lecture_title
    )


def get_assignment_prompt(transcript: str, context: str, lecture_title: str) -> str:
    """Format the assignment generation prompt."""
    return ASSIGNMENT_PROMPT.format(
        transcript=transcript[:8000],
        context=context[:4000],
        lecture_title=lecture_title
    )


def get_flashcards_prompt(transcript: str, context: str, lecture_title: str) -> str:
    """Format the flashcards generation prompt."""
    return FLASHCARDS_PROMPT.format(
        transcript=transcript[:8000],
        context=context[:4000],
        lecture_title=lecture_title
    )
