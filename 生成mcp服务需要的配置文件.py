import os
import json

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 venv 和 main.py 的路径
venv_path = os.path.join(script_dir, 'venv', 'Scripts', 'python.exe')
main_path = os.path.join(script_dir, 'main.py')

# 定义 JSON 内容
json_content = {
    "mcpServers": {
        "PDFAnalyzer": {
            "command": venv_path,
            "args": [main_path]
        }
    }
}

# 写入 JSON 文件
with open(os.path.join(script_dir, 'mcp_config.json'), 'w', encoding='utf-8') as f:
    json.dump(json_content, f, ensure_ascii=False, indent=4)