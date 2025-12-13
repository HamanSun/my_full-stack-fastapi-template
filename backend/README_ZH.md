# FastAPI 项目 - 后端

## 环境要求



* **Docker**：容器化部署平台

* **uv**：用于 Python 包和虚拟环境的管理工具

## Docker Compose 部署

请参考项目根目录下的 [../development.md](../development.md) 文档，按照步骤使用 Docker Compose 启动本地开发环境。

## 通用开发流程

默认情况下，项目依赖由 `uv` 管理，请先安装 `uv` 工具。

在 `./backend/` 目录下执行以下命令，完成依赖安装：



```
\$ uv sync
```

安装完成后，激活虚拟环境：



```
\$ source .venv/bin/activate
```

请确保你的代码编辑器已配置正确的 Python 解释器，路径为 `backend/.venv/bin/python`。

### 代码结构说明



* 数据模型与数据库表定义：修改或新增 `./backend/app/``models.py` 中的 SQLModel 模型

* API 接口开发：在 `./backend/app/api/` 目录下编写接口逻辑

* CRUD 操作工具：在 `./backend/app/``crud.py` 中实现数据的增删改查功能

## VS Code 配置

项目已内置 VS Code 调试配置，你可以直接使用断点调试功能，支持暂停程序执行、查看变量值等操作。

同时，VS Code 的 Python 测试面板也已配置完成，可直接在面板中运行测试用例。

## Docker Compose 配置覆盖

开发阶段，你可以通过 `docker-compose.override.yml` 文件修改 Docker Compose 配置，**这些修改仅对本地开发环境生效，不会影响生产环境**。你可以在该文件中添加临时配置，提升开发效率。

### 核心配置说明



1. **代码目录同步**

   后端代码目录会被挂载为容器卷，本地代码的修改会实时同步到容器内部，无需重新构建 Docker 镜像即可测试变更，大幅提升迭代速度。**该配置仅限开发环境使用**，生产环境需基于最新代码构建镜像。

2. **热重载模式**

   配置中覆盖了默认启动命令，使用 `fastapi run --reload` 替代 `fastapi run`。

> **注意**
>
> ：如果代码存在语法错误并保存，服务会崩溃退出，容器也会随之停止。修复错误后，执行以下命令重启容器：



```
\$ docker compose watch
```



* 仅启动单个服务器进程（生产环境通常启动多进程）

* 代码发生变更时自动重启服务

1. **容器常驻配置**

   文件中存在一个被注释的 `command` 配置项，取消注释并注释默认命令后，容器会运行一个 “空进程” 保持存活状态。

   这种模式下，你可以进入容器内部执行命令，例如测试依赖包、手动启动热重载服务器。

   进入容器的步骤：


   1. 启动容器栈



```
\$ docker compose watch
```



1. 打开新终端，执行 `exec` 命令进入容器



```
\$ docker compose exec backend bash
```



1. 成功进入后，终端会显示类似如下内容：



```
root@7f2607af31c3:/app#
```

此时你处于容器内的 `/app` 目录，项目代码存放在 `/app/app` 路径下。



1. 手动启动热重载服务器



```
\$ fastapi run --reload app/main.py
```

## 后端测试

### 运行测试用例

执行以下命令运行所有测试：



```
\$ bash ./scripts/test.sh
```

项目使用 Pytest 作为测试框架，测试用例存放在 `./backend/tests/` 目录下，你可以在该目录中修改或新增测试。

如果配置了 GitHub Actions，提交代码后会自动触发测试流程。

### 测试运行中的容器

若容器栈已启动，仅需运行测试，可执行以下命令：



```
docker compose exec backend bash scripts/tests-start.sh
```

该脚本会先确保容器栈正常运行，再调用 `pytest` 执行测试。

你可以传递额外参数给 `pytest`，例如**遇到第一个错误时停止测试**：



```
docker compose exec backend bash scripts/tests-start.sh -x
```

### 测试覆盖率

测试运行完成后，会在项目中生成 `htmlcov/index.html` 文件，在浏览器中打开该文件，即可查看测试覆盖率报告。

## 数据库迁移

本地开发环境中，应用代码目录被挂载为容器卷，因此你可以在容器内执行 `alembic` 迁移命令，迁移文件会同步到本地代码目录，方便提交到 Git 仓库。

> **重要**
>
> ：每次修改数据模型后，必须创建迁移版本并更新数据库，否则应用会因表结构不匹配而报错。

### 迁移步骤



1. 进入后端容器的交互式终端



```
\$ docker compose exec backend bash
```



1. Alembic 已配置为从 `./backend/app/``models.py` 导入 SQLModel 模型，无需额外配置。

2. 修改模型后（例如新增 `last_name` 字段），在容器内创建迁移版本



```
\$ alembic revision --autogenerate -m "为 User 模型添加 last\_name 字段"
```



1. 将 `alembic` 目录下生成的迁移文件提交到 Git 仓库。

2. 执行迁移，更新数据库表结构



```
\$ alembic upgrade head
```

### 禁用数据库迁移

如果不需要使用迁移功能，可按以下步骤操作：



1. 打开 `./backend/app/core/``db.py` 文件，取消注释以 `SQLModel.metadata.create_all(engine)` 结尾的代码行。

2. 打开 `scripts/``prestart.sh` 文件，注释掉包含 `alembic upgrade head` 的代码行。

### 清空初始迁移记录

若不想使用默认模型，需从零开始修改，可删除 `./backend/app/alembic/versions/` 目录下的所有迁移文件（`.py` 文件），然后按照上述步骤创建第一个迁移版本。

## 邮件模板

邮件模板存放在 `./backend/app/email-templates/` 目录下，包含两个子目录：



* `src`：存放 MJML 格式的模板源文件

* `build`：存放编译后的 HTML 格式模板文件，供应用程序使用

### 模板编译步骤



1. 确保你的 VS Code 已安装 **MJML 扩展**。

2. 在 `src` 目录下创建或修改 `.mjml` 格式的模板文件。

3. 打开该文件，按下 `Ctrl+Shift+P` 打开命令面板，搜索并执行 `MJML: Export to HTML` 命令。

4. 将生成的 HTML 文件保存到 `build` 目录中。



***

© 2025 GitHub, Inc.

> （注：文档部分内容可能由 AI 生成）