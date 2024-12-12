import random
import re
from fastapi import FastAPI, HTTPException
import grpc
import logging
from model.bank_model import BankLoanRequest

'''
    Each bank will vary its behavior by the following parameters:

    MIN_CREDIT_SCORE - the customer's minimum credit score required to receive a quote from this bank.
    MAX_LOAN_AMOUNT - the maximum amount the bank is willing to lend to a customer.
    BASE_RATE - the minimum rate the bank might give. The actual rate increases for a lower credit score and some randomness.
    BANK_ID - as the loan broker processes multiple responses, knowing which bank supplied the quote will be handy.
'''

BANK_ID = "union-vault"
MIN_CREDIT_SCORE = 400
MAX_LOAN_AMOUNT = 900000
BASE_RATE = 3

logging.basicConfig(level=logging.INFO)
app = FastAPI()


def calculate_interest_rate(amount: int, score: int):
    if amount <= float(MAX_LOAN_AMOUNT) and score >= float(MIN_CREDIT_SCORE):
        return BASE_RATE + random.random() * ((1000 - score) / 100.0)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post('/loan-quote')
def bank_loan_request(loanRequest: BankLoanRequest):
    logging.info(f"Received loan request {loanRequest} for {BANK_ID}")

    rate = calculate_interest_rate(loanRequest.amount, loanRequest.credit.score, )

    if rate:
        quote = {
            'rate': rate,
            'bankId': BANK_ID,

        }
        logging.info("Union Vault Approved load Request with qoute", quote)
        return {
            'status': 'APPROVED',
            'quote': quote
        }
    else:
        logging.info('Union Vault Rejected Loan Request')
        return {
            'status': 'DENIED',
            'bankId': BANK_ID,
            'message': 'Loan Rejected'
        }