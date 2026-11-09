"""
main.py - Console Application Runner
AI Email & Message Assistant
Course: Generative AI (Weeks 1-3)
Author: Generative AI Student

This module provides a terminal-based interface demonstrating core Python concepts:
variables, data types, lists, dictionaries, functions, while loops, if-elif-else,
exception handling, and Groq LLM API integration.
"""

from prompts import build_prompt, MESSAGE_TYPES, TONES
from groq_service import generate_message, check_api_status


def show_options(options, title):
    """
    Displays a numbered list of options.
    Demonstrates: Functions, loops, f-strings, list traversal.
    """
    print(f"\n===== {title} =====")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")


def select_option(options, title):
    """
    Prompts the user to select an option by number.
    Demonstrates: While loop, try/except error handling, conditionals.
    """
    show_options(options, title)
    while True:
        try:
            choice = int(input("\nEnter your choice (number): ").strip())
            if 1 <= choice <= len(options):
                return options[choice - 1]
            print(f"Invalid choice. Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer number.")


def create_message():
    """
    Handles user input collection, prompt generation, Groq API call,
    and display of the resulting AI-improved message.
    """
    # Step 1: Select Message Type
    message_type = select_option(
        MESSAGE_TYPES,
        "SELECT MESSAGE TYPE"
    )

    # Step 2: Select Tone
    tone = select_option(
        TONES,
        "SELECT WRITING TONE"
    )

    # Step 3: Enter rough message
    print("\n-------------------------------------------")
    print("Enter your rough or informal message below:")
    print("(Press Enter when finished)")
    message = input(">>> ").strip()

    # Step 4: Validate input
    if not message:
        print("\n[!] Error: Message cannot be empty. Returning to menu.")
        return

    # Step 5: Build AI Prompt
    prompt = build_prompt(
        message=message,
        message_type=message_type,
        tone=tone
    )

    # Step 6: Call Groq API
    print("\nGenerating your message with Groq AI...")
    result = generate_message(prompt)

    # Step 7: Display Output
    print("\n=======================================================")
    print("               AI GENERATED MESSAGE                    ")
    print("=======================================================")
    print(result)
    print("=======================================================")

    # Submenu for regeneration, new message, or return
    while True:
        print("\nOptions:")
        print("1. Regenerate Message (Fresh AI request)")
        print("2. Create Another Message")
        print("3. Return to Main Menu")

        sub_choice = input("Enter choice (1-3): ").strip()

        if sub_choice == "1":
            print("\nRegenerating fresh response with Groq AI...")
            result = generate_message(prompt)
            print("\n=======================================================")
            print("                 NEW AI RESPONSE                       ")
            print("=======================================================")
            print(result)
            print("=======================================================")
        elif sub_choice == "2":
            create_message()
            return
        elif sub_choice == "3":
            return
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")


def main():
    """
    Main loop for the terminal application.
    Demonstrates: Program entry point, control flow, menu loop.
    """
    # Display startup status
    api_status = check_api_status()

    while True:
        print("\n=======================================================")
        print("            AI EMAIL & MESSAGE ASSISTANT               ")
        print("                 Powered by Groq AI                    ")
        print("=======================================================")
        if not api_status["configured"]:
            print(" [!] NOTICE: GROQ_API_KEY is not set in .env file.")
        print("1. Generate New Message")
        print("2. View Available Message Types")
        print("3. View Available Writing Tones")
        print("4. Check API Configuration Status")
        print("5. Exit Application")
        print("=======================================================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            create_message()
        elif choice == "2":
            show_options(MESSAGE_TYPES, "AVAILABLE MESSAGE TYPES")
        elif choice == "3":
            show_options(TONES, "AVAILABLE WRITING TONES")
        elif choice == "4":
            status = check_api_status()
            print(f"\nConfiguration Status: {status['message']}")
        elif choice == "5":
            print("\nThank you for using AI Email & Message Assistant. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid number (1-5).")


if __name__ == "__main__":
    main()

