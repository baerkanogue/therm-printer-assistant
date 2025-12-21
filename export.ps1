$ErrorActionPreference = "Stop"

& .\.venv\Scripts\Activate.ps1

pyinstaller --onefile --noconsole --icon=icons\printer3d.ico --add-data "samples\sample.jpg;samples" --add-data "icons\printer3d.ico;icons" --add-data "icons\logo.ico;icons" --name "ThermPrinter_Assistant" .\scripts\gui\main.py

pyinstaller --onefile --icon=icons\printer2d.ico --name "ThermPrinter_Assistant_TUI" .\scripts\tui\main.py 

pyinstaller --onefile --name "cm_inch_converter" .\scripts\cm_inch_convert.py

New-Item -ItemType Directory -Force -Path export | Out-Null
New-Item -ItemType Directory -Force -Path export/misc | Out-Null

Copy-Item dist/ThermPrinter_Assistant export/ThermPrinter_Assistant -Force
Copy-Item dist/ThermPrinter_Assistant_TUI export/misc/ThermPrinter_Assistant_TUI -Force
Copy-Item dist/cm_inch_converter export/misc/cm_inch_converter -Force

Copy-Item config.cfg export/config.cfg -Force
Copy-Item license.md export/misc/license.md -Force
Copy-Item portable_readme.txt export/misc/readme.txt -Force

Push-Location export
Compress-Archive -Path * -DestinationPath "TPA_windows_VERSION.zip" -Force
Pop-Location

Write-Output "export preparations done"
