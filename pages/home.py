import base64
import streamlit as st
from streamlit_option_menu import option_menu
import os

# Define and apply custom fonts using Google Fonts
st.markdown(
    """
    <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square.css" rel="stylesheet">
    <style>
        * {
            font-family: 'NanumSquareAcl', sans-serif !important;
        }
    .stApp {
        background: #D0E4FF;
    }
    .Container {
        width: 710px;
        width: 100%; /* 부모 컨테이너 너비 */
        height: 105vh; /* 부모 컨테이너 높이 */
        overflow: hidden;
        border-radius: 30px;
        margin-top: 20px;
    }
    .homeImg {
        position: relative; /* 내부 요소 고정 */
        width: 707px;
        height: 471px;
    }
    .textContainer {
        position: absolute;
        top: 10%;
        left: 75%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        color: white;
        width: 170px;
        height: 90px;
        text-align: start;
    }
    .logo {
        font-size: 60px;
        font-weight: 100;
        color: white;
        font-family: "Inter", sans-serif;
    }
    .logo-below {
        position: absolute; /* 위치 고정 */
        top: 65%;
        left: 11%;
        width: 120px;
        font-size: 13px;
        font-weight: 100;
        color: white;
        font-family: "Inter", sans-serif;
    }
    .adText {
        position: absolute; /* 위치 고정 */
        top: 45%;
        left: 27%;
        transform: translateX(-50%);
        width: 229px;
        height: 95px;
        font-size: 40px;
        font-weight: 400px;
        color: white;
        font-family: "Inter", sans-serif;
        line-height: 1.2;
    }
    .mainContainer {
        display: flex;
        flex-direction: column;
        align-items: center;
        position: absolute;
        top: 50%;
        width: 707px;
        height: 1900px;
        background-color: white;
        border-radius: 30px 30px 30px 30px;
    }
    .contentIndex {
        font-weight: bold;
        font-size: 20px;
        margin-top: 20px;
        margin-bottom: 30px;
        color: black;
        font-family: 'Nanum Pen Script', cursive;
    }
    .aboutUsContent {
        text-align: center;
        margin: 15px 0px;
        font-size: 17px;
        font-family: 'NanumSquareAcl', sans-serif !important;
    }
    .divider {
        width: 250px;
        height: 1px;
        background-color: #000000;
    }
    .service1, .service2, .service3{
        display: flex;
        flex-direction: column;
        align-items: start;
        border-radius: 30px;
        background-color: #EDF0F5;
        margin-bottom:20px;
    }
    .service1 {
        margin-left: 25px;
        width: 315px;
        height: 275px;
    }
    .service2{
        width: 320px;
        height: 317px;
    }
    .service3{
        margin-left:25px;
        width: 315px;
        height: 307px;
    }
    .titleContainer {
        margin: 25px 20px;
        position: relative;
        width: 200;
        height: 56px;
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .titleBar {
        position: relative;
        width: 2px;
        height: 45px;
        background-color: #091F5B;
        margin-right: 7px;
    }
    .title {
        margin-top: 3px;
        margin-right: 40px;
        font-size: 20px;
        color: #091F5B;
        line-height: 1.2;
        font-family: 'NanumSquareExtraBold', sans-serif !important; ;
    }
    .serviceDetail {
        margin-left: 20px;
        margin-bottom: 20px;
        font-size: 16px;
        text-align: start;
        line-height: 1.4;
        width: 300px;
        height: 50px;
    }
    .imgContainer{
        margin: 20px 0px 40px 0px;
    }
    .img2Container {
        margin: 40px 0px 60px 25px;
        border-radius: 30px;
    }
    .img3Container {
        margin: 20px 25px 50px 0px;
        border-radius: 30px;
    }
    .img4Container {
        margin: 50px 0px 20px 25px;
        border-radius: 30px;
    }
    .copyRightDivider {
        width: 600px;
        height: 1.7px;
        background-color: black;
        margin-bottom: 55px;
    }
    .contact {
        margin: 0px 12px;
        font-size: 10px;
        font-family: 'Nanum Gothic', sans-serif;
    }
    .whatWeDoText{
        font-weight: bold;
        font-size: 20px;
        margin-top: 50px;
        color: black;
        font-family: 'Nanum Pen Script', cursive;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def load_image(image_path):
    if not os.path.exists(image_path):
        st.error(f"File not found: {image_path}")
        return None
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        encoded_image = base64.b64encode(data).decode()
        return encoded_image
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

image_path = "./media/homeImg.jpg"
Img1_path = './media/Img1.png'
Img2_path = './media/Img2.jpg'
Img3_path = './media/Img3.jpg'
Img4_path = './media/Img4.jpg'

homeImg = load_image(image_path)
if homeImg:
    st.markdown(f'''
        <div class="Container">
            <div class="homeImg">
                <img src="data:image/jpg;base64,{homeImg}" />
                <div class="textContainer">
                    <div class="logo">MomE</div>
                </div>
                <div class="adText">We Care<br>Your Mind</div>
                <div class="logo-below">Always here for you</div>
            </div>
            <div class="mainContainer">
                <div class="contentIndex">About Us</div>
                <div class="divider"></div>
                <div class="aboutUsContent">
                    MomE은 산후우울증을 겪었거나 겪고 있는 엄마와 가족들을 위한 특별한 공간입니다.<br>
                    당신의 여정에 함께하며 희망과 회복의 길로 안내합니다. <br><br>
                    산후우울증은 많은 엄마들이 경험하는 어려운 감정입니다. <br>
                    MomE는 이러한 감정을 이해하고 공감하며, 회복을 도와드리기 위해 만들어졌습니다. <br>
                    당신의 마음을 치유하고, 행복한 순간들을 만들어 나갈 수 있는 여정,<br>
                    MomE와 함께하세요.
                </div>
                <div class="divider"></div>
                <div class="whatWeDoText">What we do</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.write('')
    st.write('')
    st.write('')
    st.write('')

    row1, row2 = st.columns(2)

    with row1:
        st.markdown(
                f"""
                <div class="service1">
                    <div class="titleContainer">
                        <div class="titleBar"></div>
                        <div class="title">일기장 감정 <br>분석 서비스</div>
                    </div>
                    <p class="serviceDetail">
                        일기장을 작성할 때 사용한 단어들을 분석해<br>
                        특정 단어 사용의 빈도 수 정보를 제공합니다.<br><br>
                        시간이 지남에 따라 나의 감정 표현의 변화를<br>
                        관찰하며, 자신의 감정을 한층 더 깊이
                        이해할<br>수 있습니다.
                    </p>
                </div>
            """,
            unsafe_allow_html=True
        )

        Img_02 = load_image(Img2_path)
        if Img_02:
            st.markdown(
                f'''
                <div class="img2Container">
                    <img src="data:image/jpg;base64,{Img_02}" />
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown(f"""
            <div class="service3">
                <div class="titleContainer">
                    <div class="titleBar"></div>
                    <div class="title"> 육아 SNS<br>서비스</div>
                </div>
                <div class="serviceDetail">
                    육아의 소중한 순간을 담아 사람들과<br>
                    나눌 수 있는 공간을 만들었습니다.<br><br>
                    아이와 함께했던 특별한 순간들을 기록하고<br>
                    공유해보세요. 경험과 조언을 교환하고<br>
                    서로의 이야기에 귀 기울이며 함께 성장할<br>
                    수 있습니다. 부모로서의 여정을 함께<br>
                    걸어가며 소중한 인연을 만들어보세요.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        Img_04 = load_image(Img4_path)
        if Img_04:
            st.markdown(
                f'''
                <div class="img4Container">
                    <img src="data:image/jpg;base64,{Img_04}"/>
                </div>
                ''',
                unsafe_allow_html=True
            )

    with row2:
        Img_01 = load_image(Img1_path)
        if Img_01:
            st.markdown(
                f'''
                <div class="imgContainer">
                    <img src="data:image/jpg;base64,{Img_01}" />
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown(f"""
            <div class="service2">
                <div class="titleContainer">
                    <div class="titleBar"></div>
                    <div class="title">산후우울증 자가검진<br>테스트</div>
                </div>
                <p class="serviceDetail">
                    산후우울증 자가진단 테스트로 마음의 건강을<br>체크하세요.<br><br>
                    에딘버러 산후우울증 척도(K-EPDS)를 근거로<br>
                    한 산후우울증을 자가검진 할 수 있는 서비스를<br>
                    제공합니다. 자가 검진 테스트 결과를
                    바탕으로 <br>
                    시각화된 데이터를 확인하여 마음의
                    상태를<br>  쉽게 확인할 수 있습니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        Img_03 = load_image(Img3_path)
        if Img_03:
            st.markdown(
                f'''
                <div class="img3Container">
                    <img src="data:image/jpg;base64,{Img_03}" />
                </div>
                ''',
                unsafe_allow_html=True
            )

        st.markdown(
                f"""
                <div class="service2">
                    <div class="titleContainer">
                        <div class="titleBar"></div>
                        <div class="title">가족과의 공유</div>
                    </div>
                    <p class="serviceDetail">
                        일기장을 작성할 때 사용한 단어들을 분석해<br>
                        특정 단어 사용의 빈도 수 정보를 제공합니다.<br><br>
                        시간이 지남에 따라 나의 감정 표현의 변화를<br>
                        관찰하며, 자신의 감정을 한층 더 깊이
                        이해할<br>수 있습니다.
                    </p>
                </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # 문의 및 저작권 표시
    st.markdown("""
        <div class="contact body-font">
            MomE ｜ 주소 경기도 용인시 처인구 외대로 81 한국외국어대학교 ｜ 이메일 susu492@naver.com<br>
            ⓒ MomE
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("Failed to load the home image.")

# Sidebar menu
with st.sidebar:
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #FFF9F0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    menu = option_menu("MomE", ['Home', 'Diary', "Mom'ents", '하루 자가진단', 'LogOut'],
                        icons=['bi bi-house', 'bi bi-book', 'bi bi-chat-square-heart', 'bi bi-clipboard-plus', 'box-arrow-in-right'],
                        menu_icon="baby", default_index=0,
                        styles={
                            "icon": {"font-size": "19px"},
                            "title": {"font-weight": "bold", "font-family":"'NanumSquareAceb', sans-serif !important"},
                            "nav-link-selected": {"font-size":"17px","background-color": "#FFF9EF", "color":"#091F5B","font-weight":"bold",},
                            "container": {"background-color": "#FFF9EF", "color":"#6F96D1"} 
                        })

    # Page navigation
    if menu == 'Diary':
        st.switch_page('pages/diary_page.py')
    elif menu == "Mom'ents":
        st.switch_page('pages/SNS2.py')
    elif menu == '하루 자가진단':
        st.switch_page('pages/self_diagnosis.py')
    elif menu == 'LogOut':
        st.switch_page('dd1.py')
