package com.seiremu.timeboxing;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebResourceRequest;
import android.webkit.WebViewClient;

/**
 * タイムボクシング。assets に同梱した timeboxing.html を WebView で表示するだけの
 * 単一画面アプリ。ネットワークは一切使わないため権限も宣言していない。
 */
public class MainActivity extends Activity {

    private static final String APP_URL = "file:///android_asset/timeboxing.html";

    private WebView webView;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);
        webView.setBackgroundColor(0xFF0C0E13);
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        // ゴングは開始ボタン(ユーザー操作)で鳴らすが、WebView 既定の制限を外しておく
        settings.setMediaPlaybackRequiresUserGesture(false);
        // 端末の文字サイズ設定でタイマーのレイアウトが崩れないようにする
        settings.setTextZoom(100);
        // ローカル asset 以外は読まない
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);

        // asset 内のページ以外への遷移は行わせない
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !APP_URL.equals(request.getUrl().toString());
            }
        });

        webView.addJavascriptInterface(new HostBridge(), "AndroidHost");

        setContentView(webView);

        if (savedInstanceState == null) {
            webView.loadUrl(APP_URL);
        } else {
            webView.restoreState(savedInstanceState);
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        webView.saveState(outState);
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    /** ページ側の「計測中は画面を消灯させない」設定を Android の画面点灯フラグにつなぐ。 */
    private final class HostBridge {
        @JavascriptInterface
        public void setKeepScreenOn(final boolean on) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (on) {
                        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                    } else {
                        getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                    }
                }
            });
        }
    }
}
