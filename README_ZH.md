# 全栈 FastAPI 模板



![测试 Docker Compose]()



![测试后端]()



![代码覆盖率]()

## 技术栈和功能



* ⚡ **FastAPI** 用于构建 Python 后端 API


  * 🧰 **SQLModel** 用于 Python 数据库交互（ORM 框架）

  * 🔍 **Pydantic**（FastAPI 内置依赖）用于数据验证和配置管理

  * 💾 **PostgreSQL** 作为 SQL 数据库

* 🚀 **React** 用于前端开发


  * 💃 基于 TypeScript、React Hooks、**Vite** 构建现代化前端技术栈

  * 🎨 基于 **Tailwind CSS** 和 **shadcn/ui** 实现前端组件开发

  * 🤖 自动生成前端 API 调用客户端

  * 🧪 **Playwright** 用于端到端测试

  * 🦇 支持深色模式

* 🐋 **Docker Compose** 适配开发与生产环境

* 🔒 默认启用安全的密码哈希机制

* 🔑 支持 JWT（JSON Web Token）身份认证

* 📫 基于邮件的密码找回功能

* 📬 **Mailcatcher** 用于开发环境下的本地邮件测试

* ✅ 使用 **Pytest** 进行后端测试

* 📞 **Traefik** 作为反向代理 / 负载均衡器

* 🚢 提供完整的 Docker Compose 部署文档，包含 Traefik 反向代理配置及 HTTPS 证书自动生成方案

* 🏭 基于 GitHub Actions 实现持续集成（CI）与持续部署（CD）

### Dashboard Login

[![API docs](img/login.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Admin

[![API docs](img/dashboard.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Items

[![API docs](img/dashboard-items.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Dashboard - Dark Mode

[![API docs](img/dashboard-dark.png)](https://github.com/fastapi/full-stack-fastapi-template)

### Interactive API Documentation

[![API docs](img/docs.png)](https://github.com/fastapi/full-stack-fastapi-template)

## 快速上手

你可以**直接 Fork 或克隆**本仓库，并直接投入使用。

✨ 开箱即用 ✨

### 如何搭建私有仓库

GitHub 不支持直接将公共仓库的 Fork 版本转为私有仓库，如需搭建私有仓库，请按以下步骤操作：



1. 在 GitHub 上创建一个新的空白仓库，例如命名为 `my-full-stack`

2. 手动克隆本模板仓库，并指定新项目名称：



```
git clone git@github.com:fastapi/full-stack-fastapi-template.git my-full-stack
```



1. 进入项目目录：



```
cd my-full-stack
```



1. 将本地仓库的远程地址修改为你新建的私有仓库地址（地址可从 GitHub 仓库页面复制）：



```
git remote set-url origin git@github.com:你的用户名/my-full-stack.git
```



1. 添加原模板仓库为上游远程仓库，以便后续同步更新：



```
git remote add upstream git@github.com:fastapi/full-stack-fastapi-template.git
```



1. 将代码推送到你的私有仓库：



```
git push -u origin master
```

### 同步原模板的更新

克隆仓库并完成自定义开发后，如需同步原模板的最新更新，可按以下步骤操作：



1. 先确认已添加原模板仓库为上游远程仓库，执行以下命令查看远程仓库配置：



```
git remote -v
```

正常配置会显示如下内容：



```
origin    git@github.com:你的用户名/my-full-stack.git (fetch)

origin    git@github.com:你的用户名/my-full-stack.git (push)

upstream    git@github.com:fastapi/full-stack-fastapi-template.git (fetch)

upstream    git@github.com:fastapi/full-stack-fastapi-template.git (push)
```



1. 拉取上游仓库的最新代码（不自动合并）：



```
git pull --no-commit upstream master
```

此命令会下载原模板的最新代码，但不会自动创建合并提交，方便你在提交前检查代码冲突。



1. 若出现代码冲突，在代码编辑器中手动解决冲突。

2. 冲突解决完成后，完成合并提交：



```
git merge --continue
```

### 项目配置

你可以通过修改项目中的 `.env` 文件来完成自定义配置。

在部署项目前，请务必修改以下关键配置项的默认值：



* `SECRET_KEY`

* `FIRST_SUPERUSER_PASSWORD`

* `POSTGRES_PASSWORD`

**建议**：将这些敏感配置项通过环境变量注入，而非直接写入 `.env` 文件。

更多部署细节请参考 deployment.md 文档。

### 生成密钥

`.env` 文件中部分配置项的默认值为 `changethis`，需要替换为安全的随机密钥。

你可以通过以下 Python 命令生成密钥：



```
python -c "import secrets; print(secrets.token\_urlsafe(32))"
```

复制命令输出的字符串，即可作为密码或密钥使用。重复执行该命令可生成多个不同的安全密钥。

## 另一种使用方式：基于 Copier 生成项目

本仓库支持通过 **Copier** 工具生成新项目，Copier 会自动复制模板文件、交互式询问配置信息，并根据你的输入自动更新 `.env` 文件。

### 安装 Copier

你可以通过 pip 安装 Copier：



```
pip install copier
```

如果你已安装 **pipx**，推荐使用 pipx 运行 Copier（无需手动安装）：



```
pipx install copier
```

**注意**：若已安装 pipx，无需单独安装 Copier，可直接通过 pipx 调用。

### 使用 Copier 生成项目



1. 先确定新项目的目录名称，例如 `my-awesome-project`

2. 进入需要创建项目的父目录，执行以下命令生成项目：



```
copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```



1. 若使用 pipx 且未安装 Copier，可直接运行：



```
pipx run copier copy https://github.com/fastapi/full-stack-fastapi-template my-awesome-project --trust
```

**注意**：`--trust` 参数是必须的，它允许 Copier 执行项目生成后的脚本（用于自动更新 `.env` 文件）。

### 配置项说明

运行 Copier 后，工具会交互式询问一系列配置项。你可以提前准备好相关信息，也可以在生成项目后通过修改 `.env` 文件调整配置。

以下是所有配置项及其默认值（部分为自动生成）：



* `project_name`：（默认值：`"FastAPI Project"`）项目名称，会展示给 API 用户（对应 `.env` 文件配置）

* `stack_name`：（默认值：`"fastapi-project"`）用于 Docker Compose 标签和项目命名的堆栈名称（不允许包含空格和句点，对应 `.env` 文件配置）

* `secret_key`：（默认值：`"changethis"`）项目密钥，用于安全验证（对应 `.env` 文件配置），可通过前文的 Python 命令生成

* `first_superuser`：（默认值：`"``admin@example.com``"`）初始超级管理员邮箱（对应 `.env` 文件配置）

* `first_superuser_password`：（默认值：`"changethis"`）初始超级管理员密码（对应 `.env` 文件配置）

* `smtp_host`：（默认值：空字符串）发送邮件的 SMTP 服务器地址，可后续在 `.env` 文件中配置

* `smtp_user`：（默认值：空字符串）发送邮件的 SMTP 服务器用户名，可后续在 `.env` 文件中配置

* `smtp_password`：（默认值：空字符串）发送邮件的 SMTP 服务器密码，可后续在 `.env` 文件中配置

* `emails_from_email`：（默认值：`"``info@example.com``"`）发件人邮箱地址，可后续在 `.env` 文件中配置

* `postgres_password`：（默认值：`"changethis"`）PostgreSQL 数据库密码（对应 `.env` 文件配置），可通过前文的 Python 命令生成

* `sentry_dsn`：（默认值：空字符串）Sentry 监控系统的 DSN 地址，若使用 Sentry 可后续在 `.env` 文件中配置

## 后端开发

后端开发文档请参考：backend/README.md

## 前端开发

前端开发文档请参考：frontend/README.md

## 部署指南

部署相关文档请参考：deployment.md

## 开发指南

通用开发文档请参考：development.md

文档内容包含 Docker Compose 使用、自定义本地域名配置、`.env` 文件配置等内容。

## 发行说明

发行说明请查看：release-notes.md

## 许可证

本全栈 FastAPI 模板基于 MIT 许可证开源。



***

© 2025 GitHub, Inc.

#### 页脚导航



* 服务条款

* 隐私政策

* 安全中心

* 平台状态

* 社区支持

* 官方文档

* 联系我们

* Cookie 设置

* 不共享我的个人信息

> 你目前无法执行此操作

我可以帮你整理这个中文 MD 文件的**目录结构**，方便你直接整合到项目中，需要吗？

> （注：文档部分内容可能由 AI 生成）