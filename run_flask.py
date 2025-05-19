#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import time
from pathlib import Path


def main():
    # 获取项目根目录（脚本所在目录）
    project_dir = Path(__file__).parent.resolve()
    print(f"项目目录: {project_dir}")

    # 确定虚拟环境目录
    if platform.system() == "Windows":
        venv_dir = project_dir / ".venv" / "Scripts"
        python_exe = venv_dir / "python.exe"
        activate_script = venv_dir / "activate.bat"
    else:
        venv_dir = project_dir / ".venv" / "bin"
        python_exe = venv_dir / "python"
        activate_script = venv_dir / "activate"

    # 检查虚拟环境是否存在
    if not python_exe.exists():
        print("错误：未找到虚拟环境！请确保已在项目目录下创建了.venv虚拟环境。")
        sys.exit(1)

    print("正在激活虚拟环境...")

    # 检查Flask是否已安装
    print("正在检查Flask是否已安装...")
    try:
        result = subprocess.run(
            [str(python_exe), "-m", "pip", "show", "flask"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("错误：虚拟环境中未安装Flask！")
            print("请在虚拟环境中运行: pip install flask")
            sys.exit(1)
        print(f"已安装 Flask {result.stdout.splitlines()[1].split(':')[1].strip()}")
    except Exception as e:
        print(f"错误：检查Flask安装时出错 - {e}")
        sys.exit(1)

    # 设置Flask应用（可根据实际情况修改）
    flask_app = "flask_demo.py"  # 修改为你的Flask应用入口文件
    app_path = project_dir / flask_app

    # 检查应用文件是否存在
    if not app_path.exists():
        print(f"警告：指定的Flask应用文件不存在！")
        print(f"当前设置: {flask_app}")
        print(f"请确认文件名是否正确，或修改此脚本中的flask_app变量。")
        print("-" * 50)

    # 启动Flask应用
    print("正在启动Flask应用...")
    print("访问地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务器")
    print("-" * 50)

    try:
        # 设置环境变量并启动Flask
        env = os.environ.copy()
        env["FLASK_APP"] = flask_app
        env["FLASK_ENV"] = "development"

        # 启动Flask服务器
        subprocess.run([str(python_exe), "-m", "flask", "run"], env=env)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"错误：启动Flask应用时出错 - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
