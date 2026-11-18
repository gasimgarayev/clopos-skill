#!/usr/bin/env python3
"""Check normalized AZN purchase arithmetic locally; never write to Clopos."""
import argparse
import json
import re
from decimal import Decimal, ROUND_HALF_UP, localcontext
from pathlib import Path

CENT = Decimal('0.01')
NUMBER = re.compile(r'-?\d{1,18}(?:\.\d{1,6})?', re.ASCII)


class InputError(ValueError):
    pass


def fields(value, required, path):
    if not isinstance(value, dict) or set(value) != set(required):
        raise InputError(f'{path}: tələb olunan sahələr: {", ".join(required)}')


def label(value, path):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f'{path}: boş olmayan mətn tələb olunur')
    return value


def money(value):
    return format(value.quantize(CENT, rounding=ROUND_HALF_UP), '.2f')


def check_purchase(data):
    """Values are decimal strings or explicit nulls. No implicit unit conversion."""
    fields(data, ['currency', 'rounding', 'invoice_total', 'lines', 'adjustments'], '$')
    if data['currency'] != 'AZN' or data['rounding'] != 'half_up_2dp':
        raise InputError('Yalnız currency=AZN və açıq rounding=half_up_2dp dəstəklənir')
    if not isinstance(data['lines'], list) or not data['lines']:
        raise InputError('lines: ən azı bir sətir tələb olunur')
    if not isinstance(data['adjustments'], list):
        raise InputError('adjustments: siyahı tələb olunur; əlavə məbləğ yoxdursa [] yazın')
    issues, results, totals, adjustment_values = [], [], [], []
    seen = set()

    def issue(path, code, message):
        issues.append({'path': path, 'code': code, 'message': message})

    def number(value, path, signed=False):
        if value is None:
            issue(path, 'missing_value', 'Mənbədə dəqiqləşdirilməlidir; sıfır qəbul edilmir')
            return None
        if not isinstance(value, str) or not NUMBER.fullmatch(value):
            raise InputError(f'{path}: nöqtə ilə yazılmış onluq mətn tələb olunur; məsələn "2.50"')
        parsed = Decimal(value)
        if not signed and parsed < 0:
            raise InputError(f'{path}: mənfi məbləğ/miqdar dəstəklənmir')
        return parsed

    with localcontext() as ctx:
        ctx.prec = 64
        invoice_total = number(data['invoice_total'], 'invoice_total')
        for i, row in enumerate(data['lines']):
            path = f'lines[{i}]'
            fields(row, ['id', 'quantity', 'unit', 'unit_price', 'price_unit',
                         'discount_amount', 'tax_amount', 'line_total'], path)
            row_id = label(row['id'], path + '.id')
            if row_id in seen:
                issue(path + '.id', 'duplicate_line_id', 'Eyni sətir identifikatoru təkrarlanır')
            seen.add(row_id)
            unit = label(row['unit'], path + '.unit')
            price_unit = label(row['price_unit'], path + '.price_unit')
            same_unit = unit == price_unit
            if not same_unit:
                issue(path, 'unit_mismatch', 'Miqdar və qiymət fərqli vahidlərdədir; çevrilmə fərz edilmir')
            q, p, discount, tax, total = [number(row[k], path + '.' + k) for k in
                                        ['quantity', 'unit_price', 'discount_amount', 'tax_amount', 'line_total']]
            # Printed AZN totals must be actual cent amounts, not silently rounded inputs.
            for key, value in [('discount_amount', discount), ('tax_amount', tax), ('line_total', total)]:
                if value is not None and value != value.quantize(CENT):
                    raise InputError(f'{path}.{key}: məbləğ qəpik dəqiqliyində olmalıdır')
            if q == 0:
                issue(path + '.quantity', 'zero_quantity', 'Sıfır miqdarlı alış sətri yoxlanmalıdır')
            expected = None
            if same_unit and all(x is not None for x in (q, p, discount, tax)):
                expected = (q * p - discount + tax).quantize(CENT, rounding=ROUND_HALF_UP)
                if expected < 0:
                    issue(path, 'negative_expected_total', 'Endirim və vergi məbləğləri sətri mənfiyə salır')
                if total is not None and expected != total:
                    issue(path + '.line_total', 'line_total_mismatch', 'Sətir cəmi hesablamaya uyğun deyil')
            totals.append(total)
            results.append({'id': row_id, 'expected_total': money(expected) if expected is not None else None,
                            'declared_total': money(total) if total is not None else None})
        for i, item in enumerate(data['adjustments']):
            path = f'adjustments[{i}]'
            fields(item, ['label', 'amount'], path)
            label(item['label'], path + '.label')
            amount = number(item['amount'], path + '.amount', signed=True)
            if amount is not None and amount != amount.quantize(CENT):
                raise InputError(f'{path}.amount: məbləğ qəpik dəqiqliyində olmalıdır')
            adjustment_values.append(amount)
        if invoice_total is not None and invoice_total != invoice_total.quantize(CENT):
            raise InputError('invoice_total: məbləğ qəpik dəqiqliyində olmalıdır')
        summed = None
        delta = None
        if all(x is not None for x in totals + adjustment_values):
            summed = sum(totals + adjustment_values, Decimal('0'))
            if invoice_total is not None:
                delta = summed - invoice_total
                if delta:
                    issue('invoice_total', 'invoice_total_mismatch', 'Yazılmış sətir cəmləri və əlavələr qaimə cəminə uyğun deyil')
        return {'status': 'review_required' if issues else 'arithmetic_match', 'currency': 'AZN',
                'lines': results, 'sum_of_declared_lines_and_adjustments': money(summed) if summed is not None else None,
                'invoice_total': money(invoice_total) if invoice_total is not None else None,
                'difference': money(delta) if delta is not None else None, 'issues': issues,
                'scope': 'Yalnız hesab uyğunluğu; məhsul uyğunluğu, ödəniş və canlı status yoxlanmayıb'}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f'Təkrarlanan JSON sahəsi: {key}')
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Normalized JSON input; original file is never changed')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        result = check_purchase(data)
        exit_code = 0 if result['status'] == 'arithmetic_match' else 1
    except (InputError, OSError, json.JSONDecodeError) as exc:
        result = {'status': 'invalid_input', 'error': str(exc)}
        exit_code = 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
