import sys
import os
import traceback

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from wxManager.decrypt.get_bias_addr import BiasAddr
    import psutil
except ImportError:
    print("请先安装依赖: pip install -r requirements.txt")
    sys.exit(1)

def get_wechat_pid():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'WeChat.exe':
            return proc.info['pid']
    return None

if __name__ == "__main__":
    print("="*50)
    print("WeChat v3 偏移获取工具")
    print("="*50)
    
    pid = get_wechat_pid()
    if not pid:
        print("❌ 未检测到 WeChat.exe 进程！")
        print("请先启动微信并登录，然后再运行此脚本。")
        print("注意：此工具仅适用于 WeChat v3 (3.9.x) 版本。")
        print("如果是 WeChat v4 (4.0.x)，通常无需手动获取偏移，直接运行主程序即可。")
        sys.exit(1)
    
    print("✅ 检测到微信进程 PID:", pid)
    print("\n请输入以下信息以辅助定位（直接回车跳过，但可能影响成功率）：")
    
    name = input("微信昵称 (Name): ").strip()
    account = input("微信号 (Account): ").strip()
    mobile = input("手机号 (Mobile): ").strip()
    
    print("\n🚀 正在扫描内存获取偏移，请稍候...")
    
    try:
        # BiasAddr(account, mobile, name, key, db_path)
        # Passing None or empty string if not provided
        bias_finder = BiasAddr(
            account if account else "None", 
            mobile if mobile else "None", 
            name if name else "None", 
            None, # Key
            None  # db_path
        )
        
        result = bias_finder.run()
        
        print("\n" + "="*50)
        print("🎉 扫描结果 (请复制以下内容):")
        print("="*50)
        print(result)
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        print("详细堆栈:")
        traceback.print_exc()
