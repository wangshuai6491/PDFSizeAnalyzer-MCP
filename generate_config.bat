@echo off
set "venvPath=%~dp0venv\Scripts\python.exe"
set "mainPath=%~dp0main.py"
set "jsonContent={\"mcpServers\":{\"PDFAnalyzer\":{\"command\":\"%venvPath%\",\"args\":[\"%mainPath%\"]}}}"
(echo %jsonContent%) > mcp_config.json