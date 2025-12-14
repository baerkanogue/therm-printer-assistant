#!/bin/bash

rm scripts/gui/qtui.py

pyuic6 -x qt/main.ui -o ./scripts/gui/qtui.py

echo "main.ui -> qtui.py"