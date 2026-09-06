# EPUB Japanese Brightness

将轻小说机翻机器人下载的中日双语 EPUB 进行亮暗对调：

- 日语设为亮色，作为主要阅读内容
- 中文设为暗色，作为辅助参考
- 原始 EPUB 不会被覆盖
- 默认使用 `opacity` 调整文字明暗，适合深色背景阅读器
- 无需安装第三方 Python 依赖

## 环境要求

- Windows（使用 `处理EPUB.bat` 时）
- Python 3.10 或更高版本

## 使用方法

### 拖拽运行

1. 确认 `处理EPUB.bat` 和 `epub_language_brightness.py` 在同一个文件夹。
2. 将 EPUB 文件拖到 `处理EPUB.bat` 图标上。
3. 输出文件会生成在原 EPUB 所在文件夹，文件名增加 `.bright-japanese`。

例如：

```text
输入文件.epub
输入文件.bright-japanese.epub
```

也可以直接使用命令行：

```powershell
python .\epub_language_brightness.py "输入文件.epub"
```

指定输出文件和明暗程度：

```powershell
python .\epub_language_brightness.py "输入文件.epub" `
  --japanese-opacity 1 `
  --chinese-opacity 0.4 `
  -o "输出文件.epub"
```

透明度范围为 `0` 到 `1`：

- `1`：完全显示
- `0.4`：半透明偏暗
- `0`：完全透明，不建议使用

## 识别规则

脚本处理 EPUB 内 XHTML、HTML 和 HTM 文件中的实际正文段落：

- 含汉字并含平假名或片假名时，识别为日语
- 含汉字但不含假名时，识别为中文
- 不含汉字或无法判断的内容保持原样
- 外层 `div` 容器不会参与语言判断，避免整页中日文被一起处理

这种规则适用于轻小说机翻机器人常见的中日双语排版。不同 EPUB 的排版方式可能不同，建议先用副本测试。

## 注意事项

- 输出文件不会覆盖输入文件。
- 如果阅读器仍显示旧效果，请关闭书籍后删除阅读器缓存，重新导入最新输出文件。
- 如果中文和日文位于同一个段落，脚本会按该段落整体判断，不能分别设置段落内部的文字。
- 脚本会修改原 EPUB 中已有的 `opacity`，确保日文段落能恢复为亮色。

## 操作说明

更详细的中文操作步骤见 [EPUB处理操作说明.md](EPUB处理操作说明.md)。

## 开源协议

本项目使用 [MIT License](LICENSE) 发布。
