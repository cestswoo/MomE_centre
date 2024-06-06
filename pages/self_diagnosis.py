import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    # Create table for self-diagnosis
    c.execute('''
        CREATE TABLE IF NOT EXISTS self_diagnosis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            q1 INTEGER,
            q2 INTEGER,
            q3 INTEGER,
            q4 INTEGER,
            q5 INTEGER,
            q6 INTEGER,
            q7 INTEGER,
            q8 INTEGER,
            q9 INTEGER,
            q10 INTEGER,
            total_score INTEGER
        )
    ''')
    # Create table for PHQ-9
    c.execute('''
        CREATE TABLE IF NOT EXISTS phq9 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            date TEXT,
            q1 INTEGER,
            q2 INTEGER,
            q3 INTEGER,
            q4 INTEGER,
            q5 INTEGER,
            q6 INTEGER,
            q7 INTEGER,
            q8 INTEGER,
            q9 INTEGER,
            total_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to save self-diagnosis result to the database
def save_result(user, selected_date, scores, total_score, table):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    columns = ', '.join([f'q{i+1}' for i in range(len(scores))])
    values = ', '.join(['?'] * (len(scores) + 3))
    c.execute(f'''
        INSERT INTO {table} (user, date, {columns}, total_score)
        VALUES ({values})
    ''', (user, selected_date, *scores.values(), total_score))
    conn.commit()
    conn.close()

# Function to retrieve results from the database
def get_results(user, table):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f'''
        SELECT date, q1, q2, q3, q4, q5, q6, q7, q8, q9, total_score
        FROM {table}
        WHERE user = ?
        ORDER BY date DESC
    ''', (user,))
    results = c.fetchall()
    conn.close()
    return results

# Survey question function
def question_block(text, answer_option, key):
    text_area = st.container()
    text_area.write(text)
    answer = st.radio("", options=list(answer_option.keys()), key=key, help=" ")
    return answer_option[answer]  # Return the integer score

def main():

    user = st.session_state.get('logged_in_user', '')  # session_state에서 사용자 이름 가져오기
    if not user:
        st.error("로그인이 필요합니다.")
        return
    
    # Sidebar menu
    with st.sidebar:
        selected_menu = option_menu("Option", ['산후우울증이란', 'K-EPDS', 'PHQ-9'],
                                    icons=['book', 'clipboard-data', 'clipboard-check'],
                                    menu_icon="baby", default_index=0,
                                    styles={
                                        "icon": {"font-size": "23px"},
                                        "title": {"font-weight": "bold"},
                                        "nav-link-selected": {"background-color": "#D0E3FF", "color":"#091F5B", "font-family":"'NanumSquareAceb', sans-serif !important"},
                                        "container": {"background-color": "#D0E3FF", "color":"#FFF9EF"}
                                    })

    # 산후우울증이란 tab
    if selected_menu == '산후우울증이란':
        st.markdown(
    """
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
    <style>
        * {
            font-family: 'NanumSquare';
        }
        .stApp{
            background: #FFF9EF;
        }
        .container1{
            background-color: #ffffff;
            width: 340px;
            height:240px;
            border-radius:30px;
            padding: 20px;
        }
        .titleContainer {
            position: relative;
            width: 200;
            height: 56px;
            display: flex;
            flex-direction: row;
            align-items: center;
            margin-bottom:10px;
        }
        .titleBar {
            position: relative;
            width: 3px;
            height: 32px;
            background-color: #091F5B;
            margin-right: 5px;
        }
        .servTitle {
            font-weight: bold;
            font-size: 28px;
            color: #091F5B;
            margin-top: 15px;
            font-family: 'NanumSquareExtraBold', sans-serif !important;
        }
        .stTabs [data-baseweb="tab-list"] 
            button [data-testid="stMarkdownContainer"] p {
            font-size:16px;
            color: #091F5B;
            font-family: 'NanumSquareAceb', sans-serif !important;
            }
             div[data-testid="stTabs"] div[role="tablist"] {
                background-color: #FFF9EF;
                padding: 10px;
            }
            div[data-testid="stTabs"] button[aria-selected="true"] {
                background-color: #EDF0F5;
                color: white;
                border-radius: 30px;
                padding: 0px 5px;
            }
    </style>
    """,
    unsafe_allow_html=True
    )

        video_row1, video_row2 = st.columns(2)
        st.write("")
        st.write("")
        #st.divider()
        row1, row2 = st.columns(2)

        with video_row1:
            video_url = 'https://youtu.be/zqfFHWuS8aQ?feature=shared'
            st.video(video_url)

        with video_row2:
            st.markdown(
                """
                <div class="container1">
                    <div class="titleContainer">
                        <div class="titleBar"></div>
                        <p class="servTitle"> 산후 우울증이란?</p>
                    </div>
                    산후우울증은 임신 마지막 달부터 출산 후 4주 이내에
                    우울증 증상(우울, 불안초조, 불면, 죄책감 등)이 발생해
                    그 증상이 2주 이상 지속되는 것을 말합니다.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        tab1, tab2, tab3 = st.tabs(['산후 우울증 예방법', '산후 우울증 극복기', '남편의 역할'])

        with tab1:
            video_data = [
                {"link": "https://youtu.be/ZLSleUyjhC0?feature=shared", "description": "산후우울증의 원인과 예방방법은?"},
                {"link": "https://youtu.be/bfYV3vR6b-A?feature=shared", "description": "예방을 위해선 어떤 노력을? 치료는 어떻게… "},
                {"link": "https://youtu.be/1LvXgJJwVAI?feature=shared", "description": "산후우울증 예방을 위해 명심해야 할것"}
            ]

            col1, col2, col3 = st.columns(3)

            for i, video_info in enumerate(video_data):
                with eval(f"col{i+1}"):
                    st.video(video_info["link"])
                    st.write(video_info["description"])

        with tab2:
            video_data1 = [
                {"link": "https://youtu.be/ptaJoWapgn8?feature=shared", "description": "슬기롭게 산후우울증 극복하는 세가지 방법"},
                {"link": "https://youtu.be/pWBcSvJzdVQ?feature=shared", "description": "산후우울증 극복하기/ 임신 출산 후 우울감은 왜 생길까?"},
                {"link": "https://youtu.be/PDqGEFPpiUE?feature=shared", "description": "아이도 같이 행복해지는 산후 우울증 극복하기"}
            ]

            col1, col2, col3 = st.columns(3)

            for i, video_info in enumerate(video_data1):
                with eval(f"col{i+1}"):
                    st.video(video_info["link"])
                    st.write(video_info["description"])

        with tab3:
            video_data2 = [
                {"link": "https://youtu.be/JkMauvDHAzk?feature=shared", "description": "내 남편이 산후우울증?"},
                {"link": "https://youtu.be/E33Bzdav3Bo?feature=shared", "description": "엄마의 산후우울증을 몰랐던 아빠?"},
                {"link": "https://youtu.be/oMsyz-0IChM?feature=shared", "description": "아내가 출산 후 예민해졌어요. 어떻게 도와줘야 하나요?"}
            ]

            col1, col2, col3 = st.columns(3)

            for i, video_info in enumerate(video_data2):
                with eval(f"col{i+1}"):
                    st.video(video_info["link"])
                    st.write(video_info["description"])

        st.write("")
        st.write("")
        st.write("")
        st.markdown('''
            <style>
            .link-container {
                margin-bottom: 10px;
            }
            a {
                text-decoration: none;  /* Remove underline from links */
                color: #000000;  /* Link color */
            }
            a:hover {
                color: #007BFF;  /* Change color on hover */
            }
            h3 {
                font-size: 20px;  /* Reduce the font size of h3 headers */
            }
            </style>
        ''', unsafe_allow_html=True)

        st.divider()

        # Layout with 3 columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<h3>난임·우울증</h3>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://www.nmc.or.kr/nmc22762276/main/main.do">국립중앙의료원(전국)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://www.mindcare-for-family.kr/">강남세브란스병원(서울권역)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://happyfamily.dumc.or.kr/">동국대 일산병원(경기북부권역)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://happyfamily3375.or.kr/#none">인구보건복지협회(경기도권역)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://id-incheon.co.kr/">가천대 길병원(인천권역)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="http://www.hwc1234.co.kr/">현대여성아동병원(전남권역)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://happymoa.kr/">안동의료원(경북권역)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="http://www.healthymom.or.kr/">경북대 병원(대구권역)</a></div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<h3>임신·육아</h3>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://www.childcare.go.kr/?menuno=1">임신육아종합포털</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="http://www.familynet.or.kr">가족센터(1577-9337)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://www.129.go.kr/index.do">보건복지부상담센터(전국)</a></div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<h3>정신건강</h3>', unsafe_allow_html=True)
            st.markdown('<div class="link-container"><a href="https://www.lifeline.or.kr/">한국생명의전화(1588-9191)</a></div>', unsafe_allow_html=True)
            st.markdown('<div class="link-container">위기상담전화(1577-0199)</a></div>', unsafe_allow_html=True)
    

        
    
    # 에딘버러 tab
    elif selected_menu == 'K-EPDS':
        st.header('K-EPDS')
        st.write("K-EPDS(Korean version of Edinburgh Postnatal Depression Scale)는 현재 가장 많이 사용되고 있는 산후우울증 선별 검사도구입니다. 일반적인 우울검사보다 산후우울증을 경험하면서 겪게 되는 증상들을 평가하고 있습니다. Cox 등에 의해 1987년 개발되었고 우리나라에서는 김용구 등에 의해 2005년 번안되고 표준화 된 검사도구입니다.  ")
        st.write("")
        sub_tab1, sub_tab2 = st.tabs(['검사', '검사결과'])
    

        # Self-diagnosis tab
        with sub_tab1:
            # Date selection
            st.write("[ Test 실시 방법 ]")
            st.write("- 문항을 너무 오래 생각하지 말고 즉각적으로 솔직하게 응답하시면 됩니다.\n - 현재 기분이 아니라 지난 2주일 동안 기분​​을 가장 잘 나타낸다고 생각되는 문항의 번호를 선택하시면 됩니다.")
            st.divider()

            selected_date = st.date_input("오늘의 날짜를 선택해 주세요", value=datetime.now())
            st.write("")

            # Answer options
            answer_option = {
                '전혀 그렇지 않음': 0,
                '가끔 그렇음': 1,
                '종종 그렇음': 2,
                '대부분 그렇음': 3
            }

            q1 = question_block(f"**1. 우스운 것이 눈에 잘 띄고 웃을 수 있었다.**", answer_option, key='q1')
            st.divider()
            q2 = question_block(f'**2. 즐거운 기대감에 어떤 일을 손꼽아 기다렸다.**', answer_option, key='q2')
            st.divider()
            q3 = question_block(f"**3. 일이 잘못되면 필요 이상으로 자신을 탓해왔다.**", answer_option, key='q3')
            st.divider()  
            q4 = question_block(f"**4. 별 이유 없이 불안해지거나 걱정이 되었다.**", answer_option, key='q4')
            st.divider()
            q5 = question_block(f"**5. 별 이유 없이 겁먹거나 공포에 휩싸였다.**", answer_option, key='q5')
            st.divider()
            q6 = question_block(f"**6. 처리할 일들이 쌓여만 있다.**", answer_option, key='q6')
            st.divider()
            q7 = question_block(f"**7. 너무나 불안한 기분이 들어 잠을 잘 못 잤다.**", answer_option, key='q7')
            st.divider()
            q8 = question_block(f"**8. 슬프거나 비참한 느낌이 들었다.**", answer_option, key='q8')
            st.divider()
            q9 = question_block(f"**9. 너무나 불행한 기분이 들어 울었다.**", answer_option, key='q9')
            st.divider()  
            q10 = question_block(f"**10. 나 자신을 해치는 생각이 들었다.**", answer_option, key='q10')
            st.divider()
            
            # Show results button
            if st.button("결과 확인하기", key="edin_result"):
                st.subheader("결과")

                # Save scores
                scores = {
                    'q1': q1,
                    'q2': q2,
                    'q3': q3,
                    'q4': q4,
                    'q5': q5,
                    'q6': q6,
                    'q7': q7,
                    'q8': q8,
                    'q9': q9,
                    'q10': q10
                }

                # Calculate total score
                total_score = sum(scores.values())

                # Display result message
                if total_score >= 13:
                    st.error("치료가 시급합니다. 이 경우 반드시 정신건강 전문가의 도움을 받으셔야 합니다. 산후우울증은 정서적 문제뿐만 아니라 뇌 신경전달 물질의 불균형과 관련이 있으며, 적절한 치료를 받는 것이 중요합니다. 전문가와 함께 산후우울에 대한 이야기를 나누고 적절한 치료를 받아보시기 바랍니다.")
                elif total_score >= 9:
                    st.warning("상담이 필요합니다. 산후 우울증 위험이 높은 것으로 나타났습니다. 전문가의 상담을 받아보시는 것이 좋습니다. 무엇이든 치료보다는 예방이 좋습니다. 조금 더 정확한 결과를 알아보고 싶다면 정신건강 전문가를 방문해 상담과 진료를 받아보시길 바랍니다.")
                else:
                    st.success("정상 범위입니다. 산후 우울증 위험이 낮은 것으로 나타났습니다. 그러나 주변 지원 및 관리가 필요할 수 있습니다. 자신의 감정을 받아들이고 남편과 가족들과 나누며, 신체적 정서적 안정을 유지하는 것이 좋습니다.")

                # Save results to database
                save_result(user, selected_date.strftime("%Y-%m-%d"), scores, total_score, "self_diagnosis")

            with sub_tab2:
                color_labels = {
                    '#baef9d': '전혀 그렇지 않음 / 0점',
                    '#e8ef9d': '가끔 그렇음 / 1점',
                    '#efd39d': '종종 그렇음 / 2점',
                    '#efae9d': '대부분 그렇음 / 3점'
                }

                co1, _, co2 = st.columns([1, 0.15, 1])
                with co1:
                    st.subheader("Test Result")
                    st.write("")
                    st.write("🙂 0-8점")
                    st.write("| 정상 범위입니다")
                    st.write("🙁 9-12점")
                    st.write("| 일반적으로 산모들이 느끼는 우울보다 더 많은 우울감을 느끼고 있습니다. 전문가와의 상담을 권유드립니다.")
                    st.write("😔 13-30점")
                    st.write("| 산후 우울증을 겪고 계신 상황인 것 같습니다. 주변 병원에서 치료를 받아보시는 것을 권유드립니다.")

                with co2:
                    st.subheader("Answers")
                    for color, label in color_labels.items():
                        st.markdown(f"- <span style='color:{color}; font-size: 150%'>&#11044;</span> {label}", unsafe_allow_html=True)
                        st.write("")

                st.divider()
                st.subheader("Result Record")
                results = get_results(user, "self_diagnosis")
                if results:
                    result_df = pd.DataFrame(results, columns=["날짜", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "총점"])
                    
                    # 날짜를 datetime 형식으로 변환
                    result_df["날짜"] = pd.to_datetime(result_df["날짜"])
                    
                    # Altair 차트 만들기
                    line = alt.Chart(result_df).mark_line().encode(
                        x=alt.X('yearmonthdate(날짜):T', title='날짜', axis=alt.Axis(format='%Y-%m-%d')),
                        y='총점:Q',
                        tooltip=[alt.Tooltip('yearmonthdate(날짜):T', title='날짜', format='%Y-%m-%d'), '총점:Q']
                    ).properties(
                        title=''
                    )

                    points = alt.Chart(result_df).mark_point().encode(
                        x=alt.X('yearmonthdate(날짜):T', title='날짜', axis=alt.Axis(format='%Y-%m-%d')),
                        y='총점:Q',
                        tooltip=[alt.Tooltip('yearmonthdate(날짜):T', title='날짜', format='%Y-%m-%d'), '총점:Q']
                    ).properties(
                        title=''
                    )

                    combined_chart = line + points

                    # Streamlit에 차트 표시
                    st.write("")
                    st.write("")
                    st.altair_chart(combined_chart, use_container_width=True)
                    st.write("")
                    st.write("")
                    # 각 번호별 점수에 따른 색깔 설정
                    colors = ['#baef9d', '#e8ef9d', '#efd39d', '#efae9d']  # 연두색, 노란색, 주황색, 빨간색
                    
                    for idx, row in result_df.iterrows():
                        date = row["날짜"].strftime('%Y-%m-%d')
                        question_scores = row[1:10].tolist()  # q1 ~ q9 점수 추출
                        total_score = row["총점"]

                        # 각 번호별 점수에 따른 색깔로 시각화
                        fig, ax = plt.subplots(figsize=(8, 0.5))  # 위아래 폭 좁게 만들기
                        for i, score in enumerate(question_scores):
                            ax.scatter(i+1, 0, color=colors[score], s=500)  # 항목 숫자 위에 동그라미로 색 입히기
                            ax.text(i+1, 0, str(i+1), ha='center', va='center', fontsize=12)  # 숫자 표시
                        ax.set_xlim(0.5, len(question_scores)+0.5)  # x 축 범위 설정
                        ax.set_ylim(-0.1, 0.1)  # y 축 범위 설정
                        ax.axis('off')  # 축 숨기기

                        # Total score에 따라 이모지 추가
                        if total_score < 9:
                            st.write(f"🙂| {date} / Total score : {total_score} |")
                        elif 9 <= total_score <= 12:
                            st.write(f"🙁| {date} / Total score : {total_score} |")
                        else:
                            st.write(f"😔| {date} / Total score : {total_score} |")

                        st.pyplot(fig)
                        st.write("")  # 그래프 간격 추가
                else:
                    st.write("결과가 없습니다.")

    # PHQ-9 tab
    elif selected_menu == 'PHQ-9':
        st.title("PHQ-9")
        st.write("우울증을 진단하기 위한 다양한 선별도구 중 PHQ-9(Patient Health QuestionnairePatient Health Questionnaire)는 1999년 Spitzer등에 의해 개발되었습니다. PHQ는 자가보고식 질문지로, 주요우울장애의 진단을 위한 9개의 문항으로 구성되어 있습니다. 기존의 우울증 선별도구에 비해 문항 수가 적어 검사에 소요되는 시간이 짧으면서 우수한 민감도와 특이도를 가진다고 보고되어, 임상에서의 사용이 용이한 것으로 제시되었습니다.")
        st.write("")
        sub_tab1, sub_tab2 = st.tabs(['검사', '검사결과'])

        # PHQ-9 tab
        with sub_tab1:
            st.write("[ Test 실시 방법 ]")
            st.write("- 문항을 너무 오래 생각하지 말고 즉각적으로 솔직하게 응답하시면 됩니다.\n - 현재 기분이 아니라 지난 2주일 동안 기분​​을 가장 잘 나타낸다고 생각되는 문항의 번호를 선택하시면 됩니다.")
            st.divider()
            # Date selection
            selected_date = st.date_input("오늘의 날짜를 선택해 주세요", value=datetime.now(), key='phq_date')
            st.write("")
           # st.write("지난 2주 동안 다음과 같은 문제를 얼마나 자주 겪었는지 해당되는 항목에 표시해주세요 ")

            # Answer options
            answer_option = {
                '전혀 그렇지 않음': 0,
                '며칠동안': 1,
                '1주일 이상': 2,
                '거의 매일': 3
            }

            # Questions for PHQ-9
            phq_questions = [
                "1. 매사에 흥미나 즐거움이 거의 없었나요?",
                "2. 기분이 가라앉거나 우울하거나 희망이 없다고 느껴졌나요?",
                "3. 잠들기 어렵거나 자주 깬다거나 혹은 잠을 너무 많이 주무시나요",
                "4. 피곤하다고 느끼거나 기운이 거의 없으셨나요?",
                "5. 식욕이 줄었거나 혹은 너무 많이 드셨나요?",
                "6. 내 자신이 실패자로 여겨지거나, 가족을 실망시켰다고 느껴졌나요?",
                "7. 신문이나 TV를 보는 것과 같은 일상적인 일에 집중하기 어려우셨나요?",
                "8. 다른 사람들이 눈치 챌 정도로, 평소보다 말과 행동이 느리거나 혹은 너무 안절부절 못해서 가만히 앉아 있을 수 없었나요?",
                "9. 차라리 죽는 것이 낫겠다고 생각하거나, 어떻게든 자해를 하려고 생각하셨나요?"
            ]

            # Display questions in two columns
            phq_scores = {}
            for i, question in enumerate(phq_questions):
                phq_scores[f'q{i+1}'] = question_block(f"**{question}**", answer_option, key=f'phq_q{i+1}')
                st.divider()

            # Show results button
            if st.button("결과 확인하기", key="phq_result"):
                st.subheader("결과")

                # Calculate total score
                phq_total_score = sum(phq_scores.values())

                # Display result message
                if phq_total_score >= 20:
                    st.error("치료가 시급합니다. 이 경우 반드시 정신건강 전문가의 도움을 받으셔야 합니다. 적절한 치료를 받는 것이 중요합니다.")
                elif phq_total_score >= 15:
                    st.warning("상담이 필요합니다. 우울증 위험이 높은 것으로 나타났습니다. 전문가의 상담을 받아보시는 것이 좋습니다.")
                elif phq_total_score >= 10:
                    st.info("경미한 우울증 증상입니다. 주의 깊은 관찰과 추가 평가가 필요할 수 있습니다.")
                else:
                    st.success("정상 범위입니다. 우울증 위험이 낮은 것으로 나타났습니다.")

                # Save result to database
                save_result(user, selected_date, phq_scores, phq_total_score, "phq9")

        # Results tab
        with sub_tab2:
            color_labels = {
                '#baef9d': '전혀 그렇지 않음 / 0점',
                '#e8ef9d': '가끔 그렇음 / 1점',
                '#efd39d': '종종 그렇음 / 2점',
                '#efae9d': '대부분 그렇음 / 3점'
            }

            co1, _, co2 = st.columns([1, 0.15, 1])
            with co1:
                st.subheader("Test Result")
                st.write("")
                st.write("🙂 0-4점")
                st.write("| 정상 범위입니다. 우울증 위험이 낮은 것으로 나타났습니다.")
                st.write("🙁 5-9점")
                st.write("| 경미한 우울증 증상입니다. 주의 깊은 관찰과 추가 평가가 필요할 수 있습니다.")
                st.write("😔 10-19점")
                st.write("| 상담이 필요합니다. 우울증 위험이 높은 것으로 나타났습니다. 전문가의 상담을 받아보시는 것이 좋습니다.")
                st.write("😢 20-27점")
                st.write("| 치료가 시급합니다. 이 경우 반드시 정신건강 전문가의 도움을 받으셔야 합니다. 적절한 치료를 받는 것이 중요합니다.")

            with co2:
                st.subheader("Answers")
                for color, label in color_labels.items():
                    st.markdown(f"- <span style='color:{color}; font-size: 150%'>&#11044;</span> {label}", unsafe_allow_html=True)
                    st.write("")

            st.divider()

            results = get_results(user, "phq9")
            if results:
                result_df = pd.DataFrame(results, columns=["날짜", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "총점"])
                st.subheader("Result Record")
                # Altair 차트 만들기
                line = alt.Chart(result_df).mark_line().encode(
                    x=alt.X('날짜:T', title='날짜', axis=alt.Axis(format='%Y-%m-%d')),
                    y='총점:Q',
                    tooltip=[alt.Tooltip('날짜:T', title='날짜', format='%Y-%m-%d'), '총점:Q']
                ).properties(
                    title=''
                )

                points = alt.Chart(result_df).mark_point().encode(
                    x=alt.X('날짜:T', title='날짜', axis=alt.Axis(format='%Y-%m-%d')),
                    y='총점:Q',
                    tooltip=[alt.Tooltip('날짜:T', title='날짜', format='%Y-%m-%d'), '총점:Q']
                ).properties(
                    title=''
                )

                combined_chart = line + points

                # Streamlit에 차트 표시
                st.write("")
                st.write("")
                st.altair_chart(combined_chart, use_container_width=True)
                st.write("")
                st.write("")
        
                # 각 번호별 점수에 따른 색깔 설정
                colors = ['#baef9d', '#e8ef9d', '#efd39d', '#efae9d']  # 연두색, 노란색, 주황색, 빨간색

                for idx, row in result_df.iterrows():
                    date = row["날짜"]
                    question_scores = row[1:10].tolist()  # q1 ~ q9 점수 추출
                    total_score = row["총점"]

                    # 각 번호별 점수에 따른 색깔로 시각화
                    fig, ax = plt.subplots(figsize=(8, 0.5))  # 위아래 폭 좁게 만들기
                    for i, score in enumerate(question_scores):
                        ax.scatter(i+1, 0, color=colors[score], s=500)  # 항목 숫자 위에 동그라미로 색 입히기
                        ax.text(i+1, 0, str(i+1), ha='center', va='center', fontsize=12)  # 숫자 표시
                    ax.set_xlim(0.5, len(question_scores)+0.5)  # x 축 범위 설정
                    ax.set_ylim(-0.1, 0.1)  # y 축 범위 설정
                    ax.axis('off')  # 축 숨기기

                    # Total score에 따라 이모지 추가
                    if total_score < 5:
                        st.write(f"🙂| {date} / Total score : {total_score} |")
                    elif 10 <= total_score < 10:
                        st.write(f"🙁| {date} / Total score : {total_score} |")
                    elif 15 <= total_score < 20:
                        st.write(f"😔| {date} / Total score : {total_score} |")
                    else:
                        st.write(f"😢| {date} / Total score : {total_score} |")

                    st.pyplot(fig)
                    st.write("")  # 그래프 간격 추가
            else:
                st.write("결과가 없습니다.")

    with st.sidebar:
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #D0E3FF;
        }
        </style>
        """, unsafe_allow_html=True)
        menu = option_menu("MomE", ['Home','Diary', "Mom'ents", '하루 자가진단', 'LogOut'],
                            icons=['bi bi-house', 'bi bi-book', 'bi bi-chat-square-heart', 'bi bi-clipboard-plus', 'box-arrow-in-right'],
                            menu_icon="baby", default_index=3,
                            styles={
                                "icon": {"font-size": "23px"},
                                "title": {"font-weight": "bold"},
                                "nav-link-selected": {"background-color": "#D0E3FF", "color":"#091F5B", "font-family":"'NanumSquareAceb', sans-serif !important"},
                                "container": {"background-color": "#D0E3FF", "color":"#FFF9EF"}
                        })

        # Page navigation
        if menu == 'Diary':
            st.switch_page("pages/diary_page.py")
        elif menu == "Mom'ents":
            st.switch_page("pages/SNS2.py")
        elif menu == 'Home':
            st.switch_page("pages/home.py")
        elif menu == 'LogOut':
            st.switch_page("dd1.py")
            


if __name__ == "__main__":
    init_db()
    main()
