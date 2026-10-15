# 机构标识排版与顶部身份栏

2026年10月15日确认纳入 Skill 的横排、叠排方案。仅在当前物料明确要求管院三证合一标识与25MEM班徽共同出现时启用；只要求单个标识时仍用单体资产。启用边界见 [signature-lockup.md](signature-lockup.md)，设计思路见 [signature-design.md](signature-design.md)。

## 选用与复用

| 场景 | 选择 | 排版关系 |
|---|---|---|
| 横版、屏幕、宽幅页脚 | `horizontal` 横排 | 管院在左、班徽在右，按可见图形中心对齐 |
| 手机竖版、窄幅物料 | `stacked` 叠排 | 管院独占上行，班徽在下行居中；同宽下管院横标比横排大约 15% |
| 深色或复杂背景 | `cream` 石灰米底 | 与正文网格对齐的完整通栏承托 |
| 低干扰浅色背景 | `transparent` 透明底 | 保留原有安全空间 |

直接使用 `assets/identity/xilehui-signature-{horizontal|stacked}-{transparent|cream}.png`，等比缩放整组。四个文件只包含现行两个标识，没有校友会 Logo。不得拆出认证图形、改色、重绘或调整标识内部间距。不要把承托做成悬浮圆角卡片。

需重新生成时，从本 Skill 根目录运行：

```bash
python scripts/render_signature.py --layout horizontal --surface cream --output outputs/signature-horizontal.png
python scripts/render_signature.py --layout stacked --surface transparent --output outputs/signature-stacked.png
```

脚本从现行单体 PNG 确定性合成；输出不得写入锁定资产目录。已有输出需显式加 `--force`。

## Canva / Figma / PowerPoint 复现参数

| 项目 | 横排 | 叠排 |
|---|---|---|
| 画布 | 2400 × 352 px | 1200 × 356 px |
| 管院横标 | x=120, y=98, w=1840，等比缩放 | x=70, y=50, w=1060，等比缩放 |
| 25MEM班徽 | x=2080, y=76, w=200，等比缩放 | x=542, y=186, w=116，等比缩放 |
| 背景 | 透明或 #E7E0D3 | 透明或 #E7E0D3 |

坐标和宽度按源文件 Alpha 可见边界计算，只忽略外围完全透明像素。管院源图可见边界为 `(1, 4, 1798, 157)`，班徽为完整画布；前者仅去掉透明边，不裁掉标识主体。横排班徽直径约为管院横标可见高度的 1.28 倍，间隔为 120 px。以可见内容对齐，不机械地把外框设成同样高度。

在设计软件中优先导入整组透明 PNG、锁定长宽比再摆放；石灰米承托作为通栏背景。需独立图层时按上表放置单体，完成后编组并锁定比例，缩放整组；不要拆分管院横标中的名称和三项认证。

## 顶部身份栏

确认版同步到仓库内 `xilehui-header-footer-template` 的默认配置。顶部为 2048 × 300 px：

| 元素 | 配置 |
|---|---|
| 厦大校徽适配框 | x=88, y=58, w=180, h=180 |
| With ME 活动标识适配框 | x=1780, y=65, w=180, h=170 |
| 正式名称第一行 | x=1024, y=52，58 px，字距 1 px，居中 |
| 正式名称第二行 | x=1024, y=138，58 px，字距 1 px，居中 |
| 英文说明行 | 留空 |
| 顶部分隔线 | (88, 284) → (1960, 284)，2 px |

两行正式名称为：

```text
厦门大学管理学院 ME校友大会
第14届中秋喜乐会暨2026级迎新晚会
```

左右标识等比缩放，正式名称沿画布中轴居中。顶部模板使用各平台可用的真实中文粗体；更换字体后按实际字宽复查两侧留白。底部机构署名由本 Skill 按需合成，不自动塞入顶部／页脚模板的说明文字区域。

## 预览与验收

- [两种署名排版对比](../assets/examples/signature-layouts/layout-comparison.png)
- [顶部与页脚应用对比](../assets/examples/signature-layouts/application-comparison.png)
- [顶部身份栏](../assets/examples/signature-layouts/header-preview.png)
- [横排高清应用](../assets/examples/signature-layouts/application-horizontal.png) / [375 px 预览](../assets/examples/signature-layouts/application-horizontal-mobile.png)
- [叠排高清应用](../assets/examples/signature-layouts/application-stacked.png) / [375 px 预览](../assets/examples/signature-layouts/application-stacked-mobile.png)
- [横排署名 375 px 检查](../assets/examples/signature-layouts/signature-horizontal-mobile.png) / [叠排署名 375 px 检查](../assets/examples/signature-layouts/signature-stacked-mobile.png)

应用示意用于检查标识层级，不作为完整活动海报或以后活动的事实来源；日期和名称仍按 `current-campaign.md` 核对。示意图沿用提交前的“排版审核预览”图注，确认对象是这里记录的排版方案。

在原尺寸、25% 缩略图和目标手机尺寸检查标识完整、无遮挡、没有变形、主次清楚。375 px 预览用于判断整体识别和层级；认证细字及班徽环形细字需放大高清图核对，不承诺在手机小图中逐字可读。印刷、LED 和设计软件最终导出仍按实际使用尺寸检查。

运行 `python scripts/brand_assets.py verify` 核验图像与源母版哈希。仓库的 `tests/validate_package.py` 会从两份现行单体重建四款署名，与确认素材逐像素比较；顶部模板继续覆盖三种场景与透明中部检查。

### 本次入库检查记录

2026年10月15日本地验证：13 张确认素材与预览原样归档；完整资产库 29 张图片、6 份源母版哈希通过。四款署名重新生成后与确认稿逐像素一致；默认顶部与确认的顶部预览逐像素一致，原模板页脚像素保持不变。

横排与叠排应用图已通过深色配色审计；原尺寸顶部、整体对比及 375 px 标识预览已人工查看。两行名称完整，标识无越界、遮挡或非等比变形。机构原生色仅存在于标识内部；源资产未改写。打印、LED 和实际设计软件文档不在本次验证范围内。
