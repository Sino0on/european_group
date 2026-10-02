import re
from typing import Dict, List, Tuple

TEMPLATE = (
    "Имя: \n"
    "Телефон: \n"
    "Источник: WhatsApp / Instagram / Telegram / Другое\n"
    "Интерес: \n"
    "Страна: \n"
    "Комментарий: "
)

_FIELD_ALIASES = {
    'name': ('имя', 'фио', 'клиент', 'name'),
    'phone': ('телефон', 'тел', 'номер', 'phone'),
    'source': ('источник', 'откуда', 'source'),
    'service': ('интерес', 'услуга', 'запрос'),
    'country': ('страна', 'направление', 'country'),
    'message': ('комментарий', 'коммент', 'примечание', 'comment'),
}

_ALIAS_TO_FIELD = {alias: field for field, aliases in _FIELD_ALIASES.items() for alias in aliases}

_SOURCES = {
    'whatsapp': ('whatsapp', 'вотсап', 'ватсап', 'вацап', 'wa'),
    'instagram': ('instagram', 'инстаграм', 'инста', 'insta', 'ig'),
    'telegram': ('telegram', 'телеграм', 'тг', 'tg'),
}

_LINE_RE = re.compile(r'^\s*([^:\-—–]{1,30}?)\s*[:\-—–]\s*(.*)$')


def _normalize_source(raw: str) -> str:
    low = raw.lower()
    for key, words in _SOURCES.items():
        if any(w in low for w in words):
            return key
    return 'manager'


def parse_lead(text: str) -> Tuple[Dict[str, str], List[str]]:
    """Разбирает сообщение менеджера. Возвращает (данные, список ошибок)."""
    data: Dict[str, str] = {}
    current = None

    for line in text.splitlines():
        m = _LINE_RE.match(line)
        field = _ALIAS_TO_FIELD.get(m.group(1).strip().lower()) if m else None
        if field:
            current = field
            data[field] = m.group(2).strip()
        elif current == 'message' and line.strip():
            data['message'] = (data.get('message', '') + '\n' + line.strip()).strip()

    errors: List[str] = []

    phone = data.get('phone', '')
    digits = re.sub(r'\D', '', phone)
    if len(digits) < 7:
        errors.append('Не указан или некорректен телефон (поле «Телефон»).')
    else:
        data['phone'] = ('+' if phone.strip().startswith('+') else '') + digits

    if not data.get('name'):
        errors.append('Не указано имя (поле «Имя»).')

    data['source'] = _normalize_source(data.get('source', ''))
    return data, errors
