import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional
import requests
from decouple import config

logger = logging.getLogger(__name__)

# Путь для сохранения OAuth токенов при автоматическом обновлении
_BASE_DIR = Path(__file__).resolve().parent.parent
_TOKEN_FILE = _BASE_DIR / 'amocrm_tokens.json'

# Человекочитаемые названия источников заявок
_SOURCE_LABELS = {
    'consultation': '📋 Консультация (главная)',
    'jobs': '💼 Трудоустройство',
    'study': '🎓 Образование за рубежом',
    'visa': '🛂 Визовая поддержка',
    'tour': '✈️ Подбор тура',
    'lang': '🗣 Языковые курсы',
    'law': '⚖️ Юридическая консультация',
    'company': '🏢 Регистрация компании',
    'modal': '💬 Быстрая консультация (модал)',
    'whatsapp': '🟢 WhatsApp (менеджер)',
    'instagram': '📸 Instagram (менеджер)',
    'telegram': '✈️ Telegram (менеджер)',
    'manager': '👤 Менеджер (другое)',
}

# Человекочитаемые названия полей для примечания к сделке
_FIELD_LABELS = {
    'name': 'Имя',
    'phone': 'Телефон',
    'whatsapp': 'WhatsApp',
    'country': 'Страна',
    'role': 'Вакансия',
    'destination': 'Направление',
    'budget': 'Бюджет',
    'course': 'Курс',
    'service': 'Услуга',
    'program': 'Программа',
    'company_type': 'Тип компании',
    'experience': 'Опыт',
    'message': 'Комментарий',
    'manager': 'Менеджер',
}


def _get_subdomain() -> str:
    """Извлекает чистый поддомен amoCRM (например, 'company' из 'company.amocrm.ru')."""
    raw = config('AMO_SUBDOMAIN', default='').strip()
    if not raw:
        return ''
    cleaned = raw.replace('https://', '').replace('http://', '').split('/')[0]
    return cleaned.split('.')[0].strip()


def _get_base_url() -> str:
    subdomain = _get_subdomain()
    return f"https://{subdomain}.amocrm.ru" if subdomain else ''


def _load_stored_tokens() -> Dict[str, Any]:
    """Загружает сохраненные токены из amocrm_tokens.json."""
    if not _TOKEN_FILE.exists():
        return {}
    try:
        with open(_TOKEN_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning("Failed to read %s: %s", _TOKEN_FILE, e)
        return {}


def _save_stored_tokens(tokens: Dict[str, Any]) -> None:
    """Сохраняет токены в amocrm_tokens.json."""
    try:
        with open(_TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Failed to save %s: %s", _TOKEN_FILE, e)


def _exchange_code(auth_code: str, base_url: str) -> Optional[str]:
    """Обменивает разовый auth_code на access_token и refresh_token."""
    client_id = config('AMO_CLIENT_ID', default='').strip()
    client_secret = config('AMO_CLIENT_SECRET', default='').strip()
    redirect_uri = config('AMO_REDIRECT_URI', default='').strip()

    if not client_id or not client_secret or not auth_code:
        return None

    url = f"{base_url}/oauth2/access_token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            tokens = {
                'access_token': data['access_token'],
                'refresh_token': data['refresh_token'],
                'expires_at': int(time.time()) + int(data.get('expires_in', 86400)),
            }
            _save_stored_tokens(tokens)
            logger.info("amoCRM auth code exchanged successfully for tokens.")
            return tokens['access_token']
        logger.error("amoCRM code exchange failed (%s): %s", resp.status_code, resp.text)
    except Exception as e:
        logger.error("amoCRM code exchange exception: %s", e)
    return None


def _refresh_access_token(base_url: str, refresh_token: str) -> Optional[str]:
    """Обновляет access_token по refresh_token."""
    client_id = config('AMO_CLIENT_ID', default='').strip()
    client_secret = config('AMO_CLIENT_SECRET', default='').strip()
    redirect_uri = config('AMO_REDIRECT_URI', default='').strip()

    if not client_id or not client_secret or not refresh_token:
        return None

    url = f"{base_url}/oauth2/access_token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': redirect_uri,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            tokens = {
                'access_token': data['access_token'],
                'refresh_token': data['refresh_token'],
                'expires_at': int(time.time()) + int(data.get('expires_in', 86400)),
            }
            _save_stored_tokens(tokens)
            logger.info("amoCRM token refreshed successfully.")
            return tokens['access_token']
        logger.error("amoCRM token refresh failed (%s): %s", resp.status_code, resp.text)
    except Exception as e:
        logger.error("amoCRM token refresh exception: %s", e)
    return None


def get_access_token(force_refresh: bool = False) -> Optional[str]:
    """
    Возвращает актуальный access_token:
    1. Если в .env указан постоянный/долгосрочный AMO_ACCESS_TOKEN — использует его.
    2. Если настроен OAuth (AMO_CLIENT_ID и др.) — проверяет кэш amocrm_tokens.json,
       при необходимости обновляет по refresh_token или обменивает auth_code.
    """
    base_url = _get_base_url()
    if not base_url:
        return None

    client_id = config('AMO_CLIENT_ID', default='').strip()
    direct_token = config('AMO_ACCESS_TOKEN', default='').strip()

    # 1. OAuth 2.0 flow
    if client_id:
        stored = _load_stored_tokens()
        current_time = time.time()

        # Если токен сохранен и еще не истек (с запасом 5 минут)
        if not force_refresh and stored.get('access_token'):
            if stored.get('expires_at', 0) > current_time + 300:
                return stored['access_token']

        # Токен истек или запрошено принудительное обновление — пробуем refresh
        refresh_token = stored.get('refresh_token') or config('AMO_REFRESH_TOKEN', default='').strip()
        if refresh_token:
            new_token = _refresh_access_token(base_url, refresh_token)
            if new_token:
                return new_token

        # Если токенов в файле нет, пробуем начальный auth_code из .env
        auth_code = config('AMO_AUTH_CODE', default='').strip()
        if auth_code:
            new_token = _exchange_code(auth_code, base_url)
            if new_token:
                return new_token

    # 2. Прямой токен доступа
    if direct_token:
        return direct_token

    return None


def _add_lead_note(base_url: str, headers: dict, lead_id: int, data: dict, site_name: str, source_label: str) -> None:
    """Добавляет подробное примечание к созданной сделке со всеми полями формы."""
    lines = [
        f"📩 Заявка с сайта: {site_name}",
        f"Источник: {source_label}",
        ""
    ]

    for key, label in _FIELD_LABELS.items():
        val = str(data.get(key) or '').strip()
        if val:
            lines.append(f"{label}: {val}")

    known = set(_FIELD_LABELS) | {'source'}
    for key, val in data.items():
        if key not in known and val and str(val).strip():
            lines.append(f"{key}: {val}")

    note_text = "\n".join(lines)
    notes_url = f"{base_url}/api/v4/leads/{lead_id}/notes"
    note_payload = [
        {
            "note_type": "common",
            "params": {
                "text": note_text
            }
        }
    ]

    try:
        resp = requests.post(notes_url, json=note_payload, headers=headers, timeout=10)
        if resp.status_code in (200, 201):
            logger.info("amoCRM note added to lead %s", lead_id)
        else:
            logger.warning("amoCRM add note status (%s): %s", resp.status_code, resp.text)
    except Exception as e:
        logger.warning("Failed to add note to amoCRM lead %s: %s", lead_id, e)


def send_amocrm(data: dict, is_new_site: bool = False) -> bool:
    """
    Отправляет заявку в amoCRM:
    1. Создает сделку и контакт через /api/v4/leads/complex.
    2. Добавляет примечание со всеми деталями через /api/v4/leads/{id}/notes.
    """
    base_url = _get_base_url()
    if not base_url:
        logger.warning("amoCRM is not configured: AMO_SUBDOMAIN is empty")
        return False

    token = get_access_token()
    if not token:
        logger.warning("amoCRM access token is missing or not configured")
        return False

    source = data.get('source', 'unknown')
    source_label = _SOURCE_LABELS.get(source, f'Заявка ({source})')
    site_name = 'Mamralieva Consulting' if is_new_site else 'European Group'

    client_name = (data.get('name') or data.get('full_name') or '').strip()
    if not client_name:
        client_name = f'Заявка с сайта ({source_label})'

    phone = (data.get('phone') or data.get('tel') or '').strip()
    whatsapp = (data.get('whatsapp') or '').strip()
    email = (data.get('email') or '').strip()

    # 1. Формируем контакт
    contact_custom_fields = []
    if phone:
        contact_custom_fields.append({
            'field_code': 'PHONE',
            'values': [{'value': phone, 'enum_code': 'WORK'}]
        })
    if whatsapp and whatsapp != phone:
        contact_custom_fields.append({
            'field_code': 'PHONE',
            'values': [{'value': whatsapp, 'enum_code': 'MOB'}]
        })
    if email:
        contact_custom_fields.append({
            'field_code': 'EMAIL',
            'values': [{'value': email, 'enum_code': 'WORK'}]
        })

    contact_data = {'name': client_name}
    if contact_custom_fields:
        contact_data['custom_fields_values'] = contact_custom_fields

    # 2. Теги сделки
    tags = [
        {'name': 'Сайт'},
        {'name': site_name},
    ]
    if source and source != 'unknown':
        tags.append({'name': source})

    lead_title = f"[{site_name}] {source_label}: {client_name}"

    lead_item = {
        'name': lead_title,
        '_embedded': {
            'tags': tags,
            'contacts': [contact_data],
        }
    }

    # Опциональная воронка и этап
    pipeline_id = config('AMO_PIPELINE_ID', default='').strip()
    status_id = config('AMO_STATUS_ID', default='').strip()
    if pipeline_id.isdigit():
        lead_item['pipeline_id'] = int(pipeline_id)
    if status_id.isdigit():
        lead_item['status_id'] = int(status_id)

    payload = [lead_item]

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'EuropeanGroup/1.0',
    }

    complex_url = f"{base_url}/api/v4/leads/complex"

    try:
        resp = requests.post(complex_url, json=payload, headers=headers, timeout=10)

        # При ошибке 401 пробуем обновить токен один раз
        if resp.status_code == 401:
            logger.info("amoCRM 401 Unauthorized, attempting to refresh token...")
            new_token = get_access_token(force_refresh=True)
            if new_token:
                headers['Authorization'] = f'Bearer {new_token}'
                resp = requests.post(complex_url, json=payload, headers=headers, timeout=10)

        if resp.status_code not in (200, 201):
            logger.error("amoCRM create lead error (%s): %s", resp.status_code, resp.text)
            return False

        resp_json = resp.json()
        lead_id = None
        if isinstance(resp_json, list) and len(resp_json) > 0:
            lead_id = resp_json[0].get('id')

        logger.info("amoCRM lead created successfully with ID: %s", lead_id)

        # Добавляем примечание со всеми деталями
        if lead_id:
            _add_lead_note(base_url, headers, lead_id, data, site_name, source_label)

        return True

    except Exception as e:
        logger.error("amoCRM request exception: %s", e)
        return False
