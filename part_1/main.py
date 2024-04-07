import csv
import heapq
from collections import defaultdict


def simplify_debts(transactions):
    total = defaultdict(int)

    for giver, receiver, amount in transactions:
        total[giver] -= amount
        total[receiver] += amount

    credit = []
    debit = []

    for name, amount in total.items():
        # if amount is positive, append to credit else append to debit
        if amount > 0:
            credit.append((-amount, name))
        if amount < 0:
            debit.append((amount, name))

    heapq.heapify(credit)
    heapq.heapify(debit)
    answer = []

    while credit and debit:
        # pop the smallest value from credit and debit
        credit_value, credit_name = heapq.heappop(credit)
        debit_value, debit_name = heapq.heappop(debit)

        if credit_value < debit_value:
            # if credit value is smaller than debit value, append the credit value to answer
            amount_left = credit_value - debit_value
            answer.append((credit_name, debit_name, -1 * debit_value))
            heapq.heappush(credit, (amount_left, credit_name))

        elif debit_value < credit_value:
            # if debit value is smaller than credit value, append the debit value to answer
            amount_left = debit_value - credit_value
            answer.append((credit_name, debit_name, -1 * credit_value))
            heapq.heappush(debit, (amount_left, debit_name))

        else:
            answer.append((credit_name, debit_name, -1 * credit_value))

    return answer


with open('../test_data/debts_1.csv', 'r') as file:
    reader = csv.reader(file)
    transactions = list(reader)

# change debts to integers
transactions = [(row[0], row[1], int(row[2])) for row in transactions]

print(simplify_debts(transactions))
