from main import *


mouad = Wallet('hyd736ebhgT7RY0', 'Mouad', 1000)
rajae = Wallet('87hgt6DE466FD53', 'Rajae', 1000)
anas = Wallet('gF5ryFr5443GtR7', 'Anas', 1000)
asmae = Wallet('778dhYYt67679Vv', 'Asmae', 1000)

miner1 = Wallet('718tX45tF7679Vv', 'Omar', 100)
miner2 = Wallet('8heXhYYt67679Vv', 'Jack', 100)

t1 = Transaction(mouad, rajae, 12)
t2 = Transaction(mouad, anas, 14)
t3 = Transaction(rajae, anas, 11)
t4 = Transaction(mouad, asmae, 5)
t5 = Transaction(asmae, mouad, 4.6)
t6 = Transaction(asmae, rajae, 28)
t7 = Transaction(anas, asmae, 12)
t8 = Transaction(rajae, anas, 235)
t9 = Transaction(anas, mouad, 53.5)
t10 = Transaction(anas, mouad, 53.5)
t11 = Transaction(rajae, asmae, 2.5)

ar_coin = Blockchain(name="ARCoin", pending_transactions=[
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11
])

ar_coin.mine_new_block(miner1)
ar_coin.mine_new_block(miner2)
ar_coin.mine_new_block(miner2)
ar_coin.mine_new_block(miner1)

print(json.dumps(ar_coin.serialize(), indent=4))

print('wait...')
