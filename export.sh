source .venv/bin/activate

pyinstaller --onefile --add-data "samples/sample.jpg:samples" --add-data "icons/printer3d.ico:icons" --add-data "icons/logo.ico:icons" --name "ThermPrinter_Assistant" scripts/gui/main.py
pyinstaller --onefile --name "ThermPrinter_Assistant_TUI" scripts/tui/main.py
pyinstaller --onefile --name "cm_inch_converter" scripts/cm_inch_convert.py

mkdir export
mkdir export/misc

cp dist/ThermPrinter_Assistant export/ThermPrinter_Assistant
cp dist/ThermPrinter_Assistant_TUI export/misc/ThermPrinter_Assistant_TUI
cp dist/cm_inch_converter export/misc/cm_inch_converter

cp config.cfg export/config.cfg
cp license.md export/misc/license.md
cp portable_readme.txt export/misc/readme.txt

cd export
tar -czvf TPA_linux_VERSION.tar.gz .
cd -

echo export preparations done
