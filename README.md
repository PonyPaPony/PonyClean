[![PyPI version](https://badge.fury.io/py/pony-clean-cli.svg)](https://pypi.org/project/pony-clean-cli/)
# PonyClean

**PonyClean** — это CLI-утилита для автоматической очистки проекта от временных и мусорных файлов  
(кеши, артефакты тестов, байткод Python и т.п.).

Инструмент ориентирован на **безопасную очистку**:
- работает только внутри проекта
- поддерживает режим предварительного просмотра (`--dry-run`)
- использует как дефолтные правила, так и пользовательскую конфигурацию

---

## Возможности

- 🧹 удаление стандартных «мусорных» директорий (`__pycache__`, `.pytest_cache`, и др.)
- 📄 удаление временных файлов (`*.pyc`, `.coverage`, и т.п.)
- ⚙️ пользовательский список файлов/папок через `clean.toml`
- 🔒 защита от удаления файлов вне проекта
- 👀 режим предварительного просмотра (`--dry-run`)
- 🖥 CLI-интерфейс

### Безопасность
PonyClean никогда не удаляет:
- venv / .venv
- .git
- .ponyclean

---

## Установка

```bash
pip install pony-clean-cli
```

## Запуск
```bash
pony-clean clean
```

## Примеры
```bash
pony-clean clean
pony-clean clean --root /path/to/project
pony-clean clean --dry-run
```

## Конфигурация

```text
Перед первым использованием рекомендуется инициализировать конфигурацию
```

```bash
pony-clean init  # Создает конфиги
```
### После инициализации будут созданы файлы:
```yaml
.ponyclean/clean.toml      # правила очистки
.ponyclean/protected.toml  # защищённые пути
```

## Формат
```toml
files = [
    "build",
    "dist",
    "some/temp/file.txt"
]
```

## LICENSE
MIT

## VERSION
0.3.2
