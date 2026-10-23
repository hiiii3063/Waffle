
import streamlit as st
import time
import random
from textwrap import dedent

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

/* 와플 기계 전체 */
.machine {
    position: relative;
    width: 100%;
    max-width: 430px;
    height: 385px;
    margin: 8px auto 28px;
}

/* 열린 윗뚜껑 */
.lid {
    position: absolute;
    top: 5px;
    left: 18%;
    width: 64%;
    height: 160px;
    border-radius: 50%;
    background: #292929;
    border: 8px solid #222;
    box-shadow: inset 0 0 0 12px #484848;
    transform: rotate(-2deg);
    z-index: 1;
}
.lid-inner {
    position: absolute;
    inset: 20px;
    border-radius: 50%;
    background: #383838;
    border: 5px solid #555;
}
.lid-grid {
    position: absolute;
    inset: 28px;
    border-radius: 45%;
    background:
        repeating-linear-gradient(
            0deg, transparent 0 25px,
            #252525 26px 35px
        ),
        repeating-linear-gradient(
            90deg, transparent 0 25px,
            #252525 26px 35px
        );
    border: 4px solid #505050;
}
.lid-handle {
    position: absolute;
    top: -38px;
    left: 35%;
    width: 30%;
    height: 45px;
    border: 11px solid #292929;
    border-bottom: 0;
    border-radius: 40px 40px 0 0;
}

/* 경첩 */
.hinge {
    position: absolute;
    top: 150px;
    left: 32%;
    width: 36%;
    height: 25px;
    z-index: 4;
    display: flex;
    justify-content: space-between;
}
.hinge span {
    display: block;
    width: 20px;
    height: 40px;
    background: #282828;
    border-radius: 12px;
}

/* 아래쪽 기계 본체 */
.machine-base {
    position: absolute;
    left: 8%;
    top: 195px;
    width: 84%;
    height: 150px;
    border-radius: 50%;
    background: #282828;
    border: 8px solid #3d3d3d;
    box-shadow: 0 12px 0 #242424, 0 17px 20px #70432655;
    z-index: 2;
}

/* 원형 와플 틀 */
.pan {
    position: absolute;
    left: 12%;
    top: 202px;
    width: 76%;
    height: 130px;
    border-radius: 50%;
    background: #090909;
    border: 5px solid #111;
    box-shadow: inset 0 0 0 5px #484848;
    z-index: 3;
}

/* 와플 모양 */
.waffle {
    position: absolute;
    left: 8%;
    top: 8%;
    width: 84%;
    height: 84%;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid #e59a50;
    box-shadow: inset 0 0 0 3px #f3c478;
    background-color: #eab760;
    background-image:
        repeating-linear-gradient(
            0deg, transparent 0 20px,
            #a45b2b 21px 28px
        ),
        repeating-linear-gradient(
            90deg, transparent 0 20px,
            #a45b2b 21px 28px
        ),
        linear-gradient(135deg, #ffdc91, #d99342);
    z-index: 5;
}

/* 덜 익은 와플 */
.waffle-raw {
    background-color: #f6dfa6;
    border-color: #e8cb8e;
    background-image:
        repeating-linear-gradient(
            0deg, transparent 0 20px,
            #d7bd82 21px 28px
        ),
        repeating-linear-gradient(
            90deg, transparent 0 20px,
            #d7bd82 21px 28px
        ),
        linear-gradient(135deg, #fff0c5, #ead29a);
}

/* 적당히 익은 와플 */
.waffle-golden {
    background-color: #e6a34d;
    border-color: #f1bf69;
    background-image:
        repeating-linear-gradient(
            0deg, transparent 0 20px,
            #99471f 21px 28px
        ),
        repeating-linear-gradient(
            90deg, transparent 0 20px,
            #99471f 21px 28px
        ),
        linear-gradient(135deg, #ffdc88, #d48634 75%, #b86426);
}

/* 탄 와플 */
.waffle-burnt {
    background-color: #56301e;
    border-color: #704128;
    background-image:
        repeating-linear-gradient(
            0deg, transparent 0 20px,
            #2d170f 21px 28px
        ),
        repeating-linear-gradient(
            90deg, transparent 0 20px,
            #2d170f 21px 28px
        ),
        linear-gradient(135deg, #80502f, #3c2116 70%, #24140e);
}

/* 손잡이와 조작부 */
.handle {
    position: absolute;
    top: 180px;
    right: 8%;
    width: 65px;
    height: 17px;
    background: linear-gradient(#d7a16d, #714126);
    border: 3px solid #4d2a19;
    border-radius: 12px;
    z-index: 6;
}
.dial {
    position: absolute;
    left: 17%;
    top: 295px;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 4px solid #452819;
    background: #f1d5a7;
    z-index: 7;
}
.light {
    position: absolute;
    right: 20%;
    top: 305px;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: #8bd47b;
    border: 2px solid #e5c49a;
    box-shadow: 0 0 8px #9cde83;
    z-index: 7;
}
.feet {
    position: absolute;
    left: 18%;
    top: 333px;
    width: 18%;
    height: 18px;
    background: #392116;
    border-radius: 0 0 12px 12px;
    z-index: 1;
}
.feet.right {
    left: auto;
    right: 18%;
}
.caption {
    position: absolute;
    top: 360px;
    width: 100%;
    text-align: center;
    color: #704326;
    font-family: 'Jua', sans-serif;
    font-size: 1.05rem;
}

/* 반죽 흐름 */
.pour-beam {
    position: absolute;
    top: 160px;
    left: 49%;
    width: 10px;
    height: 75px;
    background: linear-gradient(90deg, #d9a05b, #ffe0a0, #d9a05b);
    border-radius: 8px;
    z-index: 8;
    animation: pourPulse .35s infinite alternate;
}
@keyframes pourPulse {
    from { opacity: .55; }
    to { opacity: 1; }
}

/* 뒤집는 순간 */
.flip-animation {
    animation: flipWaffle .9s ease-in-out;
}
@keyframes flipWaffle {
    0% { transform: rotateX(0deg) rotateZ(0deg) scale(1); }
    35% { transform: rotateX(180deg) rotateZ(8deg) scale(.78); }
    70% { transform: rotateX(300deg) rotateZ(-5deg) scale(.9); }
    100% { transform: rotateX(360deg) rotateZ(0deg) scale(1); }
}
</style>
""", unsafe_allow_html=True)


# ==================== 게임 상태 ====================
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
    st.session_state.pour_duration = random.uniform(4.0, 6.0)
    st.session_state.bake_start = None
    st.session_state.bake_duration = random.uniform(7.0, 9.0)
    st.session_state.results = []
    st.session_state.message = ""
    st.session_state.pending_points = 0


if "round_no" not in st.session_state:
    init_game()


# ==================== 기계 그리기 ====================
def draw_machine(waffle_class="waffle-raw",
                 pouring=False, flipping=False, caption=""):
    beam = '<div class="pour-beam"></div>' if pouring else ""
    flip_class = "flip-animation" if flipping else ""

    html = f"""
<div class="machine">
  <div class="lid">
    <div class="lid-handle"></div>
    <div class="lid-inner"></div>
    <div class="lid-grid"></div>
  </div>
  <div class="hinge"><span></span><span></span></div>
  <div class="machine-base"></div>
  <div class="pan">
    <div class="waffle {waffle_class} {flip_class}"></div>
  </div>
  <div class="handle"></div>
  <div class="dial"></div>
  <div class="light"></div>
  <div class="feet"></div>
  <div class="feet right"></div>
  {beam}
  <div class="caption">{caption}</div>
</div>
"""
    # HTML 앞뒤의 공백을 제거해 코드 블록으로 표시되는 문제 방지
    st.markdown(dedent(html).strip(), unsafe_allow_html=True)


def end_game(success, message):
    st.session_state.game_over = True
    st.session_state.won = success
    st.session_state.message = message
    st.session_state.best_score = max(
        st.session_state.best_score,
        st.session_state.score
    )


def finish_waffle(progress):
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
        end_game(False, "와플이 타기 시작했어요!")
        return

    batter = st.session_state.batter
    batter_bonus = max(0, 30 - abs(batter - 50) * 2)
    timing_bonus = max(0, 30 - int(abs(progress - 65) * 2))
    points = 100 + batter_bonus + timing_bonus

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
    1. 반죽 게이지가 움직이면 멈추기 버튼을 눌러요.
    2. 반죽 양이 40~60%이면 성공 범위예요.
    3. 와플이 익기 시작하면 굽기 게이지를 확인해요.
    4. 굽기 게이지 55~75% 사이에서 뒤집어야 성공이에요.
    5. 한 번이라도 실패하면 즉시 게임이 종료돼요.
    6. 5개를 모두 완성하면 최종 결과를 확인할 수 있어요.

    반죽 양과 타이밍이 각각 50%, 65%에 가까울수록 보너스 점수가 높아요.
    """)


# ==================== 결과 화면 ====================
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


# ==================== 반죽 준비 ====================
elif st.session_state.phase == "pour_ready":
    st.markdown(f"## 🥣 {st.session_state.round_no}번째 와플")
    st.info("열린 와플 기계에 반죽을 부을 준비를 해 주세요.")

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

        st.markdown(
            f"## 🥣 {st.session_state.round_no}번째 와플: 반죽 붓기"
        )

        elapsed = time.time() - st.session_state.pour_start
        amount = min(
            100,
            int(elapsed / st.session_state.pour_duration * 100)
        )

        draw_machine(
            waffle_class="waffle-raw",
            pouring=True,
            caption="반죽이 틀에 채워지는 중..."
        )

        st.markdown(
            f'<h3 style="text-align:center;">반죽 양: {amount}%</h3>',
            unsafe_allow_html=True
        )
        st.progress(amount / 100)

        if amount < 40:
            st.warning("아직 반죽이 부족해요.")
        elif amount <= 60:
            st.success("적당한 양이에요! 지금 멈춰 보세요.")
        else:
            st.warning("반죽이 넘치기 시작해요!")

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
                st.session_state.bake_duration = random.uniform(7.0, 9.0)

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

        st.markdown(
            f"## 🔥 {st.session_state.round_no}번째 와플: 굽기"
        )

        elapsed = time.time() - st.session_state.bake_start
        progress = min(
            100,
            int(elapsed / st.session_state.bake_duration * 100)
        )

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
            <div style="height:30px;background:#ead4b4;border:2px solid #87512f;border-radius:14px;overflow:hidden;">
                <div style="height:100%;width:{progress}%;background:{color};transition:width .15s linear;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:.8rem;color:#714426;margin-top:5px;">
                <span>덜 익음</span><span>적당히 익음</span><span>탐</span>
            </div>
            <h3 style="text-align:center;color:{color};">{status} · {progress}%</h3>
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


# ==================== 뒤집기 결과 ====================
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

    if st.session_state.round_no == 5:
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


st.markdown("---")
st.markdown(
    '<p class="note">따뜻한 주방에서 만드는 나만의 와플 🍓 🧈 🍯</p>',
    unsafe_allow_html=True
)
