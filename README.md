# Apache Superset Setup Guide
# Apache Superset 设置指南

This repository contains a configured instance of Apache Superset with enhanced visualization capabilities and custom configurations.
本仓库包含一个配置好的 Apache Superset 实例，具有增强的可视化功能和自定义配置。

## Understanding Superset's Two Databases
## 理解 Superset 的两个数据库

Superset uses two different types of databases:
Superset 使用两种不同类型的数据库：

1. **Metadata Database (元数据数据库)**
   - Purpose 用途: Stores Superset's internal metadata and configurations (存储 Superset 的内部元数据和配置)
   - Content 内容:
     - User information and permissions (用户信息和权限)
     - Dashboard configurations (仪表板配置)
     - Saved queries (保存的查询)
     - Chart definitions (图表定义)
     - Database connections (数据库连接)
     - Cache keys (缓存键)
   - Default 默认: SQLite (`superset.db` in project root) (SQLite，位于项目根目录)
   - Configuration 配置: Set via `SQLALCHEMY_DATABASE_URI` in `superset_config.py` (通过 superset_config.py 中的 SQLALCHEMY_DATABASE_URI 设置)
   - Important Notes 重要说明:
     - Encryption key (`SUPERSET_SECRET_KEY`) must remain consistent (加密密钥必须保持一致)
     - Database credentials are encrypted using this key (数据库凭据使用此密钥加密)
     - If key changes, you'll need to reset the database (如果密钥更改，需要重置数据库)
     - For production, recommended to use PostgreSQL or MySQL (生产环境建议使用 PostgreSQL 或 MySQL)

2. **Data Source Databases (数据源数据库)**
   - Purpose 用途: Store actual data for visualization (存储用于可视化的实际数据)
   - Types supported 支持的类型:
     - PostgreSQL
     - MySQL
     - SQLite
     - Oracle
     - Microsoft SQL Server
     - Apache Druid
     - StarRocks
     - And many more (等等)
   - Configuration Methods 配置方法:
     - Through Superset's UI (Data → Databases) (通过 Superset 的用户界面)
     - Via SQLAlchemy URI in configuration (通过配置中的 SQLAlchemy URI)
   - Connection Details 连接详情:
     - Uses SQLAlchemy URI format (使用 SQLAlchemy URI 格式)
     - Credentials encrypted in metadata DB (凭据在元数据库中加密)
     - Supports SSH tunneling (支持 SSH 隧道)
     - Can use connection pooling (可以使用连接池)
   - Special Configurations 特殊配置:
     - StarRocks setup requires Docker container (StarRocks 设置需要 Docker 容器)
     - Some databases need additional drivers (某些数据库需要额外的驱动程序)
     - Can configure query timeouts per database (可以为每个数据库配置查询超时)

## Prerequisites 前提条件

- Python 3.10 or higher (Python 3.10 或更高版本)
- Virtual environment (虚拟环境)
- Redis (optional, for caching) (可选，用于缓存)
- Node.js and npm (Node.js 和 npm)
- Docker (for StarRocks and other containerized databases) (用于 StarRocks 和其他容器化数据库)

## Installation Steps 安装步骤

1. Create and activate virtual environment 创建并激活虚拟环境:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies 安装依赖:
```bash
pip install apache-superset
```

3. Initialize the database 初始化数据库:
```bash
superset db upgrade
```

4. Create an admin user 创建管理员用户:
```bash
superset fab create-admin
```

5. Load example data 加载示例数据:
```bash
superset load_examples
```

## Configuration 配置

### Architecture Overview 架构概述

- **Frontend Layer 前端层**:
  - React-based web interface (基于 React 的 Web 界面)
  - Visualization plugins (可视化插件)
  - Dashboard builder (仪表板构建器)

- **Backend Layer 后端层**:
  - Flask application server (Flask 应用服务器)
  - SQLAlchemy ORM (SQLAlchemy 对象关系映射)
  - Celery for async tasks (Celery 异步任务处理)
  - Redis for caching (Redis 缓存)

- **Storage Layer 存储层**:
  - Metadata database (元数据数据库)
  - Query results cache (查询结果缓存)
  - Thumbnail cache (缩略图缓存)

### Database Configuration 数据库配置

1. **Metadata Database Configuration 元数据数据库配置**:
```python
# SQLite (default 默认)
SQLALCHEMY_DATABASE_URI = 'sqlite:///path/to/superset.db'

# PostgreSQL (recommended for production 推荐用于生产环境)
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/superset'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/superset'

# Important security settings 重要安全设置
SUPERSET_SECRET_KEY = 'your-long-random-string'  # Must be consistent 必须保持一致
PREVENT_UNSAFE_DB_CONNECTIONS = True
```

2. **Data Source Database Example Configurations 数据源数据库示例配置**:
```python
# PostgreSQL
postgresql://user:password@localhost:5432/database

# MySQL
mysql://user:password@localhost:3306/database

# StarRocks
starrocks://user:password@localhost:9030/database

# Additional database parameters 额外的数据库参数
?connect_timeout=10&pool_timeout=30
```

### Storage Configuration 存储配置

Customize storage locations in `superset_config.py` 在 superset_config.py 中自定义存储位置:

1. **Cache Configuration 缓存配置**:
```python
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/path/to/cache',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24  # 1 day 一天
}
```

2. **Thumbnail Configuration 缩略图配置**:
```python
THUMBNAIL_CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': '/path/to/thumbnail_cache'
}
```

3. **Upload Configuration 上传配置**:
```python
UPLOAD_FOLDER = '/path/to/uploads'
IMG_UPLOAD_FOLDER = '/path/to/image/uploads'
```

## Starting Superset 启动 Superset

Use the provided startup script 使用提供的启动脚本:
```bash
./start_superset.sh
```

Or manually 或手动:
```bash
export PYTHONPATH=$PYTHONPATH:$PWD
export SUPERSET_CONFIG_PATH=superset_config.py
source venv/bin/activate
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger
```

## Accessing Superset 访问 Superset

- Local access 本地访问: http://127.0.0.1:8088
- Network access 网络访问: http://[your-ip]:8088
- Default login 默认登录:
  - Username 用户名: admin
  - Password 密码: admin

## Troubleshooting 故障排除

1. Database connection issues 数据库连接问题:
   - Verify database URI in config (验证配置中的数据库 URI)
   - Check database permissions (检查数据库权限)
   - For metadata DB encryption issues 元数据库加密问题:
     - Ensure `SUPERSET_SECRET_KEY` is consistent (确保 SUPERSET_SECRET_KEY 保持一致)
     - May need to reset the database if key changes (如果密钥更改，可能需要重置数据库)
   - For StarRocks StarRocks 相关:
     - Ensure Docker container is running (确保 Docker 容器正在运行)
     - Check container logs for connection issues (检查容器日志中的连接问题)

2. Cache issues 缓存问题:
   - Ensure cache directories are writable (确保缓存目录可写)
   - Clear cache directories if needed (如果需要，清除缓存目录)

3. Visualization problems 可视化问题:
   - Check browser console for errors (检查浏览器控制台的错误)
   - Verify required dependencies (验证所需的依赖项)

## Additional Resources 其他资源

- [Apache Superset Documentation Apache Superset 文档](https://superset.apache.org/docs/intro)
- [Superset GitHub Repository Superset GitHub 仓库](https://github.com/apache/superset)
- [StarRocks Documentation StarRocks 文档](https://docs.starrocks.io/)