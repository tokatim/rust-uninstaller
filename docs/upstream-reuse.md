# Использование существующего BCU

Дата: 25 ноября 2026 года. Решение принято по просьбе владельца использовать уже
реализованные функции BCU. Исходники подключены в `third_party/bcu` на commit
`30da609384c98ba6e35c6530129541ea4ff3970a`. Перенос в наши исполняемые модули ещё не начат.

## Подход

Не разрабатывать заново правила совместимости там, где BCU уже содержит полезную
реализацию. Извлекать подходящие алгоритмы, модели, установочные признаки и тестовые
случаи, адаптировать их на Rust и сохранять attribution. Перевод C# в Rust считается
переносом с изменениями; языковая переработка не стирает авторство и условия лицензии.

Публичный репозиторий Rust-проекта имеет собственную историю и pinned связь с upstream.
Это позволяет развивать новый UI и ядро без автоматического наследования старых
release workflows, .NET-сборки, брендинга и несвязанных компонентов. Полная история
BCU остаётся доступна в исходном репозитории; pointer фиксирует используемую версию.

## Карта модулей

Все пути в таблице относительны `third_party/bcu/source`. Статус каждой строки —
«исходник найден, перенос не начат». Лицензия каждой фактически используемой части
проверяется перед переносом; таблица не является blanket-разрешением для каталога.

| Область | Существующий исходник | Как используем | Этап |
| --- | --- | --- | --- |
| Чтение реестра | `UninstallTools/Factory/RegistryFactory.cs` | Поля и случаи записей → Rust provider; проекции через явные Windows flags | M1 |
| Объединение результатов | `UninstallTools/Factory/ApplicationUninstallerFactory.cs`, `ApplicationEntryTools.cs` рядом | Доказательства связи, dedup и порядок обогащения → чистые функции и фикстуры | M1 |
| Модель программы | `UninstallTools/ApplicationUninstallerEntry.cs` | Список свойств и возможностей → типизированная модель с unknown и provenance | M1 |
| MSI API | `KlocTools/IO/MsiTools.cs`, `KlocTools/Native/MsiWrapper.cs` | Требуемые вызовы/коды → Rust Windows adapter; чужую FFI-обёртку целиком не предполагать необходимой | M2 |
| Тип установщика | `UninstallTools/Factory/InfoAdders/UninstallerTypeAdder.cs` | Признаки → адаптеры с объяснимым распознаванием и проверками | M2 |
| Тихие режимы | `UninstallTools/Factory/InfoAdders/InnoSetupQuietUninstallStringGenerator.cs`, `MsiUninstallStringGenerator.cs`, `NsisQuietUninstallStringGenerator.cs` | Проверенные режимы → отдельные adapters; учесть зависимость NSIS от автоматизации | M2/M5 |
| Очередь и конфликты | `UninstallTools/Uninstaller/BulkUninstallTask.cs` | Политики совместимости → scheduler; начать последовательно, не копировать весь threading/UI-код | M2 |
| Процессы и исходы | `UninstallTools/Uninstaller/BulkUninstallEntry.cs` | Exit/reboot и сценарии дочерних процессов → state machine; исключить опасное глобальное завершение процессов | M2 |
| Остатки | `UninstallTools/Junk/JunkManager.cs`, `Finders/` | Категории/правила → ограниченные Rust scanners с дополнительными path/data guardrails | M3 |
| Уверенность | `UninstallTools/Junk/Confidence/ConfidenceCollection.cs`, `ConfidenceGenerators.cs` | Доказательства → объяснимая классификация; score не выдавать за вероятность | M3 |
| Реестр остатков | `UninstallTools/Junk/Finders/Registry/SoftwareRegKeyScanner.cs` | Поля явной связи и негативные примеры → fixtures; не переносить broad scan без защиты | M3 |
| Store и Steam | `StoreAppHelper/AppManager.cs`, `SteamHelper/`, factories в `UninstallTools/Factory/` | Форматы и API-последовательности → Rust providers, актуальность API проверять отдельно | M4 |
| CLI и сериализация | `BCU-console/Program.cs`, `UninstallTools/ApplicationEntrySerializer.cs` | Форматы и сценарии → наш versioned contract; upstream CLI — сравнительный инструмент в VM | M5 |
| Проверочные примеры | `BulkCrapUninstallerTests/` | Подходящие cases → регрессионные тесты; старые assertions не заменяют наши safety-критерии | M1–M5 |

Новые функции продукта, например независимая авторизация helper и наш backup,
могут потребовать собственной реализации. Они остаются явно отделены от уже
существующих upstream-возможностей в требованиях и истории.

## Почему не подключаем DLL немедленно

`UninstallTools.csproj` ссылается на KlocTools и ObjectListView; общие build props
включают Windows Forms. В ObjectListView найдены headers GPL-3.0-or-later.
Поэтому копирование библиотеки целиком не означает получение автономного Rust-ядра
и требует отдельного анализа зависимостей/лицензирования.

Начальный путь — перенос выбранных Apache-совместимых исходников. Если временный
.NET helper заметно ускорит конкретную функцию, это оформляется отдельным ADR:
точный состав, лицензии, API, runtime, привилегии, тесты и план замены на Rust.
Обёртка над всем BCU не объявляется Rust-переписыванием.

## Процедура переноса

1. Выбрать требование и точный upstream file/commit.
2. Проверить headers, зависимости и применимую лицензию.
3. Описать исходное поведение и ограничения на синтетических примерах.
4. Перенести минимальную полезную логику на Rust, изолировав Windows API от правил.
5. Сохранить copyright, license и notice об адаптации; обновить THIRD_PARTY_NOTICES.
6. Проверить позитивные и негативные cases; расхождения с BCU объяснить в коммите.
7. Для системного действия выполнить VM-сценарий и только после этого отметить требование готовым.

Пример заголовка для производного Rust-файла после проверки условий источника:

```text
SPDX-License-Identifier: Apache-2.0
Portions adapted from Bulk Crap Uninstaller, Copyright <original author/year>.
Source: <upstream commit and repository-relative path>.
Modified for Rust Uninstaller in 2026: <brief description>.
```

Исходных авторов/год брать из конкретного файла, а не заменять шаблоном автоматически.
При обновлении upstream просматривать изменения только относящихся к нашим модулям
файлов и повторно проверять лицензии. Автоматического слияния upstream в наш main нет.
