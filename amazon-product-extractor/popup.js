// popup.js
const AMAZON_HOST = /(^|\.)amazon\.(co\.jp|com)$/;

const FIELDS = [
  { key: "title", label: "商品名" },
  { key: "price", label: "価格" },
  { key: "asin", label: "ASIN" },
  { key: "brand", label: "ブランド" },
  { key: "rating", label: "評価" },
  { key: "reviewCount", label: "レビュー" },
  { key: "availability", label: "在庫" },
  { key: "image", label: "画像URL" },
  { key: "url", label: "URL" },
  { key: "extractedAt", label: "取得日時" }
];

const els = {
  message: document.getElementById("message"),
  result: document.getElementById("result"),
  status: document.getElementById("status"),
  image: document.getElementById("image"),
  title: document.getElementById("title")
};

let current = null;
let statusTimer = null;

function showMessage(text, isError = false) {
  els.message.textContent = text;
  els.message.hidden = false;
  els.message.classList.toggle("error", isError);
  els.result.hidden = true;
}

function setStatus(text) {
  els.status.textContent = text;
  clearTimeout(statusTimer);
  if (text) {
    statusTimer = setTimeout(() => { els.status.textContent = ""; }, 2000);
  }
}

function setField(id, value) {
  const el = document.getElementById(id);
  el.textContent = value || "取得できませんでした";
  el.classList.toggle("missing", !value);
}

function render(data) {
  current = data;

  els.title.textContent = data.title || "商品名を取得できませんでした";
  if (data.image) {
    els.image.src = data.image;
    els.image.alt = data.title || "";
    els.image.hidden = false;
  } else {
    els.image.removeAttribute("src");
    els.image.hidden = true;
  }

  setField("price", data.price);
  setField("asin", data.asin);
  setField("brand", data.brand);
  setField("rating", data.rating);
  setField("reviewCount", data.reviewCount);
  setField("availability", data.availability);

  els.message.hidden = true;
  els.result.hidden = false;
}

function sendExtractMessage(tabId) {
  return new Promise((resolve, reject) => {
    chrome.tabs.sendMessage(tabId, { action: "extract" }, (response) => {
      const error = chrome.runtime.lastError;
      if (error) {
        reject(new Error(error.message));
      } else {
        resolve(response);
      }
    });
  });
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function extract() {
  showMessage("商品情報を取得しています…");

  const tab = await getActiveTab();
  if (!tab || !tab.id || !tab.url) {
    showMessage("タブの情報を取得できませんでした。", true);
    return;
  }

  let host;
  try {
    host = new URL(tab.url).hostname;
  } catch {
    host = "";
  }
  if (!AMAZON_HOST.test(host)) {
    showMessage("Amazonの商品ページを開いた状態で実行してください。", true);
    return;
  }

  let data;
  try {
    data = await sendExtractMessage(tab.id);
  } catch {
    // ページ読み込み前に拡張機能を入れた場合など、content scriptが未注入のとき
    try {
      await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["content.js"] });
      data = await sendExtractMessage(tab.id);
    } catch (injectError) {
      showMessage("ページに接続できませんでした。ページを再読み込みしてから試してください。", true);
      console.error(injectError);
      return;
    }
  }

  if (!data) {
    showMessage("商品情報を取得できませんでした。", true);
    return;
  }

  if (!data.asin && !data.title) {
    showMessage("商品ページではないようです。商品ページで実行してください。", true);
    return;
  }

  render(data);
  chrome.storage.local.set({ lastProduct: data });
}

function toText(data) {
  return FIELDS
    .filter(({ key }) => data[key])
    .map(({ key, label }) => `${label}: ${data[key]}`)
    .join("\n");
}

function toCsv(data) {
  const escape = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;
  const header = FIELDS.map(({ label }) => escape(label)).join(",");
  const row = FIELDS.map(({ key }) => escape(data[key])).join(",");
  return `${header}\n${row}`;
}

async function copy(text, label) {
  if (!text) {
    setStatus("コピーできる情報がありません");
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
    setStatus(`${label}をコピーしました`);
  } catch (error) {
    console.error(error);
    setStatus("コピーに失敗しました");
  }
}

document.getElementById("copyText").addEventListener("click", () => {
  if (current) copy(toText(current), "テキスト");
});

document.getElementById("copyJson").addEventListener("click", () => {
  if (current) copy(JSON.stringify(current, null, 2), "JSON");
});

document.getElementById("copyCsv").addEventListener("click", () => {
  if (current) copy(toCsv(current), "CSV");
});

document.getElementById("reload").addEventListener("click", () => {
  extract();
});

extract();
