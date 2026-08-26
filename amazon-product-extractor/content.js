// content.js

// 「ブランド: Anker」「Ankerのストアを表示」「Visit the Anker Store」のような
// 表記からブランド名だけを取り出す
function normalizeBrand(text) {
  if (!text) return null;

  const brand = text
    .replace(/\s+/g, ' ')
    .trim()
    // 先頭の「ブランド:」「メーカー:」「Brand:」「Visit the」を落とす
    .replace(/^(?:ブランド|メーカー|販売元|Brand|Visit the)\s*[:：]?\s*/i, '')
    // 末尾の「のストアを表示」「のストア」「Store」を落とす
    .replace(/(?:のストアを表示|のストア|ブランドストアを表示)$/, '')
    .replace(/\s+Store$/i, '')
    .trim();

  return brand || null;
}

function extractProductInfo() {
  // ASINをURLから取得（最も確実）
  const asinMatch = window.location.href.match(/\/(?:dp|gp\/product|product)\/([A-Z0-9]{10})/i);
  const asin = asinMatch ? asinMatch[1].toUpperCase() : 
               document.querySelector('input[name="ASIN"]')?.value || 
               document.querySelector('[data-asin]')?.dataset.asin || null;

  // タイトル
  const title = document.querySelector('#productTitle')?.textContent?.trim() ||
                document.querySelector('#title')?.textContent?.trim() ||
                null;

  // 価格（.a-offscreenが比較的安定）
  let price = document.querySelector('.a-price .a-offscreen')?.textContent?.trim() ||
              document.querySelector('#corePrice_feature_div .a-offscreen')?.textContent?.trim() ||
              document.querySelector('#corePriceDisplay_desktop_feature_div .a-offscreen')?.textContent?.trim() ||
              document.querySelector('.priceToPay .a-offscreen')?.textContent?.trim() ||
              null;

  // 評価
  const rating = document.querySelector('#acrPopover .a-icon-alt')?.textContent?.trim() ||
                 document.querySelector('[data-hook="rating-out-of-text"]')?.textContent?.trim() ||
                 null;

  // レビュー数
  const reviewCount = document.querySelector('#acrCustomerReviewText')?.textContent?.trim() ||
                      document.querySelector('[data-hook="total-review-count"]')?.textContent?.trim() ||
                      null;

  // ブランド（#bylineInfoは「ブランド: Anker」「Ankerのストアを表示」
  // 「Visit the Anker Store」などの形なので、ブランド名だけを取り出す）
  const brand = normalizeBrand(
    document.querySelector('#bylineInfo')?.textContent ||
    document.querySelector('a#bylineInfo')?.textContent ||
    null
  );

  // メイン画像
  const image = document.querySelector('#landingImage')?.src ||
                document.querySelector('#imgTagWrapperId img')?.src ||
                null;

  // 在庫状況
  const availability = document.querySelector('#availability span')?.textContent?.trim() ||
                       document.querySelector('#availability')?.textContent?.trim() ||
                       null;

  return {
    asin,
    title,
    price,
    rating,
    reviewCount,
    brand,
    image,
    availability,
    url: window.location.href,
    extractedAt: new Date().toISOString()
  };
}

// ポップアップからのメッセージを受け取る
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "extract") {
    const data = extractProductInfo();
    sendResponse(data);
  }
  return true; // 非同期対応
});
