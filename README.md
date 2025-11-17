# IPAddressQuery

这是一个用于查询IP地址地理位置信息的Python工具，支持单个IP查询、批量文件查询、随机User-Agent设置、多语言支持以及通过Git进行自动更新等功能。

## 📌 版本信息

当前版本: 3.2.0  
作者: codervibe/ZapcoMan  
最后更新时间: 脚本执行时可通过 -v 或 --version 查看

📌 功能概述 
- ✅ 单个或批量 IP 查询  
- ✅ 支持多语言输出：英语、中文、日语、西班牙语、德语  
- ✅ 使用随机 User-Agent 提高兼容性  
- ✅ 脚本版本检查与 Git 更新功能  
- ✅ 结构化输出字段：国家、省份、城市、经纬度、ISP 等  
- ✅ 合并两个不同API（ipgeolocation.io 和 ip-api.com）的结果以获取更完整的数据  

## 🛠️ 安装与使用

### 下载项目

~~~bash
 git clone https://github.com/codervibe/IPAddressQuery 
 cd IPAddressQuery/main
~~~
### 安装（可选）

~~~bash
 cp ./IPAddressQuery.py /usr/bin/IPAddressQuery 
 chmod +x /usr/bin/IPAddressQuery
~~~
## 🔧 依赖库

- requests
- yaml
- json
- argparse
- logging
- random
- subprocess (用于更新功能)
- git (用于更新功能，需安装并添加到系统路径)

## 📝 配置

编辑 [config.yaml](file://E:\python\Python_project\IPAddressQuery\main\config.yaml) 文件以配置API密钥：

~~~yaml
# 注意：此文件包含敏感信息，请勿提交到公开仓库或共享给非授权人员
# 推荐使用环境变量替代明文密钥
api_key: your_api_key_here

~~~
## 🧪 主要功能

1. **单个IP查询**：通过命令行参数 `-a` 指定单个IP地址进行查询。
2. **批量文件查询**：通过命令行参数 `-f` 指定包含IP地址列表的文件进行批量查询。
3. **随机User-Agent**：通过命令行参数 `-r` 启用随机User-Agent以避免被目标服务器识别为爬虫。
4. **多语言支持**：通过命令行参数 `--lang` 选择输出语言，支持英语、中文、日语、西班牙语和德语。
5. **版本查询**：通过命令行参数 `-v` 或 `--version` 查看当前脚本的版本信息。
6. **自动更新**：通过命令行参数 `-u` 或 `--update` 使用 Git 自动更新到最新版本。

## 🌍 查询功能说明

该工具整合了两个不同的IP地理位置查询API：
1. ipgeolocation.io (主要API)
2. ip-api.com (备用API)

通过合并两个API的结果，可以获得更完整的信息。例如：
- ipgeolocation.io 提供了详细的地理信息和欧盟国家标识
- ip-api.com 提供了额外的ISP信息

## 📁 目录结构
~~~
IPAddressQuery/ 
├── main/ # 主程序目录 
│ ├── IPAddressQuery.py # 主程序文件 
│ ├── init.py # Python模块初始化文件 
│ └── config.yaml # 配置文件 
└── README.md # 项目说明文档
~~~

## 📊 输出说明

当查询一个IP地址时，脚本将输出以下信息：

- IP地址
- 国家名称
- 省份/州
- 城市
- 经纬度
- 组织（ISP）
- 是否欧盟国家

## 📚 示例命令

~~~base

单个IP查询（默认语言为英文）
python IPAddressQuery.py -a 8.8.8.8
使用随机User-Agent进行查询
python IPAddressQuery.py -a 8.8.8.8 -r
批量文件查询
python IPAddressQuery.py -f ips.txt
查询并输出中文结果
python IPAddressQuery.py -a 8.8.8.8 --lang 2
显示版本信息
python IPAddressQuery.py -v
更新脚本
python IPAddressQuery.py -u
~~~

📎 示例输出
~~~base
🌍 IP 地理位置信息 IP地址: 8.8.8.8 
国家名称: United States / Unknown 
省份/州: California / Unknown 
城市: Mountain View / Unknown 
经纬度: 37.4056, -122.0775 / 经度:Unknown, 纬度:Unknown 
组织: AS15169 Google LLC / ISP: Unknown 
是否欧盟国家: 否
~~~

## 📝 日志与错误处理

所有运行时错误和异常都会被记录并打印到控制台。
API 请求失败时会自动捕获并提示具体错误。
若无法读取配置文件或缺少 API 密钥，程序将终止执行。

