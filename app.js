:root {
    --bg-color: #f1f5f9;
    --card-bg: #ffffff;
    --text-main: #1e293b;
    --text-sub: #64748b;

    --color-elec: #2299c5;
    --color-water: #84cc16;
    --color-gas: #eab308;

    --radius-premium: 40px;
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }

.window-wrapper {
    width: 100%;
    max-width: 1050px;
    min-height: 500px;
    position: relative;
}

.premium-card {
    background: var(--card-bg);
    border-radius: var(--radius-premium);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
    display: none;
    width: 100%;
    padding: 50px 60px;
    border: 1px solid rgba(0,0,0,0.02);
    position: relative;
    overflow: hidden;
}
.premium-card.active { display: flex; animation: slideEffect 0.5s ease-in-out; }

@keyframes slideEffect {
    from { opacity: 0; transform: scale(0.98); }
    to { opacity: 1; transform: scale(1); }
}

.back-arrow {
    position: absolute;
    left: -70px;
    top: 40px;
    width: 50px;
    height: 50px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: all 0.2s;
}
.back-arrow:hover { transform: translateX(-3px); background: #f8fafc; }

/* 홈 화면 레이아웃 */
.home-layout { justify-content: space-between; align-items: center; }
.home-left { flex: 1.2; }
.home-left .intro-tag { font-size: 28px; color: #475569; font-weight: 300; margin-bottom: -5px; }
.home-left .intro-tag span { font-style: italic; font-family: Georgia, serif; color: #2299c5; }
.home-left h1 { font-size: 42px; font-weight: 800; color: var(--text-main); margin-bottom: 15px; letter-spacing: -1px; }
.home-left p { font-size: 14px; color: var(--text-sub); line-height: 1.6; max-width: 320px; margin-bottom: 35px; }

.action-btn {
    background-color: #2299c5; color: white; border: none; padding: 12px 35px;
    border-radius: 25px; font-size: 14px; font-weight: 600; cursor: pointer;
    display: inline-flex; align-items: center; gap: 15px; transition: all 0.3s;
}
.action-btn:hover { background-color: #1d7fa5; transform: translateY(-2px); }
.action-btn .circle-arrow { width: 22px; height: 22px; background: white; color: #2299c5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; }

.deco-text {
    font-family: Georgia, serif; font-size: 110px; color: #e2e8f0; font-style: italic;
    position: absolute; left: 45%; transform: rotate(-90px); opacity: 0.5; pointer-events: none;
}

.home-right-dots { display: flex; flex-direction: column; gap: 15px; align-items: center; justify-content: center; padding-left: 40px; }
.dot { width: 18px; height: 18px; border-radius: 50%; }
.dot.b { background-color: #2299c5; }
.dot.g { background-color: #cbd5e1; }
.dot.v { background-color: #84cc16; }

/* 대시보드 화면 레이아웃 */
.dashboard-layout { flex-direction: column; align-items: center; text-align: center; }
.dashboard-layout h2 { font-size: 22px; font-weight: 700; margin-bottom: 5px; color: #334155; }
.dashboard-layout .sub-info { font-size: 12px; color: var(--text-sub); font-style: italic; margin-bottom: 40px; }

.charts-row { display: flex; justify-content: center; gap: 60px; width: 100%; }
.chart-item { display: flex; flex-direction: column; align-items: center; }

.ring-graph {
    width: 140px; height: 140px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    position: relative; margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}
.ring-graph::after {
    content: ''; position: absolute; width: 112px; height: 112px;
    background: white; border-radius: 50%; z-index: 1;
}
.ring-value { position: relative; z-index: 2; font-size: 22px; font-weight: 700; color: #334155; letter-spacing: -0.5px; }
.chart-item label { font-size: 15px; font-weight: 600; color: #475569; }