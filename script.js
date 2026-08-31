/**
 * TimeFlow - Real-Time Time Progress & Desktop Widget Controller
 */

const QUOTES = [
  "เวลาคือสิ่งเดียวที่ผ่านไปแล้วไม่ย้อนกลับ จงใช้มันกับสิ่งที่สำคัญจริง ๆ ⏳",
  "อย่ารอให้พร้อมถึงจะเริ่ม แต่จงเริ่มเพื่อที่จะพร้อม 🚀",
  "สิ่งที่คุณทำในวันนี้ คือสิ่งที่จะสร้างอนาคตในวันพรุ่งนี้ 🌟",
  "ชีวิตสั้นเกินกว่าจะเสียเวลาให้กับความลังเล 🪽",
  "ทุก ๆ วินาทีคือโอกาสใหม่ในการเริ่มต้น 🌿",
  "ก้าวเล็ก ๆ ในทุกวัน ดีกว่าการหยุดอยู่กับที่ 🌾",
  "ทำให้ดีที่สุดในวันนี้ เพื่อขอบคุณตัวเองในวันข้างหน้า ✨"
];

const THAI_MONTHS = [
  'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
  'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
];

const THAI_DAYS = ['วันอาทิตย์', 'วันจันทร์', 'วันอังคาร', 'วันพุธ', 'วันพฤหัสบดี', 'วันศุกร์', 'วันเสาร์'];

class TimeFlowWidget {
  constructor() {
    this.isPinned = false;
    this.isMini = false;
    this.birthDate = localStorage.getItem('timeflow_birthdate') || '2002-01-01';
    this.theme = localStorage.getItem('timeflow_theme') || 'glass-dark';
    this.opacity = localStorage.getItem('timeflow_opacity') || '85';

    this.init();
  }

  init() {
    this.applyTheme(this.theme);
    this.applyOpacity(this.opacity);
    this.initControls();
    this.initTabs();
    this.initSettings();
    this.initWebDrag();
    this.updateQuote();

    // Start Live Clock & Progress Loop
    this.update();
    setInterval(() => this.update(), 1000);
  }

  update() {
    const now = new Date();

    // 1. Clock & Date Display
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('live-time').textContent = `${hours}:${minutes}:${seconds}`;

    const dayName = THAI_DAYS[now.getDay()];
    const dateNum = now.getDate();
    const monthName = THAI_MONTHS[now.getMonth()];
    const yearCE = now.getFullYear();
    document.getElementById('live-date').textContent = `${dayName}ที่ ${dateNum} ${monthName} ${yearCE}`;

    // 2. Year Progress
    const yearStart = new Date(yearCE, 0, 1, 0, 0, 0, 0);
    const yearEnd = new Date(yearCE + 1, 0, 1, 0, 0, 0, 0);
    const yearTotalMs = yearEnd - yearStart;
    const yearPassedMs = now - yearStart;
    const yearPct = ((yearPassedMs / yearTotalMs) * 100).toFixed(1);

    document.getElementById('current-year').textContent = yearCE;
    document.getElementById('year-pct').textContent = `${yearPct}%`;
    document.getElementById('year-bar').style.width = `${yearPct}%`;

    const yearRemainingDays = Math.ceil((yearEnd - now) / (1000 * 60 * 60 * 24));
    document.getElementById('year-sub').textContent = `เหลืออีก ${yearRemainingDays} วันในปีนี้`;

    // 3. Month Progress
    const monthStart = new Date(yearCE, now.getMonth(), 1, 0, 0, 0, 0);
    const monthEnd = new Date(yearCE, now.getMonth() + 1, 1, 0, 0, 0, 0);
    const monthTotalMs = monthEnd - monthStart;
    const monthPassedMs = now - monthStart;
    const monthPct = ((monthPassedMs / monthTotalMs) * 100).toFixed(1);

    document.getElementById('month-name').textContent = monthName;
    document.getElementById('month-pct').textContent = `${monthPct}%`;
    document.getElementById('month-bar').style.width = `${monthPct}%`;

    const monthRemainingDays = Math.ceil((monthEnd - now) / (1000 * 60 * 60 * 24));
    document.getElementById('month-sub').textContent = `เหลืออีก ${monthRemainingDays} วันในเดือนนี้`;

    // 4. Week Progress (Monday to Sunday)
    const dayOfWeek = (now.getDay() + 6) % 7; // 0 = Mon, 6 = Sun
    const weekStart = new Date(now);
    weekStart.setDate(now.getDate() - dayOfWeek);
    weekStart.setHours(0, 0, 0, 0);

    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 7);

    const weekTotalMs = weekEnd - weekStart;
    const weekPassedMs = now - weekStart;
    const weekPct = ((weekPassedMs / weekTotalMs) * 100).toFixed(1);

    document.getElementById('week-pct').textContent = `${weekPct}%`;
    document.getElementById('week-bar').style.width = `${weekPct}%`;

    const weekRemainingDays = Math.max(0, 6 - dayOfWeek);
    document.getElementById('week-sub').textContent = `เหลืออีก ${weekRemainingDays} วันในสัปดาห์นี้`;

    // 5. Day Progress
    const dayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
    const dayEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0, 0);
    const dayTotalMs = dayEnd - dayStart;
    const dayPassedMs = now - dayStart;
    const dayPct = ((dayPassedMs / dayTotalMs) * 100).toFixed(1);

    document.getElementById('day-pct').textContent = `${dayPct}%`;
    document.getElementById('day-bar').style.width = `${dayPct}%`;

    const remainingMs = dayEnd - now;
    const remainingHours = Math.floor(remainingMs / (1000 * 60 * 60));
    const remainingMins = Math.floor((remainingMs % (1000 * 60 * 60)) / (1000 * 60));
    document.getElementById('day-sub').textContent = `เหลืออีก ${remainingHours} ชม. ${remainingMins} นาที`;

    // Mini Capsule View updates
    const miniText = document.getElementById('mini-year-text');
    const miniBar = document.getElementById('mini-bar-fill');
    if (miniText) miniText.innerHTML = `ปี ${yearCE}: <strong>${yearPct}%</strong>`;
    if (miniBar) miniBar.style.width = `${yearPct}%`;

    // Update Life Matrix if visible
    this.updateLifeMatrix(now);
  }

  updateLifeMatrix(now) {
    const birth = new Date(this.birthDate);
    if (isNaN(birth.getTime())) return;

    const diffMs = now - birth;
    const ageYears = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 365.25));
    const ageMonths = Math.floor((diffMs % (1000 * 60 * 60 * 24 * 365.25)) / (1000 * 60 * 60 * 24 * 30.4375));

    document.getElementById('life-age-text').textContent = `${ageYears} ปี ${ageMonths} เดือน`;

    const avgLifespanYears = 80;
    const totalLifeMs = avgLifespanYears * 365.25 * 24 * 60 * 60 * 1000;
    const lifePct = Math.min(100, Math.max(0, ((diffMs / totalLifeMs) * 100))).toFixed(1);

    document.getElementById('life-pct-text').textContent = `${lifePct}%`;

    // Render Matrix Dots (e.g. 52 weeks x 80 years = 4160 weeks or scaled sample of 520 dots)
    const grid = document.getElementById('life-matrix-grid');
    if (grid && !grid.dataset.rendered) {
      grid.dataset.rendered = "true";
      grid.innerHTML = '';

      const totalDots = 520; // 10 years per 52 dots sample
      const passedDots = Math.round((lifePct / 100) * totalDots);

      for (let i = 0; i < totalDots; i++) {
        const dot = document.createElement('div');
        dot.className = 'dot-week';
        if (i < passedDots) {
          dot.classList.add('passed');
        } else if (i === passedDots) {
          dot.classList.add('current');
        }
        grid.appendChild(dot);
      }
    }
  }

  updateQuote() {
    const dayOfYear = Math.floor((new Date() - new Date(new Date().getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
    const quote = QUOTES[dayOfYear % QUOTES.length];
    document.getElementById('daily-quote').textContent = `"${quote}"`;
  }

  initControls() {
    const btnPin = document.getElementById('btn-pin');
    const btnMini = document.getElementById('btn-mini');
    const btnMiniExpand = document.getElementById('btn-mini-expand');
    const btnClose = document.getElementById('btn-close');

    // Pin Toggle (Always on top)
    btnPin.addEventListener('click', () => {
      this.isPinned = !this.isPinned;
      btnPin.classList.toggle('active-pinned', this.isPinned);

      if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.set_on_top(this.isPinned);
      }
    });

    // Mini Capsule Toggle
    const toggleMini = () => {
      this.isMini = !this.isMini;
      const fullView = document.getElementById('view-full');
      const miniView = document.getElementById('view-mini');

      if (this.isMini) {
        fullView.style.display = 'none';
        miniView.style.display = 'block';
        if (window.pywebview && window.pywebview.api) {
          window.pywebview.api.resize_mini();
        }
      } else {
        fullView.style.display = 'block';
        miniView.style.display = 'none';
        if (window.pywebview && window.pywebview.api) {
          window.pywebview.api.resize_full();
        }
      }
    };

    btnMini.addEventListener('click', toggleMini);
    btnMiniExpand.addEventListener('click', toggleMini);

    // Close Widget
    btnClose.addEventListener('click', () => {
      if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.close();
      } else {
        window.close();
      }
    });
  }

  initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const tabId = tab.dataset.tab;
        document.getElementById('tab-progress').classList.toggle('active', tabId === 'progress');
        document.getElementById('tab-life').classList.toggle('active', tabId === 'life');
      });
    });
  }

  initSettings() {
    const btnSettings = document.getElementById('btn-settings');
    const btnCloseSettings = document.getElementById('btn-close-settings');
    const drawer = document.getElementById('settings-drawer');
    const themeSelect = document.getElementById('theme-selector');
    const opacitySlider = document.getElementById('opacity-slider');
    const opacityVal = document.getElementById('opacity-val');
    const birthInput = document.getElementById('birthdate-input');

    btnSettings.addEventListener('click', () => drawer.classList.add('active'));
    btnCloseSettings.addEventListener('click', () => drawer.classList.remove('active'));

    // Theme selector
    themeSelect.value = this.theme;
    themeSelect.addEventListener('change', (e) => {
      this.applyTheme(e.target.value);
    });

    // Opacity slider
    opacitySlider.value = this.opacity;
    opacityVal.textContent = `${this.opacity}%`;
    opacitySlider.addEventListener('input', (e) => {
      this.applyOpacity(e.target.value);
      opacityVal.textContent = `${e.target.value}%`;
    });

    // Birthdate input
    birthInput.value = this.birthDate;
    birthInput.addEventListener('change', (e) => {
      this.birthDate = e.target.value;
      localStorage.setItem('timeflow_birthdate', this.birthDate);
      const grid = document.getElementById('life-matrix-grid');
      if (grid) delete grid.dataset.rendered;
      this.updateLifeMatrix(new Date());
    });
  }

  applyTheme(theme) {
    this.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('timeflow_theme', theme);
  }

  applyOpacity(val) {
    this.opacity = val;
    const container = document.getElementById('widget-container');
    if (container) {
      container.style.opacity = parseInt(val) / 100;
    }
    localStorage.setItem('timeflow_opacity', val);
  }

  // Fallback web drag when running in browser
  initWebDrag() {
    if (window.pywebview) return; // Native PyWebView handles drag automatically

    const widget = document.getElementById('widget-container');
    const header = document.querySelector('.widget-header');
    let isDragging = false;
    let offsetX = 0, offsetY = 0;

    header.addEventListener('mousedown', (e) => {
      if (['BUTTON', 'INPUT', 'SELECT'].includes(e.target.tagName)) return;
      isDragging = true;
      offsetX = e.clientX - widget.getBoundingClientRect().left;
      offsetY = e.clientY - widget.getBoundingClientRect().top;
      widget.style.position = 'fixed';
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      widget.style.left = `${e.clientX - offsetX}px`;
      widget.style.top = `${e.clientY - offsetY}px`;
    });

    document.addEventListener('mouseup', () => {
      isDragging = false;
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.timeFlow = new TimeFlowWidget();
});
