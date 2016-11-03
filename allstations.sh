#!/bin/bash

hostapd_cli all_sta wlan0 | grep dot11RSNAStatsSTAAddress
