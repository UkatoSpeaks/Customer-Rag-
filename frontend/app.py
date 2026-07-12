import uuid
import requests
import streamlit as st
import os


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GigaCorp Support",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Backend URL ────────────────────────────────────────────────────────────────
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://customer-rag-2.onrender.com",
)
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
        padding: 2rem 1rem 1rem;
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

    /* ── Native chat message bubbles ── */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 16px !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 0.5rem !important;
        backdrop-filter: blur(10px);
        animation: fadeUp 0.25s ease;
        transition: box-shadow 0.2s ease;
    }
    [data-testid="stChatMessage"]:hover {
        box-shadow: 0 4px 24px rgba(124,58,237,0.18);
    }
    /* User messages – slightly highlighted */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(124, 58, 237, 0.12) !important;
        border-color: rgba(124, 58, 237, 0.25) !important;
    }
    /* Message text colour */
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #e2e8f0 !important;
    }
    /* Avatar circles */
    [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        border-radius: 50% !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #0ea5e9, #34d399) !important;
        border-radius: 50% !important;
    }

    /* ── Source pills ── */
    .source-pills {
        margin-top: 0.6rem;
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
        transition: opacity 0.2s;
    }
    [data-testid="stChatInput"] button:hover { opacity: 0.85; }

    /* ── Thinking indicator ── */
    .thinking-dot {
        display: inline-block;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #a78bfa;
        margin: 0 2px;
        animation: bounce 1.2s infinite;
    }
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }

    /* ── Animations ── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); }
        40%            { transform: translateY(-6px); }
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
        r = requests.get(
            f"{BACKEND_URL}/health",
            timeout=3,
        )
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
        <div class="subtitle">AI-powered customer support &nbsp;·&nbsp; Ask anything about our products &amp; services</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Chat history (native st.chat_message for smooth rendering) ─────────────────
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
        role = msg["role"]
        with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
            st.markdown(msg["content"])

# ── Chat input ─────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your question here…"):
    # 1) Show the user bubble immediately (no rerun needed yet)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # 2) Show animated thinking indicator while waiting
    with st.chat_message("assistant", avatar="🤖"):
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<span class="thinking-dot"></span>'
            '<span class="thinking-dot"></span>'
            '<span class="thinking-dot"></span>',
            unsafe_allow_html=True,
        )

        result = send_message(prompt, st.session_state.session_id)

        # 3) Replace indicator with the actual answer
        thinking_placeholder.empty()

        if "error" in result:
            answer = f"⚠️ {result['error']}"
            sources = []
        else:
            answer = result.get("answer", "No answer returned.")

        st.markdown(answer)

    # 4) Persist the assistant message for history
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
