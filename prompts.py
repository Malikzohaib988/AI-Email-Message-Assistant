"""
prompts.py - Prompt Construction Module
AI Email & Message Assistant
Author: Generative AI Student

This module manages message categories, writing tones, and constructs
optimized prompts for the Groq Large Language Model API.
"""

# Available message categories (List data structure)
MESSAGE_TYPES = [
    "Professional Email",
    "Student Message",
    "Leave Application",
    "Formal Request"
]

# Available writing tones (List data structure)
TONES = [
    "Professional",
    "Polite",
    "Friendly"
]

# Category-specific guidance (Dictionary data structure)
CATEGORY_GUIDELINES = {
    "Professional Email": (
        "Structure as a formal email with a clear 'Subject:' line, respectful greeting, "
        "well-organized paragraphs, professional call-to-action or closing, and a formal sign-off (e.g., 'Best regards, [Your Name]')."
    ),
    "Student Message": (
        "Format as a concise, respectful student communication directed to a teacher, professor, or peer. "
        "Include a polite salutation, clear question or request, and courteous closing."
    ),
    "Leave Application": (
        "Structure as a standard formal leave request or application. Include a clear 'Subject: Leave Application - [Reason]', "
        "formal address, clear statement of dates/duration, specific reason, assurance of catching up on work/classes, and a formal closing."
    ),
    "Formal Request": (
        "Structure as an official administrative or organizational request with a clear 'Subject:' line, "
        "objective statement of need, justification, proposed next steps, and respectful sign-off."
    )
}

# Tone-specific guidance (Dictionary data structure)
TONE_GUIDELINES = {
    "Professional": (
        "Tone should be business-appropriate, courteous, concise, and articulate. Avoid slang or overly casual phrases."
    ),
    "Polite": (
        "Tone should be exceptionally warm, considerate, respectful, and appreciative. Use gentle courtesy phrases like 'I would appreciate', 'kindly'."
    ),
    "Friendly": (
        "Tone should be warm, approachable, collaborative, and conversational while still maintaining appropriate grammatical standards."
    )
}


def build_prompt(message: str, message_type: str = "Professional Email", tone: str = "Professional", include_urdu: bool = False, length_preference: str = "balanced") -> str:
    """
    Constructs an optimized prompt for the Groq LLM based on user inputs.

    Parameters:
        message (str): The raw user input message.
        message_type (str): The selected message category.
        tone (str): The chosen writing tone.
        include_urdu (bool): Whether to include an Urdu translation.
        length_preference (str): 'concise', 'balanced', or 'detailed'.

    Returns:
        str: The full constructed prompt string.
    """
    # Sanitize and validate inputs
    cleaned_message = message.strip() if message else ""
    cat_guide = CATEGORY_GUIDELINES.get(message_type, "Format clearly and appropriately.")
    tone_guide = TONE_GUIDELINES.get(tone, "Maintain a balanced, respectful tone.")

    length_instructions = {
        "concise": "Keep the message brief, direct, and to the point (1-2 short paragraphs).",
        "detailed": "Provide a comprehensive, fully elaborated message covering all nuances clearly.",
        "balanced": "Maintain standard, balanced length with necessary context and clarity."
    }.get(length_preference.lower(), "Maintain standard, balanced length.")

    urdu_instruction = ""
    if include_urdu:
        urdu_instruction = (
            "\n9. BONUS - URDU TRANSLATION: After providing the complete English message, "
            "add a divider '---' and provide an accurate, natural Urdu translation of the message under the heading '### اردو ترجمہ (Urdu Translation)'."
        )

    prompt = f"""You are a professional AI writing assistant.
Your task is to transform the user's rough, informal, or grammatically flawed message into an improved, polished, and ready-to-send message.

Message Category: {message_type}
Category Guidelines: {cat_guide}

Writing Tone: {tone}
Tone Guidelines: {tone_guide}

Length Preference: {length_instructions}

Original Rough Message:
\"\"\"
{cleaned_message}
\"\"\"

Instructions:
1. Correct all grammar, spelling, punctuation, and capitalization errors.
2. Improve clarity, coherence, sentence flow, and readability.
3. Preserve the original meaning, intent, and facts strictly.
4. Do NOT invent false names, fictitious dates, arbitrary deadlines, or unsupported details. Use placeholders like [Your Name], [Recipient Name], [Date] only when essential.
5. If the category is 'Professional Email', 'Leave Application', or 'Formal Request', always include a relevant 'Subject:' line at the very top.
6. Provide an appropriate greeting/salutation and a professional closing/sign-off.
7. Return only the final improved message ready to use. Do not include conversational introductory phrases (such as "Here is your message:").{urdu_instruction}
"""
    return prompt.strip()


def extract_subject_and_body(text: str) -> dict:
    """
    Splits the generated text into subject and body if a Subject line is present.

    Returns:
        dict: {'subject': str or None, 'body': str}
    """
    lines = text.strip().split("\n")
    subject = None
    body_lines = []

    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not subject and line_clean.lower().startswith("subject:"):
            subject = line_clean[len("subject:"):].strip()
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    return {
        "subject": subject,
        "body": body if body else text
    }

