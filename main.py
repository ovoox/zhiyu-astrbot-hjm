from astrbot.api.star import Context, Star
from astrbot.api.event import filter
from astrbot.api.message_components import Image, Plain
from astrbot.api.event.message_event import AstrMessageEvent
import os
import random

@register("meme_sticker", "知鱼", "超多表情包插件", "1.0")
class MemeStickerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def _send_random_image(self, event: AstrMessageEvent, subfolder: str):
        plugin_dir = os.path.dirname(__file__)
        image_folder = os.path.join(plugin_dir, "meme", subfolder)

        if not os.path.exists(image_folder):
            yield event.chain_result([
                Plain(text=f"❌ 文件夹 `meme/{subfolder}` 不存在，请检查插件目录！")
            ])
            return

        supported_ext = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
        image_files = [
            f for f in os.listdir(image_folder)
            if os.path.isfile(os.path.join(image_folder, f)) and f.lower().endswith(supported_ext)
        ]

        if not image_files:
            yield event.chain_result([
                Plain(text=f"📁 `meme/{subfolder}` 中没有图片，请放入图片后再试~")
            ])
            return

        chosen = random.choice(image_files)
        image_path = os.path.join(image_folder, chosen)
        yield event.chain_result([Image.fromFileSystem(image_path)])

    @filter.command("fufu")
    async def fufu(self, event: AstrMessageEvent):
        async for result in self._send_random_image(event, "fufu"):
            yield result

    @filter.command("loopy")
    async def loopy(self, event: AstrMessageEvent):
        async for result in self._send_random_image(event, "loopy"):
            yield result

    @filter.command("cheems")
    async def cheems(self, event: AstrMessageEvent):
        async for result in self._send_random_image(event, "cheems"):
            yield result

    @filter.command("konata")
    async def konata(self, event: AstrMessageEvent):
        async for result in self._send_random_image(event, "konata"):
            yield result