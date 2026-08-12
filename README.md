# 喜乐会品牌视觉生产智能体

[![Validate](https://github.com/Catmint103/xilehui-brand-agent/actions/workflows/validate.yml/badge.svg)](https://github.com/Catmint103/xilehui-brand-agent/actions/workflows/validate.yml)
[![Pages](https://github.com/Catmint103/xilehui-brand-agent/actions/workflows/pages.yml/badge.svg)](https://github.com/Catmint103/xilehui-brand-agent/actions/workflows/pages.yml)

面向厦门大学管理学院 ME 校友会喜乐会品牌宣传组的 Codex 工程。它把主视觉规范、活动口径、推文与邀请函文案库、标准素材、管院三证合一标识与25MEM班徽联合署名、创意路由和质量审计装进一个可复用的品牌 skill，并通过项目级 `AGENTS.md` 编排海报、电子门票、报名长图、社交媒体图片和屏幕画面。

项目主页：<https://catmint103.github.io/xilehui-brand-agent/>

## 最快开始

推荐组员克隆完整工程：

```bash
git clone https://github.com/Catmint103/xilehui-brand-agent.git
cd xilehui-brand-agent
./install.sh
codex --cd .
```

只安装品牌 skill：

```bash
curl -fsSL https://catmint103.github.io/xilehui-brand-agent/install.sh | bash
```

也可以使用 Codex 自带的标准 skill installer：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Catmint103/xilehui-brand-agent \
  --path skills/create-xilehui-brand-poster
```

安装后重新开始一个 Codex 任务，即可用 `$create-xilehui-brand-poster`。如果本机已有旧版本，使用 `./install.sh --force`；脚本会先备份旧目录，不会静默删除。

## 第一次任务

把文案、渠道、尺寸和已有二维码放进 `inputs/`，然后告诉 Codex：

```text
请为第14届中秋喜乐会暨2026级迎新晚会建立一套系列物料，包含 4:5 预热海报、9:16 报名长图和 16:9 屏幕画面。先整理需求卡和规格矩阵，再给 3 个差异明显的视觉命题。地点、价格和二维码尚未确认，不要从旧稿推断。
```

智能体会先区分“已锁定 / 可自主 / 待确认”，再完成创意探索、正式编排、品牌审计和交付留痕。

## 工程结构

```text
.
├── AGENTS.md                         # Codex 项目级智能体入口
├── skills/create-xilehui-brand-poster/
│   ├── SKILL.md                      # 品牌生产工作流
│   ├── agents/openai.yaml            # Skill UI 元数据
│   ├── references/                   # 品牌、活动、文案知识、联合署名、路由与审美规则
│   ├── scripts/                      # 资产验真与配色审计
│   └── assets/                       # 锁定的建筑、标志与纹样母版
├── inputs/                            # 组员放入文案、二维码和待审原稿
├── outputs/                           # Codex 任务输出，默认不提交
├── examples/                          # 演示提示词与验收量表
├── docs/                              # GitHub Pages 静态站点
├── tests/                             # 工程与资产完整性检查
└── install.sh                         # 一键安装品牌 skill
```

## 环境要求

- Codex CLI 或 Codex 桌面应用；
- Git；
- Python 3.10+；
- `pip install -r requirements.txt`，用于资产验真、配色审计和报告构建。

核心视觉生成可按任务调用 Codex 当前环境中的图像、画布或 Figma 能力；这些辅助能力不是仓库安装脚本的一部分。

## 自动检查

```bash
python3 -m pip install -r requirements.txt
python3 tests/validate_package.py
python3 skills/create-xilehui-brand-poster/scripts/brand_assets.py verify
bash -n install.sh
```

GitHub Actions 会在每次推送和 Pull Request 上运行同样的验证，并从 `main` 分支自动部署 Pages。

## 品牌与素材许可

代码和原创文档采用 MIT License。`skills/create-xilehui-brand-poster/assets/` 中的厦大标志、建筑、校方模板提取元素及活动品牌素材不由 MIT License 再授权，仅供已经获得厦门大学或活动组织授权的场景使用。详见 [ASSET-LICENSE.md](ASSET-LICENSE.md)。

## 安全边界

- 不从历史物料推断本届地点、票价、报名截止时间或二维码。
- 不让生成模型重画校徽、建筑、二维码或最终文字。
- 所有对外审核稿和发布稿同时保留管院三证合一标识与25MEM班徽，并使用标准联合署名资产。
- 所有对外发布与业务事实变更必须由品牌宣传组组长确认。
- 公开提交前检查 `inputs/` 与 `outputs/`，避免上传个人信息、内部二维码和未发布物料。
