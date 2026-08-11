# 标准资产目录

这些母版均从用户提供的两套厦大 PPT 提取。两套 PPT 的共同建筑、凤凰花和校徽文件哈希一致。使用时直接读取资产文件，不凭截图重画。

这些机构标志、建筑形象和活动素材不由仓库的 MIT License 再授权。使用者必须确认自己已获得适用场景所需的校方或活动组织授权；完整边界见仓库根目录 `ASSET-LICENSE.md`。

## 建筑

| ID | 文件 | 像素 | 适合场景 |
|---|---|---:|---|
| A01 | `assets/architecture/xmu-01-statue-front.png` | 1773×2364 | 竖版正中主景、纪念性构图 |
| A02 | `assets/architecture/xmu-02-phoenix-corner.png` | 1536×2730 | 竖版侧景、凤凰花前景 |
| A03 | `assets/architecture/xmu-03-pitched-roof-hall.png` | 2730×1535 | 横版顶部、横向框景 |
| A04 | `assets/architecture/xmu-04-tower-front-source.png` | 1773×2364 | 正面塔楼完整源图 |
| A04-C | `assets/architecture/xmu-04b-tower-front-cutout.png` | 1500×2000 | 横版左侧、透明叠加 |
| A05 | `assets/architecture/xmu-05-tiered-main-building-cutout.png` | 2000×1124 | 顶部横章、标题上方金线稿 |
| A06 | `assets/architecture/xmu-06-phoenix-building-landscape-cutout.png` | 2000×1124 | 横版左侧、凤凰花与建筑结合 |
| A07 | `assets/architecture/xmu-07-roof-eave-right-cutout.png` | 1125×2000 | 右侧屋檐裁切、边框式构图 |

A01-A05 对应对话中确认的五类官方建筑。A06-A07 是同一 PPT 内更适合横版的原始透明素材。优先使用透明资产；需要使用 RGB 白底源图时，通过 `brand_assets.py tint` 提取线稿，不得手工描边。

## 凤凰花

| 文件 | 用途 |
|---|---|
| `assets/motifs/phoenix-flower-line.png` | 细线水印、低对比背景纹样 |
| `assets/motifs/phoenix-flower-emboss.png` | 纸压、错位压花、局部暗纹 |

保持纹样比例。允许旋转、裁切和镜像，但不要改变花瓣结构或重复成高密度墙纸。

## 厦大标志

| 文件 | 用途 |
|---|---|
| `assets/identity/xmu-lockup.png` | 厦门大学中英文组合标志 |
| `assets/identity/xmu-seal.png` | 独立圆形校徽 |

校徽和组合标志属于完整身份标志。不得拆字、重排、拉伸、描边或让生图模型重建。只有用户明确要求出现校徽时才使用。

## 来源与验真

- `2026厦大ppt模板 - 芙蓉春暖.pptx` SHA-256：`7bf7e1a09b19343ba664b83b75ffacf64cb3ba3ba7c74d06196de7477998b939`
- `2026厦大ppt模板-鹭岛听潮.pptx` SHA-256：`13c38ec3c664b4e6c339a834ca867cb69af467f938888ac3263b0a49f12a2d59`
- `喜乐会-With ME同行-视觉方向初探-工作稿-20260728-v4.pdf` SHA-256：`28d1678632380ddc4d965329f1e157f361d27bea9a3f5600369107b05b58ddf7`

具体资产哈希记录在 `assets/manifest.json`。运行 `python scripts/brand_assets.py verify` 验证安装后的母版是否完整。
