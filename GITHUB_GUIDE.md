# GitHub 上传指引（0 基础也能照做）

> 全程用鼠标，不碰终端、不碰 git 命令。第一次大概 10 分钟搞定。
> 唯一的前提：**需要一个免费 GitHub 账号**。

---

## 第一步：注册一个免费 GitHub 账号（约 3 分钟）

1. 打开浏览器，访问 <https://github.com>。
2. 点右上角 **Sign up**。
3. 按提示填 **邮箱**、**密码**、**用户名**（用户名会用在你仓库的网址里，建议用 `maluyao` 或拼音）。
4. 完成邮箱验证（GitHub 会给你邮箱发一封邮件，点里面的链接）。
5. 回到 GitHub，你就有一个账号了。

> 全程免费，不需要绑银行卡，选 Free 方案即可。

## 第二步：网页新建一个仓库（约 1 分钟）

1. 登录后，点页面右上角的 **＋**，选 **New repository**。
2. 在 **Repository name** 填一个名字，比如 `cosrx-insight-agent`。
3. **Description** 可填一句话（可选）。
4. 选 **Public**（公开，方便面试官直接点开看）。
5. **不要**勾选 "Add a README"（你的 README 我们待会自己传）。
6. 点绿色的 **Create repository** 按钮。

## 第三步：上传文件（网页拖拽，约 3 分钟）

1. 进入刚建好的仓库页面，点 **Add file**，选 **Upload files**。
2. 打开你电脑上的 `cosrx-insight-agent` 文件夹。
3. 把下面「要上传的文件」**整个文件夹选中，拖进浏览器中间的上传区**（也可以先选文件再点选择）。
   GitHub 支持直接拖文件夹，会自动保留目录结构。
4. 等文件列表出现，确认没有漏。
5. 拉到最下面，**Commit changes** 的输入框里填一句说明，比如 `first version`。
6. 点绿色的 **Commit changes** 按钮。

完成。你的项目现在在 GitHub 上了，网址是 `github.com/你的用户名/cosrx-insight-agent`，面试时直接甩这个链接。

## 要上传哪些文件

| 文件 / 文件夹 | 要不要传 | 说明 |
|---|---|---|
| `README.md` | ✅ 必传 | 项目介绍 |
| `RESULTS.md` | ✅ 必传 | 数据与结果报告 |
| `architecture.html` | ✅ 必传 | 架构图（网页版） |
| `scripts/` | ✅ 必传 | 6 个 Agent 脚本，demo 靠它跑 |
| `data/` | ✅ 必传 | 原始 + 清洗后数据 |
| `output/` | ✅ 必传 | 洞察、策划案、质检报告 |
| `INTERVIEW_QA.md` | 🟡 可选 | 追问题库，偏个人，传不传都行 |
| `RESUME_BULLETS.md` | 🟡 可选 | 简历描述，偏个人 |
| `CHANGE_LOG.md` | 🟡 可选 | 修改记录，建议填几行再传 |

## 传完怎么验收

1. 打开仓库网址，确认能点开 `README.md`（内容正常显示）。
2. 点开 `architecture.html` 右上角的 **Download** 或直接点文件名预览（GitHub 网页渲染 HTML 有限，下载到本地双击打开看效果最好）。
3. 确认 `output/` 里的 `marketing_plan_v2.md`、`qa_report.md` 都在。

---

## 附：有基础的用户（可选项）

如果你用过 git，也可以用命令行推：

```bash
cd cosrx-insight-agent
git init
git add .
git commit -m "first version"
git remote add origin https://github.com/你的用户名/cosrx-insight-agent.git
git push -u origin main
```

没把握就退回上面的网页拖拽，效果一样，面试官只看仓库内容。
