def load_styles():
    import streamlit as st
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
/* Modal styling that works with Streamlit */
.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}
.modal-content {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    max-width: 500px;
    width: 90%;
    text-align: center;
    border: 3px solid var(--secondary-color);
}
.modal-title {
    color: var(--secondary-color);
    margin-bottom: 20px;
    font-size: 1.5rem;
    font-weight: bold;
}
.modal-message {
    margin-bottom: 25px;
    font-size: 1.1rem;
    line-height: 1.5;
}
.modal-buttons-container {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

