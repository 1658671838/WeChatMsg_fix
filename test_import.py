import sys
import os

print("=== Python路径检查 ===")
print(f"当前工作目录: {os.getcwd()}")
print(f"脚本所在目录: {os.path.dirname(os.path.abspath(__file__))}")
print("\n系统路径(sys.path):")
for i, path in enumerate(sys.path[:10]):  # 只显示前10个
    print(f"  {i}: {path}")

print(f"\n'wxManager'目录存在吗? {os.path.exists('wxManager')}")
print(f"'wxManager/__init__.py'存在吗? {os.path.exists('wxManager/__init__.py')}")

print("\n=== 尝试导入 ===")
try:
    from wxManager import Me
    print("✓ 导入成功!")
except ImportError as e:
    print(f"✗ 导入失败: {e}")
    print("\n尝试手动添加路径...")
    # 添加当前目录到路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from wxManager import Me
        print("✓ 手动添加路径后导入成功!")
    except ImportError as e2:
        print(f"✗ 仍然失败: {e2}")