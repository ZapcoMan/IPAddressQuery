#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- 作者： codervibe -*-
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
# User-Agent集合
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

# 语言映射表
LANG_MAP = {
    "1": "en",
    "2": "cn",
    "3": "ja",
    "4": "es",
    "5": "de"
}

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==================== API调用相关函数 ====================
def get_ip_geolocation(ip_address: str, api_key: str, lang: str = "en") -> dict:
    """
    获取指定 IP 的地理位置信息。
    
    参数:
    ip_address (str): 需要查询地理位置信息的 IP 地址。
    api_key (str): 使用 API 服务所需的密钥，用于验证用户身份。
    lang (str): 返回内容的语言
    
    返回:
    dict: 包含 IP 地理位置信息的字典。如果请求失败或发生错误，返回一个空字典。
    """
    url = "https://api.ipgeolocation.io/v2/ipgeo"
    params = {
        "apiKey": api_key,
        "ip": ip_address,
        "lang": lang
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"请求过程中发生错误：{e}")
        return {}

def bulk_query_ips(api_key: str, ips: list) -> list:
    """
    批量查询多个 IP 的地理信息。
    
    参数:
    api_key (str): IP 地理信息查询的 API 密钥。
    ips (list): 需要查询的 IP 地址列表。
    
    返回:
    list: 查询到的 IP 地理信息列表。
    """
    url = f"https://api.ipgeolocation.io/v2/ipgeo-bulk?apiKey={api_key}"
    data = json.dumps({"ips": ips})
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, headers=headers, timeout=(10, 130))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            logging.error("❌ HTTP 401 错误：API 密钥无效，请检查 apiKey 是否正确。")
        elif response.status_code == 403:
            logging.error("❌ HTTP 403 错误：当前 API 密钥无权限访问此接口。")
        elif response.status_code == 429:
            logging.error("❌ HTTP 429 错误：API 请求频率超过限制，请稍后再试。")
        else:
            logging.error(f"❌ HTTP 请求失败：{e}")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"网络请求过程中发生错误：{e}")
        return []

def get_local_country(api_key: str) -> dict:
    """
    获取调用者所在 IP 的国家名称（无需传入 IP）。
    
    参数:
    api_key (str): API 的密钥，用于认证用户。
    
    返回:
    dict: 包含国家名称的字典，如果请求失败或解析错误，则返回空字典。
    """
    url = f"https://api.ipgeolocation.io/v2/ipgeo?apiKey={api_key}"
    params = {"fields": "location.country_name"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"获取本地国家失败：{e}")
        return {}

# ==================== 配置和工具函数 ====================
def load_api_key_from_config(config_path: str) -> str:
    """
    从YAML配置文件中加载API密钥。
    
    参数:
    config_path (str): 配置文件的路径。
    
    返回:
    str: 从配置文件中读取的API密钥，如果没有找到或发生错误，则返回空字符串。
    """
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

# ==================== 显示函数 ====================
def display_geolocation_info(data: dict):
    """显示完整的 IP 地理位置信息（英文字段）"""
    if not data:
        print("没有可显示的地理信息。")
        return

    location = data.get("location", {})
    network = data.get("network", {}).get("asn", {})

    print("\n🌍 Geolocation Information")
    print(f"IP地址: {data.get('ip', 'Unknown')}")
    print(f"大陆代码: {location.get('continent_code', 'Unknown')}")
    print(f"大陆名称: {location.get('continent_name', 'Unknown')}")
    print(f"国家/地区名称: {location.get('country_name', 'Unknown')}")
    print(f"省/市/自治区: {location.get('state_prov', 'Unknown')} ({location.get('state_code', 'Unknown')})")
    print(f"城市: {location.get('city', 'Unknown')}")
    print(f"纬度,经度: {location.get('latitude', 'Unknown')}, {location.get('longitude', 'Unknown')}")
    print(f"组织: {network.get('organization', 'Unknown')}")
    print(f"是否欧盟国家: {'是' if location.get('is_eu', False) else '否'}")

def display_geolocation_info_cn(data: dict):
    """使用中文字段格式化展示 IP 地理位置相关信息"""
    if not data:
        print("没有可显示的地理信息。")
        return

    location = data.get("location", {})

    print("\n🌍 地理位置信息（中文）")
    print(f"IP地址: {data.get('ip', '未知')}")
    print(f"大陆名称: {location.get('continent', '未知')}")
    print(f"国家名称: {location.get('country', '未知')}")
    print(f"省份/州: {location.get('region', '未知')} ({location.get('region_code', '未知')})")
    print(f"城市: {location.get('city', '未知')}")
    print(f"邮编: {location.get('zipcode', '未知')}")
    print(f"经纬度: {location.get('latitude', '未知')}, {location.get('longitude', '未知')}")
    print(f"是否欧盟国家: {'是' if location.get('is_eu', False) else '否'}")

def display_geolocation_info_ja(data: dict):
    """使用日文字段格式化展示 IP 地理位置相关信息"""
    if not data:
        print("地理情報がありません。")
        return

    location = data.get("location", {})

    print("\n🌍 地理位置情報（日本語）")
    print(f"IPアドレス: {data.get('ip', '不明')}")
    print(f"大陸名: {location.get('continent', '不明')}")
    print(f"国名: {location.get('country', '不明')}")
    print(f"都道府県: {location.get('region', '不明')} ({location.get('region_code', '不明')})")
    print(f"都市: {location.get('city', '不明')}")
    print(f"郵便番号: {location.get('zipcode', '不明')}")
    print(f"緯度・経度: {location.get('latitude', '不明')}, {location.get('longitude', '不明')}")
    print(f"EU加盟国: {'はい' if location.get('is_eu', False) else 'いいえ'}")

def display_geolocation_info_es(data: dict):
    """使用西班牙语字段格式化展示 IP 地理位置相关信息"""
    if not data:
        print("No hay información geográfica disponible.")
        return

    location = data.get("location", {})

    print("\n🌍 Información de Ubicación Geográfica (Español)")
    print(f"Dirección IP: {data.get('ip', 'Desconocida')}")
    print(f"Continente: {location.get('continent', 'Desconocido')}")
    print(f"País: {location.get('country', 'Desconocido')}")
    print(f"Estado/Provincia: {location.get('region', 'Desconocido')} ({location.get('region_code', 'Desconocido')})")
    print(f"Ciudad: {location.get('city', 'Desconocida')}")
    print(f"Código Postal: {location.get('zipcode', 'Desconocido')}")
    print(f"Latitud y Longitud: {location.get('latitude', 'Desconocido')}, {location.get('longitude', 'Desconocido')}")
    print(f"Miembro de la UE: {'Sí' if location.get('is_eu', False) else 'No'}")

def display_geolocation_info_de(data: dict):
    """使用德语字段格式化展示 IP 地理位置相关信息"""
    if not data:
        print("Keine geografischen Informationen verfügbar.")
        return

    location = data.get("location", {})

    print("\n🌍 Geografische Standortinformationen (Deutsch)")
    print(f"IP-Adresse: {data.get('ip', 'Unbekannt')}")
    print(f"Kontinent: {location.get('continent', 'Unbekannt')}")
    print(f"Land: {location.get('country', 'Unbekannt')}")
    print(f"Bundesland: {location.get('region', 'Unbekannt')} ({location.get('region_code', 'Unbekannt')})")
    print(f"Stadt: {location.get('city', 'Unbekannt')}")
    print(f"Postleitzahl: {location.get('zipcode', 'Unbekannt')}")
    print(f"Breiten- und Längengrad: {location.get('latitude', 'Unbekannt')}, {location.get('longitude', 'Unbekannt')}")
    print(f"EU-Mitglied: {'Ja' if location.get('is_eu', False) else 'Nein'}")

def display_bulk_result(results: list):
    """显示批量查询结果"""
    if not results:
        print("无批量数据返回。")
        return

    for item in results:
        location = item.get("location", {})
        print(f"{item['ip']}: {location.get('country_name', '未知')}")

def display_local_country_info(data: dict):
    """显示本机 IP 所在国家名称"""
    if not data:
        print("无法获取本地国家信息。")
        return

    location = data.get("location", {})
    print(f"\n📍 你的 IP 所属国家是：{location.get('country_name', '未知')}")

# ==================== 命令行参数处理 ====================
def get_parameter():
    """
    解析命令行参数，包括IP地址、文件路径、是否使用随机User-Agent、显示版本信息和更新脚本
    :return: 返回解析后的参数对象
    """
    parser = argparse.ArgumentParser(description='查看IP的归属地')
    parser.add_argument('-a', dest='ipaddr', type=str, default='', help='输入查询IP')
    parser.add_argument('-f', dest='file', type=str, default='', help='从文件中读取IP列表进行查询')
    parser.add_argument('-r', '--random-agent', action='store_true', help='启用随机User-Agent')
    parser.add_argument('-v', '--version', action='store_true', help='显示脚本的版本信息')
    parser.add_argument('-u', '--update', action='store_true', help='更新脚本')
    parser.add_argument('--lang', choices=LANG_MAP.keys(), default='1',
                        help='选择输出语言: 1-English, 2-中文, 3-日本語, 4-Español, 5-Deutsch')
    
    args = parser.parse_args()

    # 检查参数并打印帮助信息
    if not args.ipaddr and not args.file and not args.version and not args.update:
        parser.print_help()
        parser.exit()

    return args

# ==================== 辅助功能 ====================
def update_script():
    """更新本地仓库到最新版本"""
    try:
        result = subprocess.run(['git', 'pull'], check=True, capture_output=True, text=True)
        logging.info("更新成功: %s", result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("更新失败: %s", e.stderr)
    except FileNotFoundError:
        logging.error("Git 命令未找到，请确保已安装 Git 并将其添加到系统路径中。")

def read_ips_from_file(file_path: str) -> list:
    """从文件读取IP地址列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error("指定的文件不存在。")
        return []
    except Exception as e:
        logging.error(f"读取文件时发生错误: {e}")
        return []

# ==================== 主要功能实现 ====================
def handle_single_ip_query(api_key: str, ip: str, lang: str):
    """处理单个IP查询"""
    result = get_ip_geolocation(ip, api_key, lang)
    
    if not result:
        print(f"❌ 无法获取 {ip} 的地理位置信息。")
        return
    
    # 根据语言选择显示函数
    display_functions = {
        "en": display_geolocation_info,
        "cn": display_geolocation_info_cn,
        "ja": display_geolocation_info_ja,
        "es": display_geolocation_info_es,
        "de": display_geolocation_info_de
    }
    
    display_func = display_functions.get(lang, display_geolocation_info)
    display_func(result)

def handle_bulk_query(api_key: str, file_path: str, lang: str):
    """处理批量IP查询"""
    ips = read_ips_from_file(file_path)
    
    if not ips:
        return
    
    results = bulk_query_ips(api_key, ips)
    
    if not results:
        print("❌ 批量查询失败，无法获取任何结果。")
        return
    
    display_bulk_result(results)

def handle_local_ip_query(api_key: str):
    """处理本机IP查询"""
    result = get_local_country(api_key)
    display_local_country_info(result)

# ==================== 主函数 ====================
def main():
    """主程序入口"""
    args = get_parameter()
    config_path = "config.yaml"
    
    # 处理--version和--update参数
    if args.version:
        print("IPQuery version 3.0.0")
        return
        
    if args.update:
        update_script()
        return
    
    # 加载配置
    api_key = load_api_key_from_config(config_path)
    if not api_key:
        logging.error("❌ 未能读取到有效的 API 密钥，请检查 config.yaml 文件。")
        return
    
    # 解析语言参数
    lang = LANG_MAP.get(args.lang, "en")
    
    # 处理IP查询
    if args.ipaddr:
        handle_single_ip_query(api_key, args.ipaddr, lang)
    elif args.file:
        handle_bulk_query(api_key, args.file, lang)
    else:
        # 如果没有提供有效参数，显示帮助信息
        parser = argparse.ArgumentParser(description='查看IP的归属地')
        parser.print_help()

if __name__ == '__main__':
    main()
