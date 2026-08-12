# GitHub 仓库配置清单

## 仓库

- Owner：`Catmint103`
- Repository：`xilehui-brand-agent`
- Visibility：Public（GitHub Pages 与一键下载安装需要公开读取）
- Default branch：`main`
- Description：`Codex agent and reusable brand skill for Xilehui visual production`
- Homepage：`https://catmint103.github.io/xilehui-brand-agent/`
- Topics：`codex`、`agent`、`skill`、`brand-design`、`poster`、`xiamen-university`

## GitHub Pages

- Source：GitHub Actions
- Workflow：`.github/workflows/pages.yml`
- 所需权限：`contents: read`、`pages: write`、`id-token: write`
- 发布地址：`https://catmint103.github.io/xilehui-brand-agent/`
- 一键安装地址：`https://catmint103.github.io/xilehui-brand-agent/install.sh`

## Actions

仓库工作流需要允许 GitHub Actions 运行。`validate.yml` 只读仓库内容；`pages.yml` 只写 Pages deployment，不需要仓库写权限或任何 Secret。

## 本地身份

推送前运行：

```bash
gh auth status
gh api user --jq .login
git remote -v
```

三项应分别确认已登录 `github.com`、用户为 `Catmint103`、远程为 `https://github.com/Catmint103/xilehui-brand-agent.git`。不要添加公司 GitLab remote，也不要把 GitLab token 写入此仓库。

## 协作者

组员只使用时无需仓库写权限，直接 clone 即可。需要共同维护规则或素材时，再在 GitHub 仓库 Settings → Collaborators 中按 GitHub 用户名邀请，并通过 Pull Request 合并。

## 发布前检查

1. `python3 tests/validate_package.py`
2. `python3 skills/create-xilehui-brand-poster/scripts/brand_assets.py verify`
3. 检查 `inputs/`、`outputs/` 没有个人信息、内部二维码或未发布物料。
4. 新增品牌资产时更新 `assets/manifest.json`，并说明来源与使用权限；管院三证合一标识和25MEM班徽母版必须同时校验源文件哈希与生产 PNG 哈希。
