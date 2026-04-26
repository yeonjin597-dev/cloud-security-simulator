import streamlit as st
import pandas as pd
import time

# ==========================================
# (1) 페이지 기본 설정 및 레이아웃
# ==========================================
st.set_page_config(
    page_title="클라우드 보안 사고 대응 퀴즈", 
    page_icon="🛡️", 
    layout="wide"
)

# ==========================================
# (2) 상태 관리 (Session State)
# ==========================================
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'server_hp' not in st.session_state:
    st.session_state.server_hp = 100
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'is_finished' not in st.session_state:
    st.session_state.is_finished = False
if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False

# ==========================================
# (3) 캐싱 기능 (@st.cache_data)
# ========================================
@st.cache_data
def load_server_logs():
    with st.spinner("🔍 시스템에서 대용량 보안 로그를 정밀 분석 중입니다..."):
        # 1.2초보다 3초가 나은듯? 캐싱기능시연
        time.sleep(3.0) 
        data = pd.read_csv("data/server_logs.csv")
    return data

# ==========================================
# (4) 메인 헤더
# ==========================================
def show_header():
    st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 6px solid #2e59d9; margin-bottom: 20px;">
            <h2 style="color: #333333; margin-bottom: 5px;">🛡️ 통합 클라우드 보안 사고 대응 퀴즈</h2>
            <p style="color: #555555; margin-top: 10px; font-size: 16px;">
                <b>담당 관리자:</b> 정연진 (학번: 2025404018)
            </p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# (5) 로그인 화면
# ==========================================
def login_screen():
    show_header()
    st.markdown("### 🔒 관리자 인증")
    col1, _ = st.columns([1, 1])
    with col1:
        with st.form("login_form"):
            user_id = st.text_input("아이디 (admin)")
            user_pw = st.text_input("비밀번호 (2006)", type="password")
            if st.form_submit_button("시스템 접속"):
                if user_id == "admin" and user_pw == "2006":
                    st.session_state.is_logged_in = True
                    st.rerun()
                else:
                    st.error("인증 정보가 올바르지 않습니다.")

# ==========================================
# (6) 메인 대시보드
# ==========================================
def main_dashboard():
    # 사이드바 구성
    with st.sidebar:
        st.markdown("### 📊 실시간 상태")
        st.metric(label="서버 무결성(HP)", value=f"{st.session_state.server_hp}%")
        st.progress(st.session_state.server_hp / 100)
        st.markdown("---")
        if st.button("🔌 안전하게 로그아웃"):
            st.session_state.clear()
            st.rerun()

    if st.session_state.is_finished:
        show_final_report()
        return    
      

    # [중요] 로그 뷰어 상시 노출 (초보자를 위해 항상 위에 배치)
    st.markdown("### 🔍 실시간 서버 로그 모니터링")
    logs = load_server_logs()
    st.dataframe(logs, use_container_width=True, height=250)
    st.caption("※ 이 로그 데이터는 캐싱 기술을 통해 분석 속도가 최적화되었습니다.")
    st.markdown("---")


    quiz_data = {
        1: {
            "title": "1단계: 공격자 IP 추적",
            "q": "현재 서버에 누군가 강제로 접속하려는 시도가 포착되었습니다. 로그에서 'CRITICAL' 경고와 함께 'BRUTE FORCE ATTACK'을 일으키는 공격자의 IP 주소를 찾아 입력하세요.",
            "ans": "203.0.113.42",
            "exp": """**답: [ 203.0.113.42 ]**\n\n
**상세 해설:**\n
이 과정은 보안 사고 발생 시 **'누가 우리 서버를 공격하는가'**를 파악하는 가장 기초적인 단계입니다. 로그 데이터의 5번 줄을 보면 'BRUTE FORCE ATTACK DETECTED'라는 메시지가 있습니다.\n\n
**무차별 대입 공격(Brute Force Attack)**이란, 해커가 비밀번호를 알아내기 위해 가능한 모든 조합을 하나씩 다 대입해보는 공격입니다. 마치 수만 개의 열쇠를 하나씩 자물쇠에 꽂아보는 것과 같습니다. 보안 로그는 이 시도를 '전부 기록'하기 때문에, 짧은 시간 내에 반복적으로 실패한 기록이 남은 **203.0.113.42**라는 주소가 바로 범인의 '인터넷상 주소'임을 알 수 있습니다."""
        },
        2: {
            "title": "2단계: 네트워크 방화벽 차단",
            "q": "추적한 공격자 IP(203.0.113.42)가 다시는 우리 서버에 발을 들이지 못하게 막아야 합니다. 가장 적절한 리눅스 명령어를 선택하세요.",
            "opts": ["ls -al /var/log", "iptables -A INPUT -s 203.0.113.42 -j DROP", "chmod 777 /etc/passwd"],
            "ans": "iptables -A INPUT -s 203.0.113.42 -j DROP",
            "exp": """**답: [ iptables -A INPUT -s 203.0.113.42 -j DROP ]**\n\n
**상세 해설:**\n
리눅스 서버에는 **iptables**라는 아주 똑똑한 '문지기(방화벽)'가 있습니다. 이 문지기에게 내리는 명령의 뜻을 하나씩 풀어볼까요?\n\n
1. **iptables**: 방화벽을 관리하겠다는 명령어입니다.\n
2. **-A INPUT**: 우리 서버로 '들어오는(INPUT)' 길에 규칙을 '추가(Append)'하겠다는 뜻입니다.\n
3. **-s 203.0.113.42**: '출발지(Source)'가 이 주소인 녀석을 찾으라는 명령입니다.\n
4. **-j DROP**: 해당 주소에서 오는 모든 데이터 패킷을 '그냥 버려라(DROP)'라고 명령하는 것입니다. \n\n
이 명령어를 실행하면, 해커는 우리 서버의 존재 자체를 찾을 수 없게 됩니다. 이는 리눅스 마스터 자격증에서도 다루는 핵심적인 서버 보안 기술입니다."""
        },
        3: {
            "title": "3단계: 악성 프로세스 강제 종료",
            "q": "해커가 남기고 간 악성 프로그램이 서버의 CPU를 99%나 사용하고 있습니다. 로그 상단에서 과부하를 일으키는 프로세스 번호(4092)를 찾아 강제로 종료시키는 명령어를 입력하세요.",
            "ans": "kill -9 4092",
            "exp": """**답: [ kill -9 4092 ]**\n\n
**상세 해설:**\n
리눅스 서버에서 실행되는 모든 프로그램은 **PID(Process ID)**라는 고유 번호를 가집니다. 마치 사람의 주민등록번호와 같습니다. \n\n
해커의 악성 코드가 우리 서버의 자원을 갉아먹고 있다면, 우리는 **kill**이라는 명령어로 이 프로그램을 종료시켜야 합니다. \n\n
하지만 악성 프로그램은 스스로 죽지 않으려고 저항할 때가 많습니다. 이때 사용하는 옵션이 바로 **-9**입니다. 이것은 운영체제에게 '이유 불문하고 즉시 이 프로그램을 강제로 죽여라(SIGKILL)'라고 내리는 가장 강력한 명령입니다. 4092번 프로그램을 강제로 종료함으로써 서버의 속도를 다시 정상으로 돌려놓을 수 있습니다."""
        },
        4: {
            "title": "4단계: 중요 폴더 권한 잠금",
            "q": "해커가 노렸던 /backup 폴더의 보안을 강화해야 합니다. '나(소유자)' 외에는 아무도 이 폴더를 보지도, 건드리지도 못하게 만드는 명령어를 선택하세요.",
            "opts": ["chmod 777 /backup", "chmod 700 /backup", "chmod 400 /backup"],
            "ans": "chmod 700 /backup",
            "exp": """**답: [ chmod 700 /backup ]**\n\n
**상세 해설:**\n
리눅스 권한(Permission) 시스템은 숫자로 표현됩니다. '700'이라는 숫자의 비밀을 알려드릴게요.\n\n
숫자는 **[나 / 그룹 / 남들]** 세 자리를 의미합니다. \n
- **7**: 읽기(4) + 쓰기(2) + 실행(1)의 합입니다. 즉, 모든 권한을 가진다는 뜻입니다.\n
- **0**: 아무 권한도 없다는 뜻입니다.\n\n
따라서 **700**은 '나(소유자)에게는 모든 권한을 주지만, 그룹원이나 낯선 남들에게는 아무것도 허용하지 않겠다'는 뜻입니다. 해커가 다른 경로로 서버에 들어오더라도, 이 권한 설정을 해두면 백업 데이터만큼은 절대로 훔쳐갈 수 없습니다. 보안의 기본 중의 기본입니다."""
        },
        5: {
            "title": "5단계: 데이터 유출 이상 탐지",
            "q": "데이터 분석(ADsP) 관점에서, 서버 내부의 자료가 밖으로 빠져나간 '유출 시작 시각'을 로그에서 찾아 입력하세요. (형식: 00:00:00)",
            "ans": "10:13:00",
            "exp": """**답: [ 10:13:00 ]**\n\n
**상세 해설:**\n
침해 사고 대응에서 가장 무서운 것은 데이터 유출입니다. 로그의 마지막 줄을 보면 'Unusual outbound traffic'이라는 경고가 **10:13:00**에 발생했습니다.\n\n
**아웃바운드 트래픽(Outbound Traffic)**이란 우리 서버에서 '외부 인터넷'으로 나가는 데이터를 말합니다. 평소보다 갑자기 많은 데이터가 외부로 전송되기 시작했다면, 해커가 우리 서버의 데이터를 자신의 컴퓨터로 빼돌리기 시작했다는 강력한 증거입니다. 데이터 분석가(ADsP)는 이런 로그의 이상 패턴을 분석해 언제, 얼마나 많은 자료가 유출되었는지 파악하는 중요한 역할을 수행합니다."""
        },
        6: {
            "title": "6단계: AWS 근본 보안 강화",
            "q": "앞으로는 이런 공격이 아예 우리 서버 입구 근처에도 못 오게 막고 싶습니다. AWS 클라우드에서 '네트워크망' 전체를 지키는 가장 바깥쪽 방화벽은 무엇일까요?",
            "opts": ["Amazon S3", "AWS IAM", "Network ACL"],
            "ans": "Network ACL",
            "exp": """**답: [ Network ACL ]**\n\n
**상세 해설:**\n
AWS(아마존 웹 서비스)는 보안을 여러 겹으로 쌓아서 관리합니다. \n\n
1. **Security Group(보안 그룹)**: 내 컴퓨터 바로 앞에 있는 '현관문 잠금장치'입니다.\n
2. **Network ACL**: 우리 집이 속한 '마을 입구의 검문소'입니다.\n\n
해커의 IP를 미리 알고 있다면, 개별 컴퓨터마다 막는 것보다 마을 입구(Network ACL)에서부터 차단하는 것이 훨씬 효과적이고 안전합니다. 이를 통해 서버(EC2)에 부하를 주지 않고도 공격을 원천적으로 봉쇄할 수 있습니다. 이것이 바로 전문가들이 설계하는 클라우드 아키텍처의 핵심입니다."""
        }
    }

    # 현재 단계 데이터
    current_step = st.session_state.step
    data = quiz_data[current_step]

    st.subheader(f"대응 단계 {current_step}: {data['title']}")
    st.info(data["q"])

    # 해설 보기 전
    if not st.session_state.show_explanation:
        with st.form(f"quiz_form_{current_step}"):
            if "opts" in data:
                user_ans = st.radio("알맞은 해결책을 선택하세요:", data["opts"])
            else:
                user_ans = st.text_input("분석된 정답을 입력하세요:")
            
            if st.form_submit_button("명령어 실행 및 상세 분석 확인"):
                # 정답 판별
                is_correct = False
                if "opts" in data:
                    is_correct = (user_ans == data["ans"])
                else:
                    is_correct = (user_ans.strip().lower() == data["ans"].lower())
                
                if is_correct:
                    st.session_state.is_correct = True
                    st.toast("대응 성공!", icon="🟢")
                else:
                    st.session_state.is_correct = False
                    st.session_state.server_hp -= 20
                    st.toast("대응 실패! 서버가 손상되었습니다.", icon="🔴")
                
                st.session_state.show_explanation = True
                st.rerun()

    # 해설 보기 상태
    else:
        if st.session_state.is_correct:
            st.success("✅ 정확한 조치입니다!")
        else:
            st.error(f"❌ 잘못된 조치입니다. 정답은 {data['ans']} 입니다.")
        
        # 해설 출력
        st.markdown(f"""
        <div style="background-color: #f1f3f5; padding: 25px; border-radius: 8px; border-left: 5px solid #6c757d; margin: 20px 0;">
            {data['exp']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("내용을 이해했습니다. 다음 단계로 ➡"):
            st.session_state.show_explanation = False
            if current_step < 6:
                st.session_state.step += 1
            else:
                st.session_state.is_finished = True
            st.rerun()

# ==========================================
# (7) 결과 리포트
# ==========================================
def show_final_report():
    st.markdown("## 📜 최종 보안 사고 대응 리포트")
    hp = st.session_state.server_hp
    
    if hp == 100: grade, title = "S", "🏆 수석 클라우드 아키텍트"
    elif hp >= 60: grade, title = "A", "⭐ 보안 운영 엔지니어"
    elif hp > 0: grade, title = "B", "🔧 시스템 관리 실무자"
    else: grade, title = "F", "💀 보안 관제 실패"

    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 30px; border-radius: 8px; text-align: center; margin-bottom: 20px;">
        <h3 style="color: #333;">최종 시스템 보존율: <span style="color: #2e59d9; font-size: 32px;">{hp}%</span></h3>
        <h4 style="color: #555;">종합 평가 등급: {grade}</h4>
        <h4 style="color: #2e59d9;">획득 칭호: {title}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("본 시뮬레이션을 통해 리눅스 서버 보안, 데이터 분석, 그리고 AWS 클라우드 인프라 방어의 핵심 원리를 실습하였습니다.")
    
    if st.button("다시 처음부터 실습하기"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 메인 제어 로직
# ==========================================
if not st.session_state.is_logged_in:
    login_screen()
else:
    main_dashboard()