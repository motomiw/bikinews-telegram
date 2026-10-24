package ru.bikinews.app;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.res.ColorStateList;
import android.content.res.Configuration;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Typeface;
import android.net.ConnectivityManager;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.Menu;
import android.view.View;
import android.view.Window;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.PopupMenu;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

/**
 * Быки News — приложение-читалка сайта bikinews.ru.
 * Страницы сайта показываются во встроенном WebView, а навигация, обновление,
 * офлайн-режим, «Поделиться» и внешние ссылки сделаны нативно.
 */
public class MainActivity extends Activity {

    static final String SITE = "https://bikinews.ru/";
    static final String UA_MARK = " BikinewsApp/";

    // Вкладки: подпись, иконка, адрес
    static final int[] TAB_LABELS = {R.string.tab_home, R.string.tab_news, R.string.tab_matches, R.string.tab_table, R.string.tab_more};
    static final int[] TAB_ICONS = {R.drawable.ic_tab_home, R.drawable.ic_tab_news, R.drawable.ic_tab_matches, R.drawable.ic_tab_table, R.drawable.ic_tab_more};
    static final String[] TAB_URLS = {SITE, SITE + "news.html", SITE + "matches.html", SITE + "#table", null};

    WebView web;
    SwipeRefreshLayout swipe;
    ProgressBar progress;
    View offline;
    LinearLayout tabs;
    int current = -1;
    boolean mainFrameFailed = false;
    int uiNight;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        uiNight = nightBits();
        setContentView(R.layout.activity_main);
        setupWindow();

        web = findViewById(R.id.web);
        swipe = findViewById(R.id.swipe);
        progress = findViewById(R.id.progress);
        offline = findViewById(R.id.offline);
        tabs = findViewById(R.id.tabs);

        applyInsets();
        buildTabs();
        setupWeb();
        NewsJob.schedule(this);
        PushSetup.sync(this);
        askNotifyPermission();

        swipe.setColorSchemeColors(getColor(R.color.accent));
        swipe.setProgressBackgroundColorSchemeColor(getColor(R.color.surface));
        swipe.setOnRefreshListener(() -> {
            updateCacheMode();
            web.reload();
        });
        findViewById(R.id.retry).setOnClickListener(v -> {
            offline.setVisibility(View.GONE);
            updateCacheMode();
            if (web.getUrl() == null || web.getUrl().startsWith("about:")) web.loadUrl(SITE);
            else web.reload();
        });

        if (state != null && web.restoreState(state) != null) {
            selectTabFor(web.getUrl());
        } else {
            String deep = linkFrom(getIntent());
            web.loadUrl(deep != null ? deep : SITE);
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        String deep = linkFrom(intent);
        if (deep != null) web.loadUrl(deep);
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    public void onBackPressed() {
        if (offline.getVisibility() == View.VISIBLE && web.canGoBack()) {
            offline.setVisibility(View.GONE);
            web.goBack();
        } else if (web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onPause() { super.onPause(); web.onPause(); }

    @Override
    protected void onResume() { super.onResume(); web.onResume(); }

    @Override
    protected void onDestroy() {
        if (web != null) web.destroy();
        super.onDestroy();
    }

    // ---------- отступы под системные панели (Android 15 рисует приложение «от края до края») ----------
    void applyInsets() {
        View root = findViewById(R.id.root);
        final int tabsPadBottom = tabs.getPaddingBottom();
        root.setOnApplyWindowInsetsListener((v, insets) -> {
            int top, bottom, left, right;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                top = i.top; bottom = i.bottom; left = i.left; right = i.right;
            } else {
                top = insets.getSystemWindowInsetTop(); bottom = insets.getSystemWindowInsetBottom();
                left = insets.getSystemWindowInsetLeft(); right = insets.getSystemWindowInsetRight();
            }
            v.setPadding(left, top, right, 0);
            tabs.setPadding(tabs.getPaddingLeft(), tabs.getPaddingTop(), tabs.getPaddingRight(), tabsPadBottom + bottom);
            return insets;
        });
    }

    // ---------- нижняя панель ----------
    void buildTabs() {
        for (int i = 0; i < TAB_LABELS.length; i++) {
            final int idx = i;
            LinearLayout item = new LinearLayout(this);
            item.setOrientation(LinearLayout.VERTICAL);
            item.setGravity(Gravity.CENTER_HORIZONTAL);
            item.setPadding(0, dp(2), 0, dp(2));
            item.setLayoutParams(new LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f));
            item.setContentDescription(getString(TAB_LABELS[i]));
            TypedValue tv = new TypedValue();
            getTheme().resolveAttribute(android.R.attr.selectableItemBackgroundBorderless, tv, true);
            item.setBackgroundResource(tv.resourceId);

            ImageView icon = new ImageView(this);
            icon.setImageResource(TAB_ICONS[i]);
            icon.setPadding(dp(18), dp(4), dp(18), dp(4));
            icon.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);
            item.addView(icon, new LinearLayout.LayoutParams(dp(64), dp(32)));

            TextView label = new TextView(this);
            label.setText(TAB_LABELS[i]);
            label.setTextSize(TypedValue.COMPLEX_UNIT_SP, 12);
            label.setMaxLines(1);
            label.setImportantForAccessibility(View.IMPORTANT_FOR_ACCESSIBILITY_NO);
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT, LinearLayout.LayoutParams.WRAP_CONTENT);
            lp.topMargin = dp(2);
            item.addView(label, lp);

            item.setOnClickListener(v -> onTab(idx, v));
            tabs.addView(item);
        }
        paintTabs();
    }

    void onTab(int idx, View anchor) {
        if (TAB_URLS[idx] == null) { showMore(anchor); return; }
        offline.setVisibility(View.GONE);
        String url = web.getUrl();
        if (idx == 3 && url != null && stripHash(url).equals(SITE)) {
            // уже на главной — просто прокрутить к таблице
            web.evaluateJavascript("(function(){var t=document.getElementById('table');if(t)t.scrollIntoView({behavior:'smooth'});})()", null);
            setCurrent(3);
            return;
        }
        if (idx == current && url != null && stripHash(url).equals(stripHash(TAB_URLS[idx]))) {
            web.evaluateJavascript("window.scrollTo({top:0,behavior:'smooth'})", null);
            return;
        }
        updateCacheMode();
        web.loadUrl(TAB_URLS[idx]);
        setCurrent(idx);
    }

    void setCurrent(int idx) { current = idx; paintTabs(); }

    void paintTabs() {
        int on = getColor(R.color.accent), off = getColor(R.color.muted), ink = getColor(R.color.ink);
        for (int i = 0; i < tabs.getChildCount(); i++) {
            LinearLayout item = (LinearLayout) tabs.getChildAt(i);
            ImageView icon = (ImageView) item.getChildAt(0);
            TextView label = (TextView) item.getChildAt(1);
            boolean sel = i == current;
            // выбранная вкладка отличается не только цветом: подложка-«пилюля» и жирная подпись
            icon.setImageTintList(ColorStateList.valueOf(sel ? on : off));
            icon.setBackgroundResource(sel ? R.drawable.tab_pill : 0);
            label.setTextColor(sel ? ink : off);
            label.setTypeface(Typeface.DEFAULT, sel ? Typeface.BOLD : Typeface.NORMAL);
            item.setSelected(sel);
        }
    }

    void selectTabFor(String url) {
        if (url == null) return;
        Uri u = Uri.parse(url);
        String path = u.getPath() == null ? "/" : u.getPath();
        String frag = u.getFragment();
        int idx;
        if (path.equals("/") || path.equals("/index.html")) idx = "table".equals(frag) ? 3 : 0;
        else if (path.equals("/news.html")) idx = 1;
        else if (path.equals("/matches.html")) idx = 2;
        else if (path.equals("/squad.html") || path.equals("/club.html") || path.equals("/privacy.html")) idx = 4;
        else idx = 1; // отдельная страница новости
        if (idx != current) setCurrent(idx);
    }

    void showMore(View anchor) {
        PopupMenu pm = new PopupMenu(this, anchor, Gravity.END);
        Menu m = pm.getMenu();
        m.add(0, 1, 1, R.string.more_squad);
        m.add(0, 2, 2, R.string.more_club);
        m.add(1, 3, 3, R.string.more_tg);
        m.add(1, 4, 4, R.string.more_max);
        m.add(2, 5, 5, R.string.more_share);
        m.add(2, 6, 6, R.string.more_privacy);
        m.add(2, 7, 7, R.string.more_about);
        m.add(3, 8, 8, NewsJob.enabled(this) ? R.string.more_notify_off : R.string.more_notify_on);
        pm.setOnMenuItemClickListener(it -> {
            switch (it.getItemId()) {
                case 1: go(SITE + "squad.html"); setCurrent(4); break;
                case 2: go(SITE + "club.html"); setCurrent(4); break;
                case 3: openOutside("https://t.me/bikinews"); break;
                case 4: openOutside("https://max.ru/channel_bikinews"); break;
                case 5: sharePage(); break;
                case 6: go(SITE + "privacy.html"); setCurrent(4); break;
                case 7: showAbout(); break;
                case 8: toggleNotify(); break;
            }
            return true;
        });
        pm.show();
    }

    // ---------- уведомления о новых новостях ----------
    static final int REQ_NOTIFY = 7;

    void askNotifyPermission() {
        if (Build.VERSION.SDK_INT < 33 || !NewsJob.enabled(this)) return;
        if (checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) == android.content.pm.PackageManager.PERMISSION_GRANTED) return;
        android.content.SharedPreferences p = getSharedPreferences(NewsJob.PREFS, MODE_PRIVATE);
        if (p.getBoolean("asked", false)) return;   // спрашиваем один раз; дальше — через меню «Ещё»
        p.edit().putBoolean("asked", true).apply();
        requestPermissions(new String[]{android.Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIFY);
    }

    void toggleNotify() {
        boolean on = !NewsJob.enabled(this);
        NewsJob.setEnabled(this, on);
        PushSetup.sync(this);
        if (on && Build.VERSION.SDK_INT >= 33
                && checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
            if (shouldShowRequestPermissionRationale(android.Manifest.permission.POST_NOTIFICATIONS)
                    || !getSharedPreferences(NewsJob.PREFS, MODE_PRIVATE).getBoolean("asked", false)) {
                getSharedPreferences(NewsJob.PREFS, MODE_PRIVATE).edit().putBoolean("asked", true).apply();
                requestPermissions(new String[]{android.Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIFY);
            } else {
                // разрешение отклонено навсегда — открываем настройки уведомлений приложения
                Intent i = new Intent(android.provider.Settings.ACTION_APP_NOTIFICATION_SETTINGS);
                i.putExtra(android.provider.Settings.EXTRA_APP_PACKAGE, getPackageName());
                try { startActivity(i); } catch (ActivityNotFoundException ignored) { }
            }
        }
        Toast.makeText(this, on ? R.string.notify_on_toast : R.string.notify_off_toast, Toast.LENGTH_SHORT).show();
    }

    void go(String url) {
        offline.setVisibility(View.GONE);
        updateCacheMode();
        web.loadUrl(url);
    }

    void sharePage() {
        String url = web.getUrl() != null && !web.getUrl().startsWith("about:") ? web.getUrl() : SITE;
        String title = web.getTitle() != null ? web.getTitle() : getString(R.string.app_name);
        Intent send = new Intent(Intent.ACTION_SEND);
        send.setType("text/plain");
        send.putExtra(Intent.EXTRA_SUBJECT, title);
        send.putExtra(Intent.EXTRA_TEXT, title + "\n" + url);
        startActivity(Intent.createChooser(send, getString(R.string.share_via)));
    }

    void showAbout() {
        String ver = "";
        try {
            PackageInfo pi = getPackageManager().getPackageInfo(getPackageName(), 0);
            ver = pi.versionName;
        } catch (Exception ignored) { }
        new AlertDialog.Builder(this)
                .setTitle(R.string.about_title)
                .setMessage(getString(R.string.about_text, ver))
                .setPositiveButton(R.string.about_ok, null)
                .setNeutralButton(R.string.about_mail, (d, w) -> openOutside("mailto:i@bikinews.ru"))
                .show();
    }

    // ---------- WebView ----------
    void setupWeb() {
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);           // на сайте на JS построены таблица, матчи и лента
        s.setDomStorageEnabled(true);           // настройки версии для слабовидящих и согласие на cookie
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setSupportMultipleWindows(false);     // ссылки target=_blank идут через shouldOverrideUrlLoading
        s.setUserAgentString(s.getUserAgentString() + UA_MARK + versionName());
        // Сайт свёрстан под обычный размер шрифта; системное «крупный шрифт» в WebView раздувало текст.
        // Берём 90% от обычного и не даём системе увеличить больше чем до 100% (для крупного шрифта на сайте есть режим для слабовидящих).
        float fs = getResources().getConfiguration().fontScale;
        s.setTextZoom(Math.round(90 * Math.min(Math.max(fs, 0.85f), 1.11f)));
        updateCacheMode();

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int p) {
                progress.setProgress(p);
                progress.setVisibility(p < 100 ? View.VISIBLE : View.GONE);
            }
        });

        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
                Uri u = req.getUrl();
                if (isOurs(u)) {
                    String p = u.getPath() == null ? "" : u.getPath();
                    // служебные файлы и страница для MAX — во внешнем браузере
                    if (p.endsWith(".xml") || p.endsWith(".json") || p.equals("/max.html")) {
                        openOutside(u.toString());
                        return true;
                    }
                    return false;
                }
                openOutside(u.toString());
                return true;
            }

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                mainFrameFailed = false;
                selectTabFor(url);
            }

            @Override
            public void doUpdateVisitedHistory(WebView view, String url, boolean isReload) {
                selectTabFor(url);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                swipe.setRefreshing(false);
                if (!mainFrameFailed) offline.setVisibility(View.GONE);
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest req, WebResourceError err) {
                if (req.isForMainFrame()) {
                    mainFrameFailed = true;
                    swipe.setRefreshing(false);
                    offline.setVisibility(View.VISIBLE);
                }
            }
        });
    }

    /** Без сети берём страницы из кэша, при сети — свежие с сайта. */
    void updateCacheMode() {
        web.getSettings().setCacheMode(isOnline() ? WebSettings.LOAD_DEFAULT : WebSettings.LOAD_CACHE_ELSE_NETWORK);
    }

    boolean isOnline() {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        if (cm == null) return true;
        if (Build.VERSION.SDK_INT >= 23) {
            NetworkCapabilities nc = cm.getNetworkCapabilities(cm.getActiveNetwork());
            return nc != null && nc.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET);
        }
        return true;
    }

    static boolean isOurs(Uri u) {
        String h = u.getHost();
        return "https".equals(u.getScheme()) && h != null && (h.equals("bikinews.ru") || h.equals("www.bikinews.ru"));
    }

    static String linkFrom(Intent intent) {
        if (intent == null || !Intent.ACTION_VIEW.equals(intent.getAction()) || intent.getData() == null) return null;
        return isOurs(intent.getData()) ? intent.getData().toString() : null;
    }

    void openOutside(String url) {
        try {
            Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            i.addCategory(Intent.CATEGORY_BROWSABLE);
            startActivity(i);
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, R.string.no_app, Toast.LENGTH_SHORT).show();
        }
    }

    String versionName() {
        try { return getPackageManager().getPackageInfo(getPackageName(), 0).versionName; }
        catch (Exception e) { return "1"; }
    }

    static String stripHash(String url) {
        int i = url.indexOf('#');
        return i >= 0 ? url.substring(0, i) : url;
    }

    int dp(int v) { return Math.round(v * getResources().getDisplayMetrics().density); }

    int nightBits() { return getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK; }

    @Override
    public void onConfigurationChanged(Configuration c) {
        int before = uiNight;
        super.onConfigurationChanged(c);
        // при смене светлой/тёмной темы пересоздаём экран, чтобы обновить цвета (страница сохранится)
        if ((c.uiMode & Configuration.UI_MODE_NIGHT_MASK) != before) recreate();
    }

    // ---------- окно «от края до края» на всех версиях Android ----------
    void setupWindow() {
        Window w = getWindow();
        boolean night = nightBits() == Configuration.UI_MODE_NIGHT_YES;
        w.setStatusBarColor(Color.TRANSPARENT);
        w.setNavigationBarColor(Build.VERSION.SDK_INT >= 27 ? Color.TRANSPARENT : getColor(R.color.turf));
        if (Build.VERSION.SDK_INT >= 29) w.setNavigationBarContrastEnforced(false);
        if (Build.VERSION.SDK_INT >= 30) {
            w.setDecorFitsSystemWindows(false);
            WindowInsetsController c = w.getInsetsController();
            if (c != null) {
                // светлые значки в строке состояния (фон тёмно-зелёный); значки навигации — под тему
                c.setSystemBarsAppearance(night ? 0 : WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS,
                        WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS | WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS);
            }
        } else {
            int f = View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION;
            if (Build.VERSION.SDK_INT >= 27 && !night) f |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
            w.getDecorView().setSystemUiVisibility(f);
        }
    }
}
