# -*- coding: utf-8 -*-

import ipywidgets as widgets
from IPython.display import display, clear_output
import requests
import time
import pandas as pd

API_HOST = "advanced-subdomain-scanner.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}/api/v1"

# UI Components
title = widgets.HTML("<h2>🚀 RapidRecon Subdomain Discovery</h2><p>Enter a target domain to extract live targets, open ports, and CDN information.</p>")
api_key_input = widgets.Password(description='API Key:', placeholder='Enter RapidAPI Key...', layout=widgets.Layout(width='50%'))
domain_input = widgets.Text(description='Domain:', placeholder='e.g., tesla.com', layout=widgets.Layout(width='50%'))
scan_button = widgets.Button(description='🔍 Start Scan', button_style='success', layout=widgets.Layout(width='20%'))
output_area = widgets.Output()

def on_button_clicked(b):
    output_area.clear_output()
    api_key = api_key_input.value.strip()
    domain = domain_input.value.strip()

    with output_area:
        if not api_key or not domain:
            print("[!] Please provide both an API Key and a Target Domain.")
            return

        print(f"[*] Initiating deep scan for '{domain}'...")

        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Host": API_HOST,
            "X-RapidAPI-Key": api_key
        }

        # 1. Initiate Scan
        try:
            resp = requests.post(f"{BASE_URL}/scan", json={"domain": domain}, headers=headers)
            if resp.status_code == 401:
                print("[!] Error: Invalid API Key. Please verify your RapidAPI subscription.")
                return
            elif resp.status_code not in [200, 202]:
                print(f"[!] Server Error ({resp.status_code}): {resp.text}")
                return

            job_id = resp.json().get("data", {}).get("jobId")
            print(f"[+] Scan successfully queued. Job ID: {job_id}")
            print("[*] Polling system status (this may take ~40 seconds)...")
        except Exception as e:
            print(f"[!] Connection Error: {e}")
            return

        # 2. Status Polling
        while True:
            try:
                res = requests.get(f"{BASE_URL}/scan/{job_id}/status", headers=headers)
                if res.status_code == 200:
                    status_data = res.json().get("data", {})
                    status = status_data.get("status")

                    if status == "COMPLETED":
                        print("[*] Scan finished. Fetching results...")

                        # 3. Fetch Final Results
                        final_res = requests.get(f"{BASE_URL}/scan/{job_id}", headers=headers)

                        if final_res.status_code == 200:
                            data = final_res.json().get("data", {})
                            print(f"\n[+] Scan completed in {data.get('scanDurationMs', 0)/1000:.1f} seconds.")

                            summary = data.get("summary", {})
                            print(f"[*] Total Discovered: {summary.get('totalSubdomains', 0)} | Alive Targets: {summary.get('aliveSubdomains', 0)}\n")

                            subdomains = data.get("subdomains", [])
                            table_data = []

                            for sub in subdomains:
                                # 1. Group Technologies, Server Header, and CDN info
                                tech_list = []
                                if sub.get("isCdn") and sub.get("cdnProvider"):
                                    tech_list.append(f"CDN: {sub.get('cdnProvider')}")
                                if sub.get("serverHeader"):
                                    tech_list.append(f"Server: {sub.get('serverHeader')}")
                                if sub.get("technologies"):
                                    tech_list.extend(sub.get("technologies"))
                                tech_str = " | ".join(tech_list) if tech_list else "-"

                                # 2. Handle Multiple IPs (Join all, handle empty cases)
                                ips = sub.get("ipAddresses")
                                ip_str = ", ".join(ips) if ips else "-"


                                # Build the row
                                table_data.append({
                                    "Subdomain": sub.get("subdomain", "-"),
                                    "State": "🟢 Alive" if sub.get("alive") else "🔴 Dead",
                                    "HTTP": str(sub.get("httpStatus", "-")),
                                    "IP Addresses": ip_str,
                                    "Ports": ", ".join(map(str, sub.get("openPorts", []))) if sub.get("openPorts") else "-",
                                    "Title": sub.get("title", "-"),
                                    "CNAME Chain": sub.get("cname", "-"),
                                    "Tech & Server": tech_str,
                                })

                            if table_data:
                                df = pd.DataFrame(table_data)
                                styled_df = df.style.hide(axis="index").set_properties(**{
                                    'text-align': 'left',
                                    'white-space': 'pre-wrap',
                                    'word-break': 'break-word',
                                    'min-width': '100px',
                                    'max-width': '350px',
                                    'vertical-align': 'top',
                                    'padding': '8px'
                                }).set_table_styles([
                                    {'selector': 'th', 'props': [('text-align', 'left'), ('font-weight', 'bold'), ('background-color', '#f8f9fa'), ('color', '#333')]}
                                ])

                                display(styled_df)
                            else:
                                print("[-] No subdomains found for this target.")
                        else:
                            print(f"[!] Error fetching results: {final_res.status_code}")
                        break

                    elif status in ["PENDING", "RUNNING"]:
                        time.sleep(5)
                    else:
                        print(f"[!] Scan failed or aborted. Status: {status}")
                        break
                else:
                    time.sleep(5)
            except Exception as e:
                print(f"[!] Polling Error: {e}")
                break

scan_button.on_click(on_button_clicked)

# Render UI
ui = widgets.VBox([title, api_key_input, domain_input, scan_button, output_area])
display(ui)
