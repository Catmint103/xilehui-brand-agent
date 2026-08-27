# 参数说明

所有尺寸和坐标均以像素计，默认基准画布为 2048×3072。

## 快速使用

生成默认版：

```bash
python scripts/render_template.py --output-dir outputs
```

复制 `assets/default-config.json` 后完整定制：

```bash
python scripts/render_template.py --config my-config.json --output-dir outputs
```

只覆盖少量参数：

```bash
python scripts/render_template.py --output-dir outputs \
  --set colors.background=#F4EEE4 \
  --set colors.primary=#6A1524 \
  --set text.organization.size=64 \
  --set assets.seal.variant=champagne-gold
```

PowerShell 中数组或带空格文字要整体加引号：

```powershell
python scripts/render_template.py --output-dir outputs `
  --set 'assets.logo.box=[1660,20,310,230]' `
  --set 'text.footer_line_1.content=自定义第一行文字'
```

## 可调字段

- `canvas`：总宽高、顶部高度、底部高度。
- `colors`：主色、辅色、金色强调、背景色、蓝灰和炭黑。文字和分隔线通过颜色名称引用。
- `fonts`：每种字体的候选文件路径，按顺序查找。
- `assets.seal`：校徽显示开关、版本、路径、位置尺寸、去白底和单色着色。
- `assets.logo`：With ME Logo 显示开关、版本、路径、位置尺寸、去白底和单色着色。
- `text.*`：内容、x/y、字体、字号、字距、颜色和对齐方式。
- `dividers`：上下分隔线的位置、粗细和颜色。
- `output.prefix`：输出文件名前缀。

## 资产选择

校徽可选 `deep-wine-red` 或 `champagne-gold`；With ME Logo 可选 `transparent` 或 `red-background`。

要使用自己的文件，把 `custom_path` 改为绝对路径，或改为相对于配置文件／Skill 根目录的相对路径。`custom_path` 非空时优先于 `variant`。

`tint` 为 `null` 时保留原色；填入 `#RRGGBB` 时按原透明度转为单色。红底 Logo 不建议使用 `tint`，因为它本身含不透明底色。

## 输出

- `<prefix>-header.png`：独立顶部栏。
- `<prefix>-footer.png`：独立底部栏。
- `<prefix>-overlay.png`：上下固定、中间透明的完整叠加层。
- `<prefix>-effective-config.json`：本次实际使用的配置，便于他人复现。

