"""
Verify installation and configuration of the Multi-Agent Company Research System.
Run this script after installation to check if everything is set up correctly.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.9 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version: {version.major}.{version.minor}.{version.micro} (requires 3.9+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        "langgraph",
        "langsmith",
        "langchain_community",
        "langchain_google_genai",
        "tavily",
        "streamlit",
        "plotly",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (not installed)")
            missing.append(package)
    
    return len(missing) == 0


def check_env_file():
    """Check if .env file exists and has required keys."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Run: copy .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Check for required keys
    with open(env_path) as f:
        content = f.read()
    
    required_keys = ["GOOGLE_API_KEY", "TAVILY_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if key in content and "your_" not in content.split(key)[1].split("\n")[0]:
            print(f"✅ {key} configured")
        else:
            print(f"⚠️  {key} not configured")
            missing_keys.append(key)
    
    return len(missing_keys) == 0


def check_project_structure():
    """Check if project structure is correct."""
    required_dirs = ["src", "src/agent", "src/agents", "src/graph", "src/tools", "src/ui", "docs"]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (missing)")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("🔍 Multi-Agent Company Research System - Setup Verification")
    print("=" * 60)
    print()
    
    print("📦 Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("📚 Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("🔑 Checking environment configuration...")
    env_ok = check_env_file()
    print()
    
    print("📁 Checking project structure...")
    structure_ok = check_project_structure()
    print()
    
    print("=" * 60)
    if python_ok and deps_ok and env_ok and structure_ok:
        print("✅ All checks passed! You're ready to go!")
        print()
        print("Next steps:")
        print("  1. Run the UI: streamlit run ui.py")
        print("  2. Or test the system: python test_intelligent_graph_quick.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        if not deps_ok:
            print("To install dependencies:")
            print("  pip install -r requirements.txt")
        if not env_ok:
            print("To configure API keys:")
            print("  1. Copy .env.example to .env")
            print("  2. Edit .env and add your API keys")
    print("=" * 60)


if __name__ == "__main__":
    main()
