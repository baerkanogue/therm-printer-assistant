mkdir export
mkdir export/misc

cp dist/ThermPrinter_Assistant export/ThermPrinter_Assistant
cp dist/ThermPrinter_Assistant_TUI export/misc/ThermPrinter_Assistant_TUI
cp dist/cm_inch_converter export/misc/cm_inch_converter

cp config.cfg export/config.cfg
cp license.md export/misc/license.md
cp portable_readme.txt export/misc/readme.txt

cd export
tar -czvf ThermPrinter_Assistant_linux_VERSION.tar.gz .
cd -

