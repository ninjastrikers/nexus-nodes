import requests
import base64
import os
import json
import urllib.parse
import time
import re
import socket
import concurrent.futures
from datetime import datetime, timezone

SOURCES =[
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/MrAbolfazlNorouzi/iran-configs/refs/heads/main/configs/working-configs.txt",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
    "https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub1.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub2.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub3.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub4.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/refs/heads/main/all_configs.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
    "https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/sub/vless.txt",
    "https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/sub/vmess.txt",
    "https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/sub/ss.txt",
    "https://raw.githubusercontent.com/hamedcode/port-based-v2ray-configs/main/sub/trojan.txt",
]

def decode_base64(text):
    text = text.strip()
    text += "=" * ((4 - len(text) % 4) % 4)
    try:
        return base64.b64decode(text).decode('utf-8', errors='ignore')
    except:
        return text

def fetch_configs(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.text
        if "://" not in content:
            content = decode_base64(content)
        return content.splitlines()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return[]

def extract_address(config):
    if config.startswith(('vless://', 'trojan://', 'ss://')):
        try:
            return urllib.parse.urlparse(config).hostname
        except:
            pass
    elif config.startswith('vmess://'):
        try:
            b64_str = config[8:] + "=" * ((4 - len(config[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64_str).decode('utf-8'))
            return data.get('add')
        except:
            pass
    return None

def extract_ip_port(config):
    if config.startswith(('vless://', 'trojan://', 'ss://', 'ssr://')):
        try:
            parsed = urllib.parse.urlparse(config)
            port = parsed.port if parsed.port else 443
            return parsed.hostname, port
        except:
            pass
    elif config.startswith('vmess://'):
        try:
            b64_str = config[8:] + "=" * ((4 - len(config[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64_str).decode('utf-8'))
            return data.get('add'), int(data.get('port', 443))
        except:
            pass
    return None, None

def extract_remark(config):
    if config.startswith(('vless://', 'trojan://', 'ss://')):
        try:
            parsed = urllib.parse.urlparse(config)
            return urllib.parse.unquote(parsed.fragment)
        except:
            pass
    elif config.startswith('vmess://'):
        try:
            b64_str = config[8:] + "=" * ((4 - len(config[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64_str).decode('utf-8'))
            return data.get('ps', '')
        except:
            pass
    return ""

def get_override_country(remark):
    if not remark: 
        return None
        
    remark_upper = remark.upper()
    
    # 1. Flags (Safest & most exact)
    flags = {
        "🇺🇸": "us", "🇨🇦": "ca", "🇬🇧": "gb", "🇩🇪": "de", "🇫🇷": "fr", 
        "🇳🇱": "nl", "🇸🇬": "sg", "🇯🇵": "jp", "🇭🇰": "hk", "🇮🇳": "in", 
        "🇦🇺": "au", "🇷🇴": "ro", "🇷🇺": "ru", "🇹🇼": "tw", "🇰🇷": "kr", 
        "🇹🇷": "tr", "🇧🇷": "br", "🇮🇩": "id", "🇻🇳": "vn", "🇹🇭": "th", 
        "🇮🇷": "ir", "🇮🇹": "it", "🇪🇸": "es", "🇸🇪": "se", "🇨🇭": "ch", 
        "🇵🇱": "pl", "🇦🇪": "ae", "🇿🇦": "za"
    }
    for flag, code in flags.items():
        if flag in remark:
            return code
            
    # 2. Strict United States & Canada checks
    if "USA" in remark_upper or "UNITED STATES" in remark_upper or "CALIFORNIA" in remark_upper:
        return "us"
    if re.search(r'(?<![A-Z])US(?![A-Z])', remark_upper):
        return "us"
        
    if "CANADA" in remark_upper:
        return "ca"
    if re.search(r'(?<!US-)(?<!USA-)(?<![A-Z])CA(?![A-Z])', remark_upper):
        return "ca"
    
    # 3. Comprehensive Regex dictionary for 2-Letter codes & Full Names
    strict_keywords = {
        "gb": ["UK", "GB", "UNITED KINGDOM", "ENGLAND"],
        "de": ["DE", "GERMANY"],
        "fr": ["FR", "FRANCE"],
        "nl": ["NL", "NETHERLANDS"],
        "sg": ["SG", "SINGAPORE"],
        "jp": ["JP", "JAPAN"],
        "hk": ["HK", "HONG KONG"],
        "in": ["IN", "INDIA"],
        "au": ["AU", "AUSTRALIA"],
        "ro": ["RO", "ROMANIA"],
        "ru": ["RU", "RUSSIA"],
        "tw": ["TW", "TAIWAN"],
        "kr":["KR", "SOUTH KOREA"],
        "tr": ["TR", "TURKEY"],
        "br":["BR", "BRAZIL"],
        "id": ["ID", "INDONESIA"],
        "vn":["VN", "VIETNAM"],
        "th": ["TH", "THAILAND"],
        "ir":["IR", "IRAN"],
        "it": ["IT", "ITALY"],
        "es":["ES", "SPAIN"],
        "se": ["SE", "SWEDEN"],
        "ch":["CH", "SWITZERLAND"],
        "pl": ["PL", "POLAND"],
        "ae": ["AE", "UAE", "UNITED ARAB EMIRATES"],
        "za":["ZA", "SOUTH AFRICA"]
    }
    
    for code, words in strict_keywords.items():
        for word in words:
            if len(word) <= 3:
                if re.search(rf'(?<![A-Z]){word}(?![A-Z])', remark_upper):
                    return code
            else:
                if word in remark_upper:
                    return code
                    
    return None

def get_countries(addresses):
    valid_addrs = list(set([a for a in addresses if a]))
    addr_to_country = {}
    for i in range(0, len(valid_addrs), 100):
        chunk = valid_addrs[i:i+100]
        try:
            res = requests.post("http://ip-api.com/batch?fields=query,countryCode,status", json=chunk, timeout=10).json()
            for info in res:
                if info.get('status') == 'success':
                    addr_to_country[info['query']] = info['countryCode'].lower()
        except Exception as e:
            print(f"GeoIP Error: {e}")
        time.sleep(2)
    return addr_to_country

CHECK_HOST_RATE_LIMITED = False

def check_config_latency(config):
    global CHECK_HOST_RATE_LIMITED
    ip, port = extract_ip_port(config)
    
    if not ip or not port:
        return config, float('inf')
        
    latency = float('inf')
    
    if not CHECK_HOST_RATE_LIMITED:
        try:
            headers = {"Accept": "application/json"}
            url = f"https://check-host.net/check-tcp?host={ip}:{port}&max_nodes=1"
            req = requests.get(url, headers=headers, timeout=5)
            
            if req.status_code == 429:
                CHECK_HOST_RATE_LIMITED = True
            elif req.status_code == 200:
                req_id = req.json().get("request_id")
                if req_id:
                    time.sleep(2)
                    res = requests.get(f"https://check-host.net/check-result/{req_id}", headers=headers, timeout=5).json()
                    for node, checks in res.items():
                        if checks and isinstance(checks, list):
                            val = checks[0]
                            if isinstance(val, dict) and 'time' in val:
                                latency = val['time'] * 1000
                            elif isinstance(val, list) and len(val) > 1:
                                latency = float(val[1]) * 1000
        except:
            pass

    if latency == float('inf'):
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            sock.connect((ip, int(port)))
            sock.close()
            latency = (time.time() - start) * 1000
        except:
            latency = float('inf')
            
    return config, latency

def test_all_latencies(country_grouped):
    country_sorted = {}
    global_valid = []
    global_invalid =[]
    
    for cc, configs in country_grouped.items():
        results =[]
        to_test = configs[:150]
        rest = configs[150:]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures =[executor.submit(check_config_latency, c) for c in to_test]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
                
        valid =[item for item in results if item[1] != float('inf')]
        invalid = [item for item in results if item[1] == float('inf')]
        
        valid.sort(key=lambda x: x[1])
        
        global_valid.extend(valid)
        global_invalid.extend([c for c, l in invalid] + rest)
        
        country_sorted[cc] =[c for c, l in valid] +[c for c, l in invalid] + rest
        
    global_valid.sort(key=lambda x: x[1])
    all_sorted_configs =[c for c, l in global_valid] + global_invalid
    
    return country_sorted, all_sorted_configs

def main():
    all_configs = set()
    for source in SOURCES:
        for line in fetch_configs(source):
            if line.strip().startswith(("vless://", "vmess://", "trojan://", "ss://", "ssr://")):
                all_configs.add(line.strip())

    addresses =[extract_address(c) for c in all_configs]
    addr_to_country = get_countries(addresses)

    country_grouped = {}
    for config in all_configs:
        cc = addr_to_country.get(extract_address(config), "unknown")
        remark = extract_remark(config)
        override_cc = get_override_country(remark)
        
        if override_cc:
            cc = override_cc
            
        if cc not in country_grouped:
            country_grouped[cc] = []
        country_grouped[cc].append(config)

    print("Testing latency and sorting utilizing Check-Host API...")
    country_sorted, all_sorted_configs = test_all_latencies(country_grouped)

    # 🛑 APP CRASH PREVENTION LIMITS
    MAX_GLOBAL_ALL = 3000   # Limit the global mix so huge updates don't break apps
    MAX_COUNTRY_ALL = 1500  # Max per country general sub
    MAX_LIGHT = 100         # Max for lightweight (fastest 100)
    MAX_PROTO = 500         # Max per individual protocol (vless, vmess, etc.)

    # Apply limits safely
    global_cat = {
        "all": all_sorted_configs[:MAX_GLOBAL_ALL], 
        "light": all_sorted_configs[:MAX_LIGHT], 
        "vless": [], "vmess":[], "shadowsocks": [], "trojan":[]
    }
    
    country_cat = {}

    for cc, configs in country_sorted.items():
        # Trim general country list and lightweight list
        country_cat[cc] = {
            "all": configs[:MAX_COUNTRY_ALL], 
            "light": configs[:MAX_LIGHT], 
            "vless": [], "vmess": [], "shadowsocks":[], "trojan": [], "unknown":[]
        }
        
        # Populate specific protocols for the country (stopping once MAX_PROTO is hit)
        for config in configs:
            if config.startswith("vless://") and len(country_cat[cc]["vless"]) < MAX_PROTO:
                country_cat[cc]["vless"].append(config)
            elif config.startswith("vmess://") and len(country_cat[cc]["vmess"]) < MAX_PROTO:
                country_cat[cc]["vmess"].append(config)
            elif config.startswith("trojan://") and len(country_cat[cc]["trojan"]) < MAX_PROTO:
                country_cat[cc]["trojan"].append(config)
            elif config.startswith("ss://") and len(country_cat[cc]["shadowsocks"]) < MAX_PROTO:
                country_cat[cc]["shadowsocks"].append(config)
            elif not config.startswith(("vless://", "vmess://", "trojan://", "ss://")) and len(country_cat[cc]["unknown"]) < MAX_PROTO:
                country_cat[cc]["unknown"].append(config)

    # Populate specific protocols globally (stopping once MAX_PROTO is hit)
    for config in all_sorted_configs:
        if config.startswith("vless://") and len(global_cat["vless"]) < MAX_PROTO: 
            global_cat["vless"].append(config)
        elif config.startswith("vmess://") and len(global_cat["vmess"]) < MAX_PROTO: 
            global_cat["vmess"].append(config)
        elif config.startswith("trojan://") and len(global_cat["trojan"]) < MAX_PROTO: 
            global_cat["trojan"].append(config)
        elif config.startswith("ss://") and len(global_cat["shadowsocks"]) < MAX_PROTO: 
            global_cat["shadowsocks"].append(config)

    os.makedirs("configs", exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    for cat, configs in global_cat.items():
        if configs:
            encoded = base64.b64encode("\n".join(configs).encode('utf-8')).decode('utf-8')
            with open(f"configs/{cat}.txt", "w", encoding="utf-8") as f:
                f.write(encoded)

    country_stats = {}
    for cc, categories in country_cat.items():
        country_stats[cc] = len(categories["all"])
        os.makedirs(f"configs/countries/{cc}", exist_ok=True)
        for cat, configs in categories.items():
            if configs:
                encoded = base64.b64encode("\n".join(configs).encode('utf-8')).decode('utf-8')
                with open(f"configs/countries/{cc}/{cat}.txt", "w", encoding="utf-8") as f:
                    f.write(encoded)

    with open("docs/info.json", "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "countries": country_stats
        }, f, indent=4)

if __name__ == "__main__":
    main()