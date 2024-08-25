"""
More comments: This was harder than expected.
Pydantic would have been nice, but I'm just a pydantic lover so that's just me.

Thanks for the fun!
"""

class DatabaseSimulator:
    def __init__(self):
        self._data = {}
        self._transaction_stack = []

    def begin(self):
        self._transaction_stack.append({})

    def get(self, key):
        for transaction in reversed(self._transaction_stack):
            if key in transaction:
                return transaction[key]
        return self._data.get(key)

    def set(self, key, value):
        if not self._transaction_stack:
            raise NameError("No active transaction. Call begin() first.")
        self._transaction_stack[-1][key] = value

    def count(self):
        return len(self._data)

    def commit(self):
        if not self._transaction_stack:
            raise NameError("No active transaction to commit.")
        
        for transaction in self._transaction_stack:
            self._data.update(transaction)
        self._transaction_stack.clear()

    def rollback(self):
        if not self._transaction_stack:
            raise NameError("No active transaction to rollback.")
        self._transaction_stack.pop()

    def _check_active_transaction(self):
        if not self._transaction_stack:
            raise NameError("No active transaction. Call begin() first.")

