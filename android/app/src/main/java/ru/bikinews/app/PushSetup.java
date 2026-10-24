package ru.bikinews.app;

import android.content.Context;

import ru.rustore.sdk.pushclient.RuStorePushClient;

/** Подписка устройства на тему «news» в RuStore Push: включена, пока включены уведомления о новостях. */
final class PushSetup {
    static final String TOPIC = "news";

    private PushSetup() { }

    static void sync(Context ctx) {
        try {
            if (NewsJob.enabled(ctx)) {
                RuStorePushClient.INSTANCE.subscribeToTopic(TOPIC);
            } else {
                RuStorePushClient.INSTANCE.unsubscribeFromTopic(TOPIC);
            }
        } catch (Throwable ignored) {
            // нет RuStore на телефоне или SDK не готов — работает проверка ленты в фоне
        }
    }
}
