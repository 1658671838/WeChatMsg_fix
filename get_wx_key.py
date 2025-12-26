import sys
import os
import psutil
import ctypes

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from wxManager.decrypt.remote_scanner import RemoteScanner
from wxManager.decrypt.version_config import get_config_for_version

def find_weixin_pid():
    # Find process with largest memory usage
    max_mem = 0
    target_pid = None
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == 'weixin.exe':
                mem = proc.info['memory_info'].rss
                if mem > max_mem:
                    max_mem = mem
                    target_pid = proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return target_pid

def main():
    print("正在寻找 Weixin.exe 进程...")
    pid = find_weixin_pid()
    if not pid:
        print("未找到运行中的 Weixin.exe 主进程。")
        return

    print(f"找到主进程 PID: {pid}")
    
    scanner = RemoteScanner(pid)
    
    print("正在获取 Weixin.dll 模块信息...")
    mod_info = scanner.get_module_info("Weixin.dll")
    if not mod_info:
        print("未找到 Weixin.dll 模块。")
        return
        
    print(f"Weixin.dll 基址: {hex(ctypes.cast(mod_info['base_address'], ctypes.c_void_p).value)}")
    print(f"Weixin.dll 大小: {mod_info['image_size']} bytes")
    
    # Assume version >= 4.1.4
    config = get_config_for_version("4.1.6.14")
    print(f"使用特征码配置: {config['version']}")
    
    print("正在扫描特征码 (这可能需要几秒钟)...")
    addr = scanner.find_pattern(mod_info, config['pattern'], config['mask'])
    
    if addr:
        target_func = addr + config['offset']
        print(f"SUCCESS! 找到目标函数地址: {hex(target_func)}")
        print(f"相对于基址偏移: {hex(target_func - ctypes.cast(mod_info['base_address'], ctypes.c_void_p).value)}")
        print("\n[注意] 这只是找到了 Key 处理函数的入口地址。")
        print("要获取 Key，需要在此处注入 Hook 代码 (Shellcode) 并重启微信触发调用。")
        print("由于 Python 无法直接注入 C++ Shellcode，建议使用编译好的 wx_key.dll 工具。")
    else:
        print("FAILED. 未找到特征码。可能版本不匹配或特征码已失效。")

if __name__ == '__main__':
    main()
