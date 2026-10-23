
import streamlit as st
import time
import random

st.set_page_config(
    page_title="따끈따끈 와플 주방",
    page_icon="🧇",
    layout="centered"
)

# ==================== 디자인 ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Gowun+Dodum&display=swap');

.stApp {
    background: linear-gradient(180deg, #fff9ec, #f0d9b7);
    color: #54341f;
    font-family: 'Gowun Dodum', sans-serif;
}
h1, h2, h3 {
    color: #704326;
    font-family: 'Jua', sans-serif;
}
.hero {
    background: linear-gradient(135deg, #60351f, #b87943);
    color: #fff8e9;
    padding: 23px 12px;
    border-radius: 23px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 6px 0 #492817;
}
.hero h1 {
    color: #fff8e9 !important;
    font-size: 2.4rem;
}
.panel {
    background: #fffaf0;
    border: 2px solid #e2c49a;
    border-radius: 18px;
    padding: 16px;
    margin: 12px 0;
}
.stat {
    background: #fffaf0;
    border: 1px solid #dfbf94;
    border-radius: 14px;
    padding: 12px 4px;
    text-align: center;
}
.stat-label {
    color: #866044;
    font-size: .85rem;
}
.stat-value {
    color: #704126;
    font-family: 'Jua', sans-serif;
    font-size: 1.45rem;
}
div.stButton > button {
    background: #87512f;
    color: #fff8e9;
    border: 0;
    border-radius: 12px;
    min-height: 3rem;
    font-family: 'Jua', sans-serif;
    font-size: 1.08rem;
}
div.stButton > button:hover {
    background: #60371f;
    color: white;
}
.note {
    color: #866044;
    text-align: center;
    font-size: .9rem;
}

/* 와플 기계 */
.machine {
    position: relative;
    width: 100%;
    max-width: 420px;
    height: 300px;
    margin: 15px auto 20px;
}
.machine-base {
    position: absolute;
    left: 7%;
    bottom: 10px;
    width: 86%;
    height: 105px;
    border-radius: 24px 24px 35px 35px;
    background: linear-gradient(145deg, #b96e39, #784020 65%, #542b19);
    border: 5px solid #63371f;
    box-shadow: 0 9px 0 #4c2a19, 0 14px 18px #7b4a2b55;
}
.machine-top {
    position: absolute;
    left: 10%;
    top: 20px;
    width: 80%;
    height: 125px;
    border-radius: 28px 28px 22px 22px;
    background: linear-gradient(145deg, #d79a61, #94532e 70%, #60351f);
    border: 5px solid #63371f;
    transform-origin: 50% 100%;
    box-shadow: inset 0 4px 5px #f8d4a255;
}
.machine-top:before {
    content: "";
    position: absolute;
    left: 20%;
    top: 13px;
    width: 60%;
    height: 12px;
    border-radius: 10px;
    background: #f0c18a;
    opacity: .8;
}
.machine-handle {
    position: absolute;
    right: 13%;
    top: 70px;
    width: 15%;
    height: 18px;
    border-radius: 10px;
    background: linear-gradient(#e2b17b, #7a4528);
    border: 3px solid #60351f;
    z-index: 4;
}
.machine-foot {
    position: absolute;
    bottom: 0;
    width: 18%;
    height: 18px;
    background: #63371f;
    border-radius: 0 0 10px 10px;
}
.machine-foot.left { left: 16%; }
.machine-foot.right { right: 16%; }
.machine-light {
    position: absolute;
    right: 20%;
    bottom: 43px;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: #77b866;
    border: 3px solid #e8c49c;
    box-shadow: 0 0 8px #8fda79;
}
.machine-dial {
    position: absolute;
    left: 17%;
    bottom: 35px;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background: radial-gradient(circle, #f2d8b0 0 40%, #704126 43% 100%);
    border: 3px solid #482719;
}
.waffle {
    position: absolute;
    left: 20%;
    top: 85px;
    width: 60%;
    aspect-ratio: 1.25;
    border-radius: 13px;
    border: 5px solid #9b572b;
    background-color: #e9b85f;
    background-image:
        repeating-linear-gradient(0deg,
            transparent 0 17px, #8f5128 18px 22px),
        repeating-linear-gradient(90deg,
            transparent 0 17px, #8f5128 18px 22px),
        linear-gradient(135deg, #f6d58c, #d99b48);
    box-shadow: inset 0 0 8px #6d3b20aa, 0 4px 5px #49281755;
    z-index: 3;
}
.waffle-light {
    background-color: #f5d98e;
    background-image:
        repeating-linear-gradient(0deg,
            transparent 0 17px, #c99b51 18px 22px),
        repeating-linear-gradient(90deg,
            transparent 0 17px, #c99b51 18px 22px),
        linear-gradient(135deg, #fff0ba, #e9c56f);
}
.waffle-golden {
    background-color: #c88436;
    background-image:
        repeating-linear-gradient(0deg,
            transparent 0 17px, #88441e 18px 22px),
        repeating-linear-gradient(90deg,
            transparent 0 17px, #88441e 18px 22px),
        linear-gradient(135deg, #f6cf78, #c77b32 75%, #a45b25);
}
.waffle-burnt {
    background-color: #54301e;
    background-image:
        repeating-linear-gradient(0deg,
            transparent 0 17px, #32190f 18px 22px),
        repeating-linear-gradient(90deg,
            transparent 0 17px, #32190f 18px 22px),
        linear-gradient(135deg, #8a5430, #4b2819 75%, #28160f);
}
.waffle-raw {
    background-color: #f4dca5;
    background-image:
        repeating-linear-gradient(0deg,
            transparent 0 17px, #d2b982 18px 22px),
        repeating-linear-gradient(90deg,
            transparent 0 17px, #d2b982 18px 22px),
        linear-gradient(135deg, #fff0c5, #e9d49f);
}
.flip-animation {
    animation: waffleFlip .85s ease-in-out;
}
@keyframes waffleFlip {
    0% { transform: rotateX(0deg) rotateZ(0deg) scale(1); }
    45% { transform: rotateX(180deg) rotateZ(8deg) scale(.85); }
    100% { transform: rotateX(360deg) rotateZ(0deg) scale(1); }
}
.pour-beam {
    position: absolute;
    z-index: 5;
    left: 48%;
    top: 0;
    width: 10px;
    height: 100px;
    border-radius: 8px;
    background: linear-gradient(90deg, #d7a15e, #ffe2a3, #d7a15e);
    animation: pourPulse .35s infinite alternate;
}
@keyframes pourPulse {
    from { opacity: .65; }
    to { opacity: 1; }
}
.machine-caption {
    position: absolute;
    bottom: -20px;
    width: 100%;
    text-align: center;
    color: #714426;
    font-family: 'Jua', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ==================== 상태 초기화 ====================
def init_game():
    best = st.session_state.get("best_score", 0)
    st.session_state.round_no = 1
    st.session_state.score = 0
    st.session_state.best_score = best
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.phase = "pour_ready"
    st.session_state.batter = 50
    st.session_state.pour_start = None
    st.session_state.pour_duration = random.uniform(3.5, 5.0)
    st.session_state.bake_start = None
    st.session_state.bake_duration = random.uniform(6.0, 8.0)
    st.session_state.results = []
    st.session_state.message = ""
    st.session_state.flip_progress = 65
    st.session_state.pending_points = 0


if "round_no" not in st.session_state:
    init_game()


# ==================== 와플 기계 그리기 ====================
def draw_machine(waffle_class="waffle-golden",
                 pouring=False, flipping=False, caption=""):
    beam = '<div class="pour-beam"></div>' if pouring else ""
    flip_class = "flip-animation" if flipping else ""

    st.markdown(f"""
    <div class="machine">
        <div class="machine-top"></div>
        <div class="machine-handle"></div>
        <div class="machine-base"></div>
        <div class="machine-foot left"></div>
        <div class="machine-foot right"></div>
        <div class="machine-dial"></div>
        <div class="machine-light"></div>
        {beam}
        <div class="waffle {waffle_class} {flip_class}"></div>
        <div class="machine-caption">{caption}</div>
    </div>
    """, unsafe_allow_html=True)


def end_game(success, message):
    st.session_state.game_over = True
    st.session_state.won = success
    st.session_state.message = message
    st.session_state.best_score = max(
        st.session_state.best_score,
        st.session_state.score
    )


# ==================== 와플 뒤집기 판정 ====================
def finish_waffle(progress):
    st.session_state.flip_progress = progress

    if progress < 55:
        st.session_state.results.append(
            f"❌ {st.session_state.round_no}번째 와플: "
            f"덜 익었을 때 뒤집음 ({progress}%)"
        )
        end_game(False, "와플이 덜 익었을 때 뒤집었어요!")
        return

    if progress > 75:
        st.session_state.results.append(
            f"❌ {st.session_state.round_no}번째 와플: "
            f"너무 늦게 뒤집음 ({progress}%)"
        )
        end_game(False, "와플이 너무 익어 버렸어요!")
        return

    batter = st.session_state.batter
    base_points = 100
    batter_bonus = max(0, 30 - abs(batter - 50) * 2)
    timing_bonus = max(0, 30 - int(abs(progress - 65) * 2))
    points = base_points + batter_bonus + timing_bonus

    st.session_state.score += points
    st.session_state.pending_points = points
    st.session_state.results.append(
        f"✅ {st.session_state.round_no}번째 와플: "
        f"+{points}점 (반죽 {batter}%, 굽기 {progress}%)"
    )
    st.session_state.best_score = max(
        st.session_state.best_score,
        st.session_state.score
    )

    # 성공하면 뒤집기 애니메이션 화면으로 이동
    st.session_state.phase = "flip_result"


# ==================== 제목 ====================
st.markdown("""
<div class="hero">
    <div style="font-size:3rem;">🧇 ☕ 🥣</div>
    <h1>따끈따끈 와플 주방</h1>
    <div>반죽을 붓고, 완벽한 타이밍에 뒤집어 보세요!</div>
</div>
""", unsafe_allow_html=True)


# ==================== 점수판 ====================
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

with st.expander("📖 게임 방법"):
    st.markdown("""
    - 반죽 게이지가 움직일 때 **멈추기**를 눌러 양을 결정해요.
    - 반죽 양은 40~60% 사이여야 성공이에요.
    - 굽기 게이지가 55~75%일 때 뒤집어야 해요.
    - 한 번이라도 실패하면 즉시 게임이 끝나요.
    - 5개의 와플을 모두 완성하면 우승이에요.
    - 반죽 양과 뒤집기 타이밍이 50%, 65%에 가까울수록 보너스가 높아요.
    """)


# ==================== 최종 결과 ====================
if st.session_state.game_over:
    st.markdown("---")
    st.markdown("## 🍽️ 오늘의 주방 결과")

    if st.session_state.won:
        st.balloons()
        st.success(st.session_state.message)
        st.markdown("### 🏆 와플 장인 등극!")
    else:
        st.error(st.session_state.message)
        st.markdown("### 다음 도전에서 다시 만들어 봐요!")

    st.markdown(
        f'<div class="panel" style="text-align:center;">'
        f'<div>최종 점수</div>'
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


# ==================== 반죽 붓기 준비 ====================
elif st.session_state.phase == "pour_ready":
    st.markdown(f"## 🥣 {st.session_state.round_no}번째 와플")
    st.info("반죽을 부을 준비가 되었으면 시작 버튼을 눌러 주세요.")

    draw_machine(
        waffle_class="waffle-raw",
        caption="반죽을 부을 준비!"
    )

    if st.button("🥣 반죽 붓기 시작", use_container_width=True):
        st.session_state.phase = "pouring"
        st.session_state.pour_start = time.time()
        st.rerun()


# ==================== 반죽 게이지 ====================
elif st.session_state.phase == "pouring":

    @st.fragment(run_every=0.15)
    def pouring_area():
        if st.session_state.phase != "pouring":
            return

        st.markdown(f"## 🥣 {st.session_state.round_no}번째 와플: 반죽 붓기")
        elapsed = time.time() - st.session_state.pour_start
        duration = st.session_state.pour_duration
        amount = min(100, int(elapsed / duration * 100))

        draw_machine(
            waffle_class="waffle-raw",
            pouring=True,
            caption="반죽이 틀에 채워지는 중..."
        )

        st.markdown(
            f"""
            <div style="text-align:center;font-family:Jua;color:#714426;
                        font-size:1.4rem;">반죽 양: {amount}%</div>
            """,
            unsafe_allow_html=True
        )
        st.progress(amount / 100)

        if amount < 40:
            st.warning("아직 반죽이 부족해요.")
        elif amount <= 60:
            st.success("적절한 양이에요! 지금 멈추면 성공할 수 있어요.")
        else:
            st.warning("반죽이 너무 많아지고 있어요!")

        if st.button(
            "✋ 반죽 붓기 멈추기!",
            key="stop_pouring",
            use_container_width=True
        ):
            st.session_state.batter = amount

            if amount < 40 or amount > 60:
                st.session_state.results.append(
                    f"❌ {st.session_state.round_no}번째 와플: "
                    f"반죽 양 실패 ({amount}%)"
                )
                end_game(
                    False,
                    f"반죽 양이 {amount}%예요. "
                    "성공 범위인 40~60%를 벗어났어요!"
                )
            else:
                st.session_state.phase = "bake"
                st.session_state.bake_start = time.time()
                st.session_state.bake_duration = random.uniform(6.0, 8.0)

            st.rerun()

        elif amount >= 100:
            st.session_state.batter = 100
            st.session_state.results.append(
                f"❌ {st.session_state.round_no}번째 와플: 반죽 넘침"
            )
            end_game(False, "반죽이 넘쳐 버렸어요!")
            st.rerun()

    pouring_area()


# ==================== 굽기 및 뒤집기 ====================
elif st.session_state.phase == "bake":

    @st.fragment(run_every=0.15)
    def baking_area():
        if st.session_state.phase != "bake":
            return

        st.markdown(f"## 🔥 {st.session_state.round_no}번째 와플: 굽기")

        elapsed = time.time() - st.session_state.bake_start
        duration = st.session_state.bake_duration
        progress = min(100, int(elapsed / duration * 100))

        if progress < 40:
            waffle_class = "waffle-raw"
            status = "아직 덜 익었어요"
            color = "#d6a24a"
        elif progress < 55:
            waffle_class = "waffle-light"
            status = "조금만 더 기다려요"
            color = "#c99b51"
        elif progress <= 75:
            waffle_class = "waffle-golden"
            status = "완벽한 타이밍!"
            color = "#67965a"
        else:
            waffle_class = "waffle-burnt"
            status = "타기 직전이에요!"
            color = "#b94c2c"

        draw_machine(
            waffle_class=waffle_class,
            caption="와플이 익고 있어요..."
        )

        st.markdown(
            f"""
            <div style="height:30px;background:#ead4b4;border:2px solid #87512f;
                        border-radius:14px;overflow:hidden;">
                <div style="height:100%;width:{progress}%;background:{color};
                            transition:width .15s linear;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;
                        font-size:.8rem;color:#714426;margin-top:5px;">
                <span>덜 익음</span><span>적당히 익음</span><span>탐</span>
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
            key="flip_waffle",
            use_container_width=True
        ):
            finish_waffle(progress)
            st.rerun()

        elif progress >= 100:
            st.session_state.results.append(
                f"❌ {st.session_state.round_no}번째 와플: 타이밍 초과"
            )
            end_game(False, "뒤집기를 놓쳐 와플이 타 버렸어요!")
            st.rerun()

    baking_area()


# ==================== 뒤집기 애니메이션 ====================
elif st.session_state.phase == "flip_result":
    st.markdown("## 🧇 와플 뒤집기!")

    draw_machine(
        waffle_class="waffle-golden",
        flipping=True,
        caption="휙! 와플이 뒤집혔어요!"
    )

    st.success(
        f"와플 완성! +{st.session_state.pending_points}점"
    )
    st.markdown(
        f"현재 점수: **{st.session_state.score}점**"
    )

    if st.session_state.round_no >= 5:
        if st.button("🏆 최종 결과 보기", use_container_width=True):
            end_game(True, "5개의 와플을 모두 완성했어요!")
            st.rerun()
    else:
        if st.button("다음 와플 만들기 →", use_container_width=True):
            st.session_state.round_no += 1
            st.session_state.phase = "pour_ready"
            st.session_state.batter = 50
            st.session_state.bake_start = None
            st.rerun()


# ==================== 하단 ====================
st.markdown("---")
st.markdown(
    '<p class="note">따뜻한 주방에서 만드는 나만의 와플 🍓 🧈 🍯</p>',
    unsafe_allow_html=True
)
