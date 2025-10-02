@echo off
REM Launch Pattern Chat Dashboard (Streamlit)
cd /d %~dp0
streamlit run pattern_chat_dashboard.py
pause
