"""
다산고등학교 에너지 자원 모니터링 대시보드
Dasan High School Energy Resource Monitoring Dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ──────────────────────────────────────────────
# 🔧 더미 데이터 (나중에 여기만 수정하세요!)
# ──────────────────────────────────────────────

SCHOOL_INFO = {
    "name": "다산고등학교",
    "total_students": 850,        # 전교생 수
    "report_month": "2025년 5월",  # 보고 월
}

# 이번 달 에너지 사용량 및 비용
CURRENT_MONTH = {
    "electricity_kwh": 18_400,    # 전기 사용량 (kWh)
    "electricity_cost": 2_760_000,  # 전기 요금 (원)
    "water_m3": 620,              # 수도 사용량 (m³)
    "water_cost": 930_000,        # 수도 요금 (원)
    "waste_kg": 1_050,            # 폐기물 발생량 (kg)
    "waste_cost": 310_000,        # 폐기물 처리 비용 (원)
}

# 전월 에너지 사용량 및 비용
PREVIOUS_MONTH = {
    "electricity_kwh": 20_100,
    "electricity_cost": 3_015_000,
    "water_m3": 680,
    "water_cost": 1_020_000,
    "waste_kg": 1_200,
    "waste_cost": 360_000,
}

# 월별 추이 데이터 (최근 6개월)
MONTHLY_TREND = {
    "months": ["12월", "1월", "2월", "3월", "4월", "5월"],
    "electricity": [22_000, 23_500, 21_800, 20_500, 20_100, 18_400],  # kWh
    "water": [750, 720, 690, 710, 680, 620],                           # m³
    "waste": [1_350, 1_280, 1_300, 1_220, 1_200, 1_050],              # kg
}

# 환경 환산 상수
CO2_PER_KWH = 0.4594          # kg CO₂/kWh (한국전력 기준)
PINE_TREE_CO2_PER_YEAR = 6.6  # 소나무 1그루가 연간 흡수하는 CO₂ (kg)
SNACK_PRICE = 600              # 초코바 1개 가격 (원)

# ──────────────────────────────────────────────
# 🎨 페이지 설정 & 커스텀 CSS
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="다산고 에너지 모니터링",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');

/* ── 전역 배경 ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117 !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #0f2027 0%, #0d1117 50%),
                radial-gradient(ellipse at 80% 80%, #101c2c 0%, transparent 60%);
    background-color: #0d1117 !important;
    font-family: 'Noto Sans KR', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── 히어로 헤더 ── */
.hero-header {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #00e5a0, #00b8ff);
    color: #0d1117;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    padding: 0.35rem 1.1rem;
    border-radius: 50px;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}
.hero-title {
    font-size: clamp(2rem, 5vw, 3.4rem);
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 30%, #00e5a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin: 0 0 0.7rem;
}
.hero-sub {
    font-size: 1rem;
    color: #6b7a8d;
    font-weight: 300;
    letter-spacing: 0.04em;
}
.hero-divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #00e5a0, #00b8ff);
    margin: 1.5rem auto 0;
    border-radius: 2px;
}

/* ── 섹션 타이틀 ── */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #e8f4f8;
    margin: 2.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1e3a4a, transparent);
    margin-left: 0.8rem;str
}

/* ── 메트릭 카드 ── */
.metric-card {
    background: linear-gradient(145deg, #161d2b, #111827);
    border: 1px solid #1e2d3d;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card.green::before { background: linear-gradient(90deg, #00e5a0, #00c48c); }
.metric-card.blue::before  { background: linear-gradient(90deg, #00b8ff, #0077cc); }
.metric-card.orange::before{ background: linear-gradient(90deg, #ff9500, #ff6a00); }
.metric-card.purple::before{ background: linear-gradient(90deg, #c084fc, #818cf8); }

.metric-label {
    font-size: 0.78rem;
    color: #6b7a8d;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #f0f6ff;
    font-family: 'Space Mono', monospace;
    line-height: 1;
}
.metric-value.green  { color: #00e5a0; }
.metric-value.blue   { color: #00b8ff; }
.metric-value.orange { color: #ff9500; }
.metric-value.purple { color: #c084fc; }
.metric-delta {
    font-size: 0.82rem;
    margin-top: 0.45rem;
    font-weight: 500;
}
.delta-good { color: #00e5a0; }
.delta-bad  { color: #ff5555; }
.metric-icon {
    position: absolute;
    top: 1.2rem; right: 1.4rem;
    font-size: 1.8rem;
    opacity: 0.18;
}

/* ── 정보 카드 ── */
.info-card {
    background: linear-gradient(145deg, #161d2b, #111827);
    border: 1px solid #1e2d3d;
    border-radius: 16px;
    padding: 1.6rem;
}
.info-card h4 {
    color: #00e5a0;
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0 0 1rem;
}

/* ── 슬라이더 라벨 ── */
.stSlider label { color: #a8b8c8 !important; font-size: 0.9rem !important; }

/* ── 시뮬레이션 결과 박스 ── */
.sim-result {
    background: linear-gradient(135deg, #0f2820, #0a1f2e);
    border: 1px solid #00e5a040;
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    margin-top: 0.8rem;
}
.sim-big {
    font-size: 2.2rem;
    font-weight: 800;
    font-family: 'Space Mono', monospace;
}
.sim-label { font-size: 0.85rem; color: #6b7a8d; margin-top: 0.15rem; }

/* ── Streamlit 기본 요소 오버라이드 ── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #161d2b, #111827) !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
div[data-testid="metric-container"] > div:first-child { color: #6b7a8d !important; font-size: 0.8rem !important; }
div[data-testid="metric-container"] > div:nth-child(2) { color: #f0f6ff !important; font-size: 1.8rem !important; font-family: 'Space Mono', monospace !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #2d3d4d;
    font-size: 0.78rem;
    padding: 2.5rem 0 1.5rem;
    border-top: 1px solid #161d2b;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 🔢 계산 헬퍼 함수
# ──────────────────────────────────────────────

def calc_delta_pct(current, previous):
    """전월 대비 변화율(%) 계산"""
    if previous == 0:
        return 0.0
    return (current - previous) / previous * 100

def calc_total_cost(data):
    return data["electricity_cost"] + data["water_cost"] + data["waste_cost"]

def calc_co2(kwh):
    return kwh * CO2_PER_KWH

def delta_label(pct, reverse=False):
    """절약이 긍정(reverse=True)이면 감소가 좋음"""
    arrow = "▼" if pct < 0 else "▲"
    cls = "delta-good" if (pct < 0) == reverse else "delta-bad"
    # reverse=True → 감소가 좋은 것 (에너지 절약)
    sign = "+" if pct > 0 else ""
    return f'<span class="{cls}">{arrow} {sign}{pct:.1f}%&nbsp;전월 대비</span>'


# ──────────────────────────────────────────────
# 📌 히어로 헤더
# ──────────────────────────────────────────────

st.markdown(f"""
<div class="hero-header">
  <div class="hero-badge">🌿 학생 주도 에너지 모니터링</div>
  <div class="hero-title">다산고등학교<br>에너지 자원 현황</div>
  <div class="hero-sub">{SCHOOL_INFO["report_month"]} · 전교생 {SCHOOL_INFO["total_students"]:,}명 · 지구를 지키는 우리</div>
  <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 1️⃣ 메인 KPI 메트릭 카드
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">📊 이달의 핵심 지표</div>', unsafe_allow_html=True)

total_cost_cur  = calc_total_cost(CURRENT_MONTH)
total_cost_prev = calc_total_cost(PREVIOUS_MONTH)
cost_per_student = total_cost_cur / SCHOOL_INFO["total_students"]

elec_delta  = calc_delta_pct(CURRENT_MONTH["electricity_kwh"], PREVIOUS_MONTH["electricity_kwh"])
water_delta = calc_delta_pct(CURRENT_MONTH["water_m3"],        PREVIOUS_MONTH["water_m3"])
waste_delta = calc_delta_pct(CURRENT_MONTH["waste_kg"],        PREVIOUS_MONTH["waste_kg"])
cost_delta  = calc_delta_pct(total_cost_cur,                   total_cost_prev)

co2_current  = calc_co2(CURRENT_MONTH["electricity_kwh"])
co2_previous = calc_co2(PREVIOUS_MONTH["electricity_kwh"])
co2_delta    = calc_delta_pct(co2_current, co2_previous)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card green">
      <div class="metric-icon">💰</div>
      <div class="metric-label">1인당 부담금</div>
      <div class="metric-value green">{cost_per_student:,.0f}<span style="font-size:1rem;color:#6b7a8d;">원</span></div>
      <div class="metric-delta">{delta_label(cost_delta, reverse=True)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card blue">
      <div class="metric-icon">⚡</div>
      <div class="metric-label">전기 사용량</div>
      <div class="metric-value blue">{CURRENT_MONTH['electricity_kwh']:,}<span style="font-size:1rem;color:#6b7a8d;">kWh</span></div>
      <div class="metric-delta">{delta_label(elec_delta, reverse=True)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card orange">
      <div class="metric-icon">💧</div>
      <div class="metric-label">수도 사용량</div>
      <div class="metric-value orange">{CURRENT_MONTH['water_m3']:,}<span style="font-size:1rem;color:#6b7a8d;">m³</span></div>
      <div class="metric-delta">{delta_label(water_delta, reverse=True)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card purple">
      <div class="metric-icon">🌫️</div>
      <div class="metric-label">탄소 배출량</div>
      <div class="metric-value purple">{co2_current/1000:.1f}<span style="font-size:1rem;color:#6b7a8d;">tCO₂</span></div>
      <div class="metric-delta">{delta_label(co2_delta, reverse=True)}</div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 2️⃣ 비용 비중 파이차트 + 월별 트렌드
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">📈 사용 현황 분석</div>', unsafe_allow_html=True)

col_pie, col_trend = st.columns([1, 2], gap="large")

with col_pie:
    labels = ["전기", "수도", "폐기물"]
    values = [
        CURRENT_MONTH["electricity_cost"],
        CURRENT_MONTH["water_cost"],
        CURRENT_MONTH["waste_cost"],
    ]
    colors = ["#00b8ff", "#00e5a0", "#ff9500"]

    fig_pie = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#c8d8e8", size=13, family="Noto Sans KR"),
        hovertemplate="<b>%{label}</b><br>%{value:,}원<br>(%{percent})<extra></extra>",
    ))
    fig_pie.add_annotation(
        text=f"<b>{total_cost_cur/10000:.0f}</b><br><span style='font-size:10px'>만원</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color="#f0f6ff", family="Space Mono"),
        align="center",
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True,
        legend=dict(
            font=dict(color="#a8b8c8", size=12),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            x=0.5, xanchor="center", y=-0.05,
        ),
        height=320,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown(f"""
    <div style="text-align:center;color:#6b7a8d;font-size:0.8rem;margin-top:-10px">
        이달 총 에너지 비용
    </div>
    """, unsafe_allow_html=True)

with col_trend:
    df = pd.DataFrame({
        "월": MONTHLY_TREND["months"] * 3,
        "사용량": MONTHLY_TREND["electricity"] + MONTHLY_TREND["water"] + MONTHLY_TREND["waste"],
        "항목": (["전기 (kWh)"] * 6) + (["수도 (m³)"] * 6) + (["폐기물 (kg)"] * 6),
    })

    fig_line = px.line(
        df, x="월", y="사용량", color="항목",
        color_discrete_map={
            "전기 (kWh)": "#00b8ff",
            "수도 (m³)": "#00e5a0",
            "폐기물 (kg)": "#ff9500",
        },
        markers=True,
    )
    fig_line.update_traces(line_width=2.5, marker_size=7)
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8b8c8", family="Noto Sans KR"),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#6b7a8d"),
            linecolor="#1e2d3d",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1a2535",
            tickfont=dict(color="#6b7a8d"),
            linecolor="#1e2d3d",
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a8b8c8", size=12),
            orientation="h",
            x=0, y=1.12,
        ),
        margin=dict(t=40, b=10, l=10, r=10),
        height=320,
        hovermode="x unified",
    )
    st.plotly_chart(fig_line, use_container_width=True)


# ──────────────────────────────────────────────
# 3️⃣ 경제적 가치 변환 섹션
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">🍫 절약이 만든 기적 — 우리가 아낀 돈으로</div>', unsafe_allow_html=True)

saved_cost = total_cost_prev - total_cost_cur  # 전월 대비 절감액

snack_count    = int(saved_cost / SNACK_PRICE) if saved_cost > 0 else 0
snack_per_head = snack_count / SCHOOL_INFO["total_students"]

co2_saved   = co2_previous - co2_current  # kg
pine_trees  = int(co2_saved / PINE_TREE_CO2_PER_YEAR * 12) if co2_saved > 0 else 0  # 이번 달 기준 환산

c1, c2, c3 = st.columns(3)

def value_box(icon, value_text, unit, desc, color):
    return f"""
    <div class="metric-card {color}" style="text-align:center;padding:1.8rem 1rem;">
      <div style="font-size:2.5rem;margin-bottom:0.5rem">{icon}</div>
      <div class="metric-value {color}" style="font-size:2.4rem">{value_text}</div>
      <div style="color:#a8b8c8;font-size:0.85rem;font-weight:600;margin:0.2rem 0 0.6rem">{unit}</div>
      <div style="color:#6b7a8d;font-size:0.8rem;line-height:1.5">{desc}</div>
    </div>
    """

with c1:
    st.markdown(value_box(
        "🍫",
        f"{snack_count:,}",
        "개의 초코바",
        f"전월 대비 절감액 <b style='color:#f0f6ff'>{saved_cost:,}원</b>으로<br>"
        f"전교생 1인당 <b style='color:#00e5a0'>{snack_per_head:.1f}개</b>씩 나눠줄 수 있어요!",
        "green",
    ), unsafe_allow_html=True)

with c2:
    st.markdown(value_box(
        "🌲",
        f"{pine_trees:,}",
        "그루의 소나무",
        f"줄인 탄소 <b style='color:#f0f6ff'>{co2_saved:.0f}kg</b>은<br>"
        f"소나무 {pine_trees}그루가 한 달간 흡수하는 양!",
        "blue",
    ), unsafe_allow_html=True)

with c3:
    electricity_saved_pct = abs(elec_delta)
    st.markdown(value_box(
        "⚡",
        f"{abs(elec_delta):.1f}%",
        "전기 절감 달성",
        f"지난달보다 <b style='color:#f0f6ff'>{PREVIOUS_MONTH['electricity_kwh'] - CURRENT_MONTH['electricity_kwh']:,}kWh</b> 절약!<br>"
        f"계속하면 연간 <b style='color:#ff9500'>{(PREVIOUS_MONTH['electricity_kwh'] - CURRENT_MONTH['electricity_kwh'])*12:,}kWh</b> 절감 가능",
        "orange",
    ), unsafe_allow_html=True)

if saved_cost <= 0:
    st.info("💡 이번 달 비용이 전월보다 증가했어요. 함께 절약해봐요!", icon="⚠️")


# ──────────────────────────────────────────────
# 4️⃣ 참여형 절약 목표 시뮬레이션
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">🎮 에너지 절약 목표 시뮬레이터</div>', unsafe_allow_html=True)

st.markdown("""
<div style="color:#6b7a8d;font-size:0.9rem;margin-bottom:1.2rem;">
슬라이더를 움직여 "만약 우리가 이만큼 절약하면?" 시나리오를 실시간으로 확인해보세요!
</div>
""", unsafe_allow_html=True)

col_slider, col_results = st.columns([1, 2], gap="large")

with col_slider:
    st.markdown('<br>', unsafe_allow_html=True)

    goal_elec  = st.slider("⚡ 전기 절약 목표", min_value=0, max_value=30, value=10, step=1, format="%d%%")
    goal_water = st.slider("💧 수도 절약 목표", min_value=0, max_value=30, value=10, step=1, format="%d%%")
    goal_waste = st.slider("🗑️ 폐기물 감축 목표", min_value=0, max_value=30, value=10, step=1, format="%d%%")

with col_results:
    # 시뮬레이션 계산
    sim_elec_cost  = CURRENT_MONTH["electricity_cost"] * (1 - goal_elec  / 100)
    sim_water_cost = CURRENT_MONTH["water_cost"]       * (1 - goal_water / 100)
    sim_waste_cost = CURRENT_MONTH["waste_cost"]       * (1 - goal_waste / 100)

    sim_total_cost = sim_elec_cost + sim_water_cost + sim_waste_cost
    sim_saving     = total_cost_cur - sim_total_cost

    sim_elec_kwh   = CURRENT_MONTH["electricity_kwh"] * (1 - goal_elec / 100)
    sim_co2        = calc_co2(sim_elec_kwh)
    sim_co2_saved  = co2_current - sim_co2

    sim_snacks     = int(sim_saving / SNACK_PRICE)
    sim_snack_head = sim_snacks / SCHOOL_INFO["total_students"]
    sim_pines      = int(sim_co2_saved / PINE_TREE_CO2_PER_YEAR * 12)

    # 시뮬레이션 결과 차트 (현재 vs 목표)
    fig_bar = go.Figure()
    categories = ["전기", "수도", "폐기물"]
    current_vals = [
        CURRENT_MONTH["electricity_cost"],
        CURRENT_MONTH["water_cost"],
        CURRENT_MONTH["waste_cost"],
    ]
    sim_vals = [sim_elec_cost, sim_water_cost, sim_waste_cost]

    fig_bar.add_trace(go.Bar(
        name="현재", x=categories, y=current_vals,
        marker_color="#1e3a4a",
        marker_line=dict(color="#00b8ff", width=1.5),
        text=[f"{v/10000:.0f}만원" for v in current_vals],
        textposition="outside",
        textfont=dict(color="#6b7a8d", size=11),
    ))
    fig_bar.add_trace(go.Bar(
        name="목표 달성 시", x=categories, y=sim_vals,
        marker_color="#0f3020",
        marker_line=dict(color="#00e5a0", width=1.5),
        text=[f"{v/10000:.0f}만원" for v in sim_vals],
        textposition="outside",
        textfont=dict(color="#00e5a0", size=11),
    ))
    fig_bar.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a8b8c8", family="Noto Sans KR"),
        xaxis=dict(showgrid=False, tickfont=dict(color="#a8b8c8")),
        yaxis=dict(showgrid=True, gridcolor="#1a2535", tickfont=dict(color="#6b7a8d"),
                   ticksuffix="원", tickformat=","),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#a8b8c8")),
        margin=dict(t=20, b=10, l=10, r=10),
        height=240,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 시뮬레이션 요약 카드
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""
        <div class="sim-result">
          <div class="sim-label">예상 절감액</div>
          <div class="sim-big" style="color:#00e5a0">
            {sim_saving/10000:.1f}<span style="font-size:1rem;color:#6b7a8d;">만원</span>
          </div>
          <div class="sim-label">월 기준</div>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="sim-result">
          <div class="sim-label">🍫 초코바</div>
          <div class="sim-big" style="color:#00b8ff">
            {sim_snack_head:.1f}<span style="font-size:1rem;color:#6b7a8d;">개/인</span>
          </div>
          <div class="sim-label">전교생 1인당</div>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="sim-result">
          <div class="sim-label">🌲 소나무</div>
          <div class="sim-big" style="color:#ff9500">
            {sim_pines}<span style="font-size:1rem;color:#6b7a8d;">그루</span>
          </div>
          <div class="sim-label">CO₂ 흡수 환산</div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 5️⃣ 에너지 절약 실천 팁
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">💡 지금 당장 실천할 수 있는 절약 팁</div>', unsafe_allow_html=True)

tips = [
    ("⚡", "전기", "#00b8ff", "교실 이동 시 소등 필수! 컴퓨터·프로젝터 미사용 시 전원 OFF"),
    ("💧", "수도", "#00e5a0", "손 씻은 후 수도꼭지 꼭 잠그기, 화장실 절수 스티커 부착"),
    ("🗑️", "분리수거", "#ff9500", "올바른 분리배출로 재활용률 높이기, 일회용품 사용 줄이기"),
    ("🌿", "탄소중립", "#c084fc", "점심시간 에코 마일리지 참여하기, 계단 이용으로 엘리베이터 절전"),
]

tip_cols = st.columns(4)
for col, (icon, label, color, desc) in zip(tip_cols, tips):
    with col:
        st.markdown(f"""
        <div class="info-card">
          <div style="font-size:2rem;margin-bottom:0.6rem">{icon}</div>
          <div style="color:{color};font-size:0.8rem;font-weight:700;letter-spacing:0.1em;
                      text-transform:uppercase;margin-bottom:0.6rem">{label}</div>
          <div style="color:#8899aa;font-size:0.84rem;line-height:1.6">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 📌 푸터
# ──────────────────────────────────────────────

st.markdown(f"""
<div class="footer">
  🌿 {SCHOOL_INFO['name']} 학생자치회 · 에너지 절약 모니터링 시스템<br>
  <span style="color:#1e2d3d">데이터 기준: {SCHOOL_INFO['report_month']} · 문의: 학생자치회실</span>
</div>
""", unsafe_allow_html=True)
