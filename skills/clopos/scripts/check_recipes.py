#!/usr/bin/env python3
"""Audit a normalized recipe snapshot locally; never edit files or contact Clopos."""
import argparse
import json
import re
from decimal import Decimal, localcontext
from pathlib import Path

NUMBER = re.compile(r'\d{1,18}(?:\.\d{1,6})?', re.ASCII)
UNITS = {'kg': ('mass', Decimal('1000')), 'g': ('mass', Decimal('1')),
         'l': ('volume', Decimal('1000')), 'ml': ('volume', Decimal('1')),
         'pcs': ('count', Decimal('1'))}
RECIPE_TYPES = {'DISH', 'PREPARATION'}
CARD_TYPES = RECIPE_TYPES | {'GOODS', 'INGREDIENT'}


class InputError(ValueError):
    pass


def fields(value, keys, path):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise InputError(f'{path}: tələb olunan sahələr: {", ".join(keys)}')


def label(value, path):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise InputError(f'{path}: kənar boşluqsuz, boş olmayan mətn tələb olunur')
    return value


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InputError(f'Təkrarlanan JSON sahəsi: {key}')
        result[key] = value
    return result


def check_recipes(data):
    """Check explicit IDs, quantities, dimensions and graph cycles, without costing."""
    fields(data, ['currency', 'cards'], '$')
    if data['currency'] != 'AZN':
        raise InputError('currency: yalnız AZN dəstəklənir')
    if not isinstance(data['cards'], list) or not data['cards']:
        raise InputError('cards: ən azı bir kart tələb olunur')
    issues, cards, counts, lines = [], {}, {}, []

    def issue(path, code, message, **detail):
        issues.append({'path': path, 'code': code, 'message': message, **detail})

    def number(value, path):
        if value is None:
            issue(path, 'missing_value', 'Mənbədən dəqiqləşdirilməlidir; sıfır qəbul edilmir')
            return None
        if not isinstance(value, str) or not NUMBER.fullmatch(value):
            raise InputError(f'{path}: mənfi olmayan onluq mətn tələb olunur; məsələn "0.025"')
        return Decimal(value)

    def unit(value, path):
        value = label(value, path)
        if value not in UNITS:
            issue(path, 'unsupported_unit', 'Vahid təsdiqlə normallaşdırılmalıdır; çevrilmə fərz edilmir')
        return value

    # Validate every row before building a graph, including duplicate IDs.
    for i, card in enumerate(data['cards']):
        path = f'cards[{i}]'
        fields(card, ['id', 'type', 'unit', 'output_quantity', 'reported_unit_cost', 'contents'], path)
        card_id = label(card['id'], path + '.id')
        kind = label(card['type'], path + '.type')
        if kind not in CARD_TYPES:
            raise InputError(f'{path}.type: GOODS, INGREDIENT, DISH və ya PREPARATION tələb olunur')
        unit(card['unit'], path + '.unit')
        if not isinstance(card['contents'], list):
            raise InputError(f'{path}.contents: siyahı tələb olunur')
        if kind in RECIPE_TYPES:
            output = number(card['output_quantity'], path + '.output_quantity')
            if output == 0:
                issue(path + '.output_quantity', 'zero_output', 'Reseptin çıxışı sıfırdır')
            if not card['contents']:
                issue(path + '.contents', 'empty_recipe', 'Resept kartının tərkibi boşdur')
        elif card['output_quantity'] is not None or card['contents']:
            raise InputError(f'{path}: GOODS/INGREDIENT üçün output_quantity=null və contents=[] olmalıdır')
        cost = number(card['reported_unit_cost'], path + '.reported_unit_cost')
        if cost == 0:
            issue(path + '.reported_unit_cost', 'zero_reported_cost', 'Bildirilmiş maya sıfırdır; səbəbi ayrıca araşdırılmalıdır')
        used = set()
        for j, row in enumerate(card['contents']):
            row_path = f'{path}.contents[{j}]'
            fields(row, ['component_id', 'gross_quantity', 'unit'], row_path)
            component = label(row['component_id'], row_path + '.component_id')
            quantity = number(row['gross_quantity'], row_path + '.gross_quantity')
            unit(row['unit'], row_path + '.unit')
            if quantity == 0:
                issue(row_path + '.gross_quantity', 'zero_quantity', 'Tərkib miqdarı sıfırdır')
            if component in used:
                issue(row_path, 'duplicate_component', 'Eyni komponent təkrarlanır; avtomatik birləşdirilmir')
            used.add(component)
            lines.append((card_id, component, quantity, row['unit'], row_path))
        counts[card_id] = counts.get(card_id, 0) + 1
        cards[card_id] = card
        if counts[card_id] > 1:
            issue(path + '.id', 'duplicate_card_id', 'Eyni ID təkrarlanır; bu ID üzrə əlaqələr həll edilmir')

    graph = {key: [] for key in cards if counts[key] == 1}
    normalized = []
    with localcontext() as ctx:
        ctx.prec = 64
        for owner, component, quantity, row_unit, path in lines:
            result = {'path': path, 'card_id': owner, 'component_id': component,
                      'stock_unit': None, 'gross_in_stock_unit': None}
            normalized.append(result)
            if component not in cards:
                issue(path, 'missing_component', 'Komponent kartı snapshot-da yoxdur; silinmiş olduğu nəticəsi çıxarılmır')
                continue
            if counts[component] > 1 or counts[owner] > 1:
                issue(path, 'ambiguous_reference', 'Təkrarlanan kart ID-si səbəbindən əlaqə qeyri-müəyyəndir')
                continue
            graph[owner].append((component, path))
            stock_unit = cards[component]['unit']
            result['stock_unit'] = stock_unit
            if row_unit not in UNITS or stock_unit not in UNITS:
                continue
            source, target = UNITS[row_unit], UNITS[stock_unit]
            if source[0] != target[0]:
                issue(path, 'unit_dimension_mismatch', 'Kütlə, həcm və ədəd arasında çəki/sıxlıq fərz edilmir')
            elif quantity is not None:
                result['gross_in_stock_unit'] = format(quantity * source[1] / target[1], 'f')

    # Iterative DFS also handles long preparation chains without recursion limits.
    color = {}
    for start in graph:
        if color.get(start):
            continue
        color[start] = 1
        active, positions = [start], {start: 0}
        stack = [(start, iter(graph[start]))]
        while stack:
            owner, edges = stack[-1]
            edge = next(edges, None)
            if edge is None:
                color[owner] = 2
                stack.pop()
                active.pop()
                positions.pop(owner)
                continue
            component, path = edge
            if color.get(component) == 1:
                issue(path, 'recipe_cycle', 'Tərkib zənciri özünə qayıdır',
                      card_ids=active[positions[component]:] + [component])
            elif not color.get(component):
                color[component] = 1
                positions[component] = len(active)
                active.append(component)
                stack.append((component, iter(graph[component])))

    return {'status': 'review_required' if issues else 'no_issues_found',
            'checked_cards': len(data['cards']), 'checked_lines': len(lines),
            'normalized_lines': normalized, 'issues': issues,
            'scope': 'Yalnız verilmiş snapshot; maya hesablanmır, canlı kartlar, silinmə rejimi və qalıq yoxlanmır'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Normalized JSON snapshot; original file is never changed')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'), object_pairs_hook=unique_keys)
        result = check_recipes(data)
        exit_code = 0 if result['status'] == 'no_issues_found' else 1
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {'status': 'invalid_input', 'error': str(exc)}
        exit_code = 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
