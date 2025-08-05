#!/bin/bash

echo "[*] Installing dependencies for DomCapture..."

# Update & install system packages
sudo apt update -y
sudo apt full-upgrade -y
sudo apt install -y python3 python3-pip chromium chromium-driver

# Make sure chromedriver is linked properly
if ! command -v chromedriver &> /dev/null; then
  echo "[!] chromedriver not found in PATH, attempting to link..."
  sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver
fi

# Install Python packages bypassing Kali PEP 668 protections
pip3 install --break-system-packages -r requirements.txt

echo "[+] Installation complete! 🎉"
echo "    Run the tool with:"
echo "    python3 domcapture.py --input targets.txt"

