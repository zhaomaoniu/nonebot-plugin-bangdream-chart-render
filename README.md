<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://v2.nonebot.dev/logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
</div>

<div align="center">

# nonebot-plugin-bangdream-chart-render

_✨ 基于OneBot适配器的NoneBot2 BanGDream谱面渲染插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-bangdream-chart-render.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-bangdream-chart-render">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-bangdream-chart-render.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>


## 📖 介绍

通过从 [Bestdori](https://bestdori.com/) 获取谱面信息，使用 [BanGDreamChartRender](https://github.com/zhaomaoniu/BanGDreamChartRender) 进行谱面渲染，发送渲染后的图片

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-bangdream-chart-render

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-bangdream-chart-render
</details>


打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_bangdream-chart-render"]

</details>

## ⚙️ 配置

由于本人实力有限，未能实现自动更新歌曲别名（欢迎pr），故需每隔一段时间就到 [nickname_song](https://docs.qq.com/sheet/DUGxuY1FqZWlGd0JZ) 手动导出为csv放入 `Nonebot实例目录/data/bcr` 下，或导出为xlsx，使用Excel修复后放入 `Nonebot实例目录/data/bcr` 下。程序会优先读取csv文件

有关谱面渲染的配置请在 `插件目录/BanGDreamChartRender/config.py` 中参照 [BanGDreamChartRender](https://github.com/zhaomaoniu/BanGDreamChartRender) 的说明进行配置

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| bcr [歌曲名称] [歌曲难度] | 所有人 | 否 | 不限 | 获取官谱的谱面渲染图 |
| bdcr [谱面ID] | 所有人 | 否 | 不限 | 获取自制谱的谱面渲染图 |

### 效果图
![alt 效果图](https://github.com/zhaomaoniu/nonebot-plugin-bangdream-chart-render/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE.png)
