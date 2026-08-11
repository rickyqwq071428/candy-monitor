# 可予礼品竞品监控平台 - 部署指南

## 🟢 方式零：一键启动（当前已生效）

```bash
# 双击 candy_monitor/start.bat
# → 自动启动服务器 + 公网隧道
# → 公网地址: https://candy-monitor.loca.lt
```

> ⚠️ 首次访问 localtunnel 地址，会看到一个密码页面，输入你的本机公网 IP 即可通过（在 https://candy-monitor.loca.lt 页面会有提示）。

---

## 方式一：Docker 部署（推荐生产环境）

```bash
# 1. 确保已安装 Docker & Docker Compose
docker --version && docker compose version

# 2. 进入项目目录，启动
cd candy_monitor
docker compose -f deploy/docker-compose.yml up -d

# 3. 检查状态
docker compose -f deploy/docker-compose.yml ps

# 4. 访问
# http://你的服务器IP
```

## 方式二：Linux VPS 一键脚本

```bash
# 1. 将整个 candy_monitor 文件夹上传到服务器
scp -r candy_monitor/ user@your-server:/tmp/

# 2. SSH 登录服务器
ssh user@your-server

# 3. 进入目录，运行部署脚本
cd /tmp/candy_monitor
sudo bash deploy/deploy.sh

# 4. 访问 http://你的服务器IP
```

## 方式三：本地 + 内网穿透（无需服务器）

### 使用 Cloudflare Tunnel（免费）

```bash
# 安装 cloudflared
# Windows: https://github.com/cloudflare/cloudflared/releases
# Linux: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared

# 启动隧道（无需注册）
cloudflared tunnel --url http://localhost:5000

# 会得到一个公网地址，如 https://xxx.trycloudflare.com
```

### 使用 frp 内网穿透

参考: https://github.com/fatedier/frp

## 环境变量说明

| 变量 | 默认值 | 说明 |
|------|--------|------|
| CANDY_HOST | 0.0.0.0 | 监听地址 |
| CANDY_PORT | 5000 | 监听端口 |
| CANDY_THREADS | 4 | 工作线程数 |
| CANDY_DEBUG | false | 调试模式 |

## 常用管理命令

```bash
# 查看服务状态
sudo systemctl status candy_monitor

# 重启服务
sudo systemctl restart candy_monitor

# 查看实时日志
sudo journalctl -u candy_monitor -f

# Nginx 重载配置
sudo nginx -t && sudo systemctl reload nginx
```
