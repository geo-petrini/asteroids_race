pip install pyinstaller
pyinstaller --onefile --noconsole race.py --icon=.\resources\icon.ico
copy .\dist\race.exe .