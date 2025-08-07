# DomCapture

DomCapture is a Python-based CLI tool for capturing website screenshots for bug bounty reconnaissance. Built for use in Kali Linux and designed to be flexible, modular, and ready for automation.

---

## 🛠 Features

✅ Multi-Threaded Domain Screenshot Capture
✅ Custom Delay Between Captures
✅ Custom Viewport Support
✅ Proper Screenshot Naming
✅ Screenshot and Report Folder Organization
✅ Automatic CSV and HTML Report Generation
✅ Enhanced HTML Report View
✅ Proper Error Logging & Feedback
✅ Graceful Ctrl+C (KeyboardInterrupt) Handling
✅ Wait for Full Page Load Before Screenshot
✅ Headless Chrome Browser Control (Selenium + undetected_chromedriver)
✅ Custom Input File Support
✅ Support for PDF and Non-HTML Pages
✅ Failsafe Screenshot Format
✅ Portable Reports
✅ Title Extraction for Each Page
✅ URL Labeling Below Each Screenshot
✅ Single Screenshot per URL (No Overwrite Bug)
✅ Resizable Screenshot Display (HTML Report)
---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/domcapture.git
cd domcapture
chmod +x install.sh
./install.sh
```

---

## ⚙️ Usage

```bash
python3 domcapture.py --input Target_list.txt --threads 3 --delay 6 --viewport 1366x768
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--input` | Single URL or file path |
| `--threads` | Number of threads (default: 3) |
| `--delay` | Delay (in seconds) after page load |
| `--viewport` | Viewport size (e.g., 1366x768) |

---

## 📂 Output Structure

```
DomCapture/
├── screenshots/
│   ├── example.com.png
│   └── failed/
│       └── broken.com.log
├── reports/
│   ├── report.csv
│   └── report.html
```

---

## 👨‍💻 Author

Built by [SHIVRAJ-KHANDEKAR]( https://github.com/Shivraj-33)

---

## 🧪 License

This project is licensed under the MIT License - see the LICENSE file for details.
