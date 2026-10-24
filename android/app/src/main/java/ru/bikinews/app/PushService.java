package ru.bikinews.app;

import java.util.List;
import java.util.Map;

import ru.rustore.sdk.pushclient.messaging.model.RemoteMessage;
import ru.rustore.sdk.pushclient.messaging.service.RuStoreMessagingService;

/**
 * Получает пуши RuStore. Сервер (poster.py) присылает только данные: id, заголовок, текст,
 * рубрику, время и страницу новости. Уведомление рисуем сами тем же кодом, что и фоновая
 * проверка ленты, поэтому новость, пришедшая двумя путями, показывается один раз.
 */
public class PushService extends RuStoreMessagingService {

    @Override
    public void onNewToken(String token) {
        // подписка на тему «news» привязана к устройству и повторяется при каждом запуске приложения
    }

    @Override
    public void onMessageReceived(RemoteMessage message) {
        try {
            Map<String, String> d = message.getData();
            if (d == null) return;
            String id = d.get("id");
            String title = d.get("title");
            if (id == null || id.isEmpty() || title == null || title.isEmpty()) return;
            if (!NewsJob.enabled(this) || NewsJob.wasSeen(this, id)) return;
            long ts = 0;
            try { ts = Long.parseLong(d.get("ts")); } catch (Exception ignored) { }
            NewsJob.notifyNews(this, id, title, d.get("text"), d.get("tag"), ts, d.get("page"));
            NewsJob.markSeen(this, id);
        } catch (Exception ignored) { }
    }

    @Override
    public void onDeletedMessages() { }

    @Override
    @SuppressWarnings("rawtypes")
    public void onError(List errors) { }
}
