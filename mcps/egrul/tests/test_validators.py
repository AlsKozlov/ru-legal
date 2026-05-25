"""Юнит-тесты для локальной валидации ИНН/ОГРН.

Эталонные значения проверены через калькуляторы ФНС.
"""

from __future__ import annotations

import pytest

from egrul_mcp.validators import (
    classify_identifier,
    is_valid_inn,
    is_valid_ogrn,
)


class TestINN10:
    """ИНН юридического лица — 10 цифр."""

    def test_valid_inn_10(self) -> None:
        # ИНН Сбербанка — известный публичный ИНН
        assert is_valid_inn("7707083893") is True

    def test_invalid_check_digit(self) -> None:
        # Сменили последнюю цифру
        assert is_valid_inn("7707083894") is False

    def test_wrong_length(self) -> None:
        assert is_valid_inn("770708389") is False
        assert is_valid_inn("77070838930") is False

    def test_non_digit(self) -> None:
        assert is_valid_inn("770708389A") is False
        assert is_valid_inn("") is False


class TestINN12:
    """ИНН физлица / ИП — 12 цифр."""

    def test_valid_inn_12(self) -> None:
        # Сгенерированный валидный ИНН ФЛ (проверено через калькулятор)
        assert is_valid_inn("500100732259") is True

    def test_invalid_check_digit(self) -> None:
        assert is_valid_inn("500100732258") is False


class TestOGRN:
    """ОГРН — 13 цифр."""

    def test_valid_ogrn(self) -> None:
        # ОГРН Сбербанка
        assert is_valid_ogrn("1027700132195") is True

    def test_invalid_check_digit(self) -> None:
        assert is_valid_ogrn("1027700132196") is False

    def test_wrong_length(self) -> None:
        assert is_valid_ogrn("102770013219") is False
        assert is_valid_ogrn("10277001321951") is False


class TestOGRNIP:
    """ОГРНИП — 15 цифр."""

    def test_valid_ogrnip(self) -> None:
        # Сгенерированный валидный ОГРНИП
        assert is_valid_ogrn("304500116000157") is True

    def test_invalid(self) -> None:
        assert is_valid_ogrn("304500116000158") is False


class TestClassify:
    """classify_identifier — детектор типа идентификатора."""

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("7707083893", "inn-ul"),
            ("500100732259", "inn-fl"),
            ("1027700132195", "ogrn"),
            ("304500116000157", "ogrnip"),
            ("7707083894", "invalid"),
            ("abc", "invalid"),
            ("", "invalid"),
            ("12345", "invalid"),
        ],
    )
    def test_classify(self, value: str, expected: str) -> None:
        assert classify_identifier(value) == expected
