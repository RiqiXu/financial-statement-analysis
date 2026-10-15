# 从零开始：Mac 上的基本面量化项目

适用：Mac（包括 M2），希望借助 Codex 学习项目流程的人。核对日期：2026-10-09。

你不用一天做完。每次只完成一课，看到验收结果后再继续。安装过程因网络速度不同，可能需要较长时间。

## 0. 先认清工具

| 工具 | 用来做什么 | 你会在哪看到它 |
| --- | --- | --- |
| Python | 执行 .py 程序 | 终端中的 python 命令 |
| VS Code | 编辑文件、看项目、运行命令 | 代码编辑器窗口 |
| 终端 Terminal | 输入命令并查看输出 | Mac 自带终端，或 VS Code 下方终端 |
| .venv | 给这个项目单独安装依赖 | 项目中的环境文件夹 |
| AKShare / pandas | 获取金融数据 / 处理表格 | Python 中 import 的库 |
| Git | 在本地保存可追溯的代码版本 | git status、git commit 等命令 |
| GitHub | 托管并分享 Git 仓库 | 后续使用的网站 |
| Codex | 解释、修改代码，协助运行和排错 | VS Code 中的 Codex 面板 |

本教程中，bash 代码框的内容输入到终端，python 代码写进 .py 文件。不要把命令前面额外加上 $。一行命令按一次回车；遇到报错先停在当前步骤。

## 第 1 课：安装 Python，让电脑能够执行代码

**操作位置：浏览器 → Finder → Mac 自带终端。**

1. 打开 https://www.python.org/downloads/macos/ 。在稳定版本中选择 Python 3.13.x 的 macOS installer。AKShare 当前官方安装说明推荐 3.13.x，本教程统一使用它。
2. 打开下载的 .pkg，按安装向导完成。官方 universal2 安装包支持 Apple Silicon 和 Intel。
3. 在 Finder 的“应用程序”中找到 Python 3.13 文件夹，双击 Install Certificates.command，完成证书安装。
4. 按 Command + Space，输入 Terminal 或“终端”，打开它。若安装前已经开着终端，关闭旧窗口重新打开。
5. 输入：

```bash
python3.13 --version
```

**验收：** 出现 Python 3.13.x。这里的 x 是补丁版本，不用和别人的完全一样。若你已安装并且此命令正常，跳过重新安装。

你学到的：安装解释器后，终端可以用它执行程序。这里还没有安装金融数据工具。

## 第 2 课：安装 VS Code，并打开项目文件夹

**操作位置：浏览器 → Finder → VS Code。**

1. 打开 https://code.visualstudio.com/download ，M2 选择 Mac Apple silicon 版本。解压后把 Visual Studio Code 拖到“应用程序”。
2. 解压本起步包。把整个 fundamental-quant-starter 文件夹放到 Finder → 个人文件夹 → Documents（文稿）。保留英文文件夹名，后续命令更方便。
3. 打开 VS Code，选择 File → Open Folder（文件 → 打开文件夹），选中这个文件夹。若询问信任文件，先查看内容后再信任自己要使用的项目。
4. 点击左侧 Extensions（扩展）图标，搜索 Python，安装 Microsoft 发布的 Python 扩展。
5. 选择 Terminal → New Terminal（终端 → 新建终端）。后续命令都在这个下方窗口中输入。

```bash
pwd
ls
```

**验收：** pwd 输出以 fundamental-quant-starter 结尾；ls 能看到 README.md、START_HERE.md、requirements.txt、scripts、reports。

如果文件夹在别的位置，也可以直接从 VS Code 打开它，不必搬动。关键是终端当前目录与项目目录一致。

如果希望从配置环境开始就让 Codex 在编辑器里协助，现在可以先按第 9 课安装并登录扩展，然后回来做第 3 课。

你学到的：项目就是一组文件和文件夹。编辑器负责打开它，终端负责在这个目录中执行命令。

## 第 3 课：建立项目自己的 Python 环境

**操作位置：VS Code 下方终端。** 以下命令逐行运行。

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python --version
python -c "import sys; print(sys.executable)"
```

第一行创建环境；第二行让当前终端使用这个环境；最后两行检查实际使用的解释器。

**验收：** 版本是 3.13.x，解释器路径以 /.venv/bin/python 结尾。终端提示前面通常会出现 (.venv)，但以解释器路径为准。

再按 Command + Shift + P，搜索 Python: Select Interpreter，选项目的 .venv/bin/python。若没有列出，选择输入解释器路径并定位到这个文件。

安装依赖并记录实际版本：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip freeze > requirements-lock.txt
python -c "import akshare, pandas; print('依赖安装成功')"
```

**验收：** 最后一行显示“依赖安装成功”，项目中出现 requirements-lock.txt。

requirements.txt 写需要哪些库；requirements-lock.txt 记录本次实际装了哪些版本。后续复现同一环境可安装后者，但不同操作系统或 Python 版本仍可能存在兼容性差异。

每次新开终端，需要检查当前目录，再执行 source .venv/bin/activate。VS Code 可能自动激活环境，你仍可用 sys.executable 确认。退出环境用 deactivate。

## 第 4 课：运行第一个 Python 文件

**操作位置：VS Code 文件编辑区 + 下方终端。**

点击左侧 scripts 文件夹，再打开 hello.py，查看这几行：

```python
import sys

print("我的基本面量化项目启动了！")
print("当前 Python：", sys.executable)
```

在终端运行：

```bash
python scripts/hello.py
```

**验收：** 显示启动文字和 .venv 的解释器路径。

**自己动手：** 把第一句打印内容改成“我完成了第一段 Python 程序”，按 Command + S 保存，再运行。输出应随之变化。

你学到的：代码写进文件 → 保存 → Python 执行文件 → 查看结果。编辑文件与执行文件是两个动作。

## 第 5 课：写项目目标

**操作位置：VS Code 中的 README.md。**

包中已写了一份起步目标。读完以后，用自己的话修改“研究问题”和“第一阶段交付物”。你应能回答：

- 我要研究什么？先理解盈利能力与现金流质量。
- 第一家公司是谁？贵州茅台，600519，用作数据学习样例。
- 哪个年度？先核对 2024 年度完整财报。
- 本阶段交什么？三张原始表、字段字典、三个指标、一页研究笔记。
- 怎样算完成？能重跑代码、讲清数据来源和指标公式，并与年报核对。

这一步先定义一个能完成的小任务。多公司选股、组合和历史回测放在后续阶段。

**验收：** 不看教程，也能用三句话向别人说明项目做什么、现在做到哪一步、下一步是什么。

## 第 6 课：安装 Git，保存第一份本地版本

**操作位置：VS Code 下方终端。**

```bash
git --version
```

如果 Mac 弹出安装开发者命令行工具的窗口，完成安装，再运行上面命令。若没有可用 Git，运行：

```bash
xcode-select --install
```

完成系统安装后再次检查 git --version；若提示工具已经安装，就继续检查 Git 的具体错误。这里使用 Apple 命令行工具提供的 Git。

在项目目录中初始化仓库：

```bash
git init
git branch -M main
```

下面两行中的名字和邮箱，请替换成你自己的提交署名。它们只配置当前仓库。若以后公开仓库，署名邮箱会随提交公开，可以先在 GitHub 中获取自己的隐私邮箱再填写。

```bash
git config user.name "你的提交署名"
git config user.email "你的提交邮箱"
git status
```

检查 .gitignore 已忽略 .venv、data/raw、缓存和 .env。然后保存代码和说明：

```bash
git add README.md START_HERE.md requirements.txt requirements-lock.txt .gitignore scripts reports
git commit -m "Start fundamental research learning project"
git status
git log --oneline -1
```

**验收：** git log 出现一条提交；git status 显示工作区干净（working tree clean）。

你学到的：修改文件 → git add 选择本次要保存的内容 → git commit 创建版本。Git 在本地工作，这一步还没有上传到 GitHub。

## 第 7 课：获取一家公司的第一张报表

**操作位置：VS Code 下方终端。** 保持 .venv 已激活。

```bash
python scripts/fetch_financials.py
```

脚本默认调用 AKShare 的 stock_financial_report_sina，使用 sh600519，获取“利润表”。这里的 sh 是这个接口需要的上海市场前缀。

脚本的核心工作只有三个：

```python
df = ak.stock_financial_report_sina(stock=args.stock, symbol=name)
df.to_csv(path, index=False, encoding="utf-8-sig")
print(df.iloc[:3, :5].to_string(index=False))
```

第一行返回一个 pandas DataFrame（可以理解为程序中的表格）；第二行把它写成 CSV；第三行预览前三行、前五列。utf-8-sig 便于常见表格软件识别中文。

其余代码负责选公司、创建保存目录、检查是否空表、记录来源和报错。第一次只需读懂这些职责，随后再逐行学习。

**验收：** 终端显示保存路径和大于零的行数；VS Code 左侧 data/raw 中出现一个带公司代码和抓取时间的文件夹，里面有 profit.csv 和 metadata.json。

CSV 不在编辑器预览中自动变成漂亮表格也没关系，双击看文本，或通过 Finder 用 Excel/Numbers 打开。遇到编码导入选项时选择 UTF-8。保留原始文件，分析结果另存。

**自己动手观察：** 找到“报告日”列，确认是否同时有年末和季度日期。此接口返回历史报表，不是只返回 2024 年度一行；不要默认第一行就是你需要的年度。

metadata.json 记录来源、抓取时间和软件版本。它没有把抓取时间当成公司公告时间。

第一张表成功以后再运行：

```bash
python scripts/fetch_financials.py --all
```

**验收：** 新的抓取文件夹中出现 profit.csv、balance.csv、cashflow.csv、metadata.json。如果后面某张表失败，可能只保存前面成功的表，metadata.json 会留下错误；这种情况不算三表完成。

## 第 8 课：从“拿到数据”进入“理解数据”

这一课以人工核对为主，不急着批量写公式。

1. 从公司官网的投资者关系栏目或交易所披露渠道获取 2024 年年度报告。确认公司名称、年度、是否有修订，并记录下载来源和公告日期。
2. 在三张 CSV 中找到报告日为 2024 年末的记录；如有重复版本，先查原因。
3. 对照年报财务报表，找到营业收入、合并净利润、归母净利润、经营活动现金流量净额、归母净资产。把准确 CSV 列名填到 reports/data_dictionary.md。
4. 检查单位，记录是否为元、万元等；核对合并报表口径。年报表格显示的单位可能与 API 不同。
5. 对照 README 中三个公式，先手工算一个净利率，再请 Codex 帮你写计算脚本。ROE 使用平均归母净资产，还需要 2023 年末数值；这里的简化计算与年报加权平均 ROE 有差别。
6. 在 reports/company_note.md 写一句现象，并回到年报寻找业务解释。

**验收：** 能解释一个具体指标的分子、分母、单位、年度和来源。若不能核对，就记录缺口，不填猜测的数值。

这一阶段的报表可能包含后续修订。报告日是会计期间结束日期，“更新日期”不一定是首次公告日期。后面做历史回测时，需要另外建立当时可获得的数据，避免使用未来信息。

修改后保存一个 Git 版本：

```bash
git diff
git add README.md reports scripts
git commit -m "Document first company financial data checks"
```

仅下载 CSV 而未改代码或笔记时，Git 可能显示没有变更，这是因为原始数据被忽略了。先完成笔记再提交即可。

## 第 9 课：在 VS Code 中使用 Codex

**操作位置：VS Code 扩展页面 → Codex 面板。**

1. 从官方说明 https://developers.openai.com/codex/ide/ 进入扩展安装入口，安装 OpenAI 发布的 Codex 扩展。
2. 点击 Codex 图标；找不到时按 Command + Shift + P，执行 Codex: Open Codex Sidebar。
3. 按界面提示使用 ChatGPT 登录。也支持 API key 登录，但本教程采用 ChatGPT 登录；具体可用性以你的账户与界面为准。
4. 保持项目文件夹已打开，让 Codex 基于当前文件指导你。

你可以这样表达自己的学习要求：

“我在 Mac 上学习这个基本面量化项目。请按 START_HERE.md 每次只指导一个小步骤，说明操作位置、命令含义和成功标准。先了解当前进度。修改代码后解释修改，并让我做一个小练习；遇到错误基于实际报错检查原因。当前目标是运行 hello.py。”

使用时形成固定节奏：先说当前小目标 → 看解释 → 自己运行 → 对照结果 → 改一个地方验证理解 → Git 保存。

学习用的请求示例：

- “解释 fetch_financials.py 中 Path 和 to_csv 分别做什么。”
- “我运行这条命令得到下面错误，请先检查解释器路径和依赖，再修复。”
- “我已经核对这些列名，请只帮我实现 2024 年净利率，并解释年度筛选。”
- “给我一个需要自己改两行代码的小练习，等我回答后检查。”

VS Code 中的 Codex 能结合本机项目文件协助。当前聊天中提供的教程和文件不会自动完成你 Mac 上的软件安装；你需要在 Mac 上运行并把具体结果反馈给助手。

## 第 10 课：准备好以后再上传 GitHub

先完成本地运行和一次提交，再进入这一步。创建远程仓库是一个独立动作。

1. 登录自己的 GitHub，选择 New repository，命名为 fundamental-quant-research。可以先选 Private，检查内容后再决定公开。
2. 不勾选自动添加 README、.gitignore、license，因为本地已有内容。
3. 复制该空仓库显示的 HTTPS URL，替换下面 YOUR_REPOSITORY_URL 整个占位内容后运行：

```bash
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

使用 GitHub 当前支持的浏览器或凭证认证流程。不要把账号密码或令牌写入代码、README 或聊天。上传前用 git status、git diff --cached 检查待提交内容。

**验收：** GitHub 页面能看到 README 和 scripts。公开开源前补充代码许可证，并核对上游数据的使用与再分发条件；本包默认不上传原始 CSV。

## 常见卡点

| 现象 | 先检查什么 | 下一步 |
| --- | --- | --- |
| python3.13: command not found | 官方安装是否完成，是否重新开终端 | 回第 1 课确认安装，不修改系统 Python |
| No module named akshare | python -c "import sys; print(sys.executable)" | 激活 .venv，再在同一环境安装 requirements.txt |
| can't open file 或文件不存在 | pwd 与 ls | 回到项目根目录，确认 scripts 文件名 |
| 编辑器说无法解析 import，但命令能跑 | VS Code 选择的解释器 | 重新选 .venv/bin/python |
| SSL 证书错误 | Python 3.13 的证书安装是否完成 | 运行官方 Install Certificates.command，保留完整错误排查 |
| 请求超时、连接失败、空表 | 网络与当前官方接口文档 | 稍后重试，记录完整报错；必要时从正式年报手工开始核对 |
| Git 提示身份未知 | 当前仓库的 user.name、user.email | 配置自己的署名，然后重新 commit |
| Git 没有追踪 CSV | .gitignore 中 data/raw/ | 这是包中设置的行为；提交脚本、说明与研究笔记 |

报错时提供三样信息：执行的命令、完整错误文本、当前解释器路径。这样排查比只说“运行不了”更有效。

## 每次重新开始工作的固定动作

1. VS Code 打开项目文件夹，打开终端。
2. 用 pwd 确认目录；用 source .venv/bin/activate 激活环境。
3. 用 git status 查看进度，读 README 的当前目标。
4. 只完成一个小任务，运行检查；用 git diff 查看修改。
5. 提交完成的代码与笔记，记下下一个小目标。

今天做到第 4 课就可以收工。下一次再完成项目目标和 Git；之后获取数据。这是一条学习顺序，不要求固定一天完成。

## 官方资料

- Python macOS 安装：https://docs.python.org/3/using/mac.html
- Python 下载：https://www.python.org/downloads/macos/
- Python venv：https://docs.python.org/3/library/venv.html
- VS Code macOS：https://code.visualstudio.com/docs/setup/mac
- VS Code Python 环境：https://code.visualstudio.com/docs/python/environments
- Apple 命令行工具：https://developer.apple.com/documentation/xcode/installing-the-command-line-tools
- Git：https://git-scm.com/docs/gittutorial
- GitHub 空仓库上传：https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
- Codex 扩展：https://developers.openai.com/codex/ide/
- Codex 登录：https://developers.openai.com/codex/auth
- AKShare 安装：https://akshare.akfamily.xyz/installation.html
- AKShare 股票接口（查 stock_financial_report_sina）：https://akshare.akfamily.xyz/data/stock/stock.html

本包检查了脚本语法、离线保存和异常记录；真实接口请求以及你的 Mac 安装结果需要实际运行验证。后续每次修复都应基于真实报错更新。
