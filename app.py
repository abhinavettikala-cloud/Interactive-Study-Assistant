import os
import gradio as gr
from google import genai


# =========================
# Gemini Configuration
# =========================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=API_KEY)


# =========================
# Gemini Study Assistant
# =========================

def study_assistant(topic, action, question):

    if not topic.strip():
        return "⚠️ Please enter a study topic or study material."

    if action == "Explain":

        prompt = f"""
You are a friendly AI study tutor.

Explain the following topic clearly to a college student.

Topic:
{topic}

Requirements:
- Use simple language
- Give examples
- Explain important concepts
- Use headings and bullet points
- Make it useful for exam preparation
"""

    elif action == "Summarize":

        prompt = f"""
You are an AI study assistant.

Summarize the following study material.

Material:
{topic}

Give:
- Short overview
- Important points
- Key concepts
- Important terms
- Exam-focused notes
"""

    elif action == "Quiz":

        prompt = f"""
You are an AI quiz generator.

Create a quiz based on:

{topic}

Create 5 questions.

Include:
- Multiple choice questions
- Short answer questions
- Conceptual questions

Provide the answer key at the end.
"""

    else:

        if not question.strip():
            return "⚠️ Please enter your question."

        prompt = f"""
You are a friendly AI study tutor.

Study topic:
{topic}

Student question:
{question}

Answer clearly and step-by-step.

Use:
- Simple explanations
- Examples
- Important points
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error: {str(e)}"


# =========================
# Custom CSS
# =========================

css = """

body {
    background: #f5f7fb;
}

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

.header {
    text-align: center;
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-bottom: 20px;
}

.header h1 {
    font-size: 36px;
    margin-bottom: 8px;
}

.header p {
    font-size: 17px;
}

.card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e5e7eb;
}

.action-btn button {
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.generate-btn button {
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

.footer {
    text-align: center;
    color: #6b7280;
    padding: 20px;
}

"""


# =========================
# Gradio UI
# =========================

with gr.Blocks(
    title="AI Study Assistant",
    theme=gr.themes.Soft(),
    css=css
) as app:

    gr.HTML("""
    <div class="header">

        <h1>🎓 AI Study Assistant</h1>

        <p>
            Learn smarter with your personal Gemini-powered study tutor.
        </p>

    </div>
    """)

    with gr.Row():

        # =========================
        # LEFT PANEL
        # =========================

        with gr.Column(scale=1):

            gr.Markdown("## 📚 Study Material")

            topic = gr.Textbox(
                label="Topic / Notes",
                placeholder="Example: Normalization in DBMS",
                lines=8
            )

            difficulty = gr.Dropdown(
                choices=[
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ],
                value="Intermediate",
                label="🎯 Difficulty Level"
            )

            gr.Markdown("### ⚡ Quick Actions")

            with gr.Row():

                explain_btn = gr.Button(
                    "💡 Explain",
                    elem_classes="action-btn"
                )

                summary_btn = gr.Button(
                    "📝 Summarize",
                    elem_classes="action-btn"
                )

            with gr.Row():

                quiz_btn = gr.Button(
                    "🧠 Quiz",
                    elem_classes="action-btn"
                )

                ask_btn = gr.Button(
                    "❓ Ask",
                    elem_classes="action-btn"
                )

            gr.Markdown("### 💬 Ask a Question")

            question = gr.Textbox(
                label="Your Question",
                placeholder="Example: What is 3NF?",
                lines=4
            )

            generate_btn = gr.Button(
                "🚀 Generate Response",
                variant="primary",
                elem_classes="generate-btn"
            )

            clear_btn = gr.ClearButton(
                components=[
                    topic,
                    question
                ],
                value="🧹 Clear"
            )

        # =========================
        # RIGHT PANEL
        # =========================

        with gr.Column(scale=2):

            gr.Markdown("## 🤖 AI Tutor")

            output = gr.Markdown(
                """
### 👋 Welcome!

I'm your AI Study Assistant.

Choose an action to get started:

💡 **Explain**  
Understand difficult concepts in simple language.

📝 **Summarize**  
Turn long study material into concise notes.

🧠 **Quiz**  
Test your knowledge with AI-generated questions.

❓ **Ask**  
Ask questions about your study topic.

### 🚀 Let's start learning!
"""
            )

    gr.HTML("""
    <div class="footer">

        Powered by Google Gemini • Built with Gradio

    </div>
    """)


    # =========================
    # Button Actions
    # =========================

    explain_btn.click(
        fn=lambda t, d, q:
            study_assistant(t, "Explain", q),
        inputs=[
            topic,
            difficulty,
            question
        ],
        outputs=output
    )

    summary_btn.click(
        fn=lambda t, d, q:
            study_assistant(t, "Summarize", q),
        inputs=[
            topic,
            difficulty,
            question
        ],
        outputs=output
    )

    quiz_btn.click(
        fn=lambda t, d, q:
            study_assistant(t, "Quiz", q),
        inputs=[
            topic,
            difficulty,
            question
        ],
        outputs=output
    )

    ask_btn.click(
        fn=lambda t, d, q:
            study_assistant(t, "Ask Question", q),
        inputs=[
            topic,
            difficulty,
            question
        ],
        outputs=output
    )

    generate_btn.click(
        fn=lambda t, d, q:
            study_assistant(t, "Ask Question", q),
        inputs=[
            topic,
            difficulty,
            question
        ],
        outputs=output
    )


# =========================
# Render Server
# =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    app.launch(
        server_name="0.0.0.0",
        server_port=port
    )
