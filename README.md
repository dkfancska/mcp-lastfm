# lastfm-mcp

MCP-сервер для [Last.fm API](https://www.last.fm/api). Позволяет LLM-агентам получать данные о музыке: профили пользователей, историю прослушиваний, топ-чарты, поиск и метаданные артистов, альбомов и треков.

## Требования

- Python 3.10+
- [API-ключ Last.fm](https://www.last.fm/api/account/create) (бесплатно)

## Установка

```bash
pip install -e .
```

## Настройка

Экспортируйте API-ключ в переменную окружения:

```bash
export LASTFM_API_KEY="your_api_key"
```

### Claude Desktop

Добавьте в `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lastfm": {
      "command": "lastfm-mcp",
      "env": {
        "LASTFM_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add lastfm -- lastfm-mcp
```

Не забудьте установить `LASTFM_API_KEY` в окружении.

## Инструменты

### Пользователь

| Инструмент | Описание |
|---|---|
| `lastfm_get_user_info` | Профиль пользователя: страна, скробблы, дата регистрации |
| `lastfm_get_recent_tracks` | Недавно прослушанные треки (включая текущий) |
| `lastfm_get_user_top_artists` | Топ артистов за период |
| `lastfm_get_user_top_albums` | Топ альбомов за период |
| `lastfm_get_user_top_tracks` | Топ треков за период |
| `lastfm_get_user_loved_tracks` | Избранные треки |

### Поиск

| Инструмент | Описание |
|---|---|
| `lastfm_search_artist` | Поиск артистов по имени |
| `lastfm_search_album` | Поиск альбомов по названию |
| `lastfm_search_track` | Поиск треков по названию |

### Артист

| Инструмент | Описание |
|---|---|
| `lastfm_get_artist_info` | Информация об артисте: био, теги, статистика |
| `lastfm_get_similar_artists` | Похожие артисты |
| `lastfm_get_artist_top_tracks` | Топ треков артиста |
| `lastfm_get_artist_top_albums` | Топ альбомов артиста |

### Альбом

| Инструмент | Описание |
|---|---|
| `lastfm_get_album_info` | Информация об альбоме: треклист, теги, описание |

### Трек

| Инструмент | Описание |
|---|---|
| `lastfm_get_track_info` | Информация о треке: длительность, теги, статистика |
| `lastfm_get_similar_tracks` | Похожие треки |

## Параметры

Инструменты с топ-чартами поддерживают параметр `period`:

| Значение | Период |
|---|---|
| `overall` | За всё время (по умолчанию) |
| `7day` | Неделя |
| `1month` | Месяц |
| `3month` | 3 месяца |
| `6month` | 6 месяцев |
| `12month` | Год |

Все списковые инструменты поддерживают пагинацию через `limit` и `page`.

## Структура проекта

```
src/lastfm_mcp/
├── server.py       # Точка входа, инициализация FastMCP
├── client.py       # HTTP-клиент, обработка ошибок, форматирование
├── models.py       # Pydantic-модели и перечисления
└── tools/
    ├── user.py     # Инструменты для работы с пользователями
    ├── search.py   # Поиск артистов, альбомов, треков
    ├── artist.py   # Информация и топы артистов
    ├── album.py    # Информация об альбомах
    └── track.py    # Информация и похожие треки
```

## Лицензия

MIT
