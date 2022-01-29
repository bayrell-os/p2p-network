#!/bin/bash

yes | rm ./dist/p2p_network_1_0_win.zip

zip -r9 ./dist/p2p_network_1_0_win.zip ./dist/p2p_network_1_0_win ./p2p_network \
	./run_network.bat ./TAP-Drivers ./peervpn ./peervpn_start_32bit.bat \
	./peervpn_start_64bit.bat

# ./run ./run_debug.bat ./zip_win64.sh ./compile.bat 