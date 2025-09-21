import os
# Response is needed for streaming, jsonify is no longer used for the main endpoint.
from flask import Flask, render_template, request, Response
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# This configuration for the local Ollama client remains the same.
client = OpenAI(
    base_url='http://127.0.0.1:11434/v1',
    api_key='ollama',
)

# The base system prompt is unchanged. We will add to it dynamically.
SYSTEM_PROMPT = """
You are 'PyGuide', a friendly and encouraging AI tutor for Python programming. Your primary goal is to help students learn by guiding them to find and fix bugs in their own code. You must act as a Socratic guide, not as a code solver.

**Your Core Mission:**
Help the student understand the *'why'* behind their error, not just the *'what'*. Your guidance should build their debugging skills and confidence.

**The Golden Rule: NEVER PROVIDE THE CORRECT CODE**
Under no circumstances should you provide the complete, corrected code or a direct line-for-line fix. Your purpose is to lead the student to the solution, not to give it to them.

**Formatting Instructions:**
- You MUST format your entire response using clean, web-friendly Markdown.
- Use standard paragraphs for explanations. Separate paragraphs with a blank line.
- Use bulleted lists with a dash (`-`) or numbered lists with (`1.`) for steps or distinct points.
- Use bold text with (`**...**`) to emphasize key terms.
- For code snippets, use triple backticks `` ```python ... ``` ``.

**Your Process for Responding:**
1.  **Acknowledge and Encourage:** Start with a positive and encouraging tone.
2.  **Analyze the Code Holistically:** Briefly analyze the student's overall approach.
3.  **Provide Hints in a Graduated Manner:** Offer hints from high-level to specific questions.
4.  **Promote Debugging Practices:** Suggest using `print()` statements or manual tracing.
5.  **End with an Open Question:** Put the ball back in the student's court.
"""

@app.route('/')
def index():
    """Renders the main page (index.html)."""
    return render_template('index.html')


@app.route('/debug', methods=['POST'])
def debug_code():
    """
    Handles the debugging request from the user and streams the AI's response.
    This function has been completely rewritten to support streaming and adaptive prompting.
    """
    # --- ENHANCEMENT 1: Get data for both the code and the user's skill level ---
    problem_description = request.form.get('problem', '')
    code_to_debug = request.form.get('code', '')
    # Provide a default value for skill_level in case it's not sent
    skill_level = request.form.get('skill', 'Beginner')

    # This function is a "generator". Instead of returning a value once, it can "yield"
    # multiple values, one after another. Flask uses this to stream data.
    def generate_stream():
        try:
            # --- ENHANCEMENT 1 (continued): Create an adaptive prompt ---
            # We dynamically add instructions to the base prompt based on the user's skill level.
            adaptive_prompt = SYSTEM_PROMPT + f"""

            IMPORTANT: The user has identified their skill level as '{skill_level}'.
            - If they are a Beginner, focus on fundamental syntax (like missing colons), variable initialization, and simple logic errors.
            - If they are Intermediate, suggest better Pythonic practices, standard library functions, or ways to avoid common pitfalls.
            - If they are Advanced, you can discuss algorithmic efficiency (Big-O), memory management, subtle edge cases, or architectural patterns.
            Tailor the depth and complexity of your hint to this specific skill level.
            """

            user_message = f"""
            Here is the problem I'm trying to solve:
            {problem_description}

            And here is my code that has a bug:
            ```python
            {code_to_debug}
            ```
            My skill level is {skill_level}. Can you help me find the bug without giving me the answer?
            """
            
            # --- ENHANCEMENT 2: Enable streaming from the client ---
            # The `stream=True` parameter tells the client to return chunks of the response as they
            # are generated, instead of waiting for the entire response.
            stream = client.chat.completions.create(
                model="phi3",
                messages=[
                    {"role": "system", "content": adaptive_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3,
                stream=True,
            )

            # We loop through the stream of chunks and yield each piece of content.
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content

        except Exception as e:
            # If an error occurs (e.g., Ollama is not running), we can yield an error message
            # that will be streamed back to the user on the frontend.
            error_message = f"\n\n**An error occurred:** {str(e)}. Please ensure the Ollama server is running and the model is available."
            yield error_message

    # Instead of `jsonify`, we return a `Response` object.
    # We pass our generator function to it, and Flask handles the streaming.
    # The mimetype 'text/event-stream' is the standard for Server-Sent Events (SSE).
    return Response(generate_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)