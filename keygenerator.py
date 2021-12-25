# Signer’s perspective (SigningKey)

from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey


# Generate a new random signing key
signing_key = SigningKey.generate()
private_key = signing_key.to_curve25519_private_key().encode(encoder=HexEncoder)
print('private key:', private_key)

# Sign a message with the signing key
signed_hex = signing_key.sign(b"Attack at Dawn", encoder=HexEncoder)

# Obtain the verify key for a given signing key
verify_key = signing_key.verify_key

# Serialize the verify key to send it to a third party
public_key = verify_key.encode(encoder=HexEncoder)
print('public key:', public_key)

# signing_key2 = SigningKey(
#     seed=private_key,
#     encoder=HexEncoder
# )


#
# Verifier’s perspective (VerifyKey)
#-----------------------------------

# Create a VerifyKey object from a hex serialized public key
verify_key = VerifyKey(public_key, encoder=HexEncoder)

# Check the validity of a message's signature
# The message and the signature can either be passed together, or
# separately if the signature is decoded to raw bytes.
# These are equivalent:
print('verification:', verify_key.verify(signed_hex, encoder=HexEncoder))
print("signed hex:", signed_hex, type(signed_hex))
print("message:", signed_hex.message, type(signed_hex.message))
print("signature:", signed_hex.signature, type(signed_hex.signature))
# signature_bytes = HexEncoder.decode(signed_hex.signature)
# verify_key.verify(signed_hex.message, signature_bytes,
#                   encoder=HexEncoder)

# Alter the signed message text
# forged = signed_hex[:-1] + bytes([int(signed_hex[-1]) ^ 1])
# Will raise nacl.exceptions.BadSignatureError, since the signature check
# is failing
# verify_key.verify(forged)
