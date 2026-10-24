# Классы приложения не обфусцируем — их мало, а стектрейсы читаемее
-keep class ru.bikinews.app.** { *; }

# RuStore Push SDK: классы вызываются по имени из манифеста и самим SDK
-keep class ru.rustore.sdk.** { *; }
-dontwarn ru.rustore.sdk.**
