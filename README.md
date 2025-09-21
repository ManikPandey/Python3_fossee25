# PyGuide AI Coding Dojo - Python Screening Task Submission

## Project Overview

This project is a submission for the "Python Screening Task 2," which required the creation of an effective prompt for an AI debugging assistant. The initial goal was to design a prompt that could guide a student through debugging their Python code without giving away the solution.

The project has since evolved into a full-fledged, interactive web application named **PyGuide AI Coding Dojo**. It's an AI-powered learning environment where users can not only get intelligent, Socratic hints for their buggy code but also execute their code directly in the browser.

The core of this project remains the carefully engineered AI prompt that powers the "Get a Hint" feature, designed to be a patient, effective, and encouraging tutor.

---

## 🚀 Features

This application goes beyond the initial requirements and includes several advanced features to create a polished, professional-grade tool:

* **Adaptive AI Tutoring**: The AI's hints adapt to the user's self-declared skill level (Beginner, Intermediate, Advanced).
* **Streaming Responses**: AI feedback is streamed in real-time, creating a fast and responsive user experience.
* **Live Code Execution**: Users can run their Python code directly in the browser using **Pyodide (Python compiled to WebAssembly)**, providing an instant feedback loop.
* **Professional IDE-like Interface**: The app features a **Monaco Editor** (the engine behind VS Code) with syntax highlighting and line numbers.
* **Modern UI/UX**: A clean, responsive, dark-themed UI built with **Tailwind CSS**, featuring a collapsible "How to Use" sidebar for a clean workspace.
* **Local Model Support**: The backend is configured to run with a local LLM (e.g., `phi3`) via **Ollama**, making it free to run and completely private.

---

## 🛠️ Setup and Running the Project

To run this project locally, you will need Python, Flask, and a local AI model running with Ollama.

### Prerequisites

1.  **Python 3.7+**
2.  **Ollama**: Download and install from [https://ollama.com/](https://ollama.com/).
3.  **A local LLM**: Pull a model optimized for coding. `phi3` is recommended.
    ```bash
    ollama pull phi3
    ```

### Installation and Execution

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link>
    cd <your-repo-name>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install Flask openai
    ```

4.  **Run the Flask application:**
    ```bash
    flask run
    ```

5.  **Open your browser** and navigate to `http://127.0.0.1:5000`. The PyGuide AI Coding Dojo should now be running.

---

## ✅ Submission Requirements

This section contains the core deliverables as required by the screening task.

### 1. The AI Prompt

The following prompt is the heart of the AI tutor. It is stored in the `app.py` file as a system prompt and dynamically adjusted based on the user's selected skill level.

```markdown
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
```

### 2. Explanation of Design Choices

* **Why you worded it the way you did:**
    * **Persona ("PyGuide"):** Giving the AI a name and a clear, friendly persona sets a constructive and non-intimidating tone, which is crucial for students who may be feeling frustrated.
    * **Strong Directives ("The Golden Rule"):** Using absolute and capitalized phrases like "NEVER PROVIDE THE CORRECT CODE" leaves no room for ambiguity. This is the most critical constraint and is worded forcefully to ensure the model adheres to it.
    * **Structured Process:** The numbered "Process for Responding" acts as a clear algorithm for the AI to follow, ensuring its output is consistently structured, pedagogical, and helpful.
    * **Explicit Formatting:** The "Formatting Instructions" section was added to solve issues with inconsistent AI output, ensuring the Markdown is always clean and web-friendly, which improves the user experience.

* **How you ensured it avoids giving the solution:**
    * The primary mechanism is the explicit negative constraint in "The Golden Rule."
    * The process encourages a **Socratic method**, focusing on asking questions ("End with an Open Question") rather than providing answers.
    * The "Graduated Hints" system instructs the model to start with high-level conceptual guidance before narrowing down to a specific area, naturally preventing it from jumping directly to a line-for-line fix.

* **How it encourages helpful, student-friendly feedback:**
    * The very first step is **"Acknowledge and Encourage,"** which ensures every interaction begins on a positive and supportive note.
    * It explicitly instructs the AI to teach meta-skills by **"Promoting Debugging Practices,"** such as using `print()` statements. This teaches the student *how* to fish instead of just giving them a fish.
    * The entire prompt is framed around building student understanding ("the 'why' behind their error") and confidence, making the feedback inherently student-centric.

### 3. Reasoning

* **What tone and style should the AI use when responding?**
    The AI should adopt a **patient, encouraging, and Socratic** tone. It should act as a friendly mentor or a knowledgeable peer, not as an automated linter. The style should be conversational and inquisitive, using questions to prompt the student's own critical thinking. It must avoid jargon where possible and maintain a positive, can-do attitude to keep the student motivated.

* **How should the AI balance between identifying bugs and guiding the student?**
    The balance is achieved through a **scaffolding approach**, as detailed in the "Graduated Hints" process. The AI's first priority is always high-level guidance.
    1.  It starts by considering the student's overall logic.
    2.  If needed, it then narrows its focus to a specific *area* of the code without revealing the exact error.
    3.  Only as a final step does it ask a very pointed Socratic question about the specific line or syntax that is incorrect.
    This ensures the AI gives the minimum help necessary, maximizing the student's opportunity for self-discovery. It identifies the bug's location and nature progressively, always prioritizing guidance over simple identification.

* **How would you adapt this prompt for beginner vs. advanced learners?**
    This functionality is **already implemented** in the final application. The prompt is dynamically adapted based on user input. The core prompt includes a placeholder section that is filled in by the backend:
    ```
    IMPORTANT: The user has identified their skill level as '{skill_level}'.
    - If they are a Beginner, focus on fundamental syntax, variable initialization, and simple logic errors.
    - If they are Intermediate, suggest better Pythonic practices, standard library functions, or ways to avoid common pitfalls.
    - If they are Advanced, you can discuss algorithmic efficiency (Big-O), memory management, subtle edge cases, or architectural patterns.
    Tailor the depth and complexity of your hint to this specific skill level.
    ```
    This approach makes the AI's guidance highly relevant. A beginner gets help with a missing colon, while an advanced user might get a hint that their recursive function could be optimized with memoization—all using the same foundational prompt.