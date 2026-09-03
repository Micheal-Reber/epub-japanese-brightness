#!/usr/bin/env python3
"""Make Japanese text bright and Chinese text dim in a reflowable EPUB."""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path


BLOCK_TAGS = ("p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6")
BLOCK_RE = re.compile(
    r"<(?P<tag>" + "|".join(BLOCK_TAGS) + r")\b(?P<attrs>[^>]*)>(?P<body>.*?)"
    r"</(?P=tag)\s*>",
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]*>")
KANA_RE = re.compile(r"[\u3040-\u30ff\u31f0-\u31ff]")
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
STYLE_RE = re.compile(r"(\sstyle\s*=\s*)(['\"])(.*?)\2", re.IGNORECASE | re.DOTALL)
OPACITY_RE = re.compile(r"(^|;)(\s*opacity\s*:\s*)[^;]*(?=;|$)", re.IGNORECASE)


def visible_text(fragment: str) -> str:
    """Remove markup and decode entities before language detection."""
    fragment = re.sub(r"<(script|style)\b[^>]*>.*?</\1\s*>", "", fragment,
                      flags=re.IGNORECASE | re.DOTALL)
    return re.sub(r"\s+", "", html.unescape(TAG_RE.sub("", fragment)))


def language_of(fragment: str) -> str | None:
    text = visible_text(fragment)
    if not HAN_RE.search(text):
        return None
    if KANA_RE.search(text):
        return "ja"
    return "zh"


def set_opacity(start_tag: str, opacity: float) -> str:
    value = f"{opacity:g}"

    def replace_style(match: re.Match[str]) -> str:
        style = match.group(3)
        if OPACITY_RE.search(style):
            style = OPACITY_RE.sub(
                lambda item: f"{item.group(1)}{item.group(2)}{value}", style, count=1
            )
        else:
            style = style.rstrip()
            if style and not style.endswith(";"):
                style += ";"
            style += f" opacity:{value};"
        return f"{match.group(1)}{match.group(2)}{style}{match.group(2)}"

    if STYLE_RE.search(start_tag):
        return STYLE_RE.sub(replace_style, start_tag, count=1)
    return start_tag[:-1] + f' style="opacity:{value};">'


def transform_xhtml(data: bytes, japanese_opacity: float, chinese_opacity: float) -> tuple[bytes, int, int]:
    text = data.decode("utf-8")
    changed = {"ja": 0, "zh": 0}

    def replace_block(match: re.Match[str]) -> str:
        language = language_of(match.group("body"))
        if language is None:
            return match.group(0)
        opacity = japanese_opacity if language == "ja" else chinese_opacity
        attrs = set_opacity(match.group("attrs"), opacity)
        changed[language] += 1
        return f"<{match.group('tag')}{attrs}>{match.group('body')}</{match.group('tag')}>"

    transformed = BLOCK_RE.sub(replace_block, text)
    return transformed.encode("utf-8"), changed["ja"], changed["zh"]


def output_path_for(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.bright-japanese{input_path.suffix}")


def convert_epub(input_path: Path, output_path: Path, japanese_opacity: float,
                 chinese_opacity: float) -> tuple[int, int]:
    if input_path.resolve() == output_path.resolve():
        raise ValueError("输出文件不能覆盖输入文件，请指定另一个路径。")

    changed_ja = changed_zh = 0
    with zipfile.ZipFile(input_path, "r") as source, zipfile.ZipFile(
        output_path, "w", allowZip64=True
    ) as target:
        entries = source.infolist()
        entries.sort(key=lambda entry: (entry.filename != "mimetype",))
        for entry in entries:
            data = source.read(entry)
            if entry.filename.lower().endswith((".xhtml", ".html", ".htm")):
                data, count_ja, count_zh = transform_xhtml(
                    data, japanese_opacity, chinese_opacity
                )
                changed_ja += count_ja
                changed_zh += count_zh

            info = zipfile.ZipInfo(entry.filename, entry.date_time)
            info.comment = entry.comment
            info.extra = entry.extra
            info.internal_attr = entry.internal_attr
            info.external_attr = entry.external_attr
            info.create_system = entry.create_system
            info.compress_type = zipfile.ZIP_STORED if entry.filename == "mimetype" else entry.compress_type
            target.writestr(info, data)
    return changed_ja, changed_zh


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="将 EPUB 中的日文设为亮色、中文设为暗色（通过 opacity）。"
    )
    parser.add_argument("input", type=Path, help="输入 EPUB 文件")
    parser.add_argument("-o", "--output", type=Path, help="输出 EPUB 文件")
    parser.add_argument("--japanese-opacity", type=float, default=1.0,
                        help="日文透明度，默认 1.0")
    parser.add_argument("--chinese-opacity", type=float, default=0.4,
                        help="中文透明度，默认 0.4")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 0 <= args.japanese_opacity <= 1 or not 0 <= args.chinese_opacity <= 1:
        print("透明度必须在 0 到 1 之间。", file=sys.stderr)
        return 2
    if not args.input.is_file():
        print(f"找不到输入文件：{args.input}", file=sys.stderr)
        return 2

    output = args.output or output_path_for(args.input)
    try:
        count_ja, count_zh = convert_epub(
            args.input, output, args.japanese_opacity, args.chinese_opacity
        )
    except (OSError, zipfile.BadZipFile, UnicodeError, ValueError) as error:
        print(f"处理失败：{error}", file=sys.stderr)
        return 1

    print(f"已生成：{output}")
    print(f"日文段落：{count_ja}（opacity={args.japanese_opacity:g}）")
    print(f"中文段落：{count_zh}（opacity={args.chinese_opacity:g}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
