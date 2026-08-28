---
name: xilehui-header-footer-template
description: 参数化生成厦门大学管理学院 ME 校友会喜乐会竖版海报的顶部身份栏、底部说明栏和透明中部叠加层。适用于需要调整文字、字体、字号、字距、颜色、校徽或 With ME Logo 版本、尺寸与位置，并希望把同一模板交给他人复用的任务；不用于生成完整海报主体。
---

# 喜乐会顶部与页脚参数化模板

用确定性排版生成固定组件，不用图像模型重绘校徽、Logo 或文字。

## 使用流程

1. 默认配置在 `assets/default-config.json`。先确定场景：通用宣传使用 `general`；周边宣传使用 `peripheral-promo`；文化衫宣传使用 `culture-shirt-promo`。无需定制时直接运行：

   ```bash
   python scripts/render_template.py --output-dir <输出目录>
   ```

2. 周边或文化衫宣传时用 `--set scenario=peripheral-promo` 或 `--set scenario=culture-shirt-promo`；这两个场景固定显示“本品销售结余全部纳入本届活动经费”。其他场景不自动带入该资金口径。
3. 用户要调整颜色、文字、字号、字距、坐标、尺寸或资产版本时，读取 [references/configuration.md](references/configuration.md)，复制默认配置后修改，或用重复的 `--set 键=值` 临时覆盖。
4. 输出包含：独立顶部栏、独立底部栏、2048×3072 的透明中部叠加层，以及本次实际生效的配置 JSON。
5. 视觉检查顶部和底部 PNG；再验证叠加层中部 Alpha 必须为 0，上下固定区 Alpha 必须为 255。

## 固定原则

- 校徽与 With ME Logo 只能复用 `assets/` 内母版或用户明确提供的替代资产，不允许 AI 重绘。
- 默认画布、位置、字号和色彩来自当前确认版；用户没有点名的参数保持默认。
- PDF 是校徽母版，渲染时默认使用同目录的高清 PNG。不要覆盖或重新保存 PDF 母版。
- 允许自定义颜色。仍要保持喜乐会官方品牌识别时，优先使用 `#4A1420`、`#7A2E3D`、`#A9976A`、`#4F6272`、`#E7E0D3`、`#2E2A26`。
- 字体通过候选路径自动查找；若目标电脑缺少中文字体，要求使用者在配置的 `fonts` 中填入本机 `.ttf` 或 `.ttc` 路径。
- Windows 默认优先微软雅黑粗体；macOS 默认优先 Hiragino Sans GB W6，并保留黑体中等字重回退。TTC 字体候选必须同时记录 `path` 与 `index`，避免误用常规字重。
- `output.prefix` 只能是文件名前缀，不得包含绝对路径、目录分隔符或 `..`。
- 这是海报组件模板，不是可直接发布的完整外宣成稿。完整成稿仍需按具体活动补齐主体信息、二维码和必要联合署名。

## 内置资产

- `assets/xmu-logo-deep-wine-red.pdf` 与对应 PNG：深酒红校徽。
- `assets/xmu-logo-champagne-gold.pdf` 与对应 PNG：香槟金校徽。
- `assets/with-me-transparent.png`：透明背景 With ME Logo，默认使用。
- `assets/with-me-red-background.png`：红底 With ME Logo。
- `assets/preview.png`：默认模板预览。

资产来源、哈希与许可边界见 [references/asset-provenance.md](references/asset-provenance.md) 和 `assets/manifest.json`。
