#!/bin/bash

iwlist wlan0 scan | grep Frequency | sort | uniq -c | sort -n
