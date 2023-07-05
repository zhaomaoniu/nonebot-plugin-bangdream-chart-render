from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.plugin import on_command
from nonebot import get_driver
from nonebot.log import logger

from .BanGDreamChartRender import render
from .utils import fuzzy_match, fetch_data
from .data_source import song_data

diff2str = {
    0: "EASY",
    1: "NORMAL",
    2: "HARD",
    3: "EXPERT",
    4: "SPECIAL"
}

diff_nickname = {
    "easy": ["简单", "easy", "ez"],
    "normal": ["普通", "normal"],
    "hard": ["困难", "hard", "hd"],
    "expert": ["专家", "expert", "ex"],
    "special": ["特殊", "special", "sp"]
}

diff2num = {
    "easy": "0",
    "normal": "1",
    "hard": "2",
    "expert": "3",
    "special": "4"
}

init = get_driver()
bdcr = on_command("bdcr", priority=10, block=True)
bcr = on_command("bcr", priority=10, block=True)


@init.on_startup
async def _():
    await song_data.init()


@bdcr.handle()
async def _(event: MessageEvent):
    chart_id = event.raw_message[4:].strip()
    if not chart_id.isdigit():
        return None

    logger.info(f"尝试获取 {chart_id} 的谱面数据")
    data = await fetch_data(
        f"https://bestdori.com/api/post/details?id={chart_id}",
        f"cache/chart/unofficial/",
        f"{chart_id}.json"
    )
    logger.success(f"成功获取 {chart_id} 的谱面数据！正在渲染图像...")
    chart_img = render(data["post"]["chart"])
    chart_info = f"{data['post']['title']}\n{data['post']['artists']}\n{diff2str[data['post']['diff']]}  {data['post']['level']}"
    logger.success("渲染成功，尝试发送中")

    await bdcr.finish(MessageSegment.text(chart_info) + MessageSegment.image(chart_img))


@bcr.handle()
async def _(event: MessageEvent):
    song_nickname = song_data.nickname
    song_datas = song_data.song
    band_datas = song_data.band

    chart_prompt = event.raw_message[3:].strip().rsplit(' ', 1)
    chart_name = chart_prompt[0]
    chart_diff = chart_prompt[1] if len(chart_prompt) > 1 else "expert"

    chart_diff = fuzzy_match(chart_diff, diff_nickname)
    chart_id = fuzzy_match(chart_name, song_nickname)

    if chart_id is None:
        # 匹配不到别名，尝试匹配原名
        for k, data in song_datas.items():
            if chart_name in data["musicTitle"]:
                chart_id = k
                break

    if chart_id is None:
        # 匹配不到原名与别名
        return None

    if chart_diff is None:
        # 匹配不到歌曲难度
        chart_diff = "expert"

    logger.info(f"尝试获取 {chart_id}({chart_diff}) 的谱面数据")
    data = await fetch_data(
        f"https://bestdori.com/api/charts/{chart_id}/{chart_diff}.json",
        f"cache/chart/official/{chart_id}/",
        f"{chart_diff}.json"
    )
    logger.success(f"成功获取 {chart_id} 的谱面数据！正在渲染图像...")

    chart_img = render(data)
    band_id = str(song_datas[chart_id]['bandId'])
    band_data = band_datas[band_id]
    band_name = band_data['bandName'][3] or band_data['bandName'][0] or band_data['bandName'][2] or band_data['bandName'][1] or band_data['bandName'][4]
    # 以 CN, JP, TW, EN, KR 的顺序获取有效的乐队名称
    diffnum = diff2num[chart_diff]
    chart_info = f"{song_nickname[chart_id][0]}\n{band_name}\n{chart_diff.upper()}  {song_datas[chart_id]['difficulty'][diffnum]['playLevel']}"
    logger.success("渲染成功，尝试发送中")

    await bcr.finish(MessageSegment.text(chart_info) + MessageSegment.image(chart_img))
