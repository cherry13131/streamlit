<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>학주봉 - 학교 자원 모니터링 시스템</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        :root {
            --bg-color: #0f172a;       /* 딥한 다크네이비 배경 */
            --card-color: #1e293b;     /* 세련된 카드 배경 */
            --accent-blue: #38bdf8;     /* 전기 포인트 컬러 */
            --accent-green: #34d399;    /* 수도 포인트 컬러 */
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --radius-large: 32px;      /* 이미지 참고한 둥근 모서리 */
            --radius-small: 16px;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Malgun Gothic', sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }

        /* 네비게이션바 (페이지네이션 역할) */
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            background-color: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255,255,255,0.05);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .logo { font-size: 24px; font-weight: bold; letter-spacing: 1px; color: var(--accent-blue); }
        .nav-links { display: flex; gap: 15px; }
        .nav-btn {
            background: none; border: none; color: var(--text-sub); font-size: 16px; font-weight: 600;
            padding: 10px 24px; cursor: pointer; border-radius: var(--radius-small); transition: all 0.3s ease;
        }
        .nav-btn.active, .nav-btn:hover {
            background-color: var(--card-color); color: var(--text-main); box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* 화면 뷰 제어 */
        .page-view { display: none; padding: 40px; max-width: 1400px; width: 100%; margin: 0 auto; flex-grow: 1; }
        .page-view.active { display: block; animation: fadeIn 0.4s ease-in-out; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ================= HOME PAGE STYLE ================= */
        .home-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 70vh; }
        .home-title { font-size: 56px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(to right, #38bdf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .home-subtitle { font-size: 20px; color: var(--text-sub); margin-bottom: 40px; }
        .home-grid { display: flex; gap: 30px; width: 100%; max-width: 900px; }
        .home-card {
            flex: 1; background-color: var(--card-color); border-radius: var(--radius-large); padding: 40px;
            cursor: pointer; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); border: 1px solid rgba(255,255,255,0.03);
        }
        .home-card:hover { transform: translateY(-10px); border-color: rgba(255,255,255,0.1); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
        .home-card i { font-size: 48px; margin-bottom: 20px; }
        .home-card.elec i { color: var(--accent-blue); }
        .home-card.water i { color: var(--accent-green); }
        .home-card h3 { font-size: 24px; margin-bottom: 10px; }

        /* ================= DASHBOARD PAGE STYLE ================= */
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 30px; margin-top: 20px; }
        .chart-card {
            background-color: var(--card-color); border-radius: var(--radius-large); padding: 35px;
            border: 1px solid rgba(255,255,255,0.03); display: flex; flex-direction: column; align-items: center;
        }
        .chart-card h2 { font-size: 22px; width: 100%; margin-bottom: 25px; display: flex; align-items: center; gap: 10px; }
        .chart-container { position: relative; width: 100%; max-width: 340px; aspect-ratio: 1; }

        /* 실시간 텍스트 수치 레이아웃 */
        .summary-box { display: flex; gap: 20px; margin-bottom: 30px; width: 100%; }
        .summary-tile {
            flex: 1; background-color: var(--card-color); border-radius: var(--radius-small); padding: 25px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .summary-tile .info h4 { color: var(--text-sub); font-size: 14px; margin-bottom: 5px; }
        .summary-tile .info p { font-size: 28px; font-weight: bold; }
    </style>
</head>
<body>

    <nav>
        <div class="logo"><i class="fa-solid fa-seedling"></i> HAKJUBONG</div>
        <div class="nav-links">
            <button class="nav-btn active" onclick="switchPage('home')">홈 화면</button>
            <button class="nav-btn" onclick="switchPage('dashboard')">실시간 사용량</button>
        </div>
    </nav>

    <div id="page-home" class="page-view active">
        <div class="home-container">
            <h1 class="home-title">학교 자원 모니터링 시스템</h1>
            <p class="home-subtitle">실시간 데이터를 분석하여 교내 에너지 낭비를 방지합니다.</p>

            <div class="home-grid">
                <div class="home-card elec" onclick="switchPage('dashboard')">
                    <i class="fa-solid fa-bolt"></i>
                    <h3>전기 사용량 조회</h3>
                    <p style="color: var(--text-sub);">본관, 체육관, 정보관 전력 현황</p>
                </div>
                <div class="home-card water" onclick="switchPage('dashboard')">
                    <i class="fa-solid fa-droplet"></i>
                    <h3>수도 사용량 조회</h3>
                    <p style="color: var(--text-sub);">급식실, 각 층 화장실 용수 현황</p>
                </div>
            </div>
        </div>
    </div>

    <div id="page-dashboard" class="page-view">

        <div class="summary-box">
            <div class="summary-tile" style="border-left: 5px solid var(--accent-blue);">
                <div class="info">
                    <h4>전체 전기 사용량</h4>
                    <p id="txt-total-electricity">1,254 kWh</p>
                </div>
                <i class="fa-solid fa-bolt" style="font-size: 32px; color: var(--accent-blue);"></i>
            </div>
            <div class="summary-tile" style="border-left: 5px solid var(--accent-green);">
                <div class="info">
                    <h4>전체 수도 사용량</h4>
                    <p id="txt-total-water">480 L</p>
                </div>
                <i class="fa-solid fa-droplet" style="font-size: 32px; color: var(--accent-green);"></i>
            </div>
        </div>

        <div class="dashboard-grid">
            <div class="chart-card">
                <h2><i class="fa-solid fa-bolt" style="color:var(--accent-blue)"></i> 전기 사용량 비율</h2>
                <div class="chart-container">
                    <canvas id="electricityDoughnutChart"></canvas>
                </div>
            </div>

            <div class="chart-card">
                <h2><i class="fa-solid fa-droplet" style="color:var(--accent-green)"></i> 수도 사용량 비율</h2>
                <div class="chart-container">
                    <canvas id="waterDoughnutChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 1. 페이지 전환 (페이지네이션 기능) 함수
        function switchPage(pageId) {
            // 모든 뷰 숨기기
            document.getElementById('page-home').classList.remove('active');
            document.getElementById('page-dashboard').classList.remove('active');

            // 모든 버튼 비활성화
            const buttons = document.querySelectorAll('.nav-btn');
            buttons.forEach(btn => btn.classList.remove('active'));

            // 선택한 뷰 및 버튼 활성화
            if(pageId === 'home') {
                document.getElementById('page-home').classList.add('active');
                buttons[0].classList.add('active');
            } else if(pageId === 'dashboard') {
                document.getElementById('page-dashboard').classList.add('active');
                buttons[1].classList.add('active');
            }
        }

        // =========================================================
        // 2. 실질적인 데이터 입력 공간 (Chart.js 설정)
        // =========================================================

        // --- 전기 데이터 설정 ---
        const ctxElec = document.getElementById('electricityDoughnutChart').getContext('2d');
        const elecChart = new Chart(ctxElec, {
            type: 'doughnut',
            data: {
                // ★ DATA INPUT HERE ★ : 전기 차트 항목 이름
                labels: ['본관', '체육관', '정보관'],
                datasets: [{
                    // ★ DATA INPUT HERE ★ : 전기 실제 수치값 입력 데이터
                    data: [650, 354, 250],
                    backgroundColor: ['#38bdf8', '#0284c7', '#bae6fd'], // 도넛 영역별 색상 순서
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 14 } } }
                }
            }
        });

        // --- 수도 데이터 설정 ---
        const ctxWater = document.getElementById('waterDoughnutChart').getContext('2d');
        const waterChart = new Chart(ctxWater, {
            type: 'doughnut',
            data: {
                // ★ DATA INPUT HERE ★ : 수도 차트 항목 이름
                labels: ['급식실', '본관 화장실', '강당'],
                datasets: [{
                    // ★ DATA INPUT HERE ★ : 수도 실제 수치값 입력 데이터
                    data: [240, 160, 80],
                    backgroundColor: ['#34d399', '#059669', '#a7f3d0'], // 도넛 영역별 색상 순서
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#94a3b8', font: { size: 14 } } }
                }
            }
        });
    </script>
</body>
</html>