(() => {
  "use strict";

  // ---------- shape / color helpers (round -> square as things fill up) ----------

  const ROUND_RADIUS = 999; // px, clamps to a full pill/blob shape
  const SQUARE_RADIUS = 6; // px, sharp corners once packed

  const SOFT_COLOR = { h: 16, s: 90, l: 75 }; // puni-puni peach
  const HARD_COLOR = { h: 212, s: 18, l: 38 }; // rigid slate

  function clamp01(n) {
    return Math.max(0, Math.min(1, n));
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function ease(t) {
    return Math.pow(t, 0.75);
  }

  function radiusForT(t) {
    return lerp(ROUND_RADIUS, SQUARE_RADIUS, ease(t));
  }

  function colorForT(t) {
    const e = ease(t);
    const h = lerp(SOFT_COLOR.h, HARD_COLOR.h, e);
    const s = lerp(SOFT_COLOR.s, HARD_COLOR.s, e);
    const l = lerp(SOFT_COLOR.l, HARD_COLOR.l, e);
    return `hsl(${h.toFixed(0)}, ${s.toFixed(0)}%, ${l.toFixed(0)}%)`;
  }

  function timingForT(t) {
    return t < 0.5 ? "cubic-bezier(0.34, 1.56, 0.64, 1)" : "cubic-bezier(0.2, 0, 0.3, 1)";
  }

  // ---------- calendar helpers ----------

  const WEEKS_PER_CYCLE = 13; // 12 working weeks + 1 buffer week
  const NORMAL_WEEKS_PER_CYCLE = 12;
  const CYCLES = 4; // 4 x 13 = 52 weeks ~= 1 year
  const TOTAL_WEEKS = WEEKS_PER_CYCLE * CYCLES;
  const WEEKDAY_LABELS = ["日", "月", "火", "水", "木", "金", "土"];

  function dateKey(d) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
  }

  function parseDateKey(key) {
    const [y, m, d] = key.split("-").map(Number);
    return new Date(y, m - 1, d);
  }

  function addDays(date, n) {
    const d = new Date(date);
    d.setDate(d.getDate() + n);
    return d;
  }

  function formatMD(date) {
    return `${date.getMonth() + 1}/${date.getDate()}`;
  }

  function formatMDW(date) {
    return `${formatMD(date)}(${WEEKDAY_LABELS[date.getDay()]})`;
  }

  function getWeekInfo(weekIndex) {
    const cycleIndex = Math.ceil(weekIndex / WEEKS_PER_CYCLE);
    const weekInCycle = ((weekIndex - 1) % WEEKS_PER_CYCLE) + 1;
    const isBuffer = weekInCycle === WEEKS_PER_CYCLE;
    const yearStartDate = parseDateKey(state.yearStart);
    const startDate = addDays(yearStartDate, (weekIndex - 1) * 7);
    const days = Array.from({ length: 7 }, (_, i) => addDays(startDate, i));
    return {
      weekIndex,
      cycleIndex,
      weekInCycle,
      isBuffer,
      startDate,
      endDate: days[6],
      days,
    };
  }

  function weekIndexForToday() {
    const yearStartDate = parseDateKey(state.yearStart);
    const diffDays = Math.round((new Date().setHours(0, 0, 0, 0) - yearStartDate.setHours(0, 0, 0, 0)) / 86400000);
    if (diffDays < 0) return null;
    const idx = Math.floor(diffDays / 7) + 1;
    return idx <= TOTAL_WEEKS ? idx : null;
  }

  // ---------- state ----------

  const STORAGE_KEY = "puni-schedule-year-state-v1";
  const OLD_DAY_KEY_PREFIX = "puni-schedule-";

  function defaultState() {
    return {
      yearStart: dateKey(new Date()),
      dailyCapacityMinutes: 480,
      days: {},
    };
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.yearStart && parsed.days) return parsed;
      }
    } catch {
      // ignore
    }

    // best-effort migration from the earlier single-day prototype
    try {
      const todayKey = dateKey(new Date());
      const oldRaw = localStorage.getItem(OLD_DAY_KEY_PREFIX + todayKey);
      if (oldRaw) {
        const old = JSON.parse(oldRaw);
        const fresh = defaultState();
        if (old && Array.isArray(old.events)) {
          fresh.days[todayKey] = { events: old.events };
        }
        if (old && old.capacityMinutes) {
          fresh.dailyCapacityMinutes = old.capacityMinutes;
        }
        return fresh;
      }
    } catch {
      // ignore
    }

    return defaultState();
  }

  let state = loadState();

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {
      // storage unavailable, ignore
    }
  }

  function getDayEvents(key) {
    return (state.days[key] && state.days[key].events) || [];
  }

  function dayUsed(key) {
    return getDayEvents(key).reduce((sum, ev) => sum + ev.duration, 0);
  }

  function weekUsed(weekInfo) {
    return weekInfo.days.reduce((sum, d) => sum + dayUsed(dateKey(d)), 0);
  }

  function weekCapacity() {
    return state.dailyCapacityMinutes * 7;
  }

  function addEventToDay(key, title, duration) {
    const used = dayUsed(key);
    const cap = state.dailyCapacityMinutes;
    if (!duration || duration <= 0) return false;
    if (used + duration > cap) return false;
    const t = clamp01((used + duration / 2) / cap);
    if (!state.days[key]) state.days[key] = { events: [] };
    state.days[key].events.push({
      id: Date.now() + Math.random(),
      title: title || "予定",
      duration,
      t,
    });
    saveState();
    return true;
  }

  function removeEventFromDay(key, id) {
    if (!state.days[key]) return;
    state.days[key].events = state.days[key].events.filter((ev) => ev.id !== id);
    saveState();
  }

  function resetDay(key) {
    delete state.days[key];
    saveState();
  }

  // ---------- routing ----------

  function currentRoute() {
    const hash = location.hash.replace("#", "") || "year";
    const m = hash.match(/^week-(\d+)$/);
    if (m) {
      const idx = parseInt(m[1], 10);
      if (idx >= 1 && idx <= TOTAL_WEEKS) return { name: "week", weekIndex: idx };
    }
    return { name: "year" };
  }

  function navigateToWeek(i) {
    location.hash = `week-${i}`;
  }

  function navigateToYear() {
    location.hash = "year";
  }

  // ---------- transient UI state (not persisted) ----------

  const selectedDayByWeek = {};
  let draftTitle = "";
  let draftDuration = "30";
  let draftPresetMin = "30";

  function getSelectedDayIdx(weekInfo) {
    if (selectedDayByWeek[weekInfo.weekIndex] !== undefined) {
      return selectedDayByWeek[weekInfo.weekIndex];
    }
    const todayKey = dateKey(new Date());
    const idx = weekInfo.days.findIndex((d) => dateKey(d) === todayKey);
    return idx >= 0 ? idx : 0;
  }

  // ---------- DOM refs ----------

  const viewRoot = document.getElementById("viewRoot");
  const dailyCapacityInput = document.getElementById("dailyCapacityInput");
  dailyCapacityInput.value = state.dailyCapacityMinutes;

  // ---------- rendering: year view ----------

  function renderYearView() {
    const todayWeekIdx = weekIndexForToday();
    let html = "";

    for (let cycle = 1; cycle <= CYCLES; cycle++) {
      const firstWeek = (cycle - 1) * WEEKS_PER_CYCLE + 1;
      const lastWeek = cycle * WEEKS_PER_CYCLE;
      const firstInfo = getWeekInfo(firstWeek);
      const lastInfo = getWeekInfo(lastWeek);

      html += `<section class="cycle-card">
        <h2 class="cycle-title">第${cycle}クール（12週+お休み1週）</h2>
        <p class="cycle-range">${formatMD(firstInfo.startDate)} 〜 ${formatMD(lastInfo.endDate)}</p>
        <div class="week-grid">`;

      for (let w = firstWeek; w <= lastWeek; w++) {
        const info = getWeekInfo(w);
        const isTodayWeek = w === todayWeekIdx;
        if (info.isBuffer) {
          html += `<div class="week-cell buffer${isTodayWeek ? " is-today-week" : ""}" data-go-week="${w}">
            <div class="week-num">お休み週</div>
            <div class="week-range">${formatMD(info.startDate)}〜${formatMD(info.endDate)}</div>
          </div>`;
        } else {
          const used = weekUsed(info);
          const cap = weekCapacity();
          const t = clamp01(used / cap);
          const radius = radiusForT(t);
          const color = colorForT(t);
          html += `<div class="week-cell${isTodayWeek ? " is-today-week" : ""}" data-go-week="${w}"
              style="border-radius:${radius}px; background:${color};">
            <div class="week-num">第${info.weekInCycle}週</div>
            <div class="week-range">${formatMD(info.startDate)}〜${formatMD(info.endDate)}</div>
          </div>`;
        }
      }

      html += `</div></section>`;
    }

    viewRoot.innerHTML = html;
  }

  // ---------- rendering: week view ----------

  function renderBufferWeek(info) {
    viewRoot.innerHTML = `
      <div class="week-header">
        <button type="button" class="back-link" data-go-year>← 年間ビューに戻る</button>
        <h2>お休み週（第${info.cycleIndex}クール）</h2>
        <p class="week-sub">${formatMD(info.startDate)} 〜 ${formatMD(info.endDate)}</p>
      </div>
      <div class="buffer-panel">
        <span class="buffer-icon">🍃</span>
        <h3>この週は予定を入れないバッファ週です</h3>
        <p>12週間ぎっしり詰めたら、ここでいったんリセット。<br />次のクールもまた丸くぷにぷにから始まります。</p>
      </div>
    `;
  }

  function renderWeekView(weekIndex) {
    const info = getWeekInfo(weekIndex);
    if (info.isBuffer) {
      renderBufferWeek(info);
      return;
    }

    const selectedIdx = getSelectedDayIdx(info);
    const selectedDate = info.days[selectedIdx];
    const selectedKey = dateKey(selectedDate);
    const cap = state.dailyCapacityMinutes;
    const used = dayUsed(selectedKey);
    const events = getDayEvents(selectedKey);
    const isFull = used >= cap;

    const wUsed = weekUsed(info);
    const wCap = weekCapacity();
    const wT = clamp01(wUsed / wCap);

    let html = `
      <div class="week-header">
        <button type="button" class="back-link" data-go-year>← 年間ビューに戻る</button>
        <h2>第${info.weekIndex}週（第${info.cycleIndex}クールの${info.weekInCycle}/12週）</h2>
        <p class="week-sub">${formatMD(info.startDate)} 〜 ${formatMD(info.endDate)}</p>
        <div class="meter" style="border-radius:${Math.max(SQUARE_RADIUS, radiusForT(wT) / 2)}px;">
          <div class="meter-fill" style="width:${Math.min(100, (wUsed / wCap) * 100)}%;
              border-radius:${radiusForT(wT)}px; background:linear-gradient(90deg, ${colorForT(Math.max(0, wT - 0.15))}, ${colorForT(wT)});"></div>
          <div class="meter-label">週合計 ${wUsed} / ${wCap} 分</div>
        </div>
        <div class="day-tabs">`;

    info.days.forEach((d, i) => {
      const active = i === selectedIdx ? " active" : "";
      html += `<button type="button" class="day-tab${active}" data-day-idx="${i}">${formatMDW(d)}</button>`;
    });

    html += `</div>
        <div class="mini-strip">`;

    info.days.forEach((d, i) => {
      const key = dateKey(d);
      const t = clamp01(dayUsed(key) / cap);
      const selected = i === selectedIdx ? " selected" : "";
      html += `<div class="mini-day${selected}" data-day-idx="${i}"
          style="border-radius:${radiusForT(t)}px; background:${colorForT(t)};" title="${formatMDW(d)}"></div>`;
    });

    html += `</div>
      </div>

      <section class="add-panel">
        <input type="text" id="titleInput" placeholder="予定のタイトル（例：ミーティング）" maxlength="40" value="${escapeAttr(draftTitle)}" />
        <div class="duration-row">
          <div class="preset-buttons" id="presetButtons">
            ${[15, 30, 60, 90, 120]
              .map(
                (m) =>
                  `<button type="button" data-preset-min="${m}" class="${String(m) === draftPresetMin ? "active" : ""}">${
                    m < 60 ? m + "分" : m === 60 ? "1時間" : m / 60 + "時間"
                  }</button>`
              )
              .join("")}
          </div>
          <div class="custom-duration">
            <input type="number" id="durationInput" min="5" max="480" step="5" value="${draftDuration}" />
            <span>分</span>
          </div>
        </div>
        <button type="button" id="addButton" class="add-button" data-add-event ${isFull ? "disabled" : ""}>予定を入れる</button>
        <p class="hint">クリックした予定は削除できます</p>
      </section>

      <div class="day-actions">
        <button type="button" class="reset-button" data-reset-day>${formatMD(selectedDate)}をリセット</button>
      </div>

      <section class="jar-wrap">
        <div class="jar${isFull ? " full" : ""}" id="jar">`;

    if (isFull) {
      html += `<div class="full-banner">予定でぎっしり！これ以上は入りません（スケジュールがカチコチです）</div>`;
    }

    if (events.length === 0) {
      html += `<p class="empty-msg">まだ予定はありません。丸くて自由な一日です。</p>`;
    } else {
      events.forEach((ev) => {
        const radius = radiusForT(ev.t);
        const width = Math.max(78, Math.min(220, 70 + ev.duration * 0.7));
        html += `<div class="block" data-remove-id="${ev.id}"
            style="border-radius:${radius}px; background:${colorForT(ev.t)}; width:${width}px;
              transition-timing-function:${timingForT(ev.t)};" title="クリックで削除">
          <div class="block-title">${escapeHtml(ev.title)}</div>
          <div class="block-duration">${ev.duration}分</div>
        </div>`;
      });
    }

    html += `</div>
      </section>
    `;

    viewRoot.innerHTML = html;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  function escapeAttr(s) {
    return escapeHtml(s);
  }

  // ---------- render dispatch ----------

  function render() {
    const route = currentRoute();
    if (route.name === "week") {
      renderWeekView(route.weekIndex);
    } else {
      renderYearView();
    }
  }

  // ---------- event delegation ----------

  viewRoot.addEventListener("click", (e) => {
    const weekCell = e.target.closest("[data-go-week]");
    if (weekCell) {
      navigateToWeek(Number(weekCell.dataset.goWeek));
      return;
    }

    const goYear = e.target.closest("[data-go-year]");
    if (goYear) {
      navigateToYear();
      return;
    }

    const dayTab = e.target.closest("[data-day-idx]");
    if (dayTab) {
      const route = currentRoute();
      if (route.name === "week") {
        selectedDayByWeek[route.weekIndex] = Number(dayTab.dataset.dayIdx);
        render();
      }
      return;
    }

    const presetBtn = e.target.closest("[data-preset-min]");
    if (presetBtn) {
      draftPresetMin = presetBtn.dataset.presetMin;
      draftDuration = presetBtn.dataset.presetMin;
      const durationInput = document.getElementById("durationInput");
      if (durationInput) durationInput.value = draftDuration;
      viewRoot.querySelectorAll("[data-preset-min]").forEach((b) => {
        b.classList.toggle("active", b.dataset.presetMin === draftPresetMin);
      });
      return;
    }

    const addBtn = e.target.closest("[data-add-event]");
    if (addBtn) {
      const route = currentRoute();
      if (route.name !== "week") return;
      const info = getWeekInfo(route.weekIndex);
      if (info.isBuffer) return;
      const selectedIdx = getSelectedDayIdx(info);
      const key = dateKey(info.days[selectedIdx]);
      const titleInput = document.getElementById("titleInput");
      const durationInput = document.getElementById("durationInput");
      const title = (titleInput.value || "").trim();
      const duration = parseInt(durationInput.value, 10);
      const ok = addEventToDay(key, title, duration);
      if (ok) {
        draftTitle = "";
        render();
      } else {
        const jar = document.getElementById("jar");
        if (jar) {
          jar.classList.remove("shake");
          void jar.offsetWidth;
          jar.classList.add("shake");
        }
      }
      return;
    }

    const removeBlock = e.target.closest("[data-remove-id]");
    if (removeBlock) {
      const route = currentRoute();
      if (route.name !== "week") return;
      const info = getWeekInfo(route.weekIndex);
      const selectedIdx = getSelectedDayIdx(info);
      const key = dateKey(info.days[selectedIdx]);
      removeEventFromDay(key, Number(removeBlock.dataset.removeId));
      render();
      return;
    }

    const resetBtn = e.target.closest("[data-reset-day]");
    if (resetBtn) {
      const route = currentRoute();
      if (route.name !== "week") return;
      const info = getWeekInfo(route.weekIndex);
      const selectedIdx = getSelectedDayIdx(info);
      const key = dateKey(info.days[selectedIdx]);
      resetDay(key);
      render();
      return;
    }
  });

  viewRoot.addEventListener("input", (e) => {
    if (e.target.id === "titleInput") draftTitle = e.target.value;
    if (e.target.id === "durationInput") draftDuration = e.target.value;
  });

  viewRoot.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && e.target.id === "titleInput") {
      const addBtn = document.getElementById("addButton");
      if (addBtn) addBtn.click();
    }
  });

  dailyCapacityInput.addEventListener("change", () => {
    const value = parseInt(dailyCapacityInput.value, 10);
    state.dailyCapacityMinutes = Number.isFinite(value) && value > 0 ? value : 480;
    saveState();
    render();
  });

  window.addEventListener("hashchange", render);

  render();
})();
