
import streamlit as st
import streamlit.components.v1 as components
import time
import random
from textwrap import dedent

st.set_page_config(
    page_title="따끈따끈 와플 주방",
    page_icon="🧇",
    layout="centered"
)

# ==================== 스타일 ====================
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
    st.session_state.pour_duration = random.uniform(4, 6)
    st.session_state.bake_start = None
    st.session_state.bake_duration = random.uniform(7, 9)
    st.session_state.results = []
    st.session_state.message = ""
    st.session_state.pending_points = 0


if "round_no" not in st.session_state:
    init_game()


# ==================== 와플 기계 ====================
def draw_machine(waffle_class="golden", pouring=False, caption=""):
    beam = """
    <div style="position:absolute;top:145px;left:49%;width:9px;
    height:75px;background:#f5d18d;border-radius:8px;z-index:8;"></div>
    """ if pouring else ""

    colors = {
        "raw": ("#f3d99c", "#d1b67d"),
        "light": ("#f5d18a", "#d4a45b"),
        "golden": ("#d38b39", "#88431e"),
        "burnt": ("#5b301b", "#2a160e"),
    }
    base, grid = colors.get(waffle_class, colors["golden"])

    html = f"""
    <div style="position:relative;width:100%;max-width:430px;
    height:375px;margin:10px auto 20px;">

      <div style="position:absolute;top:30px;left:20%;width:60%;
      height:150px;border-radius:50%;background:#303030;
      border:8px solid #222;box-shadow:inset 0 0 0 12px #484848;">
        <div style="position:absolute;inset:25px;border-radius:50%;
        background:repeating-linear-gradient(0deg,transparent 0 22px,#242424 23px 31px),
        repeating-linear-gradient(90deg,transparent 0 22px,#242424 23px 31px);
        border:4px solid #555;"></div>
        <div style="position:absolute;top:-36px;left:35%;width:30%;
        height:40px;border:10px solid #292929;border-bottom:0;
        border-radius:35px 35px 0 0;"></div>
      </div>

      <div style="position:absolute;top:175px;left:32%;width:36%;
      display:flex;justify-content:space-between;z-index:4;">
        <span style="width:18px;height:38px;background:#292929;border-radius:10px;"></span>
        <span style="width:18px;height:38px;background:#292929;border-radius:10px;"></span>
      </div>

      <div style="position:absolute;top:195px;left:8%;width:84%;
      height:145px;border-radius:50%;background:#292929;
      border:8px solid #414141;box-shadow:0 10px 0 #242424;"></div>

      <div style="position:absolute;top:202px;left:13%;width:74%;
      height:125px;border-radius:50%;background:#090909;
      border:5px solid #151515;box-shadow:inset 0 0 0 5px #484848;z-index:3;">
        <div style="position:absolute;inset:7%;border-radius:50%;
        border:3px solid #e8b36b;
        background-color:{base};
        background-image:
        repeating-linear-gradient(0deg,transparent 0 17px,{grid} 18px 24px),
        repeating-linear-gradient(90deg,transparent 0 17px,{grid} 18px 24px);
        box-shadow:inset 0 0 8px #4b281c;overflow:hidden;"></div>
      </div>

      <div style="position:absolute;top:180px;right:8%;width:65px;height:16px;
      background:#c38b56;border:3px solid #4d2a19;border-radius:12px;z-index:6;"></div>
      <div style="position:absolute;left:17%;top:290px;width:30px;height:30px;
      border-radius:50%;border:4px solid #452819;background:#f1d5a7;z-index:7;"></div>
      <div style="position:absolute;right:20%;top:300px;width:13px;height:13px;
      border-radius:50%;background:#8bd47b;border:2px solid #e5c49a;
      box-shadow:0 0 8px #9cde83;z-index:7;"></div>
      {beam}
      <div style="position:absolute;top:355px;width:100%;text-align:center;
      color:#704326;font-weight:bold;">{caption}</div>
    </div>
    """
    st.markdown(dedent(html).strip(), unsafe_allow_html=True)


# ==================== 점수 처리 ====================
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
            f"❌ {st.session_state.round_no}번째 와플: 덜 익었을 때 뒤집음"
        )
        end_game(False, "와플이 덜 익었을 때 뒤집었어요!")
        return

    if progress > 75:
        st.session_state.results.append(
            f"❌ {st.session_state.round_no}번째 와플: 너무 늦게 뒤집음"
        )
        end_game(False, "와플이 타 버렸어요!")
        return

    batter = st.session_state.batter
    batter_bonus = max(0, 30 - abs(batter - 50) * 2)
    timing_bonus = max(0, 30 - int(abs(progress - 65) * 2))
    points = 100 + batter_bonus + timing_bonus

    st.session_state.score += points
    st.session_state.pending_points = points
    st.session_state.results.append(
        f"✅ {st.session_state.round_no}번째 와플: +{points}점"
    )
    st.session_state.best_score = max(
        st.session_state.best_score,
        st.session_state.score
    )

    if st.session_state.round_no == 5:
        end_game(True, "5개의 와플을 모두 완성했어요!")
    else:
        st.session_state.phase = "flip_result"


# ==================== 제목 ====================
st.markdown("""
<div class="hero">
    <div style="font-size:3rem;">🧇 ☕ 🥣</div>
    <h1>따끈따끈 와플 주방</h1>
    <div>반죽을 붓고, 완벽한 타이밍에 뒤집어 보세요!</div>
</div>
""", unsafe_allow_html=True)

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
    1. 반죽 게이지를 40~60% 사이에서 멈춰요.
    2. 굽기 게이지 55~75% 사이에서 뒤집어요.
    3. 한 번이라도 실패하면 게임이 즉시 끝나요.
    4. 다섯 개를 모두 성공하면 와플을 토핑으로 꾸밀 수 있어요.
    5. 토핑을 마우스로 끌어 와플 위에 놓아 보세요.
    """)


# ==================== 성공 후 토핑 꾸미기 ====================
if st.session_state.game_over:
    st.markdown("---")

    if st.session_state.won:
        st.balloons()
        st.success(st.session_state.message)
        st.markdown("## 🍓 나만의 와플 만들기")
        st.write("아래 토핑을 마우스로 끌어 와플 위 원하는 위치에 놓으세요!")

        topping_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 12px 6px;
    font-family: sans-serif;
    background: transparent;
    color: #60391f;
}
h3 { text-align:center; margin:5px 0 12px; color:#704326; }
.help { text-align:center; font-size:13px; margin-bottom:14px; line-height:1.6; }
.layout { display:flex; flex-direction:column; align-items:center; gap:16px; }

.waffle-area {
    position:relative;
    width:min(88vw, 400px);
    aspect-ratio:1/1;
    border-radius:50%;
    border:12px solid #9c5b2e;
    background-color:#e5a34f;
    background-image:
      repeating-linear-gradient(0deg,transparent 0 34px,#a95c2a 35px 43px),
      repeating-linear-gradient(90deg,transparent 0 34px,#a95c2a 35px 43px),
      linear-gradient(135deg,#ffdf94,#d78a35);
    box-shadow:inset 0 0 0 6px #f4c779,0 9px 0 #714126,0 13px 22px #60391f44;
    overflow:hidden;
    touch-action:none;
}
.waffle-area:after {
    content:"";
    position:absolute;
    inset:0;
    border-radius:50%;
    pointer-events:none;
    box-shadow:inset 0 0 18px #8b481f55;
}
.topping {
    position:absolute;
    z-index:3;
    transform:translate(-50%,-50%);
    cursor:grab;
    user-select:none;
    line-height:1;
    filter:drop-shadow(0 2px 2px #5c321d44);
    touch-action:none;
}
.topping:active { cursor:grabbing; }

.cream-svg {
    width:100%;
    height:100%;
    overflow:visible;
    display:block;
}
.palette {
    width:100%;
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:10px;
}
.item {
    background:#fff8e9;
    border:2px solid #e4c49a;
    border-radius:14px;
    min-height:88px;
    padding:8px 3px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:5px;
    cursor:grab;
    user-select:none;
    touch-action:none;
}
.item:active { cursor:grabbing; background:#f4e1c3; }
.item .emoji { font-size:39px; line-height:1.1; }
.item .name { font-size:12px; font-weight:bold; }
.item .cream-icon { width:50px; height:50px; }
.controls { display:flex; justify-content:center; gap:10px; flex-wrap:wrap; width:100%; }
button {
    border:0;
    border-radius:11px;
    background:#87512f;
    color:white;
    padding:12px 16px;
    font-size:14px;
    cursor:pointer;
}
button:hover { background:#60371f; }
#notice {
    min-height:20px;
    text-align:center;
    color:#80502d;
    font-size:13px;
}
@media(max-width:360px) {
    .item .emoji { font-size:33px; }
    .item { min-height:78px; }
}
</style>
</head>
<body>

<h3>🍓 토핑을 골라 와플 위에 올려 보세요!</h3>
<div class="help">토핑을 누른 채로 끌어 와플 위 원하는 곳에 놓으세요.<br>
올린 토핑은 다시 끌어서 위치를 바꿀 수 있어요.</div>

<!-- SVG 휘핑크림 모양 정의 -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<defs>
<linearGradient id="creamGrad" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="#fffef7"/>
  <stop offset="48%" stop-color="#f8f5e8"/>
  <stop offset="78%" stop-color="#e9e4d2"/>
  <stop offset="100%" stop-color="#d5d0bd"/>
</linearGradient>
<linearGradient id="creamHighlight" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#fffefa"/>
  <stop offset="55%" stop-color="#fffdf3"/>
  <stop offset="100%" stop-color="#e9e4d4"/>
</linearGradient>
<symbol id="creamShape" viewBox="0 0 100 100">
  <path d="M49 5
    C44 14 33 19 25 29
    C16 38 15 48 23 54
    C10 65 19 78 32 83
    C43 91 68 92 80 80
    C90 70 84 60 77 55
    C88 45 77 38 66 32
    C77 22 63 18 55 11
    C52 8 50 6 49 5Z"
    fill="url(#creamGrad)"/>

  <path d="M49 6
    C43 19 48 26 59 32
    C47 30 31 34 27 44
    C22 56 39 60 58 62
    C40 62 24 67 31 77
    C39 87 65 86 76 76
    C83 68 70 61 56 57
    C73 59 82 51 73 44
    C66 38 55 35 50 29
    C45 22 47 13 49 6Z"
    fill="url(#creamHighlight)"/>

  <path d="M49 8
    C40 23 47 30 57 35
    M30 42 C24 53 39 56 52 58
    M31 69 C42 77 63 76 74 70
    M39 82 C51 87 67 82 76 76"
    fill="none" stroke="#e6e0cd" stroke-width="2.3"
    stroke-linecap="round"/>

  <path d="M49 6
    C45 18 51 25 60 30"
    fill="none" stroke="#fff" stroke-width="2.5"
    stroke-linecap="round"/>
</symbol>
</defs>
</svg>

<div class="layout">
  <div class="waffle-area" id="waffle" aria-label="토핑을 놓는 와플"></div>

  <div class="palette" id="palette">
    <div class="item" data-kind="emoji" data-value="🍓" data-size="46">
      <span class="emoji">🍓</span><span class="name">딸기</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🍌" data-size="47">
      <span class="emoji">🍌</span><span class="name">바나나</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🥝" data-size="45">
      <span class="emoji">🥝</span><span class="name">키위</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🫐" data-size="45">
      <span class="emoji">🫐</span><span class="name">블루베리</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🍒" data-size="44">
      <span class="emoji">🍒</span><span class="name">체리</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🍑" data-size="45">
      <span class="emoji">🍑</span><span class="name">복숭아</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🍍" data-size="44">
      <span class="emoji">🍍</span><span class="name">파인애플</span>
    </div>
    <div class="item" data-kind="emoji" data-value="🍫" data-size="43">
      <span class="emoji">🍫</span><span class="name">초콜릿</span>
    </div>
    <div class="item" data-kind="cream" data-value="cream" data-size="76">
      <svg class="cream-icon" viewBox="0 0 100 100">
        <use href="#creamShape"></use>
      </svg>
      <span class="name">휘핑크림</span>
    </div>
  </div>

  <div id="notice">토핑을 여러 개 놓아 나만의 와플을 완성하세요.</div>
  <div class="controls">
    <button id="undo">마지막 토핑 지우기</button>
    <button id="clear">토핑 전부 지우기</button>
  </div>
</div>

<script>
const waffle = document.getElementById("waffle");
const notice = document.getElementById("notice");
const toppings = [];
let nextId = 1;
let activeDrag = null;

function createCreamSVG() {
    const svgNS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", "0 0 100 100");
    svg.setAttribute("class", "cream-svg");

    const defs = document.createElementNS(svgNS, "defs");
    const gradient = document.createElementNS(svgNS, "linearGradient");
    gradient.setAttribute("id", "cg" + nextId);
    gradient.setAttribute("x1", "0");
    gradient.setAttribute("y1", "0");
    gradient.setAttribute("x2", "1");
    gradient.setAttribute("y2", "1");

    [
        ["0%", "#fffef7"],
        ["48%", "#f8f5e8"],
        ["78%", "#e9e4d2"],
        ["100%", "#d5d0bd"]
    ].forEach(([offset, color]) => {
        const stop = document.createElementNS(svgNS, "stop");
        stop.setAttribute("offset", offset);
        stop.setAttribute("stop-color", color);
        gradient.appendChild(stop);
    });

    defs.appendChild(gradient);
    svg.appendChild(defs);

    const paths = [
        {
            d: "M49 5 C44 14 33 19 25 29 C16 38 15 48 23 54 C10 65 19 78 32 83 C43 91 68 92 80 80 C90 70 84 60 77 55 C88 45 77 38 66 32 C77 22 63 18 55 11 C52 8 50 6 49 5Z",
            fill: "url(#cg" + nextId + ")"
        },
        {
            d: "M49 6 C43 19 48 26 59 32 C47 30 31 34 27 44 C22 56 39 60 58 62 C40 62 24 67 31 77 C39 87 65 86 76 76 C83 68 70 61 56 57 C73 59 82 51 73 44 C66 38 55 35 50 29 C45 22 47 13 49 6Z",
            fill: "#fffdf3"
        }
    ];

    paths.forEach(p => {
        const path = document.createElementNS(svgNS, "path");
        path.setAttribute("d", p.d);
        path.setAttribute("fill", p.fill);
        svg.appendChild(path);
    });

    [
        "M49 8 C40 23 47 30 57 35",
        "M30 42 C24 53 39 56 52 58",
        "M31 69 C42 77 63 76 74 70",
        "M39 82 C51 87 67 82 76 76"
    ].forEach(d => {
        const path = document.createElementNS(svgNS, "path");
        path.setAttribute("d", d);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", "#e6e0cd");
        path.setAttribute("stroke-width", "2.3");
        path.setAttribute("stroke-linecap", "round");
        svg.appendChild(path);
    });

    nextId++;
    return svg;
}

function clampToWaffle(clientX, clientY) {
    const rect = waffle.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const radius = rect.width * 0.41;

    let dx = clientX - cx;
    let dy = clientY - cy;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist > radius) {
        dx = dx * radius / dist;
        dy = dy * radius / dist;
    }

    return {
        x: (cx + dx - rect.left) / rect.width * 100,
        y: (cy + dy - rect.top) / rect.height * 100
    };
}

function addTopping(kind, value, size, x, y) {
    const el = document.createElement("div");
    el.className = "topping";
    el.dataset.id = String(nextId++);

    if (kind === "cream") {
        el.style.width = size + "px";
        el.style.height = size + "px";
        el.appendChild(createCreamSVG());
    } else {
        el.textContent = value;
        el.style.fontSize = size + "px";
    }

    el.style.left = x + "%";
    el.style.top = y + "%";
    waffle.appendChild(el);

    const obj = {el, kind, value, size, x, y};
    toppings.push(obj);
    makeMovable(obj);

    notice.textContent = kind === "cream"
        ? "휘핑크림을 올렸어요!"
        : value + " 토핑을 올렸어요!";
}

function makeMovable(obj) {
    obj.el.addEventListener("pointerdown", function(e) {
        e.preventDefault();
        e.stopPropagation();

        activeDrag = obj;
        obj.el.setPointerCapture(e.pointerId);
        obj.el.style.zIndex = 20;
    });

    obj.el.addEventListener("pointermove", function(e) {
        if (activeDrag !== obj) return;
        e.preventDefault();

        const pos = clampToWaffle(e.clientX, e.clientY);
        obj.x = pos.x;
        obj.y = pos.y;
        obj.el.style.left = obj.x + "%";
        obj.el.style.top = obj.y + "%";
    });

    function release() {
        if (activeDrag === obj) {
            activeDrag = null;
            obj.el.style.zIndex = 3;
        }
    }

    obj.el.addEventListener("pointerup", release);
    obj.el.addEventListener("pointercancel", release);
}

document.querySelectorAll(".item").forEach(item => {
    item.addEventListener("pointerdown", e => {
        e.preventDefault();

        const kind = item.dataset.kind;
        const value = item.dataset.value;
        const size = Number(item.dataset.size);

        const ghost = document.createElement("div");
        ghost.style.cssText =
            "position:fixed;z-index:9999;pointer-events:none;" +
            "left:" + e.clientX + "px;top:" + e.clientY + "px;" +
            "transform:translate(-50%,-50%);";

        if (kind === "cream") {
            ghost.style.width = size + "px";
            ghost.style.height = size + "px";
            ghost.appendChild(createCreamSVG());
        } else {
            ghost.textContent = value;
            ghost.style.fontSize = size + "px";
        }

        document.body.appendChild(ghost);

        function move(ev) {
            ghost.style.left = ev.clientX + "px";
            ghost.style.top = ev.clientY + "px";
        }

        function up(ev) {
            document.removeEventListener("pointermove", move);
            document.removeEventListener("pointerup", up);
            ghost.remove();

            const rect = waffle.getBoundingClientRect();
            const inside =
                ev.clientX >= rect.left &&
                ev.clientX <= rect.right &&
                ev.clientY >= rect.top &&
                ev.clientY <= rect.bottom;

            if (inside) {
                const pos = clampToWaffle(ev.clientX, ev.clientY);
                addTopping(kind, value, size, pos.x, pos.y);
            } else {
                notice.textContent = "토핑을 와플 위에 놓아 주세요.";
            }
        }

        document.addEventListener("pointermove", move);
        document.addEventListener("pointerup", up);
    });
});

document.getElementById("undo").addEventListener("click", () => {
    const obj = toppings.pop();
    if (obj) {
        obj.el.remove();
        notice.textContent = "마지막 토핑을 지웠어요.";
    }
});

document.getElementById("clear").addEventListener("click", () => {
    toppings.forEach(t => t.el.remove());
    toppings.length = 0;
    notice.textContent = "토핑을 모두 지웠어요.";
});
</script>
</body>
</html>
"""
        components.html(topping_html, height=940, scrolling=False)

        st.markdown(
            f"**최종 점수: {st.session_state.score}점**  ·  "
            f"최고 점수: {st.session_state.best_score}점"
        )

    else:
        st.error(st.session_state.message)
        st.markdown("### 다음 도전에서 다시 만들어 봐요!")

        st.markdown(
            f'<div class="stat"><div>최종 점수</div>'
            f'<div class="stat-value">{st.session_state.score}점</div></div>',
            unsafe_allow_html=True
        )

    if st.session_state.results:
        with st.expander("🧇 도전 기록 보기"):
            for result in st.session_state.results:
                st.write(result)

    # 꾸미기 화면 아래에 배치해 와플을 가리지 않음
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄 다시 하기", use_container_width=True):
        init_game()
        st.rerun()


# ==================== 반죽 준비 ====================
elif st.session_state.phase == "pour_ready":
    st.markdown(f"## 🥣 {st.session_state.round_no}번째 와플")
    st.info("열린 와플 기계에 반죽을 부을 준비를 해 주세요.")

    draw_machine("raw", caption="반죽을 부을 준비!")

    if st.button("🥣 반죽 붓기 시작", use_container_width=True):
        st.session_state.phase = "pouring"
        st.session_state.pour_start = time.time()
        st.rerun()


# ==================== 반죽 붓기 ====================
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

        draw_machine("raw", pouring=True, caption="반죽이 틀에 채워지는 중...")
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
                    f"반죽 양이 {amount}%예요. 성공 범위인 40~60%를 벗어났어요!"
                )
            else:
                st.session_state.phase = "bake"
                st.session_state.bake_start = time.time()
                st.session_state.bake_duration = random.uniform(7, 9)

            st.rerun()

        elif amount >= 100:
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
        progress = min(
            100,
            int(elapsed / st.session_state.bake_duration * 100)
        )

        if progress < 40:
            waffle_class = "raw"
            status = "아직 덜 익었어요"
            color = "#d6a24a"
        elif progress < 55:
            waffle_class = "light"
            status = "조금만 더 기다려요"
            color = "#c99b51"
        elif progress <= 75:
            waffle_class = "golden"
            status = "완벽한 타이밍!"
            color = "#67965a"
        else:
            waffle_class = "burnt"
            status = "타기 직전이에요!"
            color = "#b94c2c"

        draw_machine(waffle_class, caption="와플이 익고 있어요...")
        st.markdown(
            f'<h3 style="text-align:center;color:{color};">'
            f'{status} · {progress}%</h3>',
            unsafe_allow_html=True
        )
        st.progress(progress / 100)

        if st.button("🔄 지금 뒤집기!", key="flip_waffle",
                     use_container_width=True):
            finish_waffle(progress)
            st.rerun()

        elif progress >= 100:
            st.session_state.results.append(
                f"❌ {st.session_state.round_no}번째 와플: 타이밍 초과"
            )
            end_game(False, "뒤집기를 놓쳐 와플이 타 버렸어요!")
            st.rerun()

    baking_area()


# ==================== 다음 와플 ====================
elif st.session_state.phase == "flip_result":
    st.markdown("## 🧇 와플 뒤집기!")

    components.html("""
    <div style="height:160px;display:flex;justify-content:center;align-items:center;">
      <div style="font-size:110px;animation:flip .9s ease-in-out;">🧇</div>
    </div>
    <style>
    @keyframes flip {
      0% { transform:rotateX(0) rotateZ(0); }
      45% { transform:rotateX(180deg) rotateZ(10deg) scale(.8); }
      100% { transform:rotateX(360deg) rotateZ(0); }
    }
    </style>
    """, height=170)

    st.success(f"와플 완성! +{st.session_state.pending_points}점")

    if st.button("다음 와플 만들기 →", use_container_width=True):
        st.session_state.round_no += 1
        st.session_state.phase = "pour_ready"
        st.session_state.batter = 50
        st.session_state.bake_start = None
        st.rerun()


st.markdown("---")
st.markdown(
    '<p class="note">따뜻한 주방에서 만드는 나만의 와플 🍓 🍌 🫐</p>',
    unsafe_allow_html=True
)
