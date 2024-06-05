import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

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

# Styling
st.markdown(
    """
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
    <style>
        * {
            font-family: 'NanumSquare', sans-serif !important;
        }
        .header {
            color: #FF69B4;
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .intro-box {
            background-color: #fbecf7;
            color: #000000;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .intro-text {
            font-size: 20px;
            margin-bottom: 20px;
        }
        .result {
            background-color: #FFC0CB;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def main():

    user = st.session_state.get('logged_in_user', '')  # session_state에서 사용자 이름 가져오기
    if not user:
        st.error("로그인이 필요합니다.")
        return
    
    # Sidebar menu
    with st.sidebar:
        selected_menu = option_menu("MomE", ['산후우울증이란', 'K-EPDS', 'PHQ-9'],
                                    icons=['book', 'clipboard-data', 'clipboard-check'],
                                    menu_icon="baby", default_index=0,
                                    styles={
                                        "icon": {"font-size": "23px"},
                                        "title": {"font-weight": "bold"}
                                    })

    # 산후우울증이란 tab
    if selected_menu == '산후우울증이란':
        st.header("산후우울증이란")
        st.markdown(
    """
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
    <style>
        * {
            font-family: 'NanumSquare', sans-serif !important;
        }
        .container{
            background-color: #f3f3f3;
            width: 340px;
            height:220px;
            padding: 20px;
            margin-bottom: 15px;
            border-radius:10px;
        }
        .container1{
            background-color: #f3f3f3;
            width: 340px;
            height:260px;
            padding: 20px;
            margin-bottom: 15px;
            border-radius:10px;
        }
        .container2{
            background-color: #f3f3f3;
            width: 705px;
            height:300px;
            padding: 20px;
            margin-bottom: 15px;
            border-radius:10px;
        }
        .servTitle {
            font-weight: bold;
            font-size: 25px;
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
                    <p class="servTitle"> 산후 우울증이란?</p>
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

        st.markdown('''
        <a href="https://www.nmc.or.kr/nmc22762276/main/main.do">난임·우울증 상담센터 - 국립중앙의료원(전국)</a><br>
        <a href="https://www.mindcare-for-family.kr/">강남세브란스병원(서울권역)</a><br>
        <a href="https://happyfamily.dumc.or.kr/">동국대학교 일산병원(경기북부권역)</a><br>
        <a href="https://happyfamily3375.or.kr/#none">인구보건복지협회 경기도지회(경기도권역)</a><br>
        <a href="https://id-incheon.co.kr/">가천대 길병원(인천권역)</a><br>
        <a href="http://www.hwc1234.co.kr/">현대여성아동병원(전남권역)</a><br>
        <a href="https://happymoa.kr/">경상북도 안동의료원(경북권역)</a><br>
        <a href="http://www.healthymom.or.kr/">경북대학교 병원(대구권역)</a><br>
        <a href="https://www.childcare.go.kr/?menuno=1">임신육아종합포털(아이사랑)</a><br>
        <a href="www.familynet.or.kr">가족센터 1577-9337</a><br>
        <a href="https://www.129.go.kr/index.do">보건복지부 보건복지상담센터 129</a><br>
        <a href="tel:15770199">정신건강 위기상담전화 1577-0199</a><br>
        <a href="tel:15889191">한국생명의전화 1588-9191</a>
        ''', unsafe_allow_html=True)


        
        
    
    # 에딘버러 tab
    elif selected_menu == 'K-EPDS':
        st.header('K-EPDS')
        st.write("여기에 검사에 대한 정보 들어갈거에유")
        sub_tab1, sub_tab2 = st.tabs(['검사', '검사결과'])
    

        # Self-diagnosis tab
        with sub_tab1:
            # Date selection
            selected_date = st.date_input("오늘의 날짜를 선택해 주세요", value=datetime.now())
            st.write("")

            # Answer options
            answer_option = {
                '전혀 그렇지 않음': 0,
                '가끔 그렇음': 1,
                '종종 그렇음': 2,
                '대부분 그렇음': 3
            }



            col1, col2 = st.columns(2)
            with col1:
                q1 = question_block(f"**1. 우스운 것이 눈에 잘 띄고 웃을 수 있었다.**", answer_option, key='q1')
                st.divider()
                q3 = question_block(f"**3. 일이 잘못되면 필요 이상으로 자신을 탓해왔다.**", answer_option, key='q3')
                st.divider()
                q5 = question_block(f"**5. 별 이유 없이 겁먹거나 공포에 휩싸였다.**", answer_option, key='q5')
                st.divider()
                q7 = question_block(f"**7. 너무나 불안한 기분이 들어 잠을 잘 못 잤다.**", answer_option, key='q7')
                st.divider()
                q9 = question_block(f"**9. 너무나 불행한 기분이 들어 울었다.**", answer_option, key='q9')
                
            with col2:
                q2 = question_block(f'**2. 즐거운 기대감에 어떤 일을 손꼽아 기다렸다.**', answer_option, key='q2')
                st.divider()
                q4 = question_block(f"**4. 별 이유 없이 불안해지거나 걱정이 되었다.**", answer_option, key='q4')
                st.divider()
                q6 = question_block(f"**6. 처리할 일들이 쌓여만 있다.**", answer_option, key='q6')
                st.divider()
                q8 = question_block(f"**8. 슬프거나 비참한 느낌이 들었다.**", answer_option, key='q8')
                st.divider()
                q10 = question_block(f"**10. 나 자신을 해치는 생각이 들었다.**", answer_option, key='q10')

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
                    
                    # 날짜별 총점 추이 차트 생성
                    line_chart = alt.Chart(result_df).mark_line().encode(
                        x='날짜:T',
                        y='총점:Q',
                        tooltip=['날짜:T', '총점:Q']
                    ).properties(
                        title=''
                    )
                    st.write("")
                    st.write("")
                    st.altair_chart(line_chart, use_container_width=True)
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
        st.write("여기에 검사에 대한 정보 들어갈거에유")
        sub_tab1, sub_tab2 = st.tabs(['검사', '검사결과'])

        # PHQ-9 tab
        with sub_tab1:
            # Date selection
            selected_date = st.date_input("오늘의 날짜를 선택해 주세요", value=datetime.now(), key='phq_date')
            st.write("")

            # Answer options
            answer_option = {
                '전혀 그렇지 않음': 0,
                '가끔 그렇음': 1,
                '종종 그렇음': 2,
                '대부분 그렇음': 3
            }

            # Questions for PHQ-9
            phq_questions = [
                "1. 지난 2주 동안, 얼마나 자주 우울하거나 희망이 없다고 느꼈습니까?",
                "2. 지난 2주 동안, 얼마나 자주 일에 대한 흥미나 즐거움을 느끼지 못했습니까?",
                "3. 지난 2주 동안, 얼마나 자주 잠을 잘 이루지 못하거나 너무 많이 잤습니까?",
                "4. 지난 2주 동안, 얼마나 자주 피곤하거나 기운이 없었습니까?",
                "5. 지난 2주 동안, 얼마나 자주 식욕이 없거나 너무 많이 먹었습니까?",
                "6. 지난 2주 동안, 얼마나 자주 자신이 실패자라고 느끼거나 자신이나 가족을 실망시켰다고 생각했습니까?",
                "7. 지난 2주 동안, 얼마나 자주 신문이나 텔레비전을 보는 것에 집중하기 어려웠습니까?",
                "8. 지난 2주 동안, 얼마나 자주 평소보다 더 느리게 움직이거나 말했습니까? 혹은 너무 안절부절 못해서 가만히 앉아 있을 수 없었습니다.",
                "9. 지난 2주 동안, 얼마나 자주 자신이 차라리 죽는 것이 낫겠다고 생각하거나 어떤 방식으로든 자신을 해치려는 생각을 했습니까?"
            ]

            # Display questions in two columns
            col1, col2 = st.columns(2)
            phq_scores = {}
            for i, question in enumerate(phq_questions):
                with col1 if i % 2 == 0 else col2:
                    phq_scores[f'q{i+1}'] = question_block(f"**{question}**", answer_option, key=f'phq_q{i+1}')

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
                st.write("🙂 0-9점")
                st.write("| 정상 범위입니다. 우울증 위험이 낮은 것으로 나타났습니다.")
                st.write("🙁 10-14점")
                st.write("| 경미한 우울증 증상입니다. 주의 깊은 관찰과 추가 평가가 필요할 수 있습니다.")
                st.write("😔 15-19점")
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
                # 날짜별 추이 플랏
                st.line_chart(result_df.set_index("날짜")["총점"])

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
                    if total_score < 10:
                        st.write(f"🙂| {date} / Total score : {total_score} |")
                    elif 10 <= total_score < 15:
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
        menu = option_menu("MomE", ['Home','Diary', 'Mom:ents', '하루 자가진단', 'LogOut'],
                            icons=['bi bi-house-fill', 'bi bi-grid-1x2-fill', 'book-half', 'Bi bi-star-fill', 'bi bi-capsule-pill', 'box-arrow-in-right'],
                            menu_icon="baby", default_index=3,
                            styles={
                                "icon": {"font-size": "23px"},
                                "title": {"font-weight": "bold"}
                            })

        # Page navigation
        if menu == 'Diary':
            st.switch_page("pages/diary_page.py")
        elif menu == 'Mom:ents':
            st.switch_page("pages/SNS2.py")
        elif menu == 'Home':
            st.switch_page("pages/home.py")
        elif menu == 'LogOut':
            st.switch_page("dd1.py")
            


if __name__ == "__main__":
    init_db()
    main()
