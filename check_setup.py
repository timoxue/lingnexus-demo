"""环境配置检查工具

运行此脚本检查 LingNexus 所需的依赖是否正确安装
"""

import sys
from typing import List, Tuple, Optional

def check_python_version() -> Tuple[bool, str]:
    """检查 Python 版本"""
    version = sys.version_info
    if version >= (3, 9):
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"❌ Python 版本过低 ({version.major}.{version.minor})，需要 >= 3.9"

def check_package(package_name: str, import_name: Optional[str] = None) -> Tuple[bool, str]:
    """检查 Python 包是否已安装"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', '未知版本')
        return True, f"✅ {package_name} ({version})"
    except ImportError:
        return False, f"❌ {package_name} 未安装"

def check_api_key() -> Tuple[bool, str]:
    """检查 API Key 配置"""
    import json
    import os
    
    config_path = "./config/model_config.json"
    
    if not os.path.exists(config_path):
        return False, "❌ config/model_config.json 不存在"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        configured_models = []
        for config in configs:
            api_key = config.get('api_key', '')
            model_name = config.get('config_name', '未知')
            
            if api_key and api_key != "YOUR_DASHSCOPE_API_KEY" and api_key != "YOUR_DEEPSEEK_API_KEY" and api_key != "YOUR_GEMINI_API_KEY":
                configured_models.append(model_name)
        
        if configured_models:
            return True, f"✅ 已配置模型: {', '.join(configured_models)}"
        else:
            return False, "⚠️  未配置任何 API Key（请编辑 config/model_config.json）"
    
    except Exception as e:
        return False, f"❌ 配置文件读取失败: {str(e)}"

def main():
    """主检查流程"""
    print("=" * 60)
    print("🔍 LingNexus 环境配置检查")
    print("=" * 60)
    print()
    
    checks: List[Tuple[bool, str]] = []
    
    # 1. Python 版本
    print("[1/6] 检查 Python 版本...")
    result = check_python_version()
    checks.append(result)
    print(f"      {result[1]}")
    print()
    
    # 2. 核心依赖
    print("[2/6] 检查 AgentScope...")
    result = check_package("agentscope")
    checks.append(result)
    print(f"      {result[1]}")
    print()
    
    print("[3/6] 检查 RDKit...")
    result = check_package("rdkit", "rdkit")
    checks.append(result)
    print(f"      {result[1]}")
    if not result[0]:
        print("      💡 提示: 使用 conda install -c conda-forge rdkit")
    print()
    
    print("[4/6] 检查 Gradio（图形界面）...")
    result = check_package("gradio")
    checks.append(result)
    print(f"      {result[1]}")
    print()
    
    print("[5/6] 检查 DashScope（Qwen API）...")
    result = check_package("dashscope")
    checks.append(result)
    print(f"      {result[1]}")
    print()
    
    # 3. API Key 配置
    print("[6/6] 检查 API Key 配置...")
    result = check_api_key()
    checks.append(result)
    print(f"      {result[1]}")
    print()
    
    # 总结
    print("=" * 60)
    passed = sum(1 for check in checks if check[0])
    total = len(checks)
    
    if passed == total:
        print(f"🎉 恭喜！所有检查通过 ({passed}/{total})")
        print()
        print("✅ 您可以开始使用 LingNexus：")
        print("   - 图形界面: python app.py")
        print("   - 命令行: python main.py")
    else:
        print(f"⚠️  部分检查未通过 ({passed}/{total})")
        print()
        print("📝 请按照提示安装缺失的依赖：")
        print("   pip install -r requirements.txt")
        print()
        print("   或使用 conda 安装 RDKit：")
        print("   conda install -c conda-forge rdkit")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
