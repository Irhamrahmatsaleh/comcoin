from wallet import generate_key_pair, public_key_to_address, sign_message, verify_signature

# Buat wallet baru
priv, pub = generate_key_pair()
addr = public_key_to_address(pub)

print("Private Key :", priv)
print("Public Key  :", pub)
print("Address     :", addr)

# Tanda tangan dan verifikasi
msg = "Send 10 CMC to Chip Murphy"
sig = sign_message(priv, msg)

print("\nSignature   :", sig)
print("Valid?      :", verify_signature(pub, msg, sig))
