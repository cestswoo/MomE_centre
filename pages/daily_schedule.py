import sqlite3
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

# 로그인 상태를 확인하는 함수
def check_login():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("로그인 후 이용해주세요")
        st.stop()

with st.sidebar:
    menu = option_menu("MomE", ['Home', 'Dashboard', 'Diary', 'MOMents', 'To do list', '하루 자가진단', 'LogOut'],
                        icons=['bi bi-house-fill', 'bi bi-grid-1x2-fill', 'book-half', 'Bi bi-star-fill', 'Bi bi-calendar-check', 'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=4,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"}
                        })

    if menu == 'Dashboard':
        st.switch_page("pages/dashboard_page.py")
    elif menu == 'Diary':
        st.switch_page("pages/diary_page.py")
    elif menu == 'MOMents':
        st.switch_page("pages/SNS2.py")
    elif menu == 'Home':
        st.switch_page("pages/home.py")
    elif menu == '하루 자가진단':
        st.switch_page('pages/self_diagnosis.py')
    elif menu == 'LogOut':
        st.session_state['logged_in'] = False
        st.switch_page("dd1.py")

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            time TEXT,
            task TEXT,
            comments TEXT
        )
    ''')
    # user_id 열이 없는 경우 추가
    c.execute("PRAGMA table_info(schedules)")
    columns = [info[1] for info in c.fetchall()]
    if 'user_id' not in columns:
        c.execute("ALTER TABLE schedules ADD COLUMN user_id TEXT")
    conn.commit()
    conn.close()

# 데이터 삽입 및 조회 함수
def add_schedule(user_id, date, time, task, comments):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO schedules (user_id, date, time, task, comments) VALUES (?, ?, ?, ?, ?)',
              (user_id, date, time, task, comments))
    conn.commit()
    conn.close()

def get_schedules(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM schedules WHERE user_id = ? ORDER BY datetime(date) DESC, datetime(time) DESC', (user_id,))
    schedules = c.fetchall()
    conn.close()
    return schedules

def get_schedules_by_date(user_id, date):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM schedules WHERE user_id = ? AND date = ? ORDER BY datetime(time) DESC', (user_id, date))
    schedules = c.fetchall()
    conn.close()
    return schedules

def delete_schedule(schedule_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()

# 일정 작성 폼
def schedule_form(user_id):
    st.subheader("하루 일과 관리")
    date = st.date_input("날짜")
    time = st.time_input("시간")
    task = st.text_input("할 일")
    comments = st.text_area("메모")

    if st.button("일정 저장"):
        if task:
            add_schedule(user_id, date.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), task, comments)
            st.success("일정이 저장되었습니다.")
            st.rerun()
        else:
            st.error("할 일을 입력해주세요.")

# 일정 목록 표시
def schedule_list(user_id, date):
    st.subheader(f"{date}의 일과 목록")
    schedules = get_schedules_by_date(user_id, date)
    for schedule in schedules:
        st.markdown(f"""
        **시간:** {schedule[2]}  
        **할 일:** {schedule[3]}  
        **메모:** {schedule[4]}
        """, unsafe_allow_html=True)
        if st.button("일정 삭제", key=f'delete_button_{schedule[0]}'):
            delete_schedule(schedule[0])
            st.rerun()
        st.write("---")

# 일정 전체 삭제 함수
def delete_all_schedules(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('DELETE FROM schedules WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    st.success("모든 일정이 삭제되었습니다.")
    st.rerun()

# Streamlit 앱 실행
def main():
    # 로그인 상태 확인
    check_login()
    
    user_id = st.session_state.get('user_id', 'guest')  # 각 사용자별 고유한 식별자

    # CSS 스타일 추가
    st.markdown(
        """
        <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
        <style>
        * {
            font-family: 'NanumSquare', sans-serif !important;
        }
        body {
            background-color: #f0f2f6;
        }
        .reportview-container .main .block-container {
            padding: 2rem;
        }
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            font-size: 12px;
            margin: 5px 2px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .fixed-button {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("To do list")

    # 일정 작성 폼
    schedule_form(user_id)

    # 캘린더 컴포넌트를 사용하여 날짜 선택
    st.subheader("캘린더")
    selected_date = st.date_input("날짜 선택", datetime.today())

    # 페이지 상단에 고정된 버튼
    if st.button("모든 일정 삭제", key='delete_all'):
        delete_all_schedules(user_id)

    # 해당 일자의 일정 목록
    schedule_list(user_id, selected_date.strftime("%Y-%m-%d"))

if __name__ == "__main__":
    init_db()
    main()
