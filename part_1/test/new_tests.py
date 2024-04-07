import unittest
from part_1.main import simplify_debts

class SimplifyDebtsTest(unittest.TestCase):
    def test_debts_are_simplified_correctly(self):
        transactions = [('A', 'B', 10), ('B', 'C', 5), ('C', 'A', 5)]
        expected_result = [('B', 'A', 5)]
        self.assertEqual(expected_result, simplify_debts(transactions))

    def test_no_debts_left_after_simplification(self):
        transactions = [('A', 'B', 10), ('B', 'A', 10)]
        expected_result = []
        self.assertEqual(expected_result, simplify_debts(transactions))

    def test_single_transaction_is_not_simplified(self):
        transactions = [('A', 'B', 10)]
        expected_result = [('B', 'A', 10)]
        self.assertEqual(expected_result, simplify_debts(transactions))

    def test_multiple_transactions_are_simplified_correctly(self):
        transactions = [('A', 'B', 10), ('B', 'C', 5), ('C', 'A', 5), ('A', 'D', 20), ('D', 'B', 20)]
        expected_result = [('B', 'A', 25)]
        self.assertEqual(expected_result, simplify_debts(transactions))

    def test_transactions_with_zero_amount_are_ignored(self):
        transactions = [('A', 'B', 0), ('B', 'C', 0), ('C', 'A', 0)]
        expected_result = []
        self.assertEqual(expected_result, simplify_debts(transactions))

if __name__ == '__main__':
    unittest.main()
