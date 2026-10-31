from __future__ import annotations

import random
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

BG = (5, 8, 5)
PANEL = (10, 15, 10)
NEON = (57, 255, 20)
MATRIX = (0, 255, 65)
TEXT = (213, 255, 213)
MUTED = (112, 170, 120)
BORDER = (23, 77, 36)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/lucon.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    ):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def frame_base(width: int, height: int) -> Image.Image:
    image = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(image)
    for y in range(0, height, 4):
        draw.line((0, y, width, y), fill=(7, 13, 7), width=1)
    return image


def make_hero() -> None:
    width, height, count = 800, 360, 48
    f = font(18)
    small = font(14)
    messages = [
        ("[ SYSTEM BOOT ]", NEON),
        ("[ INITIALIZING DEVELOPER ENVIRONMENT... ]", TEXT),
        ("[ LOADING MODULES.................. OK ]", TEXT),
        ("[ CONNECTING TO GITHUB............. OK ]", TEXT),
        ("[ USER: ARVAZEANN ]", MATRIX),
        ("[ ACCESS GRANTED ]", NEON),
    ]
    frames: list[Image.Image] = []
    for index in range(count):
        image = frame_base(width, height)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((12, 12, width - 13, height - 13), radius=10, fill=PANEL, outline=BORDER, width=2)
        draw.rounded_rectangle((13, 13, width - 14, 48), radius=9, fill=(14, 24, 14))
        for x, color in ((30, (255, 95, 86)), (50, (255, 189, 46)), (70, (39, 201, 63))):
            draw.ellipse((x - 5, 28, x + 5, 38), fill=color)
        draw.text((width // 2, 32), "arvazeann@linux: ~", font=small, fill=MUTED, anchor="mm")

        visible = min(len(messages), max(1, (index - 2) // 5 + 1))
        for row, (message, color) in enumerate(messages[:visible]):
            draw.text((38, 70 + row * 29), message, font=small, fill=color)

        if index >= 30:
            command = "root@arvazeann:~$ whoami"
            command_x, command_y = 38, 258
            draw.text((command_x, command_y), command, font=small, fill=NEON)
            draw.text((38, 284), "ZEANAJAA", font=font(24), fill=TEXT)
            status = "INFORMATICS STUDENT  /  DEVELOPER IN PROGRESS"
            status_x, status_y = 38, 318
            draw.text((status_x, status_y), status, font=small, fill=MUTED)
            cursor = "|" if (index // 3) % 2 == 0 else " "
            cursor_x = status_x + draw.textlength(status, font=small)
            draw.text((cursor_x, status_y), cursor, font=small, fill=NEON)
        frames.append(image)

    frames[0].save(
        ASSETS / "hero-terminal.gif",
        save_all=True,
        append_images=frames[1:],
        duration=140,
        loop=0,
        optimize=True,
        disposal=2,
    )


def make_rain() -> None:
    width, height, count = 800, 150, 28
    cell, columns = 18, 45
    rng = random.Random(1403)
    glyphs = "01<>[]{}*+-=:/\\#$%&@"
    streams = [(rng.randrange(-height, height), rng.randrange(2, 8), rng.randrange(5, 12)) for _ in range(columns)]
    f = font(15)
    frames: list[Image.Image] = []
    for step in range(count):
        image = frame_base(width, height)
        draw = ImageDraw.Draw(image)
        for column, (start, speed, length) in enumerate(streams):
            head_y = (start + step * speed) % (height + length * cell) - length * cell
            for trail in range(length):
                y = int(head_y - trail * cell)
                if -cell < y < height:
                    glyph_index = (column * 13 + trail * 7 + (step * speed) // cell) % len(glyphs)
                    char = glyphs[glyph_index]
                    color = NEON if trail == 0 else (MATRIX if trail < 3 else (20, max(55, 160 - trail * 10), 35))
                    draw.text((column * cell + 2, y), char, font=f, fill=color)
        frames.append(image)
    frames[0].save(
        ASSETS / "matrix-rain.gif",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        optimize=True,
        disposal=2,
    )


def make_svg_assets() -> None:
    (ASSETS / "hero-terminal.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="360" viewBox="0 0 800 360">
  <rect width="800" height="360" rx="12" fill="#050805"/><rect x="12" y="12" width="776" height="336" rx="10" fill="#0A0F0A" stroke="#174D24" stroke-width="2"/>
  <path d="M13 48h774" stroke="#174D24"/><circle cx="30" cy="30" r="5" fill="#ff5f56"/><circle cx="50" cy="30" r="5" fill="#ffbd2e"/><circle cx="70" cy="30" r="5" fill="#27c93f"/>
  <g font-family="monospace" font-size="14"><text x="38" y="84" fill="#39FF14">[ SYSTEM BOOT ]</text><text x="38" y="113" fill="#D5FFD5">[ INITIALIZING DEVELOPER ENVIRONMENT... ]</text><text x="38" y="142" fill="#D5FFD5">[ LOADING MODULES.................. OK ]</text><text x="38" y="171" fill="#D5FFD5">[ CONNECTING TO GITHUB............. OK ]</text><text x="38" y="200" fill="#00FF41">[ USER: ARVAZEANN ]</text><text x="38" y="229" fill="#39FF14">[ ACCESS GRANTED ]</text><text x="38" y="270" fill="#39FF14">root@arvazeann:~$ whoami</text><text x="38" y="306" fill="#D5FFD5" font-size="24">ZEANAJAA</text><text x="38" y="330" fill="#83A889">INFORMATICS STUDENT / DEVELOPER IN PROGRESS</text></g>
</svg>
""",
        encoding="utf-8",
    )
    matrix = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="150" viewBox="0 0 800 150">
  <rect width="800" height="150" fill="#050805"/><g font-family="monospace" font-size="15" fill="#00AA2A">"""
    columns = ["A 0 1 { } 0 [ ] 1", "1 $ # 0 + - 1 /", "> 1 < = 0 % & 1", "0 : ; / 1 ? ! 0", "# 0 @ + 1 - * 1", "1 % & = 0 / $"]
    for index, chars in enumerate(columns):
        x = 18 + index * 130
        for row, char in enumerate(chars.split()):
            y = 22 + row * 15
            opacity = ".95" if row == 0 else str(max(.15, .75 - row * .07))
            matrix += f'<text x="{x}" y="{y}" opacity="{opacity}">{escape(char)}</text>'
    matrix += "</g></svg>\n"
    (ASSETS / "matrix-rain.svg").write_text(matrix, encoding="utf-8")

    (ASSETS / "terminal-divider.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="38" viewBox="0 0 1200 38">
  <rect x="0" y="18" width="1200" height="1" fill="#174D24"/>
  <path d="M0 19H510L530 7H670L690 19H1200" fill="none" stroke="#39FF14" stroke-opacity=".7"/>
  <circle cx="600" cy="19" r="4" fill="#39FF14"/>
  <text x="548" y="34" fill="#83A889" font-family="monospace" font-size="10">:: SYSTEM LINK ::</text>
</svg>
""",
        encoding="utf-8",
    )
    (ASSETS / "neon-footer.svg").write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="110" viewBox="0 0 1200 110">
  <rect width="1200" height="110" rx="10" fill="#050805"/>
  <path d="M0 12H450L470 32H730L750 12H1200" fill="none" stroke="#39FF14" stroke-opacity=".75"/>
  <text x="600" y="62" text-anchor="middle" fill="#39FF14" font-family="monospace" font-size="15">[ CONNECTION ESTABLISHED ]</text>
  <text x="600" y="88" text-anchor="middle" fill="#83A889" font-family="monospace" font-size="12">STAY CURIOUS.  KEEP BUILDING.</text>
</svg>
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    make_hero()
    make_rain()
    make_svg_assets()
    for path in sorted(ASSETS.iterdir()):
        if path.is_file():
            print(f"{path.name}: {path.stat().st_size:,} bytes")
