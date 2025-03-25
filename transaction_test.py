from wallet import generate_key_pair, public_key_to_address, sign_message, verify_signature
from blockchain import Transaction

# Buat wallet pengirim & penerima
priv1, pub1 = generate_key_pair()
addr1 = public_key_to_address(pub1)

priv2, pub2 = generate_key_pair()
addr2 = public_key_to_address(pub2)

# Simulasikan transaksi: addr1 kirim 15 CMC ke addr2
amount = 15
message = f"{addr1}->{addr2}:{amount}"

# Tanda tangan transaksi oleh pengirim (addr1)
signature = sign_message(priv1, message)

# Verifikasi oleh siapa pun di jaringan
is_valid = verify_signature(pub1, message, signature)

print("🔐 Simulasi Transaksi CHIP (CMC)")
print("-" * 50)
print("Alamat Pengirim :", addr1)
print("Alamat Penerima :", addr2)
print("Jumlah Transfer :", amount, "CMC")
print("Signature       :", signature)
print("Valid Signature :", is_valid)


tx = Transaction(
    sender_address=addr1,
    recipient_address=addr2,
    amount=15,
    sender_public_key=pub1
)

tx.sign(priv1)

print("\n📄 Transaksi via Class Transaction")
print("-" * 50)
print("Message       :", tx.to_message())
print("Signature     :", tx.signature)
print("Valid?        :", tx.is_valid())
