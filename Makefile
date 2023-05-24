SHELL := /usr/bin/env bash
.SILENT: sinstall sbuild stest shelp

sinstall:
	python3 -m pip install -e .
sbuild:
	python3 -m pip build -e .
stest:
	chmod 777 src/fuad/test.py
	python3 src/fuad/test.py
shelp:
	xdg-open https://github.com/VBPROGER/fuad/wiki &
	python3 -c 'import fuad; help(fuad)'