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
        self.transactions = []
        self.tmp = []

    def __str__(self):
        return str(self[-1] if self else [])

    def begin(self):
        self.transactions.append(len(self))

    def commit(self):
        self.transactions.pop()

    def rollback(self):
        if self.transactions:
            index = self.transactions.pop()
            self.state = TransactionStack.ROLLBACK
            while len(self) != index:
                action, value = self.tmp.pop()
                if action == 'pop':
                    getattr(self, action)()
                else:
                    getattr(self, action)(value)
            self.state = TransactionStack.NONE

    def push(self, value):
        super().append(value)
        if self.transactions and self.state != TransactionStack.ROLLBACK:
            self.tmp.append((TransactionStack.POP, None))

    def pop(self):
        value = super().pop()
        if self.transactions and self.state != TransactionStack.ROLLBACK:
            self.tmp.append((TransactionStack.PUSH, value))

