# domcapture.py
#!/usr/bin/env python3

import os
import sys
import time
import csv
import argparse
import threading
import logging
import requests
import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

# Setup logging
logging.basicConfig(filename='domcapture.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global lock for threading
print_lock = threading.Lock()

# Prepare folders
def setup_dirs(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "failed"), exist_ok=True)
    os.makedirs("reports", exist_ok=True)

def get_driver(viewport, headers=None, cookies=None):
    options = Options()
    options.headless = True
    options.add_argument(f"--window-size={viewport}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def is_live(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except:
        return False

def take_screenshot(driver, url, output_path, delay):
    try:
        driver.get(url)
        time.sleep(delay)
        title = driver.title or "No Title"

        # Build a safe filename from URL
        parsed_url = urlparse(url)
        safe_path = parsed_url.path.replace("/", "_").strip("_")
        if not safe_path:
            safe_path = "root"
        filename = f"{parsed_url.netloc}_{safe_path}.png"
        screenshot_path = os.path.join(output_path, filename)

        driver.save_screenshot(screenshot_path)
        return (screenshot_path, title, "OK")

    except TimeoutException:
        return (None, None, "Timeout")
    except WebDriverException as e:
        return (None, None, str(e))

def process_url(url, args, writer):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"http://{url}"

    with print_lock:
        print(f"[*] Processing: {url}")

    if not is_live(url):
        with open(os.path.join(args.output, "failed", f"{urlparse(url).netloc}.log"), "w") as f:
            f.write("Host did not respond or is down.")
        writer.writerow([url, "FAIL", "N/A", "N/A", "N/A"])
        return

    try:
        driver = get_driver(args.viewport)
        screenshot_path, title, status = take_screenshot(driver, url, args.output, args.delay)
        driver.quit()
    except Exception as e:
        screenshot_path = None
        title = None
        status = str(e)

    if screenshot_path:
        writer.writerow([url, "SUCCESS", title, datetime.datetime.now().isoformat(), screenshot_path])
    else:
        writer.writerow([url, status, "N/A", "N/A", "N/A"])
        with open(os.path.join(args.output, "failed", f"{urlparse(url).netloc}.log"), "w") as f:
            f.write(status)

def build_html_report(csv_path, html_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    with open(html_path, "w") as f:
        f.write("<html><head><title>DomCapture Report</title></head><body><h1>Screenshot Report</h1><ul>")
        for row in rows[1:]:
            if row[1] == "SUCCESS":
                f.write(f"<li><b>{row[0]}</b><br><img src='../{row[4]}' width='500'><br>{row[2]}<br><br></li>")
        f.write("</ul></body></html>")

def main():
    parser = argparse.ArgumentParser(description="DomCapture - Web Screenshot Recon Tool")
    parser.add_argument("--input", required=True, help="Single URL or file containing URLs")
    parser.add_argument("--output", default="screenshots", help="Directory to save screenshots")
    parser.add_argument("--threads", type=int, default=3, help="Number of threads")
    parser.add_argument("--delay", type=int, default=3, help="Wait time after page load (seconds)")
    parser.add_argument("--viewport", default="1366x768", help="Viewport size, e.g. 1366x768")
    args = parser.parse_args()

    setup_dirs(args.output)

    if os.path.isfile(args.input):
        with open(args.input) as f:
            urls = list(set([line.strip() for line in f if line.strip()]))
    else:
        urls = [args.input]

    csv_path = os.path.join("reports", "report.csv")
    html_path = os.path.join("reports", "report.html")
    csvfile = open(csv_path, "w", newline='')
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Status", "Title", "Timestamp", "Screenshot"])

    threads = []
    for url in urls:
        t = threading.Thread(target=process_url, args=(url, args, writer))
        t.start()
        threads.append(t)
        while threading.active_count() > args.threads:
            time.sleep(0.1)

    for t in threads:
        t.join()

    csvfile.close()
    build_html_report(csv_path, html_path)
    print("[+] Done. Report generated in 'reports/'")

if __name__ == "__main__":
    main()
