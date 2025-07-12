# IPAddressQuery
- 这是一个用于查询IP地址地理位置信息的Python工具，支持单个IP查询、批量文件查询、随机User-Agent设置、多语言支持以及通过代理进行查询等功能。

## 📌 版本信息
当前版本: 3.0.0
作者: codervibe
最后更新时间: 脚本执行时可通过 -v 或 --version 查看

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
编辑 `config.yaml` 文件以配置API密钥：
```yaml
api_key: your_api_key_here
```

## 🧪 功能特性
1. **单个IP查询**：通过命令行参数 `-a` 指定单个IP地址进行查询。
2. **批量文件查询**：通过命令行参数 `-f` 指定包含IP地址列表的文件进行批量查询。
3. **随机User-Agent**：通过命令行参数 `-r` 启用随机User-Agent以避免被目标服务器识别为爬虫。
4. **多语言支持**：通过命令行参数 `--lang` 选择输出语言，支持英语、中文、日语、西班牙语和德语。
5. **代理查询**：支持通过代理服务器进行查询，具体配置请参考代码中的网络请求部分。
6. **版本查询**：通过命令行参数 `-v` 或 `--version` 查看当前脚本的版本信息。
7. **自动更新**：通过命令行参数 `-u` 或 `--update` 使用 Git 自动更新到最新版本。

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
```bash
# 单个IP查询（默认语言为英文）
python IPAddressQuery.py -a 8.8.8.8

# 使用随机User-Agent进行查询
python IPAddressQuery.py -a 8.8.8.8 -r

# 批量文件查询
python IPAddressQuery.py -f ips.txt

# 查询并输出中文结果
python IPAddressQuery.py -a 8.8.8.8 --lang 2

# 显示版本信息
python IPAddressQuery.py -v

# 更新脚本
python IPAddressQuery.py -u
```