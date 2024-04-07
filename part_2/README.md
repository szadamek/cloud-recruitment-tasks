# DebtSimplifer

## Description task1
This is a simple program that takes in a list of debts and simplifies them. It does this by combining debts that are owed to the same person.

## Dependencies
- Python 3.12
- csv module: To read CSV files.
- heapq module: Provides heap queue algorithm.
- defaultdict from collections module: Used for handling default values for dictionary keys.

## How it works
1. Reading Transactions: The algorithm begins by reading transactions from a CSV file. Each transaction includes a giver, a receiver, and the amount transferred.
2. Simplifying Debts: It computes the net amount owed by each individual. For every transaction, it subtracts the amount from the giver's total and adds it to the receiver's total.
3. Heap Data Structures: The algorithm then constructs two heaps: one for creditors (those who are owed money) and another for debtors (those who owe money). Each heap stores tuples of (amount, name).
4. Processing Transactions: It iterates over the creditors and debtors, settling debts by matching creditors with debtors based on the amount owed.
5. Output: Finally, the algorithm returns a list of simplified transactions, indicating who owes how much to whom.

## Notes:
- Ensure that the input CSV file is formatted correctly with three columns: giver, receiver, and amount.
- This algorithm focuses on minimizing the number of transactions required to settle all debts.