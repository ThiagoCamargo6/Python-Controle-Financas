@echo off
echo Iniciando o Painel Financeiro...

REM Navega para a pasta do projeto. Use o caminho absoluto.
cd /d "C:\Users\Thiago\Desktop\Python\4. Controle_Despesas"

REM Executa o Streamlit. Use o caminho absoluto para o executável do streamlit.
REM Para descobrir o caminho, digite 'where streamlit' no seu terminal.
"C:\Users\Thiago\AppData\Local\Programs\Python\Python313\Scripts\streamlit.exe" run main.py