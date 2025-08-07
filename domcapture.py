#!/usr/bin/env python3

import os
import csv
import sys
import time
import signal
import queue
import hashlib
import argparse
import threading
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

# Timestamp folders
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
screenshot_dir = f"screenshots/screenshot-{timestamp}"
report_dir = f"reports/report-{timestamp}"
os.makedirs(screenshot_dir, exist_ok=True)
os.makedirs(report_dir, exist_ok=True)
csv_report = os.path.join(report_dir, "report.csv")
html_report = os.path.join(report_dir, "report.html")

# Global state
results = []
exit_event = threading.Event()

def signal_handler(sig, frame):
    if exit_event.is_set():
        print("[✖] Force exiting now...")
        sys.exit(1)
    print("\n[INF] CTRL+C pressed: Exiting")
    exit_event.set()
    generate_reports()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def wait_for_load(driver):
    try:
        return driver.execute_script("return document.readyState") == "complete"
    except Exception:
        return False

def capture(driver, url, output_path):
    try:
        driver.set_page_load_timeout(25)
        driver.get(url)
        time.sleep(2)
        for _ in range(20):
            if wait_for_load(driver):
                break
            time.sleep(0.5)
        title = driver.title or "Untitled"
        driver.save_screenshot(output_path)
        return "Success", title
    except TimeoutException:
        return "Timeout", "-"
    except WebDriverException as e:
        return f"Failed: {str(e).splitlines()[0]}", "-"
    except Exception as e:
        return f"Failed: {e}", "-"

def worker(q, delay, viewport):
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--window-size={viewport}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    while not q.empty() and not exit_event.is_set():
        url = q.get()
        hash_id = hashlib.md5(url.encode()).hexdigest()[:6]
        parsed = urlparse(url)
        domain = parsed.netloc.replace(":", "_")
        filename = f"{domain}-{hash_id}.png"
        screenshot_path = os.path.join(screenshot_dir, filename)

        print(f"[+] Capturing: {url}")
        status, title = capture(driver, url, screenshot_path)
        if "Success" in status:
            print(f"    [✔] Screenshot saved: {screenshot_path}")
        else:
            print(f"    [✖] Failed to capture: {url} ({status})")

        results.append((url, title, status, screenshot_path if "Success" in status else "-"))
        time.sleep(delay)

    driver.quit()

def generate_reports():
    with open(csv_report, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Page Title", "Status", "Screenshot"])
        for row in results:
            writer.writerow(row)

    with open(html_report, "w") as f:
        f.write("<html><head><title>DomCapture Screenshots</title></head>")
        f.write("<body style='text-align:center; font-family:sans-serif;'>\n")
        f.write(f"<h2>DomCapture Screenshot Report – {timestamp}</h2>\n")
        for url, title, status, screenshot in results:
            if screenshot != "-":
                abs_path = os.path.abspath(screenshot)
                f.write(f"<div style='margin: 40px auto;'>\n")
                f.write(f"<h3>{title}</h3>\n")
                f.write(f"<img src='file://{abs_path}' style='max-width: 90%; border: 2px solid black;'>\n")
                f.write(f"<p style='color: #333; margin-top: 5px;'><a href='{url}' target='_blank'>{url}</a></p>\n")
                f.write("</div>\n")
        f.write("</body></html>")
    print(f"[✔] Reports saved: {csv_report}, {html_report}")

def main(input_file, threads, delay, viewport):
    with open(input_file) as f:
        urls = [line.strip() for line in f if line.strip()]
    q = queue.Queue()
    for url in urls:
        q.put(url)

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(q, delay, viewport))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    generate_reports()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input file with URLs")
    parser.add_argument("--threads", type=int, default=2, help="Number of threads")
    parser.add_argument("--delay", type=int, default=2, help="Delay between screenshots")
    parser.add_argument("--viewport", default="1366x768", help="Browser viewport size")
    args = parser.parse_args()
    main(args.input, args.threads, args.delay, args.viewport)
