# Исходная база BCU

`bcu` — отдельный Git submodule из официального репозитория
[BCUninstaller/Bulk-Crap-Uninstaller](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller),
закреплённый на `30da609384c98ba6e35c6530129541ea4ff3970a`.

Получить содержимое после клонирования проекта:

```text
git submodule update --init --recursive
git -C third_party/bcu rev-parse HEAD
```

Исходники не изменены. Не коммитить наши правки внутрь submodule и не обновлять
его незаметно до latest. Изменение pinned commit — отдельная проверяемая задача
с просмотром upstream diff, лицензий и влияния на переносимые правила.

Наш Rust-код создаётся за пределами submodule. Подходящие алгоритмы и правила
переносятся с сохранением происхождения по [плану](../docs/upstream-reuse.md).
Прямое включение BCU runtime пока не принято. В upstream есть компоненты с
разными лицензиями: см. [уведомления](../THIRD_PARTY_NOTICES.md).

Сборка или запуск upstream может изменять систему. Для сравнительных проверок
использовать подготовленную VM, а не запускать удаление на рабочей машине.
