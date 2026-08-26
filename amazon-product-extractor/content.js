// content.js
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

  // ブランド
  const brand = document.querySelector('#bylineInfo')?.textContent?.trim() ||
                document.querySelector('a#bylineInfo')?.textContent?.trim() ||
                null;

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
