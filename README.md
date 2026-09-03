# EPUB Japanese Brightness

将轻小说机翻机器人下载的中日双语 EPUB 进行亮暗对调：

- 日语设为亮色，作为主要阅读内容
- 中文设为暗色，作为辅助参考
- 原始 EPUB 不会被覆盖
- 默认使用 `opacity` 调整文字明暗，适合深色背景阅读器

## 环境要求

- Python 3.10 或更高版本
- 无需安装第三方依赖

## 使用方法

```powershell
python epub_language_brightness.py "输入文件.epub"
```

默认会生成 `输入文件.bright-japanese.epub`。

指定输出文件和明暗程度：

```powershell
python epub_language_brightness.py "输入文件.epub" `
  --japanese-opacity 1 `
  --chinese-opacity 0.4 `
  -o "输出文件.epub"
```

透明度范围为 `0` 到 `1`：

- `1`：完全显示
- `0.4`：半透明偏暗
- `0`：完全透明，不建议使用

## 识别规则

脚本处理 EPUB 内的 XHTML/HTML 段落：

- 同时包含汉字和假名（平假名或片假名）时，识别为日语
- 只包含汉字时，识别为中文
- 无法判断的内容保持原样

这种规则适用于轻小说机翻机器人常见的中日双语排版。不同 EPUB 的排版方式可能不同，建议先用副本测试。

## 项目名称

推荐仓库名称：`epub-japanese-brightness`

## 开源协议

本项目使用 [MIT License](LICENSE) 发布。
