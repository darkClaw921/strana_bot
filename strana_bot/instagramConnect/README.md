# Instagram Business API Connector

Этот проект представляет собой коннектор к Instagram Business API, который позволяет получать и отвечать на сообщения пользователей.

## Требования

- Python 3.12+
- Poetry
- Доступ к Instagram Business API
- Настроенная Facebook Business страница
- SSL сертификат для webhook (для production)

## Получение необходимых токенов и ID

### 1. Создание Facebook App
1. Перейдите на [Facebook Developers](https://developers.facebook.com/)
2. Создайте новое приложение, выберите тип "Business"
3. В настройках приложения добавьте продукт "Instagram Messaging"

### 2. Получение INSTAGRAM_PAGE_ID
1. Перейдите в [Facebook Business Manager](https://business.facebook.com/)
2. Выберите вашу Instagram Business страницу
3. ID страницы будет в URL или в настройках страницы
4. Убедитесь, что страница подключена к вашему Facebook App

### 3. Получение INSTAGRAM_ACCESS_TOKEN
1. Перейдите в [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Выберите ваше приложение
3. Выберите ваш Instagram Business аккаунт
4. Запросите следующие разрешения:
   - instagram_basic
   - instagram_manage_messages
   - pages_messaging
5. Нажмите "Generate Access Token"
6. Для получения долгосрочного токена используйте [Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)

### 4. Настройка Webhook
1. В настройках вашего Facebook App перейдите в раздел Webhooks
2. Добавьте URL вашего сервера: `https://ваш_домен/webhook`
3. Укажите Verify Token (любая строка, которую вы укажете в WEBHOOK_VERIFY_TOKEN)
4. Подпишитесь на следующие события:
   - messages
   - messaging_postbacks
   - messaging_optins

## Настройка

1. Установите Poetry, если еще не установлен:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости проекта:
```bash
poetry install
```

3. Создайте файл `.env` в корневой директории проекта со следующими переменными:
```
INSTAGRAM_ACCESS_TOKEN=полученный_токен_доступа
INSTAGRAM_PAGE_ID=id_вашей_страницы
WEBHOOK_VERIFY_TOKEN=любая_строка_для_верификации
```

4. Настройте webhook в Facebook Developer Console:
   - URL: https://ваш_домен/webhook
   - Verify Token: тот же, что указан в WEBHOOK_VERIFY_TOKEN

## Запуск

```bash
poetry run python instagram_connector.py
```

или

```bash
poetry run uvicorn instagram_connector:app --host 0.0.0.0 --port 5009 --reload
```

## API Endpoints

- GET /webhook - Endpoint для верификации webhook
- POST /webhook - Endpoint для получения сообщений от Instagram

## Документация API

После запуска сервера, документация доступна по адресам:
- http://localhost:5009/docs - Swagger UI
- http://localhost:5009/redoc - ReDoc

## Важные примечания

1. Для production использования необходимо:
   - Настроить SSL сертификат (Instagram требует HTTPS)
   - Использовать долгосрочный access token
   - Настроить автоматическое обновление токена
   - Добавить обработку ошибок и retry-механизмы

2. Токены доступа имеют ограниченный срок действия:
   - Короткий токен действует 1 час
   - Долгосрочный токен действует 60 дней
   - Рекомендуется настроить автоматическое обновление токена
