# 🚀 Nexus Nodes

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ninjastrikers/Nexus-nodes/main.yml?label=Auto%20Update&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/ninjastrikers/Nexus-nodes?style=flat-square)
![License](https://img.shields.io/github/license/ninjastrikers/Nexus-nodes?style=flat-square)

**Nexus Nodes** is a decentralized, auto-updating V2Ray configuration aggregator. It fetches free proxies from multiple reliable sources, tests their latency, strictly categorizes them by region, and outputs ready-to-use Base64 subscription links. 


🌐 **Official Web Interface:**[https://nexus.ninjastrikers.net](https://nexus.ninjastrikers.net/)

---

## ✨ Key Features

* **⚡ Hybrid Latency Sorting:** Automatically tests all fetched nodes using the **Check-Host API** with a lightning-fast native Python TCP ping fallback. The fastest nodes are placed at the top of your subscription lists.
* **🌍 Smart Region Classification:** Uses IP Geolocation (`ip-api.com`) combined with strict Regex node-name parsing. It intelligently overrides misrouted Cloudflare CDN IPs to guarantee that US nodes stay in the US, Canada in Canada, and HK nodes aren't mislabeled as Great Britain.
* **📱 Modern Web Dashboard:** A sleek, glassmorphism-styled Web UI built with Tailwind CSS. Includes 1-click copy buttons, QR code generation, and timezone-aware update timestamps.
* **📂 Granular Subscriptions:** Grab the "Global Mix", filter by protocol (VLESS, VMess, Trojan, Shadowsocks), or choose specific countries.
* **🤖 Fully Automated:** Powered by GitHub Actions to scrape, test, and update configs every few hours without manual intervention.

---

## 🔗 Subscription Links

You can copy these raw links directly into your V2Ray client (v2rayN, v2rayNG, Nekobox, Shadowrocket, etc.). 

### 🌐 Global Mix (All Regions)
| Profile | Subscription Link |
| :--- | :--- |
| **Complete Mix** (All) | `https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/all.txt` |
| **Lightweight** (Top 50 Fastest) | `https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/light.txt` |
| **VLESS Only** | `https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/vless.txt` |
| **VMess Only** | `https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/vmess.txt` |
| **Trojan Only** | `https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/trojan.txt` |
| **Shadowsocks Only** | `https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/shadowsocks.txt` |

### 🗺️ Specific Countries
To get configs for a specific country, visit the [Web Interface](https://nexus.ninjastrikers.net/) to easily scan/copy the links, or use the following URL structure:
```text
https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/countries/{COUNTRY_CODE}/all.txt
```
(Replace {COUNTRY_CODE} with a 2-letter ISO code like us, ca, sg, hk, de, etc.)

## ⚖️ Credits & Disclaimer

This project is intended for educational purposes and network testing. We do not host, operate, or maintain any of the proxy servers provided in the aggregated lists. Please ensure your use of these networks complies with your local laws.

This repository is an aggregator. The servers are not hosted by me. Credits go to the original collectors and scanners:
- Epodonios
- Barry-Far
- MrAbolfazlNorouzi
- 4n0nymou3
- And many others.