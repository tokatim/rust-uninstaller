# Источники и происхождение решений

## BCU

Исследован публичный репозиторий
[BCUninstaller/Bulk-Crap-Uninstaller](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller).
Для воспроизводимости анализа зафиксирована версия дерева:
`30da609384c98ba6e35c6530129541ea4ff3970a`.

| Материал | Что изучено |
| --- | --- |
| [README](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/README.md) | Назначение, платформы, функции и текущий технологический стек |
| [ApplicationUninstallerFactory](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Factory/ApplicationUninstallerFactory.cs) | Сбор источников, обогащение и объединение записей |
| [RegistryFactory](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Factory/RegistryFactory.cs) | Чтение зарегистрированных программ |
| [BulkUninstallTask](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Uninstaller/BulkUninstallTask.cs) | Очередь, ограничения параллелизма, конфликты |
| [BulkUninstallEntry](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Uninstaller/BulkUninstallEntry.cs) | Процессы, exit codes и ошибки |
| [JunkManager](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Junk/JunkManager.cs) | Сканы остатков, dedup и защищённые locations |
| [ConfidenceCollection](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Junk/Confidence/ConfidenceCollection.cs) | Уровни уверенности на основе evidence |
| [SoftwareRegKeyScanner](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Junk/Finders/Registry/SoftwareRegKeyScanner.cs) | Эвристики поиска записей реестра |
| [NSIS quiet generator](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Factory/InfoAdders/NsisQuietUninstallStringGenerator.cs) | Роль отдельной автоматизации |
| [Inno quiet generator](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/source/UninstallTools/Factory/InfoAdders/InnoSetupQuietUninstallStringGenerator.cs) | Особенности тихого запуска и запрета reboot |
| [License](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/Licence.txt), [NOTICE](https://github.com/BCUninstaller/Bulk-Crap-Uninstaller/blob/30da609384c98ba6e35c6530129541ea4ff3970a/NOTICE) | Заявленная Apache-2.0 и уведомления исходного проекта |

Разбор статический: программа не запускалась, её полный набор функций и фактическое
поведение не прошли независимую проверку. Наши требования — собственная проектная
спецификация, а не утверждение о полной совместимости с BCU. Некоторые цели, например
строгое разделение прав и правила restore, задают желаемое поведение нашего продукта.

Исходный репозиторий подключён как submodule `third_party/bcu` на указанном commit.
Перенос кода в собственные Rust-модули пока не начат. Собственные материалы
лицензированы Apache-2.0. Лицензии компонентов проверяются отдельно: в исходниках
ObjectListView обнаружены GPL-3.0-or-later headers, в NBug — MIT. Корневая лицензия
BCU не заменяет эти лицензии. См. [уведомления](../THIRD_PARTY_NOTICES.md).

Перед переносом сохранять авторство, source path/commit и отметку об адаптации.
Первичный аудит не является полным аудитом всех 1917 элементов upstream-дерева.
Логотипы и названия upstream не используются как собственный бренд.

## Технологии и Windows

Официальные источники просмотрены 25 ноября 2026 года. Версии зависимостей и API
повторно проверяются перед реализацией; материалы могут меняться.

- [Tauri: назначение и frontend/backend](https://v2.tauri.app/start/) — основа выбора оболочки.
- [Tauri: WebView2 на Windows](https://v2.tauri.app/reference/webview-versions/) — зависимость поставки.
- [Tauri: security model](https://v2.tauri.app/security/) — capabilities, scopes и CSP.
- [Microsoft windows-rs](https://github.com/microsoft/windows-rs) — доступ Rust к Windows API;
  конкретные crates/bindings выбираются на M0–M2 по требуемым API.
- [MSI exit codes](https://learn.microsoft.com/en-us/windows/win32/msi/error-codes) —
  успех, отмена, конфликт и reboot имеют разные значения; нормализуются адаптером.
- [Alternate registry views](https://learn.microsoft.com/en-us/windows/win32/winprog64/accessing-an-alternate-registry-view) —
  проекции читаются явно через flags; зарезервированные Wow6432Node пути не строятся вручную.
- [Slint](https://docs.slint.dev/latest/docs/slint/) — рассматриваемая альтернатива интерфейса.

До реализации каждого source adapter изучить его актуальный официальный API,
ограничения пользовательского scope и поддерживаемые способы удаления. Этот обзор
не заменяет отдельное исследование Store, Steam или package managers.
