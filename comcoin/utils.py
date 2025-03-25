from ecdsa import VerifyingKey, SECP256k1


def is_valid_public_key(pubkey_hex):
    """
    Check if a public key (hex) is valid ECDSA key.
    """
    try:
        VerifyingKey.from_string(bytes.fromhex(pubkey_hex), curve=SECP256k1)
        return True
    except Exception:
        return False
