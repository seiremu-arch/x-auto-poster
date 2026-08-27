# JavaScript から呼ばれるブリッジは難読化・削除しない
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
