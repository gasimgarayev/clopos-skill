"""Arithmetic and CLI checks using synthetic invoice data; no Clopos access."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / 'skills/clopos/scripts/check_purchase.py'
sys.path.insert(0, str(CHECKER.parent))
from check_purchase import InputError, check_purchase


class PurchaseTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'examples/purchase.json').read_text(encoding='utf-8'))

    def codes(self, data=None):
        return {x['code'] for x in check_purchase(self.data if data is None else data)['issues']}

    def test_sample_matches_after_explicit_rounding_and_discount(self):
        result = check_purchase(self.data)
        self.assertEqual(result['status'], 'arithmetic_match')
        self.assertEqual(result['sum_of_declared_lines_and_adjustments'], '54.50')
        self.assertEqual(result['lines'][1]['expected_total'], '1.00')

    def test_decimal_money_has_no_binary_float_difference(self):
        self.data['lines'] = [self.data['lines'][0]]
        self.data['lines'][0].update(quantity='3', unit_price='0.10', line_total='0.30')
        self.data.update(invoice_total='0.30', adjustments=[])
        self.assertEqual(check_purchase(self.data)['status'], 'arithmetic_match')

    def test_wrong_line_cannot_hide_behind_matching_invoice_sum(self):
        self.data['lines'][0]['unit_price'] = '20.00'
        result = check_purchase(self.data)
        self.assertEqual(result['difference'], '0.00')
        self.assertEqual(result['status'], 'review_required')
        self.assertIn('line_total_mismatch', self.codes())

    def test_wrong_invoice_total(self):
        self.data['invoice_total'] = '55.00'
        result = check_purchase(self.data)
        self.assertEqual(result['difference'], '-0.50')
        self.assertIn('invoice_total_mismatch', self.codes())

    def test_missing_quantity_is_not_zero(self):
        self.data['lines'][0]['quantity'] = None
        result = check_purchase(self.data)
        self.assertEqual(result['status'], 'review_required')
        self.assertIsNone(result['lines'][0]['expected_total'])
        self.assertIn('missing_value', self.codes())

    def test_missing_total_prevents_claiming_invoice_reconciliation(self):
        self.data['lines'][0]['line_total'] = None
        result = check_purchase(self.data)
        self.assertIsNone(result['sum_of_declared_lines_and_adjustments'])
        self.assertIsNone(result['difference'])

    def test_units_are_not_silently_converted(self):
        self.data['lines'][0]['price_unit'] = 'ədəd'
        result = check_purchase(self.data)
        self.assertIsNone(result['lines'][0]['expected_total'])
        self.assertIn('unit_mismatch', self.codes())

    def test_duplicate_document_row_id_is_reported(self):
        self.data['lines'][1]['id'] = '1'
        self.assertIn('duplicate_line_id', self.codes())

    def test_line_discount_and_tax_are_amounts(self):
        self.data['lines'] = [self.data['lines'][0]]
        self.data['lines'][0].update(quantity='2', unit_price='10.00', discount_amount='2.00',
                                     tax_amount='3.24', line_total='21.24')
        self.data.update(invoice_total='21.24', adjustments=[])
        self.assertEqual(check_purchase(self.data)['status'], 'arithmetic_match')

    def test_ambiguous_numbers_and_implicit_rounding_rejected(self):
        for bad in ['1,250', 'NaN', 'Infinity', '1e3', 2.5, True]:
            with self.subTest(value=bad):
                data = copy.deepcopy(self.data)
                data['lines'][0]['unit_price'] = bad
                with self.assertRaises(InputError):
                    check_purchase(data)
        self.data['rounding'] = 'guess'
        with self.assertRaises(InputError):
            check_purchase(self.data)

    def test_subcent_totals_are_not_silently_rounded(self):
        self.data['invoice_total'] = '54.501'
        with self.assertRaises(InputError):
            check_purchase(self.data)

    def test_negative_purchase_amount_rejected(self):
        self.data['lines'][0]['quantity'] = '-3'
        with self.assertRaises(InputError):
            check_purchase(self.data)

    def test_unknown_field_is_not_silently_ignored(self):
        self.data['lines'][0]['tax_percentage'] = '18'
        with self.assertRaises(InputError):
            check_purchase(self.data)

    def test_checker_does_not_mutate_input(self):
        original = copy.deepcopy(self.data)
        check_purchase(self.data)
        self.assertEqual(self.data, original)

    def test_cli_exit_codes_json_output_and_input_preservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'purchase.json'
            for value, expected_exit, status in [(self.data, 0, 'arithmetic_match'),
                                                  ({**self.data, 'invoice_total': None}, 1, 'review_required'),
                                                  ({**self.data, 'currency': 'USD'}, 2, 'invalid_input')]:
                path.write_text(json.dumps(value), encoding='utf-8')
                original = path.read_bytes()
                result = subprocess.run([sys.executable, '-B', str(CHECKER), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected_exit, result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], status)
                self.assertEqual(path.read_bytes(), original)

    def test_cli_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'purchase.json'
            path.write_text('{"currency":"AZN","currency":"USD"}', encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', str(CHECKER), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['status'], 'invalid_input')


if __name__ == '__main__':
    unittest.main()
