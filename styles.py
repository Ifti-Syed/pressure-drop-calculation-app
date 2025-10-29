# import streamlit as st
#
# def add_anti_flicker_js():
#     """Inject CSS/JS to prevent flicker on app load"""
#     st.markdown(
#         """
#         <style>
#         [data-testid="stToolbar"], [data-testid="stStatusWidget"] {
#             visibility: hidden;
#         }
#         </style>
#         <script>
#         document.documentElement.style.visibility = 'hidden';
#         window.addEventListener('load', function() {
#             document.documentElement.style.visibility = 'visible';
#         });
#         </script>
#         """,
#         unsafe_allow_html=True
#     )
#
# def load_styles():
#     """Load custom CSS styles with anti-flicker fixes"""
#     st.markdown(
#         """
#         <style>
#         :root {
#             --primary-color: #f47521;
#             --secondary-color: #1c449c;
#             --white-color: #ffffff;
#         }
#
#         .top-bar {
#             background-color: var(--secondary-color);
#             padding: 14px;
#             color: var(--white-color);
#             border-radius: 10px;
#             margin-bottom: 20px;
#             text-align: center;
#         }
#
#         h2, h3, h4 {
#             color: var(--secondary-color);
#             font-weight: 700;
#         }
#
#         div.stButton > button {
#             background-color: var(--primary-color);
#             color: var(--white-color);
#             font-weight: bold;
#             border-radius: 8px;
#             border: none;
#         }
#
#         div.stButton > button:hover {
#             background-color: var(--secondary-color);
#         }
#
#         div[data-baseweb="data-table"] th {
#             font-weight: bold;
#             font-size: 1rem;
#             color: #1c449c;
#         }
#
#         .footer {
#             margin-top: 30px;
#             text-align: center;
#             color: #777;
#             font-size: 0.9rem;
#         }
#
#         .stApp { overflow-anchor: none; }
#         [data-testid="stVerticalBlock"] { overflow-anchor: none; }
#         [data-testid="stDataFrameResizable"] {
#             min-height: 500px !important;
#             transition: none !important;
#         }
#         .stDataFrame, .element-container, .row-widget {
#             transition: none !important;
#             animation: none !important;
#         }
#         [data-testid="stCheckbox"] { z-index: 100; }
#
#         .stApp > div:first-child { display: none; }
#
#         html {
#             scroll-behavior: smooth;
#             overflow-anchor: none;
#         }
#
#         .modal-backdrop {
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             background-color: rgba(0,0,0,0.5);
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             z-index: 9999;
#         }
#
#         .modal-content {
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 30px rgba(0,0,0,0.3);
#             max-width: 500px;
#             width: 90%;
#             text-align: center;
#             border: 3px solid var(--secondary-color);
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
# styles.py
import streamlit as st


def load_styles():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    :root {
        --primary-color: #f47521;
        --secondary-color: #1c449c;
        --white-color: #ffffff;
    }

    .top-bar {
        background-color: var(--secondary-color);
        padding: 14px;
        color: var(--white-color);
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }

    h2, h3, h4 {
        color: var(--secondary-color);
        font-weight: 700;
    }

    div.stButton > button {
        background-color: var(--primary-color);
        color: var(--white-color);
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }

    div.stButton > button:hover {
        background-color: var(--secondary-color);
    }

    div[data-baseweb="data-table"] th {
        font-weight: bold;
        font-size: 1rem;
        color: #1c449c;
    }

    .footer {
        margin-top: 30px;
        text-align: center;
        color: #777;
        font-size: 0.9rem;
    }

    /* Simple anti-flicker styles */
    [data-testid="stDataFrameResizable"] {
        min-height: 500px;
    }

    /* Make table more stable */
    .stDataFrame {
        border: 1px solid #e6e6e6;
        border-radius: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)