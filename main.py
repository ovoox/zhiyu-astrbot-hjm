from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Video 
import aiohttp
import json

@register("beauty_video", "美女视频", "获取美女视频的插件", "1.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "http://api.ocoa.cn/api/mvsp.php"
        self.session = aiohttp.ClientSession()
        
    async def terminate(self):
        await self.session.close()
        
    @filter.regex(r"^[/]?(美女视频|看美女)$")
    async def get_beauty_video(self, event: AstrMessageEvent):
        try:
            async with self.session.get(self.api_url) as response:
                if response.status == 200:
                    # 解析返回的JSON数据
                    data = await response.json()
                    
                    # 从JSON中获取视频URL
                    if "url" in data:
                        video_url = data["url"]
                        # 创建视频组件并发送
                        video_component = Video.fromURL(video_url)
                        yield event.chain_result([video_component])
                    else:
                        yield event.plain_result("获取视频链接失败")
                else:
                    yield event.plain_result("获取视频失败 请稍后重试")

        except json.JSONDecodeError:
            yield event.plain_result("解析视频数据失败")
        except Exception as e:
            print(f"视频异常: {e}")
            yield event.plain_result("视频异常 请稍后重试")