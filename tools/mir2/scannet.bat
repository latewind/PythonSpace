for /f "tokens=2" %%i in ('netstat -no ^|findStr "43.227"') do set ip=%%i  

set ifo=%ip%
set port=%ifo:~-7%

echo %port%
cd  D:/PythonSpace/tools/mir2/
D:

D:\Env\venv\Scripts\python.exe D:/PythonSpace/tools/mir2/scannet.py %port%
pause