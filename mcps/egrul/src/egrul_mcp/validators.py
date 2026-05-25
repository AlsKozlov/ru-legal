"""Локальная валидация ИНН и ОГРН по контрольным цифрам.

Позволяет отсечь невалидные идентификаторы до HTTP-запроса к api-fns.ru,
экономя квоту бесплатного тарифа (800 запросов на всю установку).

Алгоритмы по официальным методическим указаниям ФНС:
  - ИНН ЮЛ (10 цифр): одна контрольная цифра в конце.
  - ИНН ФЛ/ИП (12 цифр): две контрольные цифры в конце.
  - ОГРН ЮЛ (13 цифр): одна контрольная цифра в конце.
  - ОГРНИП (15 цифр): одна контрольная цифра в конце.
"""

from __future__ import annotations

_INN_10_WEIGHTS = [2, 4, 10, 3, 5, 9, 4, 6, 8]
_INN_12_WEIGHTS_FIRST = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
_INN_12_WEIGHTS_SECOND = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]


def _checksum_inn_10(digits: list[int]) -> int:
    total = sum(d * w for d, w in zip(digits[:9], _INN_10_WEIGHTS, strict=True))
    return total % 11 % 10


def _checksum_inn_12_first(digits: list[int]) -> int:
    total = sum(d * w for d, w in zip(digits[:10], _INN_12_WEIGHTS_FIRST, strict=True))
    return total % 11 % 10


def _checksum_inn_12_second(digits: list[int]) -> int:
    total = sum(d * w for d, w in zip(digits[:11], _INN_12_WEIGHTS_SECOND, strict=True))
    return total % 11 % 10


def is_valid_inn(inn: str) -> bool:
    """True если ИНН проходит проверку по контрольным цифрам."""
    if not inn.isdigit():
        return False
    digits = [int(c) for c in inn]
    if len(digits) == 10:
        return _checksum_inn_10(digits) == digits[9]
    if len(digits) == 12:
        return (
            _checksum_inn_12_first(digits) == digits[10]
            and _checksum_inn_12_second(digits) == digits[11]
        )
    return False


def is_valid_ogrn(ogrn: str) -> bool:
    """True если ОГРН/ОГРНИП проходит проверку контрольной цифры.

    ОГРН ЮЛ — 13 цифр: первые 12 % 11 % 10 == последняя.
    ОГРНИП — 15 цифр: первые 14 % 13 % 10 == последняя.
    """
    if not ogrn.isdigit():
        return False
    if len(ogrn) == 13:
        return int(ogrn[:12]) % 11 % 10 == int(ogrn[12])
    if len(ogrn) == 15:
        return int(ogrn[:14]) % 13 % 10 == int(ogrn[14])
    return False


def classify_identifier(value: str) -> str:
    """Возвращает 'inn-ul' | 'inn-fl' | 'ogrn' | 'ogrnip' | 'invalid'."""
    if not value.isdigit():
        return "invalid"
    n = len(value)
    if n == 10 and is_valid_inn(value):
        return "inn-ul"
    if n == 12 and is_valid_inn(value):
        return "inn-fl"
    if n == 13 and is_valid_ogrn(value):
        return "ogrn"
    if n == 15 and is_valid_ogrn(value):
        return "ogrnip"
    return "invalid"
