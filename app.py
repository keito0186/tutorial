import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="Pomodoro Timer", page_icon="⏱️", layout="centered")

# カスタムCSS
st.markdown("""
    <style>
    /* 全体の背景とフォント */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* タイマー表示 */
    .timer-display {
        font-size: 120px;
        font-weight: 700;
        text-align: center;
        font-family: 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
        margin: 20px 0;
        text-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    
    /* モード表示 */
    .status-label {
        font-size: 24px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    /* ボタンのスタイル調整 */
    .stButton > button {
        border-radius: 20px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    /* Startボタン */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
        background-color: #2ecc71;
        color: white;
    }
    /* Stopボタン */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
        background-color: #e74c3c;
        color: white;
    }
    /* Resetボタン */
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
        background-color: #95a5a6;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# セッション状態の初期化
if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'mode' not in st.session_state:
    st.session_state.mode = "Focus"  # Focus or Break

# ヘルパー関数
def start_timer():
    st.session_state.is_running = True

def stop_timer():
    st.session_state.is_running = False

def reset_timer():
    st.session_state.is_running = False
    if st.session_state.mode == "Focus":
        st.session_state.time_left = 25 * 60
    else:
        st.session_state.time_left = 5 * 60

def set_mode(mode):
    st.session_state.mode = mode
    st.session_state.is_running = False
    if mode == "Focus":
        st.session_state.time_left = 25 * 60
    else:
        st.session_state.time_left = 5 * 60

# --- UI構築 ---

st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Pomodoro Timer</h1>", unsafe_allow_html=True)

# メインのタイマー表示エリア
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    # モードに応じた色設定
    if st.session_state.mode == "Focus":
        mode_color = "#FF6B6B" # 落ち着いた赤
        timer_color = "#FF6B6B"
    else:
        mode_color = "#4ECDC4" # 落ち着いたティール
        timer_color = "#4ECDC4"

    st.markdown(f"<div class='status-label' style='color: {mode_color};'>{st.session_state.mode}</div>", unsafe_allow_html=True)

    mins, secs = divmod(st.session_state.time_left, 60)
    timer_str = f"{mins:02d}:{secs:02d}"
    st.markdown(f"<div class='timer-display' style='color: {timer_color};'>{timer_str}</div>", unsafe_allow_html=True)

st.write("") # スペーサー

# コントロールボタン
c1, c2, c3 = st.columns(3)
with c1:
    st.button("START", on_click=start_timer, use_container_width=True)
with c2:
    st.button("STOP", on_click=stop_timer, use_container_width=True)
with c3:
    st.button("RESET", on_click=reset_timer, use_container_width=True)

st.markdown("---")

# プリセット切り替え
st.markdown("<h4 style='text-align: center; color: #888;'>Select Mode</h4>", unsafe_allow_html=True)
c_focus, c_break = st.columns(2)
with c_focus:
    st.button("🍅 Focus (25 min)", on_click=lambda: set_mode("Focus"), use_container_width=True)
with c_break:
    st.button("☕ Break (5 min)", on_click=lambda: set_mode("Break"), use_container_width=True)

# タイマーロジック (自動更新)
if st.session_state.is_running:
    if st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        st.rerun()
    else:
        st.session_state.is_running = False
        st.balloons()
        st.success("Time's up! Take a break or start focusing.")
