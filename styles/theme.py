"""
Giao diện dark-mode corporate với hiệu ứng glow tinh tế.
CSS được inject qua st.markdown — tách biệt khỏi logic nghiệp vụ.
"""

import streamlit as st


def inject_theme() -> None:
    """Inject CSS toàn cục cho giao diện SaltWatch dark corporate."""
    st.markdown(
        """
        <style>
        /* ── Nền tổng thể ── */
        .stApp {
            background: linear-gradient(160deg, #0a0e17 0%, #111827 45%, #0d1321 100%);
        }

        /* Ẩn menu mặc định Streamlit */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
            border-right: 1px solid rgba(56, 189, 248, 0.12);
        }
        section[data-testid="stSidebar"] .stMarkdown h1,
        section[data-testid="stSidebar"] .stMarkdown h2,
        section[data-testid="stSidebar"] .stMarkdown h3 {
            color: #e2e8f0 !important;
        }

        /* ── Tiêu đề ứng dụng ── */
        .saltwatch-header {
            text-align: center;
            padding: 1.2rem 0 0.5rem;
        }
        .saltwatch-title {
            font-size: 2.4rem;
            font-weight: 700;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 0.04em;
            filter: drop-shadow(0 0 18px rgba(56, 189, 248, 0.35));
        }
        .saltwatch-subtitle {
            color: #94a3b8;
            font-size: 0.95rem;
            margin-top: 0.3rem;
        }

        /* ── KPI Cards với glow ── */
        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.15);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.06),
                        inset 0 1px 0 rgba(255, 255, 255, 0.04);
            transition: box-shadow 0.3s ease, border-color 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 0 28px rgba(56, 189, 248, 0.14);
            border-color: rgba(56, 189, 248, 0.3);
        }
        div[data-testid="stMetric"] label {
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
            font-weight: 700 !important;
        }

        /* ── Nút chọn trạm ── */
        .stButton > button {
            border-radius: 8px;
            border: 1px solid rgba(56, 189, 248, 0.2);
            background: rgba(15, 23, 42, 0.9);
            color: #cbd5e1;
            transition: all 0.25s ease;
            font-weight: 500;
        }
        .stButton > button:hover {
            border-color: rgba(56, 189, 248, 0.5);
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.2);
            color: #f1f5f9;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0 0 20px rgba(14, 165, 233, 0.35);
        }

        /* ── Khối khuyến nghị ── */
        .recommendation-safe {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(5, 150, 105, 0.08));
            border: 1px solid rgba(52, 211, 153, 0.35);
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin: 1rem 0;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.12);
        }
        .recommendation-critical {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.22), rgba(220, 38, 38, 0.1));
            border: 1px solid rgba(248, 113, 113, 0.45);
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin: 1rem 0;
            box-shadow: 0 0 35px rgba(239, 68, 68, 0.18);
            animation: pulse-alert 2.5s ease-in-out infinite;
        }
        @keyframes pulse-alert {
            0%, 100% { box-shadow: 0 0 35px rgba(239, 68, 68, 0.18); }
            50% { box-shadow: 0 0 50px rgba(239, 68, 68, 0.32); }
        }
        .rec-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .rec-title-safe { color: #34d399; }
        .rec-title-critical { color: #f87171; }
        .rec-body { color: #cbd5e1; line-height: 1.6; }
        .rec-actions {
            margin-top: 0.8rem;
            padding-left: 1.2rem;
            color: #94a3b8;
        }

        /* ── Plotly container ── */
        .js-plotly-plot .plotly .modebar { display: none !important; }

        /* ── Divider ── */
        hr {
            border-color: rgba(56, 189, 248, 0.1) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_app_header(title: str, subtitle: str) -> None:
    """Hiển thị tiêu đề ứng dụng với gradient glow."""
    st.markdown(
        f"""
        <div class="saltwatch-header">
            <div class="saltwatch-title">{title}</div>
            <div class="saltwatch-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
