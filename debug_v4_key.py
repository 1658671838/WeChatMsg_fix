import ctypes
import os
import struct
import time
from ctypes import wintypes

import pymem
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import HMAC, SHA1, SHA256, SHA512

# Constants
KEY_SIZE = 32
DEFAULT_ITER = 64000
DEFAULT_PAGESIZE = 4096 
SALT_SIZE = 16
IV_SIZE = 16
AES_BLOCK_SIZE = 16

# Known offset for WeChat/Weixin 4.1.6.14 (module base + offset -> pointer -> 32-byte key)
KEY_PTR_OFFSET_V41614 = 0x90A4B38

# Reduce extremely noisy candidate printing by default.
PRINT_UNVERIFIED_CANDIDATES = False

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('BaseAddress', ctypes.c_void_p),
        ('AllocationBase', ctypes.c_void_p),
        ('AllocationProtect', wintypes.DWORD),
        ('RegionSize', ctypes.c_size_t),
        ('State', wintypes.DWORD),
        ('Protect', wintypes.DWORD),
        ('Type', wintypes.DWORD),
    ]

def get_wechat_pid(db_header_buf=None):
    try:
        import psutil
        candidates = []
        for proc in psutil.process_iter(['pid', 'name']):
            if not proc.info.get('name'):
                continue
            if proc.info['name'].lower() in ['wechat.exe', 'weixin.exe']:
                candidates.append(proc)

        # Best: PID where known-offset key can be verified against the DB header
        if db_header_buf:
            for proc in candidates:
                try:
                    pm = pymem.Pymem(proc.pid)
                    base, _size = get_module_info(pm, 'WeChatWin.dll')
                    if not base:
                        base, _size = get_module_info(pm, 'Weixin.dll')
                    if not base:
                        continue
                    key = try_read_key_via_known_offset(pm, base, db_header_buf)
                    if key:
                        return proc.pid
                except Exception:
                    continue

        # Next: Prefer the PID that maps Weixin.dll / WeChatWin.dll
        for proc in candidates:
            try:
                for mm in proc.memory_maps(grouped=False):
                    p = (mm.path or '').lower()
                    if p.endswith('weixin.dll') or p.endswith('wechatwin.dll'):
                        return proc.pid
            except Exception:
                continue

        # Fallback: first match
        if candidates:
            return candidates[0].pid
    except ImportError:
        print('psutil not installed.')
    return None

def get_memory_regions(pm):
    regions = []
    address = 0
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    mbi = MEMORY_BASIC_INFORMATION()
    mbi_size = ctypes.sizeof(mbi)
    
    while True:
        try:
            if kernel32.VirtualQueryEx(pm.process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), mbi_size) == 0:
                break
            
            if mbi.State == 0x1000: # MEM_COMMIT
                base = mbi.BaseAddress if mbi.BaseAddress is not None else 0
                regions.append((base, mbi.RegionSize))
            
            base = mbi.BaseAddress if mbi.BaseAddress is not None else 0
            address = base + mbi.RegionSize
        except Exception as e:
            print(f'Error in VirtualQueryEx: {e}')
            break
    return regions


def get_memory_regions_detailed(pm):
    """Return (base, size, protect, state, type) for all committed regions."""
    regions = []
    address = 0
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    mbi = MEMORY_BASIC_INFORMATION()
    mbi_size = ctypes.sizeof(mbi)

    while True:
        if kernel32.VirtualQueryEx(pm.process_handle, ctypes.c_void_p(address), ctypes.byref(mbi), mbi_size) == 0:
            break

        base = int(mbi.BaseAddress or 0)
        size = int(mbi.RegionSize or 0)
        if mbi.State == 0x1000 and base and size:  # MEM_COMMIT
            regions.append((base, size, int(mbi.Protect), int(mbi.State), int(mbi.Type)))

        address = base + size
        if address <= 0:
            break

    return regions


def scan_for_key_near_db_salt(pid: int, db_header_buf: bytes):
    """Search process memory for the DB salt bytes and test nearby 32-byte candidates."""
    if not db_header_buf or len(db_header_buf) < SALT_SIZE:
        return None

    salt = db_header_buf[:SALT_SIZE]
    cases = build_verification_cases(db_header_buf)
    if not cases:
        return None

    try:
        pm = pymem.Pymem(pid)
    except Exception as e:
        print(f'[-] Could not attach to PID={pid}: {e}')
        return None

    print(f'[*] Salt-scan: PID={pid} looking for salt={salt.hex()}')

    regions = get_memory_regions_detailed(pm)
    print(f'[*] Salt-scan: {len(regions)} committed regions')

    # Skip obviously problematic regions (PAGE_GUARD=0x100, PAGE_NOACCESS=0x01).
    PAGE_GUARD = 0x100
    PAGE_NOACCESS = 0x01

    hits = 0
    chunk_size = 4 * 1024 * 1024
    for (base, size, protect, _state, _type) in regions:
        if protect & PAGE_GUARD or protect == PAGE_NOACCESS:
            continue
        # Heuristic: ignore very small regions
        if size < 0x1000:
            continue

        try:
            addr = base
            remaining = size
            while remaining > 0:
                read_size = min(chunk_size, remaining)
                try:
                    buf = pm.read_bytes(addr, read_size)
                except Exception:
                    break

                off = 0
                while True:
                    idx = buf.find(salt, off)
                    if idx == -1:
                        break
                    hit_addr = addr + idx
                    hits += 1

                    # Read a window around the hit and test nearby 32-byte candidates.
                    win_start = max(hit_addr - 0x200, 0)
                    try:
                        window = pm.read_bytes(win_start, 0x600)
                    except Exception:
                        window = b''

                    if window:
                        for k in range(0, len(window) - KEY_SIZE + 1, 8):
                            cand = window[k:k+KEY_SIZE]
                            if len(cand) != KEY_SIZE or cand == b'\x00' * KEY_SIZE:
                                continue
                            # Quick plausibility filters
                            printable = sum(1 for b in cand if 32 <= b <= 126)
                            if printable > 12:
                                continue
                            if len(set(cand)) < 20:
                                continue

                            ok, detail = verify_candidate_with_cases(cand, cases, allow_passphrase=False)
                            if ok:
                                print(f'[!!!] FOUND CORRECT KEY (salt-nearby): {cand.hex()}')
                                print(f'    hit_addr={hex(hit_addr)} win_start={hex(win_start)} detail={detail}')
                                return cand

                    off = idx + 1

                addr += read_size
                remaining -= read_size
        except Exception:
            continue

    print(f'[-] Salt-scan complete. salt hits={hits}. No key verified.')
    return None

def get_module_info(pm, module_name):
    for module in pm.list_modules():
        if module.name.lower() == module_name.lower():
            return module.lpBaseOfDll, module.SizeOfImage
    return None, None


def _is_probably_pointer(val: int) -> bool:
    # Basic sanity for user-space pointers on x64 Windows.
    return 0x10000 <= val <= 0x7FFFFFFFFFFF


def try_read_key_via_known_offset(pm, module_base: int, db_header_buf: bytes):
    try:
        ptr_loc = module_base + KEY_PTR_OFFSET_V41614
        ptr_bytes = pm.read_bytes(ptr_loc, 8)
        if not ptr_bytes or len(ptr_bytes) != 8:
            return None
        ptr = struct.unpack('<Q', ptr_bytes)[0]
        if not _is_probably_pointer(ptr):
            return None
        key = pm.read_bytes(ptr, KEY_SIZE)
        if not key or len(key) != KEY_SIZE:
            return None

        print(f'[*] Offset method candidate @ {hex(ptr_loc)} -> {hex(ptr)}: {key.hex()}')
        if verify_candidate(key, db_header_buf):
            print(f'[!!!] FOUND CORRECT KEY (offset method): {key.hex()}')
            return key
        return None
    except Exception:
        return None


def try_read_key_via_known_offset_verbose(pm, pid: int, module_name: str, module_base: int, db_header_buf: bytes):
    """Same as try_read_key_via_known_offset, but prints pointer diagnostics."""
    ptr_loc = module_base + KEY_PTR_OFFSET_V41614
    try:
        ptr_bytes = pm.read_bytes(ptr_loc, 8)
    except Exception as e:
        print(f'[-] PID={pid} {module_name} read ptr failed @ {hex(ptr_loc)}: {e}')
        return None

    if not ptr_bytes or len(ptr_bytes) != 8:
        print(f'[-] PID={pid} {module_name} ptr read empty @ {hex(ptr_loc)}')
        return None

    ptr = struct.unpack('<Q', ptr_bytes)[0]
    if ptr == 0:
        print(f'[-] PID={pid} {module_name} ptr=0 @ {hex(ptr_loc)} (key not initialized in this process/module?)')
        return None

    if not _is_probably_pointer(ptr):
        print(f'[-] PID={pid} {module_name} ptr not plausible: {hex(ptr)} @ {hex(ptr_loc)}')
        return None

    try:
        key = pm.read_bytes(ptr, KEY_SIZE)
    except Exception as e:
        print(f'[-] PID={pid} {module_name} read key failed @ {hex(ptr)}: {e}')
        return None

    if not key or len(key) != KEY_SIZE:
        print(f'[-] PID={pid} {module_name} key read invalid len @ {hex(ptr)}')
        return None

    print(f'[*] PID={pid} {module_name} offset candidate @ {hex(ptr_loc)} -> {hex(ptr)}: {key.hex()}')
    if verify_candidate(key, db_header_buf):
        print(f'[!!!] FOUND CORRECT KEY (offset method) PID={pid} {module_name}: {key.hex()}')
        return key

    print(f'[-] PID={pid} {module_name} candidate did NOT verify')
    return None


def find_key_by_offset_across_processes(db_header_buf: bytes):
    """Iterate all Weixin/WeChat processes and try the known offset in Weixin.dll/WeChatWin.dll."""
    try:
        import psutil
    except ImportError:
        print('psutil not installed.')
        return None

    candidates = []
    for proc in psutil.process_iter(['pid', 'name']):
        name = (proc.info.get('name') or '').lower()
        if name in ['wechat.exe', 'weixin.exe']:
            candidates.append(proc)

    if not candidates:
        print('WeChat/Weixin not running.')
        return None

    # Heuristic: try larger working sets first (often the main UI process).
    def _rss(p):
        try:
            return p.memory_info().rss
        except Exception:
            return 0

    candidates.sort(key=_rss, reverse=True)

    print('[*] Candidate processes (sorted by RSS):')
    for proc in candidates:
        try:
            print(f'    PID={proc.pid} name={proc.name()} rss={_rss(proc)}')
        except Exception:
            print(f'    PID={proc.pid} name=? rss={_rss(proc)}')

    for proc in candidates:
        pid = proc.pid
        try:
            pm = pymem.Pymem(pid)
        except Exception as e:
            print(f'[-] PID={pid} attach failed: {e}')
            continue

        any_module = False
        for module_name in ['WeChatWin.dll', 'Weixin.dll']:
            try:
                base, _size = get_module_info(pm, module_name)
            except Exception:
                base = None
            if not base:
                continue

            any_module = True
            print(f'[*] PID={pid} has {module_name} base={hex(base)}')

            # Poll a bit: some builds initialize the key lazily (after login / after opening chats).
            for _attempt in range(1, 16):
                key = try_read_key_via_known_offset_verbose(pm, pid, module_name, base, db_header_buf)
                if key:
                    return {'pid': pid, 'module': module_name, 'key': key}
                time.sleep(1)

        if not any_module:
            print(f'[-] PID={pid} has neither WeChatWin.dll nor Weixin.dll loaded')

    return None

def verify_candidate(key_bytes, db_header_buf):
    cases = build_verification_cases(db_header_buf)
    ok, detail = verify_candidate_with_cases(key_bytes, cases, verbose=False)
    if ok:
        print(f"[!!!] SUCCESS! Verified {detail}")
    return ok


def build_verification_cases(db_header_buf: bytes):
    """Precompute page slicing and stored MAC for a small set of likely SQLCipher-like configs."""
    if not db_header_buf or len(db_header_buf) < (SALT_SIZE + 1024):
        return []

    # Prefer common sizes first.
    page_sizes = [4096, 16384, 8192, 1024, 32768]

    # Allow KDF hash != MAC hash (some SQLCipher variants separate these).
    mac_algos = [
        (SHA512, 64),
        (SHA256, 32),
        (SHA1, 20),
    ]
    kdf_algos = [SHA512, SHA256, SHA1]
    iters = [256000, 64000, 4000]
    masks = [0x3a, 0]

    configs = []
    for (mac_algo, mac_size) in mac_algos:
        for kdf_algo in kdf_algos:
            for it in iters:
                for mask in masks:
                    configs.append({'iter': it, 'kdf_algo': kdf_algo, 'mac_algo': mac_algo, 'mac_size': mac_size, 'mask': mask})

    salt = db_header_buf[:SALT_SIZE]
    page_nos = [struct.pack('<I', 1), struct.pack('>I', 1)]
    msg_offsets = [SALT_SIZE, 0]
    cases = []
    for p_size in page_sizes:
        if len(db_header_buf) < p_size:
            continue
        first_page_data = db_header_buf[SALT_SIZE:p_size]
        if len(first_page_data) != p_size - SALT_SIZE:
            continue
        page = salt + first_page_data

        for conf in configs:
            mac_salt = bytes(x ^ conf['mask'] for x in salt)

            reserve = IV_SIZE + conf['mac_size']
            reserve = ((reserve + AES_BLOCK_SIZE - 1) // AES_BLOCK_SIZE) * AES_BLOCK_SIZE
            end = len(page)

            # Layout assumption (matches existing scripts in this repo): page end contains [IV][HMAC][padding].
            stored_mac = page[end - reserve + IV_SIZE: end - reserve + IV_SIZE + conf['mac_size']]
            if len(stored_mac) != conf['mac_size']:
                continue

            for msg_off in msg_offsets:
                msg = page[msg_off:end - reserve + IV_SIZE]
                for page_no in page_nos:
                    cases.append((p_size, conf, mac_salt, msg, stored_mac, page_no, salt, msg_off))

    return cases


def verify_candidate_with_cases(key_bytes: bytes, cases, verbose: bool = False, allow_passphrase: bool = True):
    """Try derived-key mode first (fast), optionally passphrase mode (slow)."""
    if not key_bytes or len(key_bytes) != KEY_SIZE or not cases:
        return False, ''

    # Fast path: treat key_bytes as derived key.
    for (p_size, conf, mac_salt, msg, stored_mac, page_no, _salt, _msg_off) in cases:
        try:
            mac_key = PBKDF2(key_bytes, mac_salt, dkLen=KEY_SIZE, count=2, hmac_hash_module=conf['kdf_algo'])
            mac = HMAC.new(mac_key, msg=msg + page_no, digestmod=conf['mac_algo']).digest()
            if mac == stored_mac:
                detail = f"ModeB(derived-key) config={conf} page_size={p_size}"
                return True, detail
        except Exception:
            continue

    if allow_passphrase:
        # Slow path: treat key_bytes as passphrase; derive key then re-verify.
        for (p_size, conf, mac_salt, msg, stored_mac, page_no, salt, _msg_off) in cases:
            try:
                key_a = PBKDF2(key_bytes, salt, dkLen=KEY_SIZE, count=conf['iter'], hmac_hash_module=conf['kdf_algo'])
                mac_key = PBKDF2(key_a, mac_salt, dkLen=KEY_SIZE, count=2, hmac_hash_module=conf['kdf_algo'])
                mac = HMAC.new(mac_key, msg=msg + page_no, digestmod=conf['mac_algo']).digest()
                if mac == stored_mac:
                    detail = f"ModeA(passphrase) config={conf} page_size={p_size}"
                    return True, detail
            except Exception:
                continue

    return False, ''


def _parse_pe_sections(pe_path: str):
    """Minimal PE section parser (PE32+). Returns list of (name, virtual_address, virtual_size)."""
    with open(pe_path, 'rb') as f:
        data = f.read()

    if len(data) < 0x100:
        return []
    if data[:2] != b'MZ':
        return []

    e_lfanew = struct.unpack_from('<I', data, 0x3C)[0]
    if e_lfanew <= 0 or e_lfanew + 4 + 20 > len(data):
        return []
    if data[e_lfanew:e_lfanew+4] != b'PE\x00\x00':
        return []

    # IMAGE_FILE_HEADER
    file_header_off = e_lfanew + 4
    number_of_sections = struct.unpack_from('<H', data, file_header_off + 2)[0]
    size_of_optional_header = struct.unpack_from('<H', data, file_header_off + 16)[0]

    optional_header_off = file_header_off + 20
    if optional_header_off + size_of_optional_header > len(data):
        return []

    # PE32+ magic 0x20b
    magic = struct.unpack_from('<H', data, optional_header_off)[0]
    if magic not in (0x20B, 0x10B):
        return []

    section_table_off = optional_header_off + size_of_optional_header
    sections = []
    for i in range(number_of_sections):
        off = section_table_off + i * 40
        if off + 40 > len(data):
            break
        name = data[off:off+8].rstrip(b'\x00').decode('ascii', errors='ignore')
        virtual_size = struct.unpack_from('<I', data, off + 8)[0]
        virtual_address = struct.unpack_from('<I', data, off + 12)[0]
        if virtual_size == 0:
            continue
        sections.append((name, virtual_address, virtual_size))
    return sections


def scan_weixin_module_sections_for_key(pid: int, db_header_buf: bytes):
    """Scan Weixin.dll .data/.rdata for pointers to a 32-byte key that verifies the DB header."""
    try:
        pm = pymem.Pymem(pid)
    except Exception as e:
        print(f'[-] Could not attach to PID={pid}: {e}')
        return None

    base, size = get_module_info(pm, 'Weixin.dll')
    if not base:
        print('[-] Weixin.dll not found in target process.')
        return None

    # Discover module file path via pymem.
    dll_path = None
    try:
        for m in pm.list_modules():
            if m.name.lower() == 'weixin.dll':
                dll_path = getattr(m, 'filename', None)
                break
    except Exception:
        dll_path = None

    if not dll_path or not os.path.exists(dll_path):
        print('[-] Could not resolve Weixin.dll on-disk path for PE parsing.')
        return None

    print(f'[*] Scanning Weixin.dll sections for key pointers: PID={pid} base={hex(base)} path={dll_path}')

    sections = _parse_pe_sections(dll_path)
    if not sections:
        print('[-] PE parsing failed; cannot locate sections.')
        return None

    allow_rdata = os.environ.get('SCAN_RDATA', '').strip() in {'1', 'true', 'TRUE', 'yes', 'YES'}
    wanted = [s for s in sections if s[0] == '.data']
    if allow_rdata:
        wanted += [s for s in sections if s[0] == '.rdata']
    if not wanted:
        print('[-] No sections selected for scanning (.data missing, or .rdata disabled).')
        return None

    cases = build_verification_cases(db_header_buf)
    if not cases:
        print('[-] DB header buffer too small or invalid for verification.')
        return None

    seen_ptrs = set()
    for (sec_name, va, vsz) in wanted:
        start = base + va
        end = start + vsz
        print(f'[*] Section {sec_name}: {hex(start)} - {hex(end)} (size={vsz})')

        chunk_size = 1024 * 1024
        scanned_ptrs = 0
        addr = start
        while addr < end:
            read_size = min(chunk_size, end - addr)
            try:
                buf = pm.read_bytes(addr, read_size)
            except Exception:
                addr += read_size
                continue

            count = (len(buf) // 8)
            if count <= 0:
                addr += read_size
                continue
            values = struct.unpack(f'{count}Q', buf[:count*8])

            for val in values:
                if not _is_probably_pointer(val) or (val % 8) != 0:
                    continue
                if val in seen_ptrs:
                    continue
                seen_ptrs.add(val)

                try:
                    cand = pm.read_bytes(val, KEY_SIZE)
                except Exception:
                    continue
                if not cand or len(cand) != KEY_SIZE:
                    continue
                if cand == b'\x00' * KEY_SIZE:
                    continue

                scanned_ptrs += 1
                # During section scanning, only try derived-key mode (fast). Passphrase mode is prohibitively slow.
                ok, detail = verify_candidate_with_cases(cand, cases, allow_passphrase=False)
                if ok:
                    print(f'[!!!] FOUND CORRECT KEY (section scan): {cand.hex()}')
                    print(f'    PID={pid} ptr={hex(val)} detail={detail}')
                    return cand

            addr += read_size

            if scanned_ptrs and (scanned_ptrs % 20000) == 0:
                print(f'[*] {sec_name}: scanned {scanned_ptrs} candidate pointers...')

    print('[-] Section scan complete. No key verified.')
    return None


def pick_main_wechat_pid():
    """Pick the most likely main process (largest RSS) among weixin/wechat."""
    try:
        import psutil
    except ImportError:
        return None

    best_pid = None
    best_rss = -1
    for proc in psutil.process_iter(['pid', 'name']):
        name = (proc.info.get('name') or '').lower()
        if name not in ['wechat.exe', 'weixin.exe']:
            continue
        try:
            rss = proc.memory_info().rss
        except Exception:
            rss = 0
        if rss > best_rss:
            best_rss = rss
            best_pid = proc.pid
    return best_pid

def scan_for_key_via_pointers(pid, db_header_buf, phone, nickname):
    try:
        pm = pymem.Pymem(pid)
    except Exception as e:
        print(f'[-] Could not attach to process {pid}: {e}')
        return None

    print(f'[+] Attached to Process ID: {pid}')
    
    module_used = 'WeChatWin.dll'
    wechatwin_base, wechatwin_size = get_module_info(pm, module_used)
    if not wechatwin_base:
        print('[-] Could not find WeChatWin.dll, trying Weixin.dll...')
        module_used = 'Weixin.dll'
        wechatwin_base, wechatwin_size = get_module_info(pm, module_used)
        
    if not wechatwin_base:
        print('[-] Could not find WeChatWin.dll or Weixin.dll')
        return None
    
    print(f'[+] {module_used} Base: {hex(wechatwin_base)}, Size: {hex(wechatwin_size)}')

    # Fast path: try known offset-based extraction first.
    key = try_read_key_via_known_offset(pm, wechatwin_base, db_header_buf)
    if key:
        return key

    target_strings = [phone.encode('utf-8'), nickname.encode('utf-8')]
    target_addrs = []

    print('[*] Scanning heap for target strings...')
    regions = get_memory_regions(pm)
    print(f'[*] Found {len(regions)} memory regions.')
    for i, (start, size) in enumerate(regions):
        try:
            buf = pm.read_bytes(start, size)
            for target in target_strings:
                offset = 0
                while True:
                    idx = buf.find(target, offset)
                    if idx == -1:
                        break
                    addr = start + idx
                    target_addrs.append(addr)
                    offset = idx + len(target)
        except:
            continue
            
    if not target_addrs:
        print('[-] Could not find phone or nickname in memory.')
        return None
    
    print(f'[+] Found {len(target_addrs)} occurrences of target strings.')
    
    target_pages = set()
    for addr in target_addrs:
        page = addr >> 12
        target_pages.add(page)
        target_pages.add(page - 1)
        target_pages.add(page + 1)

    print(f'[*] Starting Global Pointer Scan in {module_used}...')
    
    chunk_size = 1024 * 1024 
    
    candidates_found = 0
    
    for offset in range(0, wechatwin_size, chunk_size):
        read_size = min(chunk_size, wechatwin_size - offset)
        try:
            buf = pm.read_bytes(wechatwin_base + offset, read_size)
            count = read_size // 8
            fmt = f'{count}Q'
            values = struct.unpack(fmt, buf[:count*8])
            
            for i, val in enumerate(values):
                if val < 0x10000 or val > 0x7fffffffffff:
                    continue
                
                if val % 8 != 0:
                    continue

                if (val >> 12) in target_pages:
                    ptr_loc = wechatwin_base + offset + i*8
                    
                    try:
                        struct_buf = pm.read_bytes(val, 4096)
                        for k in range(0, len(struct_buf) - 32, 8):
                            key_candidate = struct_buf[k:k+32]
                            
                            if key_candidate == b'\x00' * 32: continue
                            printable = sum(1 for b in key_candidate if 32 <= b <= 126)
                            if printable > 28: continue
                            
                            # Verify immediately
                            if verify_candidate(key_candidate, db_header_buf):
                                print(f'[!!!] FOUND CORRECT KEY: {key_candidate.hex()}')
                                print(f'    Pointer in DLL: {hex(ptr_loc)}')
                                print(f'    Offset: {hex(ptr_loc - wechatwin_base)}')
                                return
                            
                            if PRINT_UNVERIFIED_CANDIDATES:
                                print(f'[?] Unverified Candidate: {key_candidate.hex()}')
                            candidates_found += 1
                            
                    except:
                        pass

        except Exception as e:
            pass
            
    print('[-] Global Pointer Scan complete. No key verified.')
    return None

def main():
    import sys

    db_path = sys.argv[1] if len(sys.argv) > 1 else r'e:\WeChatMsg\test_header_16k.db'
    if not os.path.exists(db_path):
        print(f'Could not find DB header file: {db_path}')
        return

    with open(db_path, 'rb') as f:
        db_header_buf = f.read()

    # 1) Preferred: try known offset across ALL candidate processes.
    found = find_key_by_offset_across_processes(db_header_buf)
    if found:
        # Key is printed in the verbose function already; stop here.
        return

    # 1b) Targeted scan: search memory for the DB salt and test nearby candidates.
    try:
        main_pid = pick_main_wechat_pid()
        if main_pid:
            key = scan_for_key_near_db_salt(main_pid, db_header_buf)
            if key:
                return
    except Exception as e:
        print(f'[-] Salt-nearby scan failed: {e}')

    # 1c) Optional: scan Weixin.dll PE sections for key pointers (can be slow).
    if os.environ.get('ENABLE_SECTION_SCAN', '').strip() in {'1', 'true', 'TRUE', 'yes', 'YES'}:
        try:
            main_pid = pick_main_wechat_pid()
            if main_pid:
                key = scan_weixin_module_sections_for_key(main_pid, db_header_buf)
                if key:
                    return
        except Exception as e:
            print(f'[-] Section scan failed: {e}')

    # 2) Optional fallback: legacy pointer scan (requires phone/nickname to be present in process memory).
    if os.environ.get('ENABLE_POINTER_SCAN', '').strip() not in {'1', 'true', 'TRUE', 'yes', 'YES'}:
        print('[!] Offset method did not find a verified key.\n'
              '    If you are logged in, open any chat list window to force DB access, then re-run.\n'
              '    To run the slow pointer-scan fallback anyway: set ENABLE_POINTER_SCAN=1')
        return

    pid = get_wechat_pid(db_header_buf)
    if not pid:
        print('WeChat/Weixin not running or no accessible PID found.')
        return

    phone = os.environ.get('WX_PHONE', '18411901231')
    nickname = os.environ.get('WX_NICK', '凌意雪')
    print('[*] Offset method failed across processes; falling back to pointer scan (may be slow/noisy).')
    scan_for_key_via_pointers(pid, db_header_buf, phone, nickname)

if __name__ == '__main__':
    main()
