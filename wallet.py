import ecdsa
import hashlib
import base58
import secrets

def generate_key_pair():
    private_key = secrets.token_bytes(32)
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = vk.to_string()
    return private_key.hex(), public_key.hex()

def public_key_to_address(public_key_hex):
    public_key_bytes = bytes.fromhex(public_key_hex)
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    hashed_pubkey = ripemd160.digest()

    # Tambahkan versi byte (0x00) di awal (seperti Bitcoin)
    versioned_payload = b'\x00' + hashed_pubkey
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    full_payload = versioned_payload + checksum

    address = base58.b58encode(full_payload).decode()
    return address

def sign_message(private_key_hex, message):
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    signature = sk.sign(message.encode())
    return signature.hex()

def verify_signature(public_key_hex, message, signature_hex):
    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
    try:
        return vk.verify(bytes.fromhex(signature_hex), message.encode())
    except ecdsa.BadSignatureError:
        return False
