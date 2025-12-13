# FastAPI 项目 - 前端

前端基于 **Vite**、**React**、**TypeScript**、**TanStack Query**、**TanStack Router** 和 **Tailwind CSS** 进行构建。

## 前端开发

开始开发前，请确保你的系统中已安装 Node 版本管理器（nvm）或快速 Node 管理器（fnm）。



1. 安装 fnm 请遵循 官方 fnm 指南；如果你更倾向于使用 nvm，可以参考 官方 nvm 指南 完成安装。

2. 安装好 nvm 或 fnm 后，进入 `frontend` 目录：



```
cd frontend
```



1. 如果你的系统中未安装 `.nvmrc` 文件指定的 Node.js 版本，可以通过以下命令进行安装：



```
\# 使用 fnm 的情况

fnm install

\# 使用 nvm 的情况

nvm install
```



1. 安装完成后，切换到该版本：



```
\# 使用 fnm 的情况

fnm use

\# 使用 nvm 的情况

nvm use
```



1. 在 `frontend` 目录下，安装所需的 NPM 包：



```
npm install
```



1. 通过以下 `npm` 脚本启动热重载开发服务器：



```
npm run dev
```



1. 最后在浏览器中打开 http://localhost:5173/ 即可访问。

> **注意**
>
> ：此开发服务器并非运行在 Docker 容器内，它适用于本地开发场景，也是我们推荐的工作流。当你完成前端开发并确认效果符合预期后，可以构建前端 Docker 镜像并启动容器，在类生产环境中进行测试。但如果每次代码变更都重新构建镜像，开发效率会远低于使用带热重载功能的本地开发服务器。

你可以查看 `package.json` 文件，了解其他可用的脚本命令。

### 移除前端模块

如果你正在开发一个**仅提供 API 接口**的应用，想要移除前端模块，可以按照以下步骤操作：



1. 删除 `./frontend` 目录。

2. 在 `docker-compose.yml` 文件中，删除整个 `frontend` 服务配置段。

3. 在 `docker-compose.override.yml` 文件中，删除 `frontend` 和 `playwright` 这两个服务的配置段。

完成以上步骤后，你就得到了一个无前端的纯 API 应用 🤓

如果需要，你还可以从以下文件中移除 `FRONTEND` 相关的环境变量：



* `.env`

* `./scripts/*.sh`

不过这一步仅用于清理冗余配置，即使保留这些变量也不会对应用产生实际影响。

## 生成前端客户端

### 自动生成



1. 激活后端的虚拟环境。

2. 在项目根目录下，运行以下脚本：



```
./scripts/generate-client.sh
```



1. 提交代码变更。

### 手动生成



1. 启动 Docker Compose 服务集群。

2. 从 `http://localhost/api/v1/openapi.json` 下载 OpenAPI JSON 描述文件，并将其复制到 `frontend` 目录根路径下，命名为 `openapi.json`。

3. 执行以下命令生成前端客户端代码：



```
npm run generate-client
```



1. 提交代码变更。

> **注意**
>
> ：每当后端代码发生变更（导致 OpenAPI 接口描述文件更新）时，你都需要重新执行上述步骤来更新前端客户端代码。

## 对接远程 API

如果你希望前端对接远程 API 服务，可以通过设置环境变量 `VITE_API_URL` 来指定远程 API 的地址。例如，你可以在 `frontend/.env` 文件中进行配置：



```
VITE\_API\_URL=https://api.my-domain.example.com
```

配置完成后，启动前端项目时，应用就会将该地址作为 API 请求的基础 URL。

## 代码结构

前端代码的目录结构如下：



* `frontend/src` - 前端核心业务代码目录

* `frontend/src/assets` - 静态资源目录（如图片、样式文件等）

* `frontend/src/client` - 自动生成的 OpenAPI 客户端代码目录

* `frontend/src/components` - 前端公共组件目录

* `frontend/src/hooks` - 自定义 React Hooks 目录

* `frontend/src/routes` - 前端路由及对应的页面组件目录

## 使用 Playwright 进行端到端测试

前端项目中内置了基于 Playwright 的端到端测试用例。运行测试前，需要先启动 Docker Compose 服务集群，执行以下命令：



```
docker compose up -d --wait backend
```

### 运行测试

执行以下命令启动测试：



```
npx playwright test
```

### UI 模式运行测试

你也可以在 UI 模式下运行测试，这种模式下可以直观地看到浏览器操作过程并进行交互：



```
npx playwright test --ui
```

### 清理测试环境

测试完成后，如需停止并移除 Docker Compose 服务集群，同时清理测试产生的数据，可以执行以下命令：



```
docker compose down -v
```

### 更新测试用例

如需更新测试用例，请进入测试目录，根据需求修改现有测试文件或新增测试文件。

更多关于编写和运行 Playwright 测试的内容，请参考 Playwright 官方文档。



***

© 2025 GitHub, Inc.

#### 页脚导航



* 服务条款

* 隐私政策

* 安全中心

* 平台状态

* 社区

* 文档

* 联系我们

* Cookie 设置

* 不共享我的个人信息

我可以帮你整理这份文档的**目录大纲**，方便快速定位内容，需要吗？

> （注：文档部分内容可能由 AI 生成）