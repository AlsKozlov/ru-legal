# Constants Registry — Single Source of Truth

> Все hardcoded values (госпошлины, штрафы, ставки, лимиты) живут здесь.
> Skills **НЕ должны хардкодить** эти числа — должны ссылаться сюда.

## Зачем

До constants-registry: каждый skill хардкодил значения типа "штраф 18 млн ₽" / "МРОТ 19 242 ₽". При изменении законодательства приходилось править 50+ skills. Часто пропускали → outdated данные → ошибки юристов.

После constants-registry: одно изменение в `2026.yaml` → 50 skills автоматически синхронизированы. Update раз в месяц (после изменений законодательства).

## Структура

```
constants/
├── README.md              # этот файл
├── 2026.yaml              # текущий год (актуальные значения)
├── 2025.yaml              # прошлый год (для аудита истории)
├── 2024.yaml              # ...
└── changelog.md           # что изменилось когда
```

## Использование в skills

### Вариант A: Через `pravo-mcp` (рекомендуется)

```markdown
Через `pravo.get_constant("data_protection.fine_legal_max", year=2026)`
получи актуальный размер штрафа.
```

Tool возвращает:
```json
{
  "value": 18000000,
  "unit": "RUB",
  "source": "ст.13.11 КоАП РФ (обновление 30.05.2025)",
  "source_date": "2025-05-30"
}
```

### Вариант B: Прямой read файла (для testing)

```python
import yaml
with open("references/constants/2026.yaml") as f:
    constants = yaml.safe_load(f)
fine_max = constants["data_protection"]["fine_legal_max"]["value"]
```

## Обновление

### Месячный update (планово)

Каждое 1-е число месяца:
1. Проверить изменения законодательства за месяц (Минюст, ФНС, ЦБ)
2. Обновить values в `{current_year}.yaml`
3. Записать в `changelog.md` что изменилось
4. Запустить regression test (gold dataset на skills использующих эти константы)
5. Commit + PR

### Real-time update (срочно)

Если законодательство изменилось вне graceful update:
1. Создать issue с label `constants-update-urgent`
2. PR в течение 24 часов
3. Уведомить в TG канале (если значимое изменение)

## Структура entry

```yaml
domain:
  constant_name:
    value: 12345          # actual value
    unit: "RUB"           # единица (RUB, percent, days, etc.)
    source: "ст.X ФЗ"     # на каком НПА основано
    source_date: "YYYY-MM-DD"  # дата нормативного источника
    note: "..."           # опц. — контекст применения
    threshold:            # опц. — если применяется до/после порога
      value: ...
      unit: ...
    formula: "tiered"     # опц. — если значение зависит от другого параметра
    tiers: [...]          # опц. — раскладка тиров
```

## История

См. [changelog.md](changelog.md) — что менялось.
