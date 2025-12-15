#!/bin/bash

rm scripts/gui/qtmain.py
rm scripts/gui/qtinfo.py

pyuic6 -x qt/main.ui -o ./scripts/gui/ui_main.py
pyuic6 -x qt/info.ui -o ./scripts/gui/ui_info.py

echo "main.ui -> ui_main.py"
echo "info.ui -> ui_info.py"