# EPUB 中日文字亮度处理操作说明

## 文件用途

- `处理EPUB.bat`：接收拖入的 EPUB 文件，并调用 Python 脚本处理。
- `epub_language_brightness.py`：扫描 EPUB 内的 XHTML、HTML 和 HTM 文件，按段落判断日文或中文并设置透明度。

## 推荐操作方法

1. 确认 `处理EPUB.bat` 和 `epub_language_brightness.py` 位于同一个文件夹。
2. 将需要处理的 `.epub` 文件直接拖到 `处理EPUB.bat` 图标上。
3. 等待命令窗口显示处理结果，然后按任意键关闭窗口。
4. 在原 EPUB 所在文件夹中找到新文件。新文件名会增加 `.bright-japanese`，例如：

   `小说.epub` -> `小说.bright-japanese.epub`

原 EPUB 不会被覆盖，建议先用阅读器打开新生成的文件确认效果。

## 处理规则

- 含有日文假名（平假名或片假名）的段落：`opacity=1.0`，保持明亮。
- 含有汉字但不含假名的段落：`opacity=0.4`，显示为较暗颜色。
- 不含汉字的段落，以及无法判断语言的内容：保持原样。
- 处理范围是 EPUB 内的 XHTML、HTML 和 HTM 文件中的常见块级段落，包括 `p`、`div`、`li` 和标题标签。

## 命令行用法（可选）

在该文件夹打开 PowerShell：

```powershell
python .\epub_language_brightness.py "小说.epub"
```

指定输出文件：

```powershell
python .\epub_language_brightness.py "小说.epub" -o "小说-处理后.epub"
```

调整透明度时，数值必须在 `0` 到 `1` 之间：

```powershell
python .\epub_language_brightness.py "小说.epub" --japanese-opacity 1 --chinese-opacity 0.4
```

其中数值越大越亮；日文默认值为 `1.0`，中文默认值为 `0.4`。

## 常见问题

### 窗口提示找不到 Python 脚本

确认 `处理EPUB.bat` 和 `epub_language_brightness.py` 在同一个文件夹，并从 BAT 图标拖入 EPUB，而不是直接在其他目录运行 BAT。

### 提示找不到输入文件

确认拖入的是实际存在的 `.epub` 文件，文件名中包含空格、中文或括号通常也可以正常处理。

### 没有明显变化

脚本按完整块级段落判断语言。如果日文和中文位于同一个段落，段落中只要出现假名，就会按日文处理；如果 EPUB 使用了特殊标签结构，可能无法匹配到对应段落。

### 阅读器无法打开输出文件

先确认源 EPUB 本身可以打开，并检查处理过程中命令窗口是否报告“处理失败”。不要在处理过程中打开或移动源文件；必要时删除输出文件后重新处理副本。