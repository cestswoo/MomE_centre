import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import random
import pandas as pd
import sqlite3
from datetime import datetime
from streamlit_option_menu import option_menu
import plotly.express as px
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 모델과 토크나이저 로드
model_name = 'nlptown/bert-base-multilingual-uncased-sentiment'
model_dir = "./models"

@st.cache_resource
def load_model_and_tokenizer():
    tokenizer = BertTokenizer.from_pretrained(model_name, cache_dir=model_dir, use_fast=True)
    model = BertForSequenceClassification.from_pretrained(model_name, cache_dir=model_dir)
    return tokenizer, model

tokenizer, model = load_model_and_tokenizer()

# SentiWord_Dict.txt 파일 로드 함수
def load_sentiword_dict(file_path):
    senti_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, score = parts
                senti_dict[word] = int(score)
    return senti_dict

sentiword_dict = load_sentiword_dict('pages/SentiWord_Dict.txt')

# BERT를 사용한 감성 분석 함수
def analyze_sentiment_bert(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs.detach().numpy()[0]

# 감성 점수 해석 및 메시지 반환 함수
def interpret_sentiment(probabilities):
    sentiments = ['매우 부정적', '부정적', '중립', '긍정적', '매우 긍정적']
    sentiment_probs = dict(zip(sentiments, probabilities))
    max_sentiment = max(sentiment_probs, key=sentiment_probs.get)

    messages = {
        '매우 부정적': ['오늘은 정말 힘든 하루였겠네요. 다음에는 분명 좋은 일들이 생길 거예요.', '하루를 마무리하기까지 정말 힘든 시간을 보내셨겠네요. 내일은 분명 더 나은 날이 될 거예요.', '어려운 하루를 보내셨겠어요. 하지만 그런 날들도 우리를 성장시키고 더 강하게 만들어 줍니다.'],
        '부정적': ['오늘은 정말 힘드셨을 테지만, 이런 날들도 지나갈 거예요.', '고된 하루를 보내셨겠네요. 내일은 분명히 더 나은 날이 될 거예요.', '어려운 하루를 보내셨을 텐데, 내일은 조금 더 나은 날이 될 거예요.'],
        '중립': ['평범한 하루였겠네요. 가끔은 그런 일상의 조용한 순간들이 가장 소중한 법이죠.', '일상적인 하루를 보내셨겠어요. 때로는 평온함이 가장 큰 축복이 될 수 있어요.', '무탈한 하루를 보내셨네요. 가벼운 일상 속에서도 소중한 순간들을 발견할 수 있어요.'],
        '긍정적': ['좋은 하루를 보내셨군요! 오늘은 그런 하루였나 봐요.', '행복한 하루를 보내셨겠어요! 이런 날들이 계속되길 바랄게요.', '좋은 하루를 보내셨네요! 감사한 마음으로 잠자리에 들 수 있을 거예요.'],
        '매우 긍정적': ['정말 멋진 하루를 보내셨겠네요! 이런 순간이 계속 이어지길 바랄게요.', '최고의 하루를 보내셨군요! 이 기쁨이 더 오래 이어지길 기대할게요.', '놀라운 하루를 보내셨군요! 이런 순간이 더 자주 찾아오길 기대할게요.']
    }

    random_message = random.choice(messages[max_sentiment])
    return sentiment_probs, random_message

# SentiWord_Dict.txt를 사용하여 일기에서 단어 찾기 함수
def find_sentiwords(text, senti_dict):
    found_words = []
    for word in text.split():
        if word in senti_dict:
            found_words.append((word, senti_dict[word]))
    return found_words

# 주제 리스트 정의
topics = [
    '일주일 중 가장 기억에 남는 순간에 대해 써 보세요.', '여태까지 당연시해 왔지만 사실 숨겨져 있었던 재능이 있다면 무엇인가요?', '친구들이 놀랄 만한 나의 좋은 점은 무엇인가요?',
    '최근 경험한 것 중 가장 좋았거나 경외심을 불러일으켰던 순간은 무엇인가요?', '최근의 일들을 되돌아 보고 이번 주에 즐거움을 준 것에 대해 적어보세요.',
    '혼자서 일할 때와 다른 사람과 함께 일할 때 언제 더 창의적이라고 느끼나요? 왜 그런다고 생각하나요?', '어렸을 때 가장 즐겼던 예술 활동이나 다른 창의적인 활동에 대해 적어 보세요',
    '최근에 영감을 받았던 경험을 떠올려 보세요. 어떤 것으로 인해 영감을 받았는지 생각해 보세요.', '아는 사람 중 가장 창의력이 풍부한 사람은 누구인가요? 그 사람의 창의력에 대해 적어보세요.',
    '최근에 했던 새로운 아이디어를 생각해 보세요. 어떤 계기로 이런 아이디어가 떠올랐고 이 아이디어를 위해 어떻게 시간을 낼 수 있었나요?', '최근에 한 가지 배운 것이 있다면 무엇인가요? 그것은 어떤 면에서 중요한가요?',
    '밤에 잠 못 이루게 하는 생각은 무엇인가요?', '소중한 관계인 사람을 마음에 떠올려 보고 그 관계에서 배울 수 있는 점을 적어보세요.', '최근에 배운 것 중 모두가 알았으면 하는 것이 있나요?',
    '지금까지 만난 사람 중 가장 지혜로운 사람은 누구이며, 왜 그런가요?', '아이에게 가장 놀랐던 순간이 있었나요? 그 순간을 공유해주세요.', '배우자에게 감동 받았던 기억이 있나요? 그 기억을 공유해주세요.',
    '아이에게 감동 받았던 순간이 있나요? 그 순간을 적어주세요.', '아이를 기르며 가장 힘들었던 순간은 언제인가요? 그 순간을 말해주세요.', '배우자와 보낸 가장 기억에 남는 시간은 언제인가요? 그 시간의 기억을 말해주세요.',
    '언제 아이가 나를 웃게 만드나요?', '지금 이 순간에 감사한 것들이 있나요?', '오늘 나에게 해주고 싶은 위로와 격려의 말이 있나요?', '주변 사람들에게 받은 지지와 응원의 말들을 기록해주세요.',
    '나 자신에게 주고 싶은 작은 선물이나 보상을 적어주세요.', '오늘 나의 몸과 마음의 상태를 체크하고, 나를 위한 휴식 방법을 적습니다.', '아기의 작은 변화나 성장 과정을 적어보세요.',
    '아기를 돌보는 중에도 나만을 위한 시간을 가졌던 순간을 적어보세요.', '하루 일과를 정리해보고, 그 중에서 좋았던 부분들을 적어보세요.', '마음 챙김이나 명상을 하며 느꼈던 평온한 감정을 기록 해보세요'
]

# 주제 추천 함수
def recommend_topics(topics, num=6):
    return random.sample(topics, num)

# SQLite 데이터베이스 초기화 함수 (존재하지 않을 경우 테이블 생성)
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            diary TEXT,
            sentiment TEXT,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_diary_to_db(username, date, diary, sentiment, message):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diary (username, date, diary, sentiment, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, date, diary, str(sentiment), message))
        conn.commit()
    except sqlite3.OperationalError as e:
        st.error(f"An error occurred while saving the diary: {e}")
    finally:
        conn.close()

def load_diary_data(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT date, diary, sentiment, message FROM diary WHERE username = ?', (username,))
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        st.error(f"An error occurred while loading the diary: {e}")
        rows = []
    conn.close()
    return pd.DataFrame(rows, columns=['date', 'Diary', 'Sentiment', 'Message'])

def send_email(subject, content, recipient_email):
    sender_email = "eseungwo0123@gmail.com"
    sender_password = "tpzglsofchulupuw"  # 여기에는 앱 비밀번호를 입력합니다
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(content, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False

# Streamlit 앱 메인 함수
def main():
    # SQLite 데이터베이스 초기화
    init_db()

    # CSS 스타일 추가
    st.markdown(
        """
        <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
        <style>
        *{
            font-family: 'NanumSquare', sans-serif !important;
        }
        .stApp{
            background: #D0E4FF;
            font-family: 'NanumSquareAcb';
            }
        .stTabs [role="tabpanel"] {
            background-color: #ffffff; /* Change this to your desired content background color */
            /* border: 2px solid #4dd0e1;  */
            border-top: none;
            padding: 20px;
            border-radius: 0 0 30px 30px;
            box-shadow: 5px 5px 5px #DFDCD5;
            height: 1300px;
        }
        .stTabs [data-baseweb="tab-list"] 
            button [data-testid="stMarkdownContainer"] p {
            font-size:16px;
            color: #091F5B;
            font-family: 'NanumSquareAceb', sans-serif !important;
            }
            div[data-testid="stTabs"] button[aria-selected="true"]::after {
                content: "";
                display: block;
                border-bottom: 4px solid #ffffff;
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
            }
             div[data-testid="stTabs"] div[role="tablist"] {
                background-color: #ffffff;
                padding: 10px;
                border-radius: 30px 30px 0px 0px;
            }
            div[data-testid="stTabs"] button[aria-selected="true"] {
                background-color: #EDF0F5;
                color: white;
                border-radius: 30px;
                padding: 0pc 5px;
            }
            div[data-testid="stTabs"] button {
                color: white;
                background-color: #ffffff;
            }
        .stButton button {
            background-color: #FFF9EF !important;
            border-radius: 12px;
            padding: 10px 24px;
            text-align: center;
            font-size: 20px;
            cursor: pointer;
            width: 30%;
            border: none;
            color: #091F5B !important;
        }
        .stButton button:hover {
            background-color: #091F5B !important;
            color: #ffffff !important;
        }
        .subtitle{
            font-size: 25px;
            font-weight:bold;
            text-align: start;
            line-height: 1;
            letter-spacing: 0;
            margin-bottom: 10px;
            color: #091F5B;
            text-align: center;
            margin-bottom: 20px;
            font-family: 'NanumSquareAceb';
        }
        .topic-card{
            color: #091F5B;
            background-color: #FFF9F0;
            box-shadow: 3px 3px 3px #DFDCD5;
            margin:5px;
            border-radius: 10px;
            padding: 7px;
            font-family: 'NanumSquareAcb', sans-serif !important;
        }
        .topic{
            margin: 7px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .sidebar .sidebar-content {
            background-color: #000000;  /* 사이드바 배경 색상 설정 */
        }
        .sidebar .sidebar-content .css-1d391kg {
            background-color: #f0f2f6;
        }
        .contact {
            margin: 0px 12px;
            font-size: 10px;
            font-family: 'Nanum Gothic', sans-serif;
        }
        .stButton button {
            background-color: #091F5B;
            border-radius: 12px;
            padding: 10px 24px;
            text-align: center;
            font-size: 20px;
            cursor: pointer;
            width: 30%;
            border: none;
            color: #000000;
        }
        .stButton button:hover {
            background-color: #091F5B;
            color: #ffffff;
           }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.image('media/diaryTitleImg.png')

    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        
        tabs = st.tabs(["일기 작성", "분석 결과", "지난 일기"])

        with tabs[0]:
            st.markdown(
                '''
                  <div class="subtitle">일기 주제 추천</div>
        
                ''',unsafe_allow_html=True
            )   
            recommended_topics = recommend_topics(topics, num=6)

            topic_cols = st.columns(2)

            for idx, topic in enumerate(recommended_topics):
                with topic_cols[idx % 2]:
                    st.markdown(f'''<div class='topic-card'>
                                        <div class='topic'>
                                            {topic}
                                        </div>
                                </div>''', unsafe_allow_html=True) 
            st.write("")

            user_input = st.text_area('', placeholder="여기에 일기를 작성해 주세요.", height=300)
            
            if st.button("분석하기"):
                probabilities = analyze_sentiment_bert(user_input)
                sentiment_probs, result_message = interpret_sentiment(probabilities)

                save_diary_to_db(st.session_state.get('logged_in_user'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_input, sentiment_probs, result_message)

                st.session_state['sentiment_probs'] = sentiment_probs
                st.session_state['result_message'] = result_message
                st.session_state['user_input'] = user_input

                st.success("분석이 완료되었습니다. '분석 결과' 탭을 확인하세요.")

        with tabs[1]:
            if 'sentiment_probs' in st.session_state:
                st.write(f"#### {st.session_state['result_message']}")
                st.divider()
                
                st.write("#### 감정 분포")
                # 원형 차트로 변경
                custom_colors = ['#A8E6CF','#DCEDC1','#E0E0E0','#FFAAA5','#FF8B94']  # 원하는 색상 리스트
                fig = px.pie(values=list(st.session_state['sentiment_probs'].values()), names=list(st.session_state['sentiment_probs'].keys()), color_discrete_sequence=custom_colors)
                st.plotly_chart(fig)

                st.write("#### 내가 쓴 일기 분석결과:")
                for sentiment, prob in st.session_state['sentiment_probs'].items():
                    st.write(f"{sentiment}: {prob:.2%}")
                
                found_words = find_sentiwords(st.session_state['user_input'], sentiword_dict)
                if found_words:
                    negative_words = [word for word, score in found_words if score < 0]
                    positive_words = [word for word, score in found_words if score > 0]
                        
                    st.write("#### 일기에서 발견된 감성 단어")
                    if negative_words:
                        st.write(f"사용한 부정 단어: {', '.join(negative_words)}")
                    else:
                        st.write("사용한 부정 단어가 없습니다.")
                    
                    if positive_words:
                        st.write(f"사용한 긍정 단어: {', '.join(positive_words)}")
                    else:
                        st.write("사용한 긍정 단어가 없습니다.")
                else:
                    st.write("일기에서 감성 단어를 찾을 수 없습니다.")
                
                share_emotion = st.checkbox("지금 이 감정을 공유하고 싶은 사람이 있나요?")
                
                if share_emotion:
                    recipient_email = st.text_input("공유할 이메일 주소를 입력하세요", "")
                    if st.button("요약 보내기"):
                        email_content = f"""
                        일기 내용: {st.session_state['user_input']}
                        감정 확률 분포: {', '.join([f'{k}: {v:.2%}' for k, v in st.session_state['sentiment_probs'].items()])}
                        {st.session_state['result_message']}
                        """
                        if send_email("감정 분석 요약", email_content, recipient_email):
                            st.success("요약이 성공적으로 전송되었습니다.")
                        else:
                            st.error("요약 전송에 실패했습니다.")
            else:
                st.write("아직 분석 결과가 없습니다. 먼저 '일기 작성' 탭에서 분석을 진행하세요.")

        with tabs[2]:
            # 지난 일기 탭 내용
            st.write("### 지난 일기")
            username = st.session_state.get('logged_in_user')
            if not username:
                st.error("로그인이 필요합니다.")
                return

            diary_data = load_diary_data(username)
           
            if not diary_data.empty:
                selected_date = st.selectbox("날짜 선택", diary_data['date'].unique())
                
                if selected_date: 
                    selected_diary = diary_data[diary_data['date'] == selected_date]
                    for idx, row in selected_diary.iterrows():
                        st.write(f"#### {row['date']}")
                        st.write(f"**일기 내용:** {row['Diary']}")
                        st.write("**분석 결과:**")
                        sentiment_probs = eval(row['Sentiment'])
                        for sentiment, prob in sentiment_probs.items():
                            st.write(f"{sentiment}: {prob:.2%}")
                        st.write(f"**ㄴ** {row['Message']}")
            else:
                st.write("저장된 일기가 없습니다.")
    else:
        st.error("로그인 후 이용해주세요")

# 앱 실행
with st.sidebar:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #FFF9F0;
        }
        </style>
    """, unsafe_allow_html=True)
    menu = option_menu("MomE", ['Home','Diary',"Mom'ents",'Self-Check', 'LogOut'],
                        icons=['bi bi-house-fill', 'book-half','Bi bi-star-fill' ,'bi bi-capsule-pill', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=1,
                        styles={
                            "icon": {"font-size": "23px"},
                            "title": {"font-weight": "bold"},
                            "nav-link-selected": {"background-color": "#FFF9EF", "color":"#091F5B", "font-family":"'NanumSquareAceb', sans-serif !important"},
                            "container": {"background-color": "#FFF9EF", "color":"#6F96D1"} 
                        })

if menu =='Home':
    st.switch_page("pages/home.py")
elif menu == "Mom'ents":
    st.switch_page("pages/SNS2.py")
elif menu =='Self-Check': 
    st.switch_page("pages/self_diagnosis.py")
elif menu =='LogOut':
    st.switch_page('dd1.py')

if __name__ == "__main__":
    main()
