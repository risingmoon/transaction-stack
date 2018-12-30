from unittest import TestCase, main

from stack import TransactionStack


class TransactionTestCase(TestCase):

    def setUp(self):
        self.stack = TransactionStack()
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)

    def test_begin_when_executed_then_increase_transaction(self):
        self.stack.begin()

        self.assertEqual(self.stack.transaction_indices, [0])

    def test_commit_when_begin_and_commit_then_empty_transaction(self):
        self.stack.begin()
        self.stack.push(4)
        self.stack.commit()

        self.assertEqual(self.stack.transaction_indices, [])
        self.assertEqual(self.stack[-1], 4)

    def test_nested_transactions_when_rollback_two_of_three_then_only_one_transaction_left(self):
        self.stack.begin()
        self.stack.push(4)
        self.stack.push(5)
        self.stack.push(6)
        self.stack.begin()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.push(7)
        self.stack.push(8)
        self.stack.begin()
        self.stack.push(9)

        self.assertEqual(len(self.stack), 3)
        self.assertEqual(self.stack.transaction_indices, [0, 3, 11])

        self.stack.rollback()

        self.assertEqual(len(self.stack), 2)
        self.assertEqual(self.stack.transaction_indices, [0, 3])

        self.stack.rollback()

        self.assertEqual(len(self.stack), 6)
        self.assertEqual(self.stack.transaction_indices, [0])

    def test_nested_transactions_when_commit_three_transaction_then_only_no_transaction_left(self):
        self.stack.begin()
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        self.stack.push(4)
        self.stack.push(5)
        self.stack.push(6)
        self.stack.begin()
        self.stack.push(7)
        self.stack.push(8)
        self.stack.begin()
        self.stack.push(9)

        self.stack.commit()
        self.stack.commit()
        self.stack.commit()

        self.assertEqual(self.stack, [4, 5, 6, 7, 8, 9])
        self.assertEqual(self.stack.transaction_indices, [])
        self.assertEqual(self.stack.transactions, [])


if __name__ == '__main__':
    main()
