"""Offline recipe snapshot checks; all records are synthetic."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / 'skills/clopos/scripts/check_recipes.py'
sys.path.insert(0, str(CHECKER.parent))
from check_recipes import InputError, check_recipes


class RecipeTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/recipes.json').read_text(encoding='utf-8'))

    def codes(self):
        return {x['code'] for x in check_recipes(self.data)['issues']}

    def test_nested_recipe_and_exact_metric_conversion(self):
        result = check_recipes(self.data)
        self.assertEqual(result['status'], 'no_issues_found')
        self.assertEqual(result['checked_cards'], 4)
        self.assertEqual([x['gross_in_stock_unit'] for x in result['normalized_lines']], ['1', '0.5', '0.3'])

    def test_conversion_both_directions_and_small_quantities(self):
        self.data['cards'][0]['unit'] = 'g'
        self.data['cards'][2]['contents'][0].update(gross_quantity='0.000001', unit='kg')
        result = check_recipes(self.data)
        self.assertEqual(result['normalized_lines'][0]['gross_in_stock_unit'], '0.001000')

    def test_no_density_or_piece_weight_is_assumed(self):
        for unit in ['l', 'pcs']:
            with self.subTest(unit=unit):
                self.data['cards'][2]['contents'][0]['unit'] = unit
                result = check_recipes(self.data)
                self.assertIn('unit_dimension_mismatch', {x['code'] for x in result['issues']})
                self.assertIsNone(result['normalized_lines'][0]['gross_in_stock_unit'])

    def test_unknown_units_are_not_guessed(self):
        self.data['cards'][2]['contents'][0]['unit'] = 'box'
        self.assertIn('unsupported_unit', self.codes())
        self.assertIsNone(check_recipes(self.data)['normalized_lines'][0]['gross_in_stock_unit'])

    def test_missing_quantity_is_not_zero(self):
        self.data['cards'][2]['contents'][0]['gross_quantity'] = None
        self.assertIn('missing_value', self.codes())
        self.assertNotIn('zero_quantity', self.codes())
        self.assertIsNone(check_recipes(self.data)['normalized_lines'][0]['gross_in_stock_unit'])

    def test_zero_output_and_zero_gross(self):
        self.data['cards'][2]['output_quantity'] = '0'
        self.data['cards'][2]['contents'][0]['gross_quantity'] = '0'
        self.assertTrue({'zero_output', 'zero_quantity'} <= self.codes())

    def test_empty_recipe_is_flagged(self):
        self.data['cards'][2]['contents'] = []
        self.assertIn('empty_recipe', self.codes())

    def test_zero_cost_is_flagged_without_inventing_a_cost(self):
        self.data['cards'][0]['reported_unit_cost'] = '0'
        self.assertIn('zero_reported_cost', self.codes())
        self.assertEqual(self.data['cards'][0]['reported_unit_cost'], '0')

    def test_missing_output_and_reported_cost(self):
        self.data['cards'][2].update(output_quantity=None, reported_unit_cost=None)
        issues = check_recipes(self.data)['issues']
        self.assertEqual(sum(x['code'] == 'missing_value' for x in issues), 2)

    def test_reference_outside_snapshot_is_flagged(self):
        self.data['cards'][2]['contents'][0]['component_id'] = 'not-in-snapshot'
        self.assertIn('missing_component', self.codes())

    def test_duplicate_card_does_not_select_a_winner(self):
        duplicate = copy.deepcopy(self.data['cards'][0])
        duplicate['unit'] = 'pcs'
        self.data['cards'].append(duplicate)
        result = check_recipes(self.data)
        self.assertTrue({'duplicate_card_id', 'ambiguous_reference'} <= {x['code'] for x in result['issues']})
        self.assertIsNone(result['normalized_lines'][0]['gross_in_stock_unit'])

    def test_duplicate_component_is_not_merged(self):
        rows = self.data['cards'][2]['contents']
        rows.append(copy.deepcopy(rows[0]))
        self.assertIn('duplicate_component', self.codes())
        self.assertEqual(check_recipes(self.data)['checked_lines'], 4)

    def test_self_reference_cycle(self):
        self.data['cards'][2]['contents'][0]['component_id'] = 'demo-dough'
        cycles = [x['card_ids'] for x in check_recipes(self.data)['issues'] if x['code'] == 'recipe_cycle']
        self.assertEqual(cycles, [['demo-dough', 'demo-dough']])

    def test_two_card_cycle(self):
        self.data['cards'][2]['contents'][0].update(component_id='demo-bread', unit='pcs')
        cycles = [x['card_ids'] for x in check_recipes(self.data)['issues'] if x['code'] == 'recipe_cycle']
        self.assertEqual(cycles, [['demo-dough', 'demo-bread', 'demo-dough']])

    def test_shared_subrecipe_is_not_a_cycle(self):
        self.data['cards'][3]['contents'].append({'component_id': 'demo-flour', 'gross_quantity': '10', 'unit': 'g'})
        self.assertEqual(check_recipes(self.data)['status'], 'no_issues_found')

    def test_long_chain_has_no_recursion_limit(self):
        cards = [{'id': str(i), 'type': 'PREPARATION', 'unit': 'kg', 'output_quantity': '1',
                  'reported_unit_cost': '1', 'contents': [{'component_id': str(i+1), 'gross_quantity': '1', 'unit': 'kg'}]}
                 for i in range(1500)]
        cards.append({'id': '1500', 'type': 'INGREDIENT', 'unit': 'kg', 'output_quantity': None,
                      'reported_unit_cost': '1', 'contents': []})
        data = {'currency': 'AZN', 'cards': cards}
        self.assertEqual(check_recipes(data)['status'], 'no_issues_found')
        cards[-1].update(type='PREPARATION', output_quantity='1',
                         contents=[{'component_id': '0', 'gross_quantity': '1', 'unit': 'kg'}])
        self.assertIn('recipe_cycle', {x['code'] for x in check_recipes(data)['issues']})

    def test_invalid_numbers_are_rejected(self):
        for bad in ['1,5', '-1', '1e3', 'NaN', 'Infinity', '0.0000001', True, 1.5]:
            with self.subTest(value=bad):
                self.data['cards'][2]['contents'][0]['gross_quantity'] = bad
                with self.assertRaises(InputError):
                    check_recipes(self.data)

    def test_unknown_fields_types_and_leaf_contents_are_rejected(self):
        mutations = [lambda d: d.update(extra='x'),
                     lambda d: d['cards'][0].update(type='UNKNOWN'),
                     lambda d: d['cards'][0].update(output_quantity='1'),
                     lambda d: d['cards'][0].update(contents=[{'component_id': 'x', 'unit': 'kg', 'gross_quantity': '1'}]),
                     lambda d: d['cards'][0].update(id=' demo-flour '),
                     lambda d: d.update(cards=[])]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                data = copy.deepcopy(self.data)
                mutate(data)
                with self.assertRaises(InputError):
                    check_recipes(data)

    def test_does_not_mutate_source(self):
        original = copy.deepcopy(self.data)
        check_recipes(self.data)
        self.assertEqual(self.data, original)

    def test_cli_statuses_input_preservation_and_duplicate_keys(self):
        review = copy.deepcopy(self.data)
        review['cards'][0]['reported_unit_cost'] = None
        cases = [(json.dumps(self.data), 0, 'no_issues_found'),
                 (json.dumps(review), 1, 'review_required'),
                 ('{"currency":"AZN","currency":"USD","cards":[]}', 2, 'invalid_input'),
                 ('not json', 2, 'invalid_input')]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'recipes.json'
            for content, code, status in cases:
                with self.subTest(status=status, content=content[:40]):
                    path.write_text(content, encoding='utf-8')
                    result = subprocess.run([sys.executable, '-B', str(CHECKER), str(path)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, code, result.stderr)
                    self.assertEqual(json.loads(result.stdout)['status'], status)
                    self.assertEqual(path.read_text(encoding='utf-8'), content)
            path.write_bytes(b'\xff')
            result = subprocess.run([sys.executable, '-B', str(CHECKER), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['status'], 'invalid_input')


if __name__ == '__main__':
    unittest.main()
