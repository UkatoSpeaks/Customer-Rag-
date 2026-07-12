import uuid
import requests
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GigaCorp Support",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Backend URL ────────────────────────────────────────────────────────────────
BACKEND_URL = "http://localhost:8000"

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── App background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.04);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* ── Hero header ── */
    .hero-header {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
    }
    .hero-header .brand {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    .hero-header .subtitle {
        color: rgba(255,255,255,0.55);
        font-size: 0.95rem;
        margin-top: 0.3rem;
        font-weight: 400;
    }

    /* ── Chat container ── */
    .chat-wrapper {
        max-width: 780px;
        margin: 0 auto;
    }

    /* ── Message bubbles ── */
    .msg-user {
        display: flex;
        justify-content: flex-end;
        margin: 0.6rem 0;
        animation: fadeUp 0.3s ease;
    }
    .msg-assistant {
        display: flex;
        justify-content: flex-start;
        margin: 0.6rem 0;
        animation: fadeUp 0.3s ease;
    }
    .bubble-user {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: #fff;
        padding: 0.85rem 1.1rem;
        border-radius: 18px 18px 4px 18px;
        max-width: 72%;
        font-size: 0.92rem;
        line-height: 1.55;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35);
    }
    .bubble-assistant {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e2e8f0;
        padding: 0.85rem 1.1rem;
        border-radius: 18px 18px 18px 4px;
        max-width: 80%;
        font-size: 0.92rem;
        line-height: 1.55;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
        margin: 0 0.55rem;
    }
    .avatar-user { background: linear-gradient(135deg,#7c3aed,#4f46e5); }
    .avatar-bot  { background: linear-gradient(135deg,#0ea5e9,#34d399); }

    /* ── Sources pill ── */
    .source-pills {
        margin-top: 0.55rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }
    .source-pill {
        background: rgba(96, 165, 250, 0.15);
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: #93c5fd;
        border-radius: 20px;
        padding: 0.2rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* ── Divider ── */
    .chat-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.07);
        margin: 0.4rem 0;
    }

    /* ── Input box ── */
    [data-testid="stChatInput"] {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        border-radius: 14px !important;
        color: #fff !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(124,58,237,0.6) !important;
        box-shadow: 0 0 0 3px rgba(124,58,237,0.2) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #fff !important;
    }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        border-radius: 10px !important;
    }

    /* ── Status badge ── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(52,211,153,0.12);
        border: 1px solid rgba(52,211,153,0.3);
        color: #34d399;
        border-radius: 20px;
        padding: 0.25rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
    }
    .status-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #34d399;
        animation: pulse 1.8s infinite;
    }
    .status-badge.offline {
        background: rgba(239,68,68,0.12);
        border-color: rgba(239,68,68,0.3);
        color: #f87171;
    }
    .status-badge.offline .status-dot { background: #f87171; animation: none; }

    /* ── Welcome card ── */
    .welcome-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.8rem;
        text-align: center;
        margin: 1.5rem auto;
        max-width: 520px;
        backdrop-filter: blur(10px);
    }
    .welcome-card h3 { color: #e2e8f0; font-size: 1.15rem; margin-bottom: 0.5rem; }
    .welcome-card p  { color: rgba(255,255,255,0.5); font-size: 0.88rem; line-height: 1.6; }
    .suggestion-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.55rem;
        margin-top: 1.2rem;
    }
    .suggestion-btn {
        background: rgba(124,58,237,0.12);
        border: 1px solid rgba(124,58,237,0.3);
        color: #c4b5fd;
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        font-size: 0.82rem;
        cursor: pointer;
        text-align: left;
        transition: all 0.2s;
    }
    .suggestion-btn:hover {
        background: rgba(124,58,237,0.25);
        border-color: rgba(124,58,237,0.5);
    }

    /* ── Animations ── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 4px; }

    /* ── Streamlit overrides ── */
    .stMarkdown p { color: inherit; }
    footer { display: none !important; }
    #MainMenu { display: none !important; }
    header   { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ──────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend_online" not in st.session_state:
    st.session_state.backend_online = False


# ── Helper: check backend health ───────────────────────────────────────────────
def check_backend():
    try:
        r = requests.get(f"{BACKEND_URL}/", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


# ── Helper: call chat endpoint ─────────────────────────────────────────────────
def send_message(question: str, session_id: str):
    try:
        r = requests.post(
            f"{BACKEND_URL}/chat",
            json={"question": question, "session_id": session_id},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to the backend. Please make sure it is running."}
    except requests.exceptions.Timeout:
        return {"error": "The request timed out. The backend may be overloaded."}
    except Exception as e:
        return {"error": str(e)}


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 GigaCorp Support")
    st.markdown("---")

    # Backend status
    st.session_state.backend_online = check_backend()
    if st.session_state.backend_online:
        st.markdown(
            '<span class="status-badge"><span class="status-dot"></span>Backend Online</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="status-badge offline"><span class="status-dot"></span>Backend Offline</span>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Session info
    st.markdown("**🔑 Session**")
    st.code(st.session_state.session_id[:8] + "...", language=None)

    st.markdown("**💬 Messages**")
    st.markdown(f"`{len(st.session_state.messages)}` in this session")

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    # New session button
    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:rgba(255,255,255,0.3)'>Powered by Mistral AI + ChromaDB<br>LangChain RAG Pipeline</small>",
        unsafe_allow_html=True,
    )

# ── Main content ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-header">
        <div class="brand">GigaCorp Support</div>
        <div class="subtitle">AI-powered customer support &nbsp;·&nbsp; Ask anything about our products & services</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Chat history ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <h3>👋 Welcome! How can I help you today?</h3>
            <p>I'm GigaCorp's AI support assistant. I can answer questions about our products,
            policies, and services using our knowledge base.</p>
            <div class="suggestion-grid">
                <div class="suggestion-btn">📦 What products do you offer?</div>
                <div class="suggestion-btn">🔄 What is your return policy?</div>
                <div class="suggestion-btn">🚚 How long does shipping take?</div>
                <div class="suggestion-btn">🛠️ How do I get technical support?</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="msg-user">
                    <div class="bubble-user">{msg["content"]}</div>
                    <div class="avatar avatar-user">👤</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            sources_html = ""
            if msg.get("sources"):
                pills = "".join(
                    f'<span class="source-pill">📄 {s["source"]} · p.{s["page"]}</span>'
                    for s in msg["sources"]
                )
                sources_html = f'<div class="source-pills">{pills}</div>'

            st.markdown(
                f"""
                <div class="msg-assistant">
                    <div class="avatar avatar-bot">🤖</div>
                    <div class="bubble-assistant">
                        {msg["content"]}
                        {sources_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ── Chat input ─────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your question here…"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show spinner while waiting for response
    with st.spinner("Thinking…"):
        result = send_message(prompt, st.session_state.session_id)

    if "error" in result:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"⚠️ {result['error']}",
                "sources": [],
            }
        )
    else:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result.get("answer", "No answer returned."),
                "sources": result.get("sources", []),
            }
        )

    st.rerun()
