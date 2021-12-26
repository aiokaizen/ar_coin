from secp256k1 import PrivateKey, PublicKey

privkey = PrivateKey()
privkey_hex = privkey.serialize()
assert privkey.deserialize(privkey_hex) == privkey.private_key

sig = privkey.ecdsa_sign(b'hello world')
verified = privkey.pubkey.ecdsa_verify(b'hello world', sig)
assert verified

sig_der = privkey.ecdsa_serialize(sig)
print('sig_der:', sig_der)
print('sig_der hex:', bytearray(sig_der).hex())
sig2 = privkey.ecdsa_deserialize(sig_der)
vrf2 = privkey.pubkey.ecdsa_verify(b'hello world', sig2)
assert vrf2

pubkey = privkey.pubkey
pub = pubkey.serialize()
print('\nprivate key:', privkey_hex)
print('public key:', bytearray(pubkey.serialize()).hex())
print()

pubkey2 = PublicKey(pub, raw=True)
assert pubkey2.serialize() == pub
assert pubkey2.ecdsa_verify(b'hello world', sig)
