# DomCapture

DomCapture is a Python-based CLI tool for capturing website screenshots for bug bounty reconnaissance. Built for use in Kali Linux and designed to be flexible, modular, and ready for automation.

---

## 🛠 Features
1. ✅ Multi-Threaded Domain Screenshot Capture  
2. ✅ Custom Delay Between Captures  
3. ✅ Custom Viewport Support  
4. ✅ Proper Screenshot Naming  
5. ✅ Screenshot and Report Folder Organization  
6. ✅ Automatic CSV and HTML Report Generation  
7. ✅ Enhanced HTML Report View  
8. ✅ Proper Error Logging & Feedback  
9. ✅ Graceful Ctrl+C (KeyboardInterrupt) Handling  
10. ✅ Wait for Full Page Load Before Screenshot  
11. ✅ Headless Chrome Browser Control (Selenium + undetected_chromedriver)  
12. ✅ Custom Input File Support  
13. ✅ Support for PDF and Non-HTML Pages  
14. ✅ Failsafe Screenshot Format  
15. ✅ Portable Reports  
16. ✅ Title Extraction for Each Page  
17. ✅ URL Labeling Below Each Screenshot  
18. ✅ Single Screenshot per URL (No Overwrite Bug)  
19. ✅ Resizable Screenshot Display (HTML Report)

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
