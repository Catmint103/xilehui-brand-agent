# 标准资产目录

建筑与基础厦大屏幕标志从用户提供的两套厦大 PPT 提取；厦大校徽及嘉庚体、鲁迅体校名字样的矢量母版来自厦门大学官网“学校标识”下载包；管院三证合一标识与25MEM班徽来自用户提供的正式 PSD／AI 源文件，管理学院校友会标识来自用户提供的校友会原图。使用时直接读取资产文件，不凭截图重画。

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

## 厦大标志与对外联合署名

| 文件 | 用途 |
|---|---|
| `assets/identity/xmu-lockup.png` | 厦门大学中英文组合标志 |
| `assets/identity/xmu-seal.png` | 独立圆形校徽 |
| `assets/identity/som-alumni-association-lockup-color.png` | 管理学院校友会透明标识 |
| `assets/identity/som-triple-accreditation-lockup-color.png` | 管院三证合一透明横向标识 |
| `assets/identity/mem25-anniversary-badge-color.png` | 25MEM 透明班徽 |
| `assets/identity/xilehui-publicity-signature-light.png` | 浅底对外物料首选联合署名 |
| `assets/identity/xilehui-publicity-signature-dark.png` | 深底对外物料米色承托联合署名 |

校徽、组合标志、管理学院校友会标识、三证合一标识和25MEM班徽都属于完整身份标志。不得拆字、重排、拉伸、描边或让生图模型重建。基础厦大校徽和校名组合标志只在用户明确要求时使用；管理学院校友会标识、三证合一标识与25MEM班徽是所有对外喜乐会物料的必选三方联合署名，完整排版规则见 `signature-lockup.md`。

## 可编辑母版

| 文件 | 格式 | 说明 |
|---|---|---|
| `assets/identity/masters/som-triple-accreditation-lockup-master.psd` | PSD | 管院三证合一透明位图母版 |
| `assets/identity/masters/som-triple-accreditation-lockup-master.ai` | AI / PDF-compatible | 管院三证合一矢量母版 |
| `assets/identity/masters/som-alumni-association-lockup-source.jpg` | JPG | 用户提供的管理学院校友会标识源图 |
| `assets/identity/masters/mem25-anniversary-badge-master.psd` | PSD | 25MEM 班徽高清母版 |
| `assets/identity/masters/xmu-seal-official-vector.pdf` | PDF | 厦大官网校徽矢量母版；印刷、喷绘和任意尺寸导出时优先使用 |
| `assets/identity/masters/xmu-wordmark-jiageng-official-vector.pdf` | PDF | 厦大官网嘉庚体“厦门大学”矢量校名字样 |
| `assets/identity/masters/xmu-wordmark-luxun-official-vector.pdf` | PDF | 厦大官网鲁迅体“厦门大学”矢量校名字样 |

母版只用于正式重新导出和核验，不直接嵌入网页或海报。日常屏幕稿继续使用透明 PNG；需要放大或交付印刷厂时使用官方 PDF。生产 PNG 由仓库根目录 `scripts/build_co_brand_assets.py` 从母版生成。

## 来源与验真

- `2026厦大ppt模板 - 芙蓉春暖.pptx` SHA-256：`7bf7e1a09b19343ba664b83b75ffacf64cb3ba3ba7c74d06196de7477998b939`
- `2026厦大ppt模板-鹭岛听潮.pptx` SHA-256：`13c38ec3c664b4e6c339a834ca867cb69af467f938888ac3263b0a49f12a2d59`
- `喜乐会-With ME同行-视觉方向初探-工作稿-20260728-v4.pdf` SHA-256：`28d1678632380ddc4d965329f1e157f361d27bea9a3f5600369107b05b58ddf7`
- 厦门大学官网“学校标识”下载包：<https://www.xmu.edu.cn/sdgl/xxbs.htm>。三份 PDF 均为单页纯矢量路径，不含嵌入位图：
  - `xmu-logo.pdf` SHA-256：`66c40b7ae36fddcf12b48f26e2488f4f392cdc88888438ee4fc5c3e2cfb9a851`
  - `xmu-zi-jiageng.pdf` SHA-256：`b88ad384bce3be68e86137c58104d51098d23ac37a7b8ad8fd8439da5ccabea7`
  - `xmu-zi-luxun.pdf` SHA-256：`40afaa615e92940639dccf539bd9c8ba99ff38ee0ca2aedc7663cc990bf30d5b`
- `三证合一管院正式LOGO2.psd`、`三证合一管院正式LOGO.ai`、管理学院校友会源图与 `25MEM班徽_定稿_260604.psd` 的源文件哈希记录在 `assets/manifest.json`，仓库内采用中性英文文件名归档。

具体资产哈希记录在 `assets/manifest.json`。运行 `python scripts/brand_assets.py verify` 验证安装后的母版是否完整。
