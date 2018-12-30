class Stack(list):

    def push(self, value):
        super().append(value)


class TransactionStack(Stack):
    ROLLBACK = 'ROLLBACK'
    NONE = None
    PUSH = 'push'
    POP = 'pop'

    def __init__(self):
        super().__init__()
        self.state = TransactionStack.NONE
        self.transaction_indices = []
        self.transactions = []

    def __str__(self):
        return str(self[-1] if self else [])

    def begin(self):
        self.transaction_indices.append(len(self.transactions))

    def commit(self):
        if self.transaction_indices:
            index = self.transaction_indices.pop()
            while len(self.transactions) != index:
                self.transactions.pop()
        else:
            self.state = TransactionStack.NONE

    def rollback(self):
        if self.transaction_indices:
            index = self.transaction_indices.pop()
            self.state = TransactionStack.ROLLBACK
            while len(self.transactions) != index:
                transaction, value = self.transactions.pop()
                if transaction == TransactionStack.POP:
                    getattr(self, transaction)()
                if transaction == TransactionStack.PUSH:
                    getattr(self, transaction)(value)
            self.state = TransactionStack.NONE

    def push(self, value):
        super().append(value)
        if self.transaction_indices and self.state != TransactionStack.ROLLBACK:
            self.transactions.append((TransactionStack.POP, None))

    def pop(self):
        value = super().pop()
        if self.transaction_indices and self.state != TransactionStack.ROLLBACK:
            self.transactions.append((TransactionStack.PUSH, value))

