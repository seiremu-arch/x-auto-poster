(() => {
  "use strict";

  const ROUND_RADIUS = 999; // px, clamps to a full pill/blob shape
  const SQUARE_RADIUS = 6; // px, sharp corners once the day is packed

  const SOFT_COLOR = { h: 16, s: 90, l: 75 }; // puni-puni peach
  const HARD_COLOR = { h: 212, s: 18, l: 38 }; // rigid slate

  const capacityInput = document.getElementById("capacityInput");
  const meterFill = document.getElementById("meterFill");
  const meterLabel = document.getElementById("meterLabel");
  const meter = document.getElementById("meter");
  const titleInput = document.getElementById("titleInput");
  const durationInput = document.getElementById("durationInput");
  const presetButtons = document.getElementById("presetButtons");
  const addButton = document.getElementById("addButton");
  const jar = document.getElementById("jar");
  const emptyMsg = document.getElementById("emptyMsg");
  const resetButton = document.getElementById("resetButton");

  const todayKey = () => `puni-schedule-${new Date().toISOString().slice(0, 10)}`;

  /** @type {{capacityMinutes: number, events: Array<{id:number,title:string,duration:number,t:number}>}} */
  let state = loadState() || { capacityMinutes: 480, events: [] };

  capacityInput.value = state.capacityMinutes;

  function loadState() {
    try {
      const raw = localStorage.getItem(todayKey());
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || !Array.isArray(parsed.events)) return null;
      return parsed;
    } catch {
      return null;
    }
  }

  function saveState() {
    try {
      localStorage.setItem(todayKey(), JSON.stringify(state));
    } catch {
      // storage unavailable, ignore
    }
  }

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

  function usedMinutes() {
    return state.events.reduce((sum, ev) => sum + ev.duration, 0);
  }

  function render() {
    const capacity = state.capacityMinutes;
    const used = usedMinutes();
    const overallT = clamp01(used / capacity);

    meterFill.style.width = `${Math.min(100, (used / capacity) * 100)}%`;
    meterFill.style.borderRadius = `${radiusForT(overallT)}px`;
    meterFill.style.background = `linear-gradient(90deg, ${colorForT(Math.max(0, overallT - 0.15))}, ${colorForT(overallT)})`;
    meter.style.borderRadius = `${Math.max(SQUARE_RADIUS, radiusForT(overallT) / 2)}px`;
    meterLabel.textContent = `${used} / ${capacity} 分`;

    jar.querySelectorAll(".block, .full-banner").forEach((el) => el.remove());
    emptyMsg.style.display = state.events.length === 0 ? "block" : "none";

    state.events.forEach((ev) => {
      const block = document.createElement("div");
      block.className = "block";
      block.dataset.id = String(ev.id);
      const radius = radiusForT(ev.t);
      block.style.borderRadius = `${radius}px`;
      block.style.background = colorForT(ev.t);
      block.style.transitionTimingFunction = timingForT(ev.t);
      block.style.width = `${Math.max(78, Math.min(220, 70 + ev.duration * 0.7))}px`;
      block.title = "クリックで削除";

      const title = document.createElement("div");
      title.className = "block-title";
      title.textContent = ev.title;
      const duration = document.createElement("div");
      duration.className = "block-duration";
      duration.textContent = `${ev.duration}分`;

      block.appendChild(title);
      block.appendChild(duration);
      block.addEventListener("click", () => removeEvent(ev.id));
      jar.appendChild(block);
    });

    const isFull = used >= capacity;
    addButton.disabled = isFull;
    jar.classList.toggle("full", isFull);

    if (isFull) {
      const banner = document.createElement("div");
      banner.className = "full-banner";
      banner.textContent = "予定でぎっしり！これ以上は入りません（スケジュールがカチコチです）";
      jar.parentElement.insertBefore(banner, jar);
    }

    saveState();
  }

  function addEvent(title, duration) {
    const capacity = state.capacityMinutes;
    const used = usedMinutes();

    if (duration <= 0) return;

    if (used + duration > capacity) {
      jar.classList.remove("shake");
      // force reflow so the animation can replay
      void jar.offsetWidth;
      jar.classList.add("shake");
      return;
    }

    const t = clamp01((used + duration / 2) / capacity);
    state.events.push({
      id: Date.now() + Math.random(),
      title: title || "予定",
      duration,
      t,
    });
    render();
  }

  function removeEvent(id) {
    state.events = state.events.filter((ev) => ev.id !== id);
    render();
  }

  presetButtons.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-min]");
    if (!btn) return;
    presetButtons.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    durationInput.value = btn.dataset.min;
  });

  durationInput.addEventListener("input", () => {
    presetButtons.querySelectorAll("button").forEach((b) => {
      b.classList.toggle("active", b.dataset.min === durationInput.value);
    });
  });

  addButton.addEventListener("click", () => {
    const title = titleInput.value.trim();
    const duration = parseInt(durationInput.value, 10);
    if (!duration || duration <= 0) return;
    addEvent(title, duration);
    titleInput.value = "";
  });

  titleInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") addButton.click();
  });

  capacityInput.addEventListener("change", () => {
    const value = parseInt(capacityInput.value, 10);
    state.capacityMinutes = Number.isFinite(value) && value > 0 ? value : 480;
    render();
  });

  resetButton.addEventListener("click", () => {
    state.events = [];
    render();
  });

  render();
})();
