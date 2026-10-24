package ru.bikinews.app;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.job.JobInfo;
import android.app.job.JobParameters;
import android.app.job.JobScheduler;
import android.app.job.JobService;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Фоновая проверка новых новостей: раз в 15 минут (так часто, как разрешает Android)
 * читает bikinews.ru/data/glavnoe.json и показывает уведомление о новостях, которых
 * приложение ещё не видело. Нажатие открывает новость в приложении.
 * Новые новости узнаются по id, а не по времени: пересказ может встать в ленту
 * со временем публикации источника раньше предыдущих.
 */
public class NewsJob extends JobService {

    static final int JOB_ID = 1001;
    static final String CHANNEL = "news";
    static final String PREFS = "news";
    static final String KEY_SEEN = "seen";
    static final String KEY_ON = "notify_on";
    static final int MAX_SHOW = 3;

    static void schedule(Context ctx) {
        JobScheduler js = (JobScheduler) ctx.getSystemService(Context.JOB_SCHEDULER_SERVICE);
        if (js == null || js.getPendingJob(JOB_ID) != null) return;
        JobInfo job = new JobInfo.Builder(JOB_ID, new ComponentName(ctx, NewsJob.class))
                .setRequiredNetworkType(JobInfo.NETWORK_TYPE_ANY)
                .setPeriodic(15 * 60 * 1000L)
                .setPersisted(true)
                .build();
        js.schedule(job);
    }

    static boolean enabled(Context ctx) {
        return ctx.getSharedPreferences(PREFS, MODE_PRIVATE).getBoolean(KEY_ON, true);
    }

    static void setEnabled(Context ctx, boolean on) {
        ctx.getSharedPreferences(PREFS, MODE_PRIVATE).edit().putBoolean(KEY_ON, on).apply();
    }

    @Override
    public boolean onStartJob(JobParameters params) {
        new Thread(() -> {
            try { check(getApplicationContext()); } catch (Exception ignored) { }
            jobFinished(params, false);
        }).start();
        return true;
    }

    @Override
    public boolean onStopJob(JobParameters params) { return true; }

    static void check(Context ctx) throws Exception {
        JSONArray items = load().getJSONArray("items");
        SharedPreferences p = ctx.getSharedPreferences(PREFS, MODE_PRIVATE);
        String saved = p.getString(KEY_SEEN, null);
        Set<String> seen = new HashSet<>();
        if (saved != null && !saved.isEmpty()) seen.addAll(Arrays.asList(saved.split(",")));

        List<JSONObject> fresh = new ArrayList<>();
        StringBuilder ids = new StringBuilder();
        int n = Math.min(items.length(), 60);
        for (int i = 0; i < n; i++) {
            JSONObject it = items.getJSONObject(i);
            String id = it.optString("id");
            if (id.isEmpty()) continue;
            if (ids.length() > 0) ids.append(',');
            ids.append(id);
            // смотрим только верх ленты: старые новости, впервые попавшие в окно, не повод для уведомления
            if (saved != null && i < 15 && !seen.contains(id)) fresh.add(it);
        }
        p.edit().putString(KEY_SEEN, ids.toString()).apply();
        if (saved == null || fresh.isEmpty() || !enabled(ctx)) return;   // первый запуск — только запоминаем ленту
        if (Build.VERSION.SDK_INT >= 33 && ctx.checkSelfPermission(android.Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) return;

        NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
        ensureChannel(ctx, nm);
        int shown = 0;
        for (JSONObject it : fresh) {
            if (shown++ >= MAX_SHOW) break;
            String page = it.optString("page");
            String url = MainActivity.SITE + page;
            String text = "";
            JSONArray paras = it.optJSONArray("paras");
            if (paras != null && paras.length() > 0) text = paras.optString(0);
            Intent open = new Intent(Intent.ACTION_VIEW, Uri.parse(url), ctx, MainActivity.class);
            open.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            PendingIntent pi = PendingIntent.getActivity(ctx, it.optString("id").hashCode(), open,
                    PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(ctx, CHANNEL) : new Notification.Builder(ctx);
            b.setSmallIcon(R.drawable.ic_stat_bull)
                    .setColor(ctx.getColor(R.color.accent))
                    .setContentTitle(it.optString("title"))
                    .setContentText(text)
                    .setStyle(new Notification.BigTextStyle().bigText(text))
                    .setSubText(it.optString("tag"))
                    .setContentIntent(pi)
                    .setAutoCancel(true)
                    .setWhen(it.optLong("ts", System.currentTimeMillis() / 1000) * 1000L)
                    .setShowWhen(true);
            nm.notify(it.optString("id").hashCode(), b.build());
        }
    }

    static void ensureChannel(Context ctx, NotificationManager nm) {
        if (Build.VERSION.SDK_INT < 26 || nm.getNotificationChannel(CHANNEL) != null) return;
        NotificationChannel ch = new NotificationChannel(CHANNEL, ctx.getString(R.string.notif_channel), NotificationManager.IMPORTANCE_DEFAULT);
        ch.setDescription(ctx.getString(R.string.notif_channel_desc));
        nm.createNotificationChannel(ch);
    }

    static JSONObject load() throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(MainActivity.SITE + "data/glavnoe.json?t=" + System.currentTimeMillis() / 60000).openConnection();
        c.setConnectTimeout(15000);
        c.setReadTimeout(20000);
        c.setUseCaches(false);
        c.setRequestProperty("User-Agent", "BikinewsApp-notify");
        try (InputStream in = c.getInputStream()) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[16384];
            int r;
            while ((r = in.read(buf)) > 0) out.write(buf, 0, r);
            return new JSONObject(out.toString("UTF-8"));
        } finally {
            c.disconnect();
        }
    }
}
