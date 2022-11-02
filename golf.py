#!/usr/bin/env python3

from algosdk.future import transaction
from algosdk.v2client import algod
from algosdk.logic import get_application_address
from algosdk.abi import UintType
from beaker import *
import base64
import random


algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

f = open("golf.teal")
accounts = sorted(
    sandbox.get_accounts(),
    key=lambda a: sandbox.clients.get_algod_client().account_info(a.address)["amount"],
)

sender = accounts.pop()
approval = base64.b64decode(algod_client.compile(f.read())["result"])

create_txn = transaction.ApplicationCreateTxn(
    sender.address,
    algod_client.suggested_params(),
    on_complete=transaction.OnComplete.NoOpOC,
    approval_program=approval,
    clear_program=approval,
    global_schema=transaction.StateSchema(0, 0),
    local_schema=transaction.StateSchema(0, 0),
)


def add_number(n):
    print(f"Adding number {n}")
    txid = send(
        transaction.ApplicationCallTxn(
            sender=sender.address,
            sp=algod_client.suggested_params(),
            index=app_id,
            on_complete=transaction.OnComplete.NoOpOC,
            boxes=[[0, "ints"], [0, "ints"], [0, "ints"], [0, "ints"]],
            app_args=[n],
        )
    )

    info = algod_client.pending_transaction_info(txid)
    log_array = []

    opcode_budget = UintType(64).decode(base64.b64decode(info["logs"][-1]))

    if len(info["logs"]) > 1:
        decoded = base64.b64decode(info["logs"][0])

        for i in range(0, len(decoded), 2):
            log_array.append(UintType(16).decode(decoded[i : i + 2]))

        print(f"New array: {log_array}")
        print(f"Array length: {len(log_array)}")

    print(f"Opcode budget: {opcode_budget}")
    print("-")

    return opcode_budget


def send(txn):
    txid = algod_client.send_transaction(txn.sign(sender.private_key))

    return txid


app_id = algod_client.pending_transaction_info(send(create_txn))["application-index"]

fund_txn = transaction.PaymentTxn(
    sender.address,
    algod_client.suggested_params(),
    receiver=get_application_address(app_id),
    amt=10_000_000,
)

send(fund_txn)

nums = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    111,
    123,
    456,
]

nums = list(range(2048))
random.shuffle(nums)
total_budget = 0
budgets = []
for n in nums:
    print(f"Iteration: {nums.index(n)+1}")
    budget = add_number(n)
    total_budget += budget
    budgets.append(budget)

print(f"Average budget left: {total_budget/len(nums)}")
print(f"Lowest budget left: {min(budgets)}")
