"""
app.py - Flask Web Application Backend
AI Email & Message Assistant
Course: Generative AI (Weeks 1-3)
Author: Generative AI Student

This module serves the web interface and handles REST API requests for
transforming rough messages into polished communications using Groq AI.
"""

from flask import Flask, render_template, request, jsonify
from prompts import (
    MESSAGE_TYPES,
    TONES,
    CATEGORY_GUIDELINES,
    TONE_GUIDELINES,
    build_prompt,
    extract_subject_and_body
)
from groq_service import generate_message, check_api_status

app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the main frontend web page.
    Passes categories, tones, and API status to the template.
    """
    api_status = check_api_status()
    return render_template(
        "index.html",
        message_types=MESSAGE_TYPES,
        tones=TONES,
        category_guidelines=CATEGORY_GUIDELINES,
        tone_guidelines=TONE_GUIDELINES,
        api_status=api_status
    )


@app.route("/api/status", methods=["GET"])
def api_status_endpoint():
    """
    Returns the current configuration status of the Groq API.
    """
    status = check_api_status()
    return jsonify({
        "success": True,
        "configured": status["configured"],
        "model": status["model"],
        "message": status["message"],
        "message_types": MESSAGE_TYPES,
        "tones": TONES
    })


@app.route("/generate", methods=["POST"])
def generate():
    """
    API endpoint to process rough messages and return AI-improved output.

    Expected JSON body:
    {
        "message": "rough message string",
        "message_type": "Professional Email",
        "tone": "Professional",
        "include_urdu": false,
        "length": "balanced"
    }

    Returns JSON:
    {
        "success": true | false,
        "generated_message": "...",
        "subject": "..." | null,
        "body": "...",
        "error": "..." | null
    }
    """
    # 1. Parse JSON payload
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "success": False,
            "error": "Invalid request: Missing JSON body."
        }), 400

    # 2. Extract and sanitize parameters
    message = data.get("message", "").strip()
    message_type = data.get("message_type", "Professional Email").strip()
    tone = data.get("tone", "Professional").strip()
    include_urdu = bool(data.get("include_urdu", False))
    length_preference = data.get("length", "balanced").strip()

    # 3. Input Validation
    if not message:
        return jsonify({
            "success": False,
            "error": "Please enter your message. The input field cannot be empty."
        }), 400

    if message_type not in MESSAGE_TYPES:
        message_type = MESSAGE_TYPES[0]

    if tone not in TONES:
        tone = TONES[0]

    # 4. Dynamic Prompt Construction
    prompt = build_prompt(
        message=message,
        message_type=message_type,
        tone=tone,
        include_urdu=include_urdu,
        length_preference=length_preference
    )

    # 5. Groq API Call
    result = generate_message(prompt)

    # 6. Check for Errors returned from Groq Service
    if result.startswith("Error:") or result.startswith("API Error:"):
        return jsonify({
            "success": False,
            "error": result
        }), 500

    # 7. Extract subject line and body for structured presentation
    parsed = extract_subject_and_body(result)

    # 8. Return Success JSON
    return jsonify({
        "success": True,
        "generated_message": result,
        "subject": parsed["subject"],
        "body": parsed["body"],
        "message_type": message_type,
        "tone": tone
    }), 200


if __name__ == "__main__":
    print("=======================================================")
    print("  AI EMAIL & MESSAGE ASSISTANT - FLASK SERVER")
    print("  Running at: http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop.")
    print("=======================================================")
    app.run(host="127.0.0.1", port=5000, debug=True)

