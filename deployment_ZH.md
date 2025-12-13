# FastAPI 项目 - 部署

你可以通过 Docker Compose 将项目部署到远程服务器。

本项目要求你使用 Traefik 代理来处理与外部网络的通信，并配置 HTTPS 证书。

你可以使用持续集成 / 持续部署（CI/CD）系统来实现自动化部署，项目中已经内置了适用于 GitHub Actions 的配置文件。

不过在此之前，你需要先完成几项配置工作。🤓

## 准备工作



1. 准备一台可用的远程服务器。

2. 将你的域名 DNS 记录配置为指向刚创建的服务器 IP 地址。

3. 为你的域名配置通配符子域名，这样你就可以为不同服务设置多个子域名，例如 `*.``fastapi-project.example.com`。这一配置有助于访问不同组件，比如 `dashboard.fastapi-project.example.com`、`api.fastapi-project.example.com`、`traefik.fastapi-project.example.com`、`adminer.fastapi-project.example.com` 等，同时也适用于测试环境（staging），例如 `dashboard.staging.fastapi-project.example.com`、`adminer.staging.fastapi-project.example.com` 等。

4. 在远程服务器上安装并配置 Docker（需安装 Docker Engine，而非 Docker Desktop）。

## 公共 Traefik 配置

我们需要使用 Traefik 代理来处理入站连接和 HTTPS 证书申请。

以下步骤仅需执行一次。

### Traefik Docker Compose 配置



1. 在远程服务器上创建一个目录，用于存放 Traefik 的 Docker Compose 文件：



```
mkdir -p /root/code/traefik-public/
```



1. 将 Traefik 的 Docker Compose 文件复制到服务器上，你可以在本地终端通过 `rsync` 命令完成该操作：



```
rsync -a docker-compose.traefik.yml root@your-server.example.com:/root/code/traefik-public/
```

### Traefik 公共网络配置

该 Traefik 代理需要一个名为 `traefik-public` 的 Docker “公共网络” 来与你的应用栈（stack）进行通信。

通过这种方式，你可以使用一个独立的公共 Traefik 代理来处理与外部网络的 HTTP 和 HTTPS 通信，而在代理后方，你可以部署一个或多个应用栈并配置不同的域名，即使这些应用栈都部署在同一台服务器上。

在远程服务器上执行以下命令，创建名为 `traefik-public` 的 Docker “公共网络”：



```
docker network create traefik-public
```

### Traefik 环境变量配置

Traefik 的 Docker Compose 文件需要在启动前配置一些环境变量，你可以在远程服务器的终端中执行以下命令来完成配置。



1. 创建 HTTP 基本认证的用户名，示例如下：



```
export USERNAME=admin
```



1. 创建 HTTP 基本认证的密码环境变量，示例如下：



```
export PASSWORD=changethis
```



1. 使用 openssl 生成该密码的 “哈希” 版本，并将其存储到环境变量中：



```
export HASHED\_PASSWORD=\$(openssl passwd -apr1 \$PASSWORD)
```



1. 你可以通过以下命令验证生成的哈希密码是否正确：



```
echo \$HASHED\_PASSWORD
```



1. 创建服务器域名的环境变量，示例如下：



```
export DOMAIN=fastapi-project.example.com
```



1. 创建 Let's Encrypt 证书申请所需的邮箱环境变量，示例如下：



```
export EMAIL=admin@example.com
```

> **注意**
>
> ：你需要填写一个真实有效的邮箱地址，
>
> `@example.com`
>
>  这类占位邮箱是无法正常使用的。

### 启动 Traefik Docker Compose

进入远程服务器上存放 Traefik Docker Compose 文件的目录：



```
cd /root/code/traefik-public/
```

在完成环境变量配置且 `docker-compose.traefik.yml` 文件已就位的情况下，执行以下命令启动 Traefik Docker Compose：



```
docker compose -f docker-compose.traefik.yml up -d
```

## 部署 FastAPI 项目

在完成 Traefik 配置后，你就可以通过 Docker Compose 部署 FastAPI 项目了。

> **提示**
>
> ：你也可以直接跳转到 
>
> **基于 GitHub Actions 的持续部署**
>
>  章节。

### 环境变量配置

首先，你需要配置以下环境变量。



1. 设置 `ENVIRONMENT` 环境变量，默认值为 `local`（适用于开发环境），部署到服务器时，你可以将其设置为 `staging`（测试环境）或 `production`（生产环境）等：



```
export ENVIRONMENT=production
```



1. 设置 `DOMAIN` 环境变量，默认值为 `localhost`（适用于开发环境），部署时请替换为你的实际域名，示例如下：



```
export DOMAIN=fastapi-project.example.com
```

除此之外，你还可以配置以下多个环境变量：



* `PROJECT_NAME`：项目名称，会用于 API 文档和邮件内容中。

* `STACK_NAME`：Docker Compose 标签和项目名称所使用的应用栈名称，测试环境和生产环境的该值应区分开，例如 `fastapi-project-example-com`（生产环境）和 `staging-fastapi-project-example-com`（测试环境）。

* `BACKEND_CORS_ORIGINS`：允许跨域请求的源列表，多个源之间用逗号分隔。

* `SECRET_KEY`：FastAPI 项目的密钥，用于生成令牌。

* `FIRST_SUPERUSER`：第一个超级用户的邮箱地址，该超级用户拥有创建新用户的权限。

* `FIRST_SUPERUSER_PASSWORD`：第一个超级用户的密码。

* `SMTP_HOST`：用于发送邮件的 SMTP 服务器地址，你可以从邮件服务提供商处获取（例如 Mailgun、Sparkpost、Sendgrid 等）。

* `SMTP_USER`：SMTP 服务器的用户名。

* `SMTP_PASSWORD`：SMTP 服务器的密码。

* `EMAILS_FROM_EMAIL`：发送邮件所使用的邮箱账号。

* `POSTGRES_SERVER`：PostgreSQL 服务器的主机名，默认值为 `db`（由同一份 Docker Compose 配置提供），除非你使用第三方数据库服务，否则无需修改。

* `POSTGRES_PORT`：PostgreSQL 服务器的端口号，使用默认值即可，除非你使用第三方数据库服务。

* `POSTGRES_PASSWORD`：PostgreSQL 数据库的密码。

* `POSTGRES_USER`：PostgreSQL 数据库的用户名，使用默认值即可。

* `POSTGRES_DB`：应用所使用的数据库名称，默认值为 `app`。

* `SENTRY_DSN`：Sentry 的 DSN 地址（如果你使用 Sentry 进行错误监控）。

### GitHub Actions 专属环境变量

还有一些仅用于 GitHub Actions 的环境变量需要你配置：



* `LATEST_CHANGES`：由 GitHub Action [latest-changes](https://github.com/marketplace/actions/latest-changes) 工具使用，用于根据合并的 Pull Request 自动生成发布说明，其值为一个个人访问令牌，具体配置请参考该工具的文档。

* `SMOKESHOW_AUTH_KEY`：用于处理和发布代码覆盖率报告，基于 [Smokeshow](https://smokeshow.readthedocs.io/) 工具实现，你可以按照其官方说明创建一个免费的 Smokeshow 密钥。

### 生成密钥

`.env` 文件中的部分环境变量默认值为 `changethis`，你需要将其替换为安全的密钥。

你可以通过以下命令生成密钥：



```
python -c "import secrets; print(secrets.token\_urlsafe(32))"
```

复制生成的内容，将其作为密码或密钥使用。重复执行该命令，可以生成更多安全密钥。

### 通过 Docker Compose 部署

在完成环境变量配置后，执行以下命令部署项目：



```
docker compose -f docker-compose.yml up -d
```

对于生产环境，你不需要启用 `docker-compose.override.yml` 文件中的覆盖配置，因此我们在命令中显式指定使用 `docker-compose.yml` 文件。

## 持续部署（CD）

你可以使用 GitHub Actions 实现项目的自动化部署。😎

本项目支持多环境部署。

目前已经配置了两个环境：`staging`（测试环境）和 `production`（生产环境）。🚀

### 安装 GitHub Actions 运行器



1. 在远程服务器上，为 GitHub Actions 创建一个专用用户：



```
sudo adduser github
```



1. 为 `github` 用户授予 Docker 操作权限：



```
sudo usermod -aG docker github
```



1. 临时切换到 `github` 用户：



```
sudo su - github
```



1. 进入 `github` 用户的主目录：



```
cd
```



1. [按照官方指南安装 GitHub Action 自托管运行器](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/add-self-hosted-runners)。

2. 当被问及标签（label）时，添加一个与环境对应的标签，例如 `production`。你也可以在后续操作中添加标签。

安装完成后，官方指南会提示你执行一条命令来启动运行器。但需要注意的是，如果你终止该进程，或者本地与服务器的连接断开，运行器就会停止工作。

为了确保运行器能够随服务器开机自动启动，并且持续运行，你可以将其安装为系统服务。操作步骤如下：



1. 退出 `github` 用户，切换回之前的用户：



```
exit
```



1. 切换到 `root` 用户（如果你当前不是 `root` 用户）：



```
sudo su
```



1. 进入 `github` 用户主目录下的 `actions-runner` 目录：



```
cd /home/github/actions-runner
```



1. 以 `github` 用户身份，将自托管运行器安装为系统服务：



```
./svc.sh install github
```



1. 启动该服务：



```
./svc.sh start
```



1. 检查服务状态：



```
./svc.sh status
```

你可以在官方指南中了解更多相关信息：[将自托管运行器应用程序配置为服务](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service)。

### 设置密钥

在你的代码仓库中，配置部署所需的环境变量密钥，也就是前文提到的各类变量，包括 `SECRET_KEY` 等。配置方法请参考 [GitHub 官方指南：设置仓库密钥](https://docs.github.com/en/actions/security-guides/encrypted-secrets)。

当前的 GitHub Actions 工作流需要以下密钥：



* `DOMAIN_PRODUCTION`

* `DOMAIN_STAGING`

* `STACK_NAME_PRODUCTION`

* `STACK_NAME_STAGING`

* `EMAILS_FROM_EMAIL`

* `FIRST_SUPERUSER`

* `FIRST_SUPERUSER_PASSWORD`

* `POSTGRES_PASSWORD`

* `SECRET_KEY`

* `LATEST_CHANGES`

* `SMOKESHOW_AUTH_KEY`

### GitHub Action 部署工作流

在项目的 `.github/workflows` 目录中，已经配置了适用于不同环境的 GitHub Action 工作流（对应带有指定标签的 GitHub Actions 运行器）：



* `staging`（测试环境）：当代码推送到（或合并到）`master` 分支时，自动触发部署。

* `production`（生产环境）：当发布新版本（release）时，自动触发部署。

如果你需要添加更多环境，可以以此为基础进行扩展。

## 访问地址

请将以下地址中的 `fastapi-project.example.com` 替换为你的实际域名。

### Traefik 主控制面板

Traefik 管理界面：`https://traefik.fastapi-project.example.com`

### 生产环境



* 前端页面：`https://dashboard.fastapi-project.example.com`

* 后端 API 文档：`https://api.fastapi-project.example.com/docs`

* 后端 API 基础地址：`https://api.fastapi-project.example.com`

* 数据库管理工具：`https://adminer.fastapi-project.example.com`

### 测试环境



* 前端页面：`https://dashboard.staging.fastapi-project.example.com`

* 后端 API 文档：`https://api.staging.fastapi-project.example.com/docs`

* 后端 API 基础地址：`https://api.staging.fastapi-project.example.com`

* 数据库管理工具：`https://adminer.staging.fastapi-project.example.com`



***

© 2025 GitHub, Inc.

#### 页脚导航



* [服务条款](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)

* [隐私政策](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement)

* [安全政策](https://github.com/security)

* [平台状态](https://www.githubstatus.com/)

* [社区](https://github.com/community)

* [文档](https://docs.github.com/)

* [联系我们](https://support.github.com/contact)

* Cookie 设置

* 不共享我的个人信息

> 你目前无法执行此操作。

我可以帮你整理这份部署文档的**关键步骤清单**，方便你部署时对照检查，需要吗？

> （注：文档部分内容可能由 AI 生成）