import hmac
import struct
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, SHA1, SHA256

# Constants
IV_SIZE = 16
KEY_SIZE = 32
AES_BLOCK_SIZE = 16
SALT_SIZE = 16

def verify_key(pkey_hex, db_path):
    if not os.path.exists(db_path):
        print(f'File not found: {db_path}')
        return

    pkey = bytes.fromhex(pkey_hex)
    
    # A: treat pkey as passphrase (SQLCipher-style)
    # B: treat pkey as already-derived 32-byte AES key (some clients expose derived key)
    configs = [
        {'iter': 64000, 'mac_algo': SHA1, 'mac_size': 20, 'mask': 0x3a},
        {'iter': 64000, 'mac_algo': SHA256, 'mac_size': 32, 'mask': 0x3a},
        {'iter': 64000, 'mac_algo': SHA512, 'mac_size': 64, 'mask': 0x3a},
        {'iter': 256000, 'mac_algo': SHA256, 'mac_size': 32, 'mask': 0x3a},
        {'iter': 256000, 'mac_algo': SHA512, 'mac_size': 64, 'mask': 0x3a},
        {'iter': 4000, 'mac_algo': SHA512, 'mac_size': 64, 'mask': 0x3a},
        {'iter': 4000, 'mac_algo': SHA1, 'mac_size': 20, 'mask': 0x3a},
        {'iter': 64000, 'mac_algo': SHA256, 'mac_size': 32, 'mask': 0},
        {'iter': 64000, 'mac_algo': SHA512, 'mac_size': 64, 'mask': 0},
        {'iter': 256000, 'mac_algo': SHA256, 'mac_size': 32, 'mask': 0},
        {'iter': 256000, 'mac_algo': SHA512, 'mac_size': 64, 'mask': 0},
    ]
    
    page_sizes = [1024, 4096, 8192, 16384, 32768]
    
    for p_size in page_sizes:
        print(f"Testing Page Size: {p_size}")
        try:
            with open(db_path, 'rb') as f:
                salt = f.read(SALT_SIZE)
                first_page_data = f.read(p_size - SALT_SIZE)
            
            if len(first_page_data) != p_size - SALT_SIZE:
                print("  Not enough data for this page size.")
                continue

            page = salt + first_page_data
            
            for conf in configs:
                mac_salt = bytes(x ^ conf['mask'] for x in salt)
                
                # Mode A: pkey -> PBKDF2 -> key
                key_a = PBKDF2(pkey, salt, dkLen=KEY_SIZE, count=conf['iter'], hmac_hash_module=conf['mac_algo'])
                mac_key_a = PBKDF2(key_a, mac_salt, dkLen=KEY_SIZE, count=2, hmac_hash_module=conf['mac_algo'])

                # Mode B: pkey is already key
                key_b = pkey
                mac_key_b = PBKDF2(key_b, mac_salt, dkLen=KEY_SIZE, count=2, hmac_hash_module=conf['mac_algo'])
                
                reserve = IV_SIZE + conf['mac_size']
                reserve = ((reserve + AES_BLOCK_SIZE - 1) // AES_BLOCK_SIZE) * AES_BLOCK_SIZE
                
                offset = SALT_SIZE
                end = len(page)
                
                stored_mac = page[end - reserve + IV_SIZE : end - reserve + IV_SIZE + conf['mac_size']]

                # Verify Mode A
                mac = hmac.new(mac_key_a, page[offset:end - reserve + IV_SIZE], conf['mac_algo'])
                mac.update(struct.pack('<I', 1))  # Page 1
                if mac.digest() == stored_mac:
                    print(f'SUCCESS: Mode A(passphrase) config={conf} page_size={p_size}')
                    return

                # Verify Mode B
                mac = hmac.new(mac_key_b, page[offset:end - reserve + IV_SIZE], conf['mac_algo'])
                mac.update(struct.pack('<I', 1))  # Page 1
                if mac.digest() == stored_mac:
                    print(f'SUCCESS: Mode B(derived-key) config={conf} page_size={p_size}')
                    return
        except Exception as e:
            print(f"  Error: {e}")
            pass

    print('All configs failed.')

if __name__ == '__main__':
    import sys
    key = sys.argv[1] if len(sys.argv) > 1 else '4e503844d526f79e9443bbcb28cc1f191e630a1e8337e6b195478bdd48a33c3a'
    db_path = r'e:\WeChatMsg\test_header_16k.db'
    verify_key(key, db_path)
