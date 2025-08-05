# DomCapture

DomCapture is a Python-based CLI tool for capturing website screenshots for bug bounty reconnaissance, inspired by [Aquatone](https://github.com/michenriksen/aquatone). Built for use in Kali Linux and designed to be flexible, modular, and ready for automation.

---

## 🛠 Features

- ✅ Single or list of URLs as input
- ✅ Headless Chrome (Selenium) for screenshot capture
- ✅ Live host check before capture
- ✅ Clickable HTML gallery + CSV report
- ✅ Metadata: status, title, timestamp, redirect chain
- ✅ Failed host logging
- ✅ Fully automated, semi-automated & custom modes
- ✅ Clean, readable CLI flags

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
python3 domcapture.py --input targets.txt --mode full --threads 5 --viewport 1366x768 --delay 3 --output screenshots/
```

### CLI Options

| Flag | Description |
|------|-------------|
| `--input` | Single URL or file path |
| `--output` | Screenshot output directory (default: ./screenshots) |
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

Built by [ramshaha](https://github.com/yourusername) — inspired by Aquatone & bug bounty recon.

---

## 🧪 License

This project is licensed under the MIT License - see the LICENSE file for details.
