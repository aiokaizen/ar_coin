import json

from blockchain import Blockchain, Wallet, Transaction


# Creating wallets
mouad = Wallet('Mouad')
rajae = Wallet('Rajae')
anas = Wallet('Anas')
asmae = Wallet('Asmae')

# Creating transactions
t1 = Transaction(mouad.pub_key, rajae.pub_key, 12)
t2 = Transaction(mouad.pub_key, anas.pub_key, 14)
t3 = Transaction(rajae.pub_key, mouad.pub_key, 50)
# t4 = Transaction(mouad.pub_key, asmae.pub_key, 5)
# t5 = Transaction(asmae.pub_key, mouad.pub_key, 4.6)
# t6 = Transaction(asmae.pub_key, rajae.pub_key, 28)
# t7 = Transaction(anas.pub_key, asmae.pub_key, 12)
# t8 = Transaction(rajae.pub_key, anas.pub_key, 235)
# t9 = Transaction(anas.pub_key, mouad.pub_key, 53.5)
# t10 = Transaction(anas.pub_key, mouad.pub_key, 53.5)
# t11 = Transaction(rajae.pub_key, asmae.pub_key, 2.5)

t1.sign_transaction(mouad.get_signing_key())
t2.sign_transaction(mouad.get_signing_key())
t3.sign_transaction(rajae.get_signing_key())

# Creating a blockchain with initial pending transactions.
ar_coin = Blockchain(name="ARCoin", pending_transactions=[
    t1, t2, t3  #, t4, t5, t6, t7, t8, t9, t10, t11
])

# Mining the blocks
ar_coin.mine_new_block(mouad.pub_key)
ar_coin.mine_new_block(rajae.pub_key)
ar_coin.mine_new_block(mouad.pub_key)

# Print the blockchain info
print(json.dumps(ar_coin.serialize(), indent=4))

# Get the new balances from the blockchain
mouad.update_balance(ar_coin);
rajae.update_balance(ar_coin);

# Print balances
print(json.dumps([
    {"name": mouad.name, "balance": mouad.balance},
    {"name": rajae.name, "balance": rajae.balance},
], indent=4))
