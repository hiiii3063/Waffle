
import streamlit as st
import time
import random

st.set_page_config(
    page_title="따끈따끈 와플 주방",
    page_icon="🧇",
    layout="centered"
)

# -------------------- 디자인 --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&display=swap');

.stApp {
    background: linear-gradient(180deg, #fff8e9, #f2dfc1);
    color: #56351f;
    font-family: 'Gowun Dodum', sans-serif;
}
h1, h2, h3 {
    color: #714426;
    font-family: 'Jua', sans-serif;
}
.hero {
    background: linear-gradient(135deg, #704126, #bd8050);
    color: #fff7e8;
    padding: 25px 15px;
    border-radius: 22px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 6px 0 #54321e;
}
.hero h1 {
    color: #fff7e8 !important;
    font-size: 2.5rem;
}
.panel {
    background: #fffaf0;
    border: 2px solid #e5c69c;
    border-radius: 18px;
    padding: 18px;
    margin: 12px 0;
}
.stat {
    background: #fffaf0;
    border: 1px solid #dfbf94;
    border-radius: 14px;
    padding: 12px 5px;
    text-align: center;
}
.stat-label {
    color: #866044;
    font-size: 0.9rem;
}
.stat-value {
    color: #704126;
    font-family: 'Jua', sans-serif;
    font-size: 1.5rem;
}
div.stButton > button {
    background: #87512f;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 3rem;
    font-family: 'Jua', sans-serif;
    font-size: 1.1rem;
}
div.stButton > button:hover {
    background: #60371f;
    color: white;
}
div[data-testid="stSlider"] label {
    color: #714426;
    font-weight: bold;
}
.note {
    color: #866044;
    text-align: center;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)


# -------------------- 게임 초기화 --------------------
def init_game():
    best = st.session_state.get("best_score", 0)

    st.session_state.round_no = 1
    st.session_state.score = 0
    st.session_state.best_score = best
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.phase = "pour"
    st.session_state.batter = 50
    st.session_state.bake_start = None
    st.session_state.bake_duration = 7.0
    st.session_state.results = []
    st.session_state.message = ""


if "round_no" not in st.session_state:
    init_game()


# -------------------- 공통 처리 --------------------
def end_game(success, message):
    st.session_state.game_over = True
    st.session_state.won = success
    st.session_state.message = message
    st.session_state.best_score = max(
        st.session_state.best_score,
        st.session_state.score
    )


def finish_waffle(progress):
    # 적절한 타이밍: 55~75%
    if progress < 55:
        st.session_state.results.append(
            f"❌ {st.session_state.round_no}번째 와플: 너무 일찍 뒤집음"
        )
        end_game(False, "와플이 덜 익었을 때 뒤집었어요!")
        return

    if progress > 75:
        st.session_state.results.append(
            f"❌ {st.session_state.round_no}번째 와플: 너무 늦게 뒤집음"
        )
        end_game(False, "뒤집기 타이밍을 놓쳐 와플이 탔어요!")
        return

    # 성공 점수 및 보너스
    batter = st.session_state.batter
    base_points = 100
    batter_bonus = max(0, 30 - abs(batter - 50) * 2)
    timing_bonus = max(0, 30 - int(abs(progress - 65) * 2))
    points = base_points + batter_bonus + timing_bonus

    st.session_state.score += points
    st.session_state.results.append(
        f"✅ {st.session_state.round_no}번째 와플: "
        f"+{points}점 (반죽 {batter}%, 굽기 {progress}%)"
    )
    st.session_state.best_score = max(
        st.session_state.best_score,
        st.session_state.score
    )

    if st.session_state.round_no == 5:
        end_game(True, "5개의 와플을 모두 완성했어요!")
    else:
        st.session_state.round_no += 1
        st.session_state.phase = "pour"
        st.session_state.batter = 50
        st.session_state.bake_start = None


# -------------------- 제목 --------------------
st.markdown("""
<div class="hero">
    <div style="font-size: 3rem;">🧇 ☕ 🥣</div>
    <h1>따끈따끈 와플 주방</h1>
    <div>반죽은 알맞게, 뒤집기는 완벽한 타이밍에!</div>
</div>
""", unsafe_allow_html=True)


# -------------------- 점수판 --------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f'<div class="stat"><div class="stat-label">도전 횟수</div>'
        f'<div class="stat-value">{min(st.session_state.round_no, 5)} / 5</div></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f'<div class="stat"><div class="stat-label">현재 점수</div>'
        f'<div class="stat-value">{st.session_state.score}</div></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f'<div class="stat"><div class="stat-label">최고 점수</div>'
        f'<div class="stat-value">{st.session_state.best_score}</div></div>',
        unsafe_allow_html=True
    )


# -------------------- 게임 설명 --------------------
with st.expander("📖 게임 방법", expanded=False):
    st.markdown("""
    1. 반죽 양을 **40~60%** 사이로 맞춰요.
    2. 반죽을 부으면 와플이 자동으로 익기 시작해요.
    3. 굽기 게이지가 **55~75%**일 때 뒤집기 버튼을 눌러요.
    4. 반죽 양이 범위를 벗어나거나 뒤집기 타이밍을 놓치면 즉시 게임이 끝나요.
    5. 5개의 와플을 모두 성공시키면 최종 결과를 확인할 수 있어요.

    **점수:** 기본 100점 + 반죽 양 보너스 최대 30점
    + 뒤집기 타이밍 보너스 최대 30점
    """)


# -------------------- 최종 결과 --------------------
if st.session_state.game_over:
    st.markdown("---")
    st.markdown("## 🍽️ 오늘의 주방 결과")

    if st.session_state.won:
        st.balloons()
        st.success(st.session_state.message)
        st.markdown("### 🏆 와플 장인 등극!")
    else:
        st.error(st.session_state.message)
        st.markdown("### 다음에는 더 완벽하게 구워 봐요!")

    st.markdown(
        f'<div class="panel" style="text-align:center;">'
        f'<div style="font-size:1.1rem;">최종 점수</div>'
        f'<div style="font-size:2.7rem;font-family:Jua;color:#87512f;">'
        f'{st.session_state.score}점</div>'
        f'<div>최고 점수: {st.session_state.best_score}점</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧇 도전 기록")
    for result in st.session_state.results:
        st.write(result)

    if st.button("🔄 다시 하기", use_container_width=True):
        init_game()
        st.rerun()


# -------------------- 반죽 붓기 --------------------
elif st.session_state.phase == "pour":
    st.markdown(
        f"## 🥣 {st.session_state.round_no}번째 와플"
    )
    st.markdown(
        '<div class="panel">반죽을 알맞게 부어 주세요. '
        '<b>40~60%</b>가 성공 범위예요.</div>',
        unsafe_allow_html=True
    )

    batter = st.slider(
        "반죽 양 조절",
        min_value=0,
        max_value=100,
        value=st.session_state.batter,
        step=5,
        format="%d%%"
    )
    st.session_state.batter = batter

    # 와플 틀 시각화
    fill_height = max(0, batter)
    st.markdown(
        f"""
        <div style="
            height:150px;
            position:relative;
            overflow:hidden;
            background:#ead4b4;
            border:5px solid #87512f;
            border-radius:18px;
            margin:12px 0;
        ">
            <div style="
                position:absolute;
                bottom:0;
                width:100%;
                height:{fill_height}%;
                background:linear-gradient(180deg,#f4d49a,#d99a54);
            "></div>
            <div style="
                position:absolute;
                inset:0;
                display:flex;
                align-items:center;
                justify-content:center;
                font-family:Jua;
                font-size:1.4rem;
                color:#60371f;
            ">와플 틀 · {batter}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if batter < 40:
        st.warning("반죽이 부족해요! 와플이 작게 만들어질 수 있어요.")
    elif batter > 60:
        st.warning("반죽이 너무 많아요! 틀 밖으로 넘칠 수 있어요.")
    else:
        st.success("반죽 양이 적절해요!")

    if st.button("🥣 반죽 붓기 완료 · 굽기 시작", use_container_width=True):
        if batter < 40 or batter > 60:
            st.session_state.results.append(
                f"❌ {st.session_state.round_no}번째 와플: "
                f"반죽 양 실패 ({batter}%)"
            )
            end_game(
                False,
                f"반죽을 {batter}% 부었어요. 적정 범위인 40~60%를 벗어났어요!"
            )
        else:
            st.session_state.phase = "bake"
            st.session_state.bake_start = time.time()
            st.session_state.bake_duration = random.uniform(6.0, 8.0)

        st.rerun()


# -------------------- 굽기 게이지 --------------------
elif st.session_state.phase == "bake":

    @st.fragment(run_every=0.2)
    def baking_area():
        # 상태가 바뀐 경우 현재 화면을 표시하지 않음
        if (
            st.session_state.game_over
            or st.session_state.phase != "bake"
        ):
            return

        st.markdown(
            f"## 🔥 {st.session_state.round_no}번째 와플: 굽기"
        )
        st.markdown(
            '<div class="panel">와플이 익고 있어요! '
            '<b>초록색 구간</b>에서 뒤집어 주세요.</div>',
            unsafe_allow_html=True
        )

        elapsed = time.time() - st.session_state.bake_start
        duration = st.session_state.bake_duration
        progress = min(100, int(elapsed / duration * 100))

        if progress < 55:
            status = "아직 덜 익었어요"
            color = "#d6a24a"
        elif progress <= 75:
            status = "완벽한 타이밍!"
            color = "#67965a"
        else:
            status = "너무 늦기 전에 뒤집으세요!"
            color = "#c45b3b"

        st.markdown(
            f"""
            <div style="
                height:30px;
                overflow:hidden;
                background:#ead4b4;
                border:2px solid #87512f;
                border-radius:14px;
            ">
                <div style="
                    height:100%;
                    width:{progress}%;
                    background:{color};
                    transition:width 0.15s linear;
                "></div>
            </div>
            <div style="
                display:flex;
                justify-content:space-between;
                font-size:0.8rem;
                margin-top:5px;
                color:#714426;
            ">
                <span>덜 익음</span>
                <span>적당히 익음</span>
                <span>탐</span>
            </div>
            <h3 style="text-align:center;color:{color};">
                {status} · {progress}%
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.progress(progress / 100)

        if st.button(
            "🔄 지금 뒤집기!",
            key="flip_button",
            use_container_width=True
        ):
            finish_waffle(progress)
            st.rerun()

        # 게이지가 끝까지 차면 자동으로 실패 처리
        elif progress >= 100:
            st.session_state.results.append(
                f"❌ {st.session_state.round_no}번째 와플: "
                "뒤집기 타이밍 초과"
            )
            end_game(False, "와플이 타 버렸어요! 뒤집기 타이밍을 놓쳤어요.")
            st.rerun()

    baking_area()


# -------------------- 하단 --------------------
st.markdown("---")
st.markdown(
    '<p class="note">따뜻한 와플 한 장에는 정확한 타이밍이 필요해요. '
    '🍓 🧈 🍯</p>',
    unsafe_allow_html=True
)
