import os
import gradio as gr
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_API_ENDPOINT"]
deployment = os.environ["AZURE_OPENAI_API_MODEL"]
subscription_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = os.environ["AZURE_OPENAI_API_VERSION"]

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

# Function to handle chat responses with streaming
def respond(user_message):
    # prepare single-turn exchange
    user_entry = {"role": "user", "content": user_message}
    assistant_entry = {"role": "assistant", "content": ""}
    history = [user_entry, assistant_entry]
    messages_for_api = [
        {"role": "system", "content": "You are a helpful assistant."},
        user_entry
    ]

    # initial: clear input & disable buttons
    yield history, "", "", gr.update(value=""), gr.update(interactive=False), gr.update(interactive=False)

    response = client.chat.completions.create(
        model=deployment,
        stream=True,
        messages=messages_for_api,
        max_tokens=8192,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    model_router_model = None
    usage_info = ""
    usage = None
    for chunk in response:
        if getattr(chunk, "usage", None) is not None:
            usage = chunk.usage
        elif isinstance(chunk, dict) and chunk.get("usage") is not None:
            usage = chunk.get("usage")

        if not getattr(chunk, "choices", []) or getattr(chunk.choices[0].delta, "content", None) is None:
            continue
        model_router_model = getattr(chunk, "model", None) or getattr(chunk, "model_name", None) or model_router_model
        assistant_entry["content"] += chunk.choices[0].delta.content or ""

        # stream back updated assistant response
        yield history, model_router_model, "", gr.update(value=""), gr.update(interactive=False), gr.update(interactive=False)

    if usage is None:
        usage = getattr(response, "usage", None)

    if usage:
        prompt_tokens = getattr(usage, "prompt_tokens", None) or (usage.get("prompt_tokens") if isinstance(usage, dict) else None)
        completion_tokens = getattr(usage, "completion_tokens", None) or (usage.get("completion_tokens") if isinstance(usage, dict) else None)
        total_tokens = getattr(usage, "total_tokens", None) or (usage.get("total_tokens") if isinstance(usage, dict) else None)

        rate_map = {
            "model-router": 0.0025,
            "gpt-4o": 0.0060,
            "gpt-4o-mini": 0.0030,
            "gpt-4.1-nano": 0.0010,
            "gpt-4.1-mini": 0.0020,
            "gpt-4.1": 0.0040,
            "o4-mini": 0.0015,
            "gpt-5-nano": 0.0015,
            "gpt-5-mini": 0.0030,
            "gpt-5-chat": 0.0060,
            "gpt-5": 0.0100,
            "gpt-5.2-chat": 0.0075,
            "gpt-5.2": 0.0120,
            "gpt-oss-120b": 0.0008,
            "Llama-4-Maverick-17B-128E-Instruct-FP8": 0.0025,
            "DeepSeek-V3.1": 0.0025,
            "DeepSeek-V3.2": 0.0030,
            "grok-4": 0.0020,
            "grok-4-fast-reasoning": 0.0030,
            "claude-haiku-4-5": 0.0035,
            "claude-sonnet-4-5": 0.0040,
            "claude-opus-4-1": 0.0045,
            "claude-opus-4-6": 0.0050,
        }
        rate = rate_map.get(model_router_model or deployment, 0.0025)
        total_tokens = total_tokens or 0
        cost = total_tokens * rate / 1000.0
        baseline_rate = 0.0050
        saved = max(0.0, (baseline_rate - rate) * total_tokens / 1000.0)

        usage_info = (
            f"Prompt tokens: {prompt_tokens or 0}\n"
            f"Completion tokens: {completion_tokens or 0}\n"
            f"Total tokens: {total_tokens}\n"
            f"Estimated cost: ${cost:.5f} at ${rate:.4f}/1K tokens\n"
            f"Estimated savings vs baseline: ${saved:.5f}"
        )
    else:
        usage_info = "Usage data not available for this request."

    # done streaming: re-enable buttons (input stays cleared)
    yield history, model_router_model, usage_info, gr.update(value=""), gr.update(interactive=True), gr.update(interactive=True)

# Function to clear chat and model info
def clear_history():
    # clear chat, model_info, usage_info, input; re-enable buttons
    return [], "model-router", "", "", gr.update(interactive=True), gr.update(interactive=True)  # Clear chatbot, model_info, usage_info, and input textbox

# Build Gradio interface
with gr.Blocks(css="""
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: radial-gradient(circle at top left, rgba(0,120,212,0.18), transparent 24%),
                    linear-gradient(180deg, #eef5fc 0%, #f8fbff 100%);
        margin: 0;
        min-height: 100vh;
        color: #0f172a;
    }
    .gradio-container {
        background: transparent !important;
        max-width: 1480px;
        margin: 32px auto 36px;
        padding: 0 24px;
    }
    .page-shell {
        background: white;
        border-radius: 34px;
        overflow: hidden;
        box-shadow: 0 30px 90px rgba(15, 23, 42, 0.12);
        border: 1px solid rgba(15, 23, 42, 0.08);
    }
    .hero-panel {
        display: grid;
        grid-template-columns: minmax(260px, 440px) 1fr;
        gap: 24px;
        align-items: center;
        padding: 40px 44px 32px;
        background: linear-gradient(135deg, #0078D4 0%, #00A4EF 100%);
        color: white;
    }
    .hero-text h1 {
        margin: 0;
        font-size: 3.4rem;
        line-height: 1.04;
        letter-spacing: -0.04em;
    }
    .hero-text p {
        margin: 20px 0 0;
        max-width: 640px;
        opacity: 0.93;
        font-size: 1.05rem;
        line-height: 1.75;
    }
    .hero-text .hero-footer {
        margin-top: 22px;
        opacity: 0.88;
        font-size: 0.98rem;
    }
    .hero-text .hero-footer a {
        color: white;
        text-decoration: underline;
    }
    .hero-badges {
        display: grid;
        gap: 16px;
    }
    .hero-card {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 18px 20px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 22px;
        min-height: 120px;
    }
    .hero-card svg {
        width: 60px;
        height: 60px;
        flex-shrink: 0;
    }
    .hero-card strong {
        display: block;
        font-size: 1rem;
        margin-bottom: 6px;
    }
    .hero-card span {
        font-size: 0.95rem;
        opacity: 0.9;
        line-height: 1.5;
    }
    .page-main {
        display: grid;
        grid-template-columns: 2.5fr 1fr;
        gap: 24px;
        padding: 24px 44px 40px;
    }
    .chat-section,
    .sidebar-section {
        display: flex;
        flex-direction: column;
        gap: 22px;
    }
    .chat-panel,
    .sidebar-card {
        background: #f8fbff;
        border-radius: 28px;
        border: 1px solid rgba(0,120,212,0.14);
        padding: 24px;
    }
    .chat-panel h2,
    .sidebar-card h2 {
        margin: 0 0 18px;
        font-size: 1.3rem;
    }
    .chatbot-container {
        border-radius: 24px;
        overflow: hidden;
        border: 1px solid rgba(15,23,42,0.06);
        box-shadow: inset 0 0 0 1px rgba(15,23,42,0.04);
        min-height: 500px;
    }
    .chatbot-container [data-testid="chatbot"] {
        border-radius: 24px !important;
    }
    .model-info-container {
        background: white;
        border: 1px solid rgba(0,120,212,0.18);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 24px;
    }
    .model-info-container label {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }
    #model_info textarea {
        font-size: 1.05rem !important;
        color: #0f172a !important;
        border: 1px solid rgba(0,120,212,0.2) !important;
        background: #fbfdff !important;
        padding: 16px !important;
        border-radius: 16px !important;
        min-height: 72px !important;
    }
    .usage-info-container {
        background: white;
        border: 1px solid rgba(0,120,212,0.16);
        border-radius: 22px;
        padding: 18px;
        margin-bottom: 24px;
    }
    .usage-info-container textarea {
        font-size: 1rem !important;
        color: #0f172a !important;
        border: none !important;
        background: #f8fbff !important;
        padding: 14px !important;
        border-radius: 14px !important;
        min-height: 100px !important;
        white-space: pre-wrap !important;
    }
    .input-group {
        background: white;
        padding: 24px;
        border-radius: 26px;
        border: 1px solid rgba(15,23,42,0.08);
        display: grid;
        gap: 18px;
    }
    .input-group textarea {
        width: 100% !important;
        min-height: 110px !important;
        font-size: 1.1rem !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 18px !important;
        padding: 18px !important;
        box-sizing: border-box !important;
        background: #fbfdff !important;
        resize: vertical !important;
    }
    .input-group .button-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    .input-group .button-row button {
        padding: 16px 20px !important;
        font-size: 1rem !important;
        border-radius: 16px !important;
        border: none !important;
        cursor: pointer !important;
        font-weight: 600 !important;
    }
    .input-group .button-row button:first-child {
        background: linear-gradient(135deg, #0078D4 0%, #00A4EF 100%) !important;
        color: white !important;
    }
    .input-group .button-row button:last-child {
        background: #eef4ff !important;
        color: #0f172a !important;
        border: 1px solid #dbeafe !important;
    }
    .sidebar-card p,
    .sidebar-card li {
        color: #334155;
        line-height: 1.7;
    }
    .sidebar-card a {
        color: #0078D4;
        text-decoration: none;
    }
    .sidebar-card a:hover {
        text-decoration: underline;
    }
    .footer-note {
        margin-top: 12px;
        color: #475569;
        opacity: 0.92;
        font-size: 0.95rem;
    }
    @media(max-width: 1080px) {
        .hero-panel { grid-template-columns: 1fr; text-align: center; }
        .hero-badges { grid-template-columns: 1fr; }
        .page-main { grid-template-columns: 1fr; padding: 24px; }
        .input-group .button-row { grid-template-columns: 1fr; }
        .hero-card { justify-content: center; }
    }
    @media(max-width: 720px) {
        .page-shell { border-radius: 22px; }
        .hero-panel { padding: 30px 20px 24px; }
    }
""") as demo:
    # inject MathJax + custom CSS + MathJax re-typeset script
    gr.HTML(
        """
        <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            },
            svg: {fontCache: 'global'}
        };
        </script>
        <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
        <script>
        // Observe chatbot for changes and re-typeset with MathJax
        function typesetChatbot() {
            if (window.MathJax && window.MathJax.typeset) {
                window.MathJax.typeset();
            }
        }
        function scrollChatbotToBottom() {
            const chatbot = document.querySelector('[data-testid="chatbot"]');
            if (chatbot) {
                chatbot.scrollTop = chatbot.scrollHeight;
            }
        }
        const observer = new MutationObserver(() => {
            typesetChatbot();
            scrollChatbotToBottom();
        });
        window.addEventListener("DOMContentLoaded", function() {
            const chatbot = document.querySelector('[data-testid="chatbot"]');
            if (chatbot) {
                observer.observe(chatbot, { childList: true, subtree: true });
            }
        });
        </script>
        """,
        visible=False
    )

    # Page shell and hero section
    gr.HTML(
        """
        <div class="page-shell">
            <div class="hero-panel">
                <div class="hero-text">
                    <div style="text-transform: uppercase; letter-spacing: 0.24em; opacity:0.82; font-size:0.86rem; margin-bottom: 18px;">Azure OpenAI Model Router</div>
                    <h1>Smart assistant with model tracking and streaming output</h1>
                    <p>Ask questions, stream answers, and see the exact model used by Model Router in real time.</p>
                    <div class="hero-footer">Developed by <a href="https://www.linkedin.com/in/anik-guha/" target="_blank">Anik Guha</a></div>
                </div>
                <div class="hero-badges">
                    <div class="hero-card">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                            <defs>
                                <linearGradient id="azureGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" style="stop-color:#0078D4"/>
                                    <stop offset="100%" style="stop-color:#00A4EF"/>
                                </linearGradient>
                            </defs>
                            <rect width="100" height="100" rx="20" fill="url(#azureGrad)"/>
                            <text x="50" y="42" text-anchor="middle" fill="white" font-family="Segoe UI, sans-serif" font-size="16" font-weight="700">Azure</text>
                            <text x="50" y="62" text-anchor="middle" fill="white" font-family="Segoe UI, sans-serif" font-size="12">OpenAI</text>
                        </svg>
                        <div>
                            <strong>Azure-branded UI</strong>
                            <span>Clean interface with blue gradient styling.</span>
                        </div>
                    </div>
                    <div class="hero-card">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="white" stroke="#0078D4" stroke-width="3"/>
                            <circle cx="34" cy="34" r="7" fill="#0078D4"/>
                            <circle cx="66" cy="34" r="7" fill="#00A4EF"/>
                            <circle cx="50" cy="66" r="9" fill="#50E6FF"/>
                            <path d="M34 34 L50 50 L66 34" stroke="#0078D4" stroke-width="2" fill="none"/>
                        </svg>
                        <div>
                            <strong>Live model tracking</strong>
                            <span>Which model handled each request.</span>
                        </div>
                    </div>
                </div>
            </div>
        """
    )

    # Main layout and sidebar
    with gr.Row(elem_classes="page-main"):
        with gr.Column(scale=3):
            with gr.Group(elem_classes="chat-panel"):
                gr.HTML('<h2>Assistant</h2>')
                with gr.Group(elem_classes="chatbot-container"):
                    chatbot = gr.Chatbot(label=None, height=520)
                with gr.Group(elem_classes="input-group"):
                    txt = gr.Textbox(show_label=False, placeholder="✨ Type your message here…", lines=3, elem_id="chat_input")
                    with gr.Row(elem_classes="button-row"):
                        submit_btn = gr.Button("🚀 Submit", variant="primary")
                        clear_btn = gr.Button("🔄 Clear")
        with gr.Column(scale=1):
            with gr.Group(elem_classes="sidebar-card"):
                gr.HTML('<h2>Model Info</h2>')
                with gr.Group(elem_classes="model-info-container"):
                    model_info = gr.Textbox(
                        label="🔹 Model used:",
                        interactive=False,
                        value="model-router",
                        elem_id="model_info"
                    )
                with gr.Group(elem_classes="usage-info-container"):
                    usage_info = gr.Textbox(
                        label="📊 Request stats",
                        interactive=False,
                        value="",
                        lines=5,
                        elem_id="usage_info"
                    )
                gr.HTML('<p>Use the model status panel to confirm which Model Router deployment answered your request.</p>')
                gr.HTML('<p class="footer-note">Developer: <a href="https://www.linkedin.com/in/anik-guha/" target="_blank">Anik Guha</a></p>')
    gr.HTML('</div>')

    # Now outputs is a list: [chatbot, model_info, usage_info]
    submit_btn.click(
        fn=respond,
        inputs=[txt],
        outputs=[chatbot, model_info, usage_info, txt, submit_btn, clear_btn],
    )
    txt.submit(
        fn=respond,
        inputs=[txt],
        outputs=[chatbot, model_info, usage_info, txt, submit_btn, clear_btn],
    )
    clear_btn.click(
        fn=clear_history,
        inputs=None,
        outputs=[chatbot, model_info, usage_info, txt, submit_btn, clear_btn],
    )

if __name__ == "__main__":
    demo.launch()
