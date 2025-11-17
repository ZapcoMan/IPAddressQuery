#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- 作者： codervibe/ZapcoMan -*-
# -*- 时间: 18:46 -*-
# -*- 获取 IP 地址定位 -*-
# -*- 版本: 3.0.0 -*-

import requests
import yaml
import json
import random
import argparse
import logging
import subprocess
from typing import Dict, List



# ==================== 配置部分 ====================
# User-Agent集合（配置项）
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0"
]

# 定义脚本版本号（配置项）
version = "3.1.0"

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 语言映射表
LANG_MAP = {
    "1": "en",
    "2": "cn",
    "3": "ja",
    "4": "es",
    "5": "de"
}

# ==================== 主要API调用函数 ====================

def get_ip_geolocation(ip_address: str, api_key: str, lang: str = "en") -> dict:
    """
    使用 ipgeolocation.io 查询 IP 的地理位置信息。
    """
    url = "https://api.ipgeolocation.io/v2/ipgeo"
    params = {"apiKey": api_key, "ip": ip_address, "lang": lang}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"ipgeolocation.io 请求失败：{e}")
        return {}

def get_ip_from_ip_api(ip_address: str, use_random_agent=False) -> dict:
    """
    使用 ip-api.com 查询 IP 的地理位置信息。
    """
    url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN"
    headers = {'Connection': 'keep-alive'}
    if use_random_agent:
        headers['User-Agent'] = random.choice(USER_AGENTS)

    try:
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        logging.error(f"ip-api.com 请求失败：{e}")
        return {}


# ==================== 辅助函数 ====================

def load_api_key(config_path: str) -> str:
    """从YAML配置文件中加载API密钥"""
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config.get('api_key', '')
    except Exception as e:
        logging.error(f"读取配置文件时出错：{e}")
        return ''

def get_random_user_agent() -> str:
    """获取随机User-Agent"""
    return random.choice(USER_AGENTS)

def parse_json(ip_str):
    """JSON 解析辅助函数"""
    try:
        return json.loads(ip_str)
    except json.JSONDecodeError:
        print("JSON解析失败，请检查返回的数据格式。")
        return None

def merge_results(result1: dict, result2: dict) -> dict:
    """合并两个 API 的结果"""
    merged = {}
    merged.update(result1)
    for key, value in result2.items():
        if key not in merged or not merged[key]:
            merged[key] = value
    return merged

# ==================== 命令行参数处理 ====================

def get_parameter():
    parser = argparse.ArgumentParser(description='查看IP的归属地')
    parser.add_argument('-a', dest='ipaddr', type=str, default='', help='输入查询IP')
    parser.add_argument('-f', dest='file', type=str, default='', help='从文件中读取IP列表进行查询')
    parser.add_argument('-r', '--random-agent', action='store_true', help='启用随机User-Agent')
    parser.add_argument('-v', '--version', action='store_true', help='显示脚本的版本信息')
    parser.add_argument('-u', '--update', action='store_true', help='更新脚本')
    parser.add_argument('--lang', choices=LANG_MAP.keys(), default='1',
                        help='选择输出语言: 1-English, 2-中文, 3-日本語, 4-Español, 5-Deutsch')

    args = parser.parse_args()

    if not args.ipaddr and not args.file and not args.version and not args.update:
        parser.print_help()
        parser.exit()

    return args


# ==================== 显示函数 ====================
def display_merged_result(data: dict, lang: str = "en"):
    if not data:
        print("没有可显示的地理信息。")
        return

    location = data.get("location", {})
    network = data.get("network", {}).get("asn", {})

    # 提取经纬度信息，优先使用location中的数据，否则使用data根级数据
    ip_lat = location.get('latitude') or data.get('lat')
    ip_lon = location.get('longitude') or data.get('lon')

    # 添加 Banner
    print("=" * 65)
    print("🌐IP地址位置查询结果".center(48))
    print("=" * 65)

    print("\n🌍 IP 地理位置信息")
    print(f"IP地址: {data.get('ip', 'Unknown')}")
    print(f"国家名称: {location.get('country', '未知')} / {data.get('country', '未知')}")
    print(f"省份/州: {location.get('region', '未知')} / {data.get('regionName', '未知')}")
    print(f"城市: {location.get('city', '未知')} / {data.get('city', '未知')}")
    print(f"经纬度: {location.get('latitude', '未知')}, {location.get('longitude', '未知')} / 经度:{data.get('lon', '未知')}, 纬度:{data.get('lat', '未知')}")
    print(f"组织: {network.get('organization', '未知')} / ISP: {data.get('isp', '未知')}")
    print(f"是否欧盟国家: {'是' if location.get('is_eu', False) else '否'}")
    if ip_lat and ip_lon:
        print(f"谷歌地图定位点:  https://www.google.com/maps/place/{ip_lat}+{ip_lon}")



# ==================== 核心逻辑 ====================

def query_ip(ip: str, api_key: str, use_random_agent: bool = False, lang: str = "en") -> dict:
    result1 = get_ip_geolocation(ip, api_key, lang)
    result2 = get_ip_from_ip_api(ip, use_random_agent)
    return merge_results(result1, result2)


def handle_single_ip_query(api_key: str, ip: str, use_random_agent: bool, lang: str):
    result = query_ip(ip, api_key, use_random_agent, lang)
    display_merged_result(result, lang)


def handle_bulk_query(api_key: str, file_path: str, use_random_agent: bool, lang: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            ips = [line.strip() for line in file if line.strip()]
        for ip in ips:
            result = query_ip(ip, api_key, use_random_agent, lang)
            display_merged_result(result, lang)
    except FileNotFoundError:
        logging.error("指定的文件不存在。")


# ==================== 更新和主入口 ====================

def update_script():
    """更新本地仓库到最新版本"""
    try:
        result = subprocess.run(['git', 'pull'], check=True, capture_output=True, text=True)
        logging.info("更新成功: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("更新失败: %s", e.stderr)
    except FileNotFoundError:
        logging.error("Git 命令未找到，请确保已安装 Git 并将其添加到系统路径中。")


if __name__ == '__main__':
    args = get_parameter()
    config_path = "config.yaml"

    # 处理--version和--update参数
    if args.version:
        print(f"IPAddressQuery version {version}")
        exit()

    if args.update:
        update_script()
        exit()

    # 加载配置
    api_key = load_api_key(config_path)
    if not api_key:
        logging.error("❌ 未能读取到有效的 API 密钥，请检查 config.yaml 文件。")
        exit()

    # 解析语言参数
    lang = LANG_MAP.get(args.lang, "en")

    # 处理IP查询
    if args.ipaddr:
        handle_single_ip_query(api_key, args.ipaddr, args.random_agent, lang)
    elif args.file:
        handle_bulk_query(api_key, args.file, args.random_agent, lang)
    else:
        parser = argparse.ArgumentParser(description='查看IP的归属地')
        parser.print_help()
