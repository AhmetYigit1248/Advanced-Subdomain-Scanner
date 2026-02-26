# 🦅 RapidRecon - Advanced Subdomain Discovery

RapidRecon is a highly optimized, blazing-fast Python tool and Jupyter UI for subdomain enumeration and validation. Built specifically for Bug Bounty Hunters, Penetration Testers, and Security Engineers.

Unlike traditional tools that dump thousands of dead DNS records, RapidRecon actively probes targets, filters out the noise, and delivers a clean, actionable list of **live** web assets.

## ⚡ Features

* **🟢 Live Target Validation:** Automatically filters out dead, parked, or strictly internal DNS records using active HTTP/HTTPS probing.
* **🕵️‍♂️ Deep Enrichment:** Extracts IP addresses, open ports, HTTP status codes, and CNAME resolution chains.
* **🛡️ CDN & Tech Detection:** Instantly identifies if a target is hiding behind Cloudflare, AWS CloudFront, Akamai, Vercel, etc., along with basic server headers.
* **🚀 Blazing Fast:** Powered by an asynchronous reactive backend. Scans typically complete in under 1 minute.
* **📊 Jupyter UI Ready:** Comes with an interactive, beautifully formatted Pandas DataFrame UI for Jupyter Lab/Notebook users.

---

## 🔑 Prerequisites: Getting Your Free API Key

RapidRecon uses the powerful **Advanced Subdomain Scanner API** as its backend engine. To use this tool, you need an API key.

1. Go to the RapidAPI page: 👉 **[Advanced Subdomain Scanner API]([https://rapidapi.com/yigitahmet248/api/advanced-subdomain-scanner])**
2. Click on the **Pricing** tab and subscribe to the **FREE Basic Plan** (Allows 5 deep scans per day).
3. Copy your `X-RapidAPI-Key` from the endpoint testing playground.

---

## 🛠️ Installation

1. Clone the repository:
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/RapidRecon.git](https://github.com/YOUR_GITHUB_USERNAME/RapidRecon.git)
cd RapidRecon
```