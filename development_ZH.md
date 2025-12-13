# FastAPI 项目 - 开发文档

## Docker Compose 部署



* 使用 Docker Compose 启动本地服务集群：



```
docker compose watch
```



* 服务启动后，可在浏览器中通过以下地址访问对应功能：


  * 前端页面（基于 Docker 构建，路由根据访问路径自动匹配）：[http://localhost:5173](http://localhost:5173)

  * 后端 API 接口（基于 OpenAPI 规范的 JSON 格式接口）：[http://localhost:8000](http://localhost:8000)

  * 自动交互式文档（Swagger UI，基于后端 OpenAPI 生成）：[http://localhost:8000/docs](http://localhost:8000/docs)

  * 数据库管理工具（Adminer）：[http://localhost:8080](http://localhost:8080)

  * 反向代理监控界面（Traefik UI，可查看路由转发规则）：[http://localhost:8090](http://localhost:8090)

**注意**：首次启动服务集群时，可能需要等待一分钟左右才能完全就绪。因为后端服务需要等待数据库初始化完成后，再进行自身的配置加载。你可以通过查看日志来监控服务启动状态。

查看所有服务的日志（在新的终端窗口执行）：



```
docker compose logs
```

查看指定服务的日志（例如仅查看后端服务日志）：



```
docker compose logs backend
```

## Mailcatcher 邮件测试工具

Mailcatcher 是一个轻量级的 SMTP 测试服务器，可捕获本地开发过程中后端服务发送的所有邮件。它不会将邮件真正发送到目标邮箱，而是将邮件内容存储并在 Web 界面中展示。

该工具的核心作用：



* 开发阶段测试邮件功能是否正常

* 验证邮件内容格式、排版是否符合预期

* 调试邮件相关功能时，避免发送真实邮件造成的干扰

在本地通过 Docker Compose 启动服务时，后端会自动配置使用 Mailcatcher（SMTP 服务端口为 1025）。所有被捕获的邮件均可通过以下地址查看：[http://localhost:1080](http://localhost:1080)

## 本地开发模式

Docker Compose 配置文件已为每个服务分配了独立的本地端口，确保服务之间不会产生端口冲突。

后端和前端服务使用的端口，与它们各自本地开发服务器的默认端口保持一致：后端服务端口为 `8000`，前端服务端口为 `5173`。

基于这一配置，你可以随时停止某个 Docker 容器服务，切换为本地开发服务器启动，且不会影响其他服务的正常运行。

例如，切换前端为本地开发模式：



1. 停止 Docker Compose 中的前端服务：



```
docker compose stop frontend
```



1. 进入前端项目目录，启动本地开发服务器：



```
cd frontend

npm run dev
```

再例如，切换后端为本地开发模式：



1. 停止 Docker Compose 中的后端服务：



```
docker compose stop backend
```



1. 进入后端项目目录，启动本地开发服务器：



```
cd backend

fastapi dev app/main.py
```

## 基于 `localhost``.``tiangolo.com` 域名的 Docker Compose 配置

默认情况下，Docker Compose 启动的服务集群使用 `localhost` 作为访问域名，不同服务通过不同端口区分。

在生产或测试环境部署时，通常会为不同服务配置独立的子域名，例如后端服务对应 `api.example.com`，前端服务对应 `dashboard.example.com`。

关于生产环境部署的详细说明，可参考**部署文档**中关于 Traefik 反向代理的部分。Traefik 是负责根据子域名将请求转发到对应服务的核心组件。

如果需要在本地环境测试子域名配置，可按照以下步骤操作：



1. 编辑本地的 `.env` 文件，修改域名配置项：



```
DOMAIN=localhost.tiangolo.com
```

该配置会被 Docker Compose 文件读取，作为所有服务的基础域名。



1. Traefik 会根据该配置，将发送到 `api.localhost.tiangolo.com` 的请求转发到后端服务，将发送到 `dashboard.localhost.tiangolo.com` 的请求转发到前端服务。

2. `localhost``.``tiangolo.com` 是一个特殊域名，其本身及所有子域名均已被配置为指向 `127.0.0.1`，可直接用于本地开发测试。

配置修改完成后，重新启动服务集群：



```
docker compose watch
```

> 补充说明：生产环境中，Traefik 通常独立于 Docker Compose 集群部署；而本地开发环境中，
>
> `docker-compose.override.yml`
>
>  文件中内置了 Traefik 配置，专门用于测试子域名转发功能。

## Docker Compose 配置文件与环境变量

项目中包含两类 Docker Compose 配置文件，分工明确：



1. `docker-compose.yml`：主配置文件，包含适用于整个服务集群的通用配置，会被 `docker compose` 命令自动加载。

2. `docker-compose.override.yml`：开发环境覆盖配置文件，包含仅适用于本地开发的特殊配置（例如将代码目录挂载为容器卷），会被 `docker compose` 命令自动加载，并覆盖主配置文件中的同名配置项。

这两类配置文件都会读取 `.env` 文件中的内容，将其中的配置项注入为容器的环境变量。

除此之外，部分配置项还会从执行 `docker compose` 命令前设置的系统环境变量中读取。

修改任何环境变量后，需重启服务集群才能使配置生效：



```
docker compose watch
```

## .env 配置文件

`.env` 文件存储了项目的所有配置项、生成的密钥和密码等敏感信息。

根据你的开发流程，**如果项目是开源的，建议将该文件排除在 Git 版本控制之外**。此时需要为 CI/CD 工具配置获取该文件的方式，以确保构建和部署流程能正常运行。

一种常见的解决方案是：将 `.env` 文件中的每个环境变量单独配置到 CI/CD 系统中，同时修改 `docker-compose.yml` 文件，使其直接读取这些系统环境变量，而非本地 `.env` 文件。

## 前置提交与代码检查

项目使用 [pre-commit](https://pre-commit.com/) 工具实现代码检查和格式化功能。

该工具会在执行 `git commit` 命令前自动运行，确保提交到代码仓库的代码符合统一的规范和格式要求。

项目根目录下的 `.pre-commit-config.yaml` 文件存储了该工具的详细配置。

### 安装 pre-commit 并配置自动运行

pre-commit 已作为项目依赖项包含在配置中，你也可以根据需要按照 [官方文档](https://pre-commit.com/) 的说明，在系统中全局安装该工具。

安装完成后，需要在本地代码仓库中执行以下命令，配置该工具在每次提交前自动运行：



```
❯ uv run pre-commit install

pre-commit installed at .git/hooks/pre-commit
```

配置完成后，每当你执行 `git commit` 命令时：



1. pre-commit 会自动运行配置好的检查和格式化脚本

2. 如果检查不通过，工具会自动修复部分问题，并提示你重新将修改后的文件加入暂存区

3. 你需要执行 `git add` 命令，将修复后的文件重新暂存，之后再执行 `git commit` 即可完成提交

### 手动运行 pre-commit 检查

你也可以手动触发 pre-commit 检查，对项目中所有文件执行代码规范校验，执行命令如下：



```
❯ uv run pre-commit run --all-files

check for added large files..............................................Passed

check toml...............................................................Passed

check yaml...............................................................Passed

ruff.....................................................................Passed

ruff-format..............................................................Passed

eslint...................................................................Passed

prettier.................................................................Passed
```

## 访问地址汇总

生产或测试环境的服务地址，仅需将以下地址中的域名替换为你的业务域名即可，路径规则保持不变。

### 本地开发默认地址



| 服务名称             | 访问地址                                                       |
| ---------------- | ---------------------------------------------------------- |
| 前端页面             | [http://localhost:5173](http://localhost:5173)             |
| 后端接口             | [http://localhost:8000](http://localhost:8000)             |
| Swagger 交互式文档    | [http://localhost:8000/docs](http://localhost:8000/docs)   |
| ReDoc 文档         | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| Adminer 数据库管理    | [http://localhost:8080](http://localhost:8080)             |
| Traefik 监控界面     | [http://localhost:8090](http://localhost:8090)             |
| Mailcatcher 邮件查看 | [http://localhost:1080](http://localhost:1080)             |

### 基于 `localhost``.``tiangolo.com` 域名的本地开发地址



| 服务名称             | 访问地址                                                                               |
| ---------------- | ---------------------------------------------------------------------------------- |
| 前端页面             | [http://dashboard.localhost.tiangolo.com](http://dashboard.localhost.tiangolo.com) |
| 后端接口             | [http://api.localhost.tiangolo.com](http://api.localhost.tiangolo.com)             |
| Swagger 交互式文档    | [http://api.localhost.tiangolo.com/docs](http://api.localhost.tiangolo.com/docs)   |
| ReDoc 文档         | [http://api.localhost.tiangolo.com/redoc](http://api.localhost.tiangolo.com/redoc) |
| Adminer 数据库管理    | [http://localhost.tiangolo.com:8080](http://localhost.tiangolo.com:8080)           |
| Traefik 监控界面     | [http://localhost.tiangolo.com:8090](http://localhost.tiangolo.com:8090)           |
| Mailcatcher 邮件查看 | [http://localhost.tiangolo.com:1080](http://localhost.tiangolo.com:1080)           |



***

© 2025 GitHub, Inc.

#### 页脚导航



* [服务条款](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service)

* [隐私政策](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement)

* [安全中心](https://github.com/security)

* [服务状态](https://www.githubstatus.com/)

* [社区支持](https://github.com/community)

* [官方文档](https://docs.github.com/)

* [联系我们](https://support.github.com/contact)

* Cookie 设置

* 不共享我的个人信息

> 提示：当前操作可能无法执行



***

我可以帮你整理这份文档的**核心操作步骤清单**，方便你快速查阅和执行，需要吗？

> （注：文档部分内容可能由 AI 生成）