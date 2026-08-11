#!/bin/bash
# ============================================
# 可予礼品竞品监控平台 - 云服务器一键部署
# 适用: Ubuntu 20.04+ / Debian 11+
# 用法: sudo bash deploy.sh [your-domain.com]
# ============================================
set -e

APP_NAME="candy_monitor"
APP_DIR="/opt/${APP_NAME}"
APP_USER="candy"
VENV_DIR="${APP_DIR}/venv"
DOMAIN="${1:-_}"  # 可选域名参数

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
step()  { echo -e "${GREEN}[+]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
err()   { echo -e "${RED}[x]${NC} $1"; exit 1; }
info()  { echo -e "${BLUE}[i]${NC} $1"; }

echo ""
echo "============================================"
echo "  可予礼品 · 竞品监控平台 - 云服务器部署"
echo "============================================"
echo ""
info "域名: ${DOMAIN} (未指定则使用 IP 访问)"

# ====== 检测系统 ======
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    err "无法检测操作系统"
fi
step "检测到系统: ${OS}"

# ====== 安装系统依赖 ======
step "安装系统依赖 (Python3 + Nginx)..."
case $OS in
    ubuntu|debian)
        export DEBIAN_FRONTEND=noninteractive
        apt update -qq
        apt install -y -qq python3 python3-pip python3-venv nginx curl ufw 2>&1 | tail -1
        ;;
    *)
        err "暂不支持的系统: ${OS}，请使用 Ubuntu 20.04+ 或 Debian 11+"
        ;;
esac

# ====== 创建应用用户 ======
if ! id -u ${APP_USER} &>/dev/null; then
    step "创建应用用户: ${APP_USER}"
    useradd -r -s /bin/false ${APP_USER}
fi

# ====== 部署代码 ======
step "部署应用代码到 ${APP_DIR}..."
mkdir -p ${APP_DIR}
# 排除部署脚本目录和 .git
rsync -a --exclude='deploy/' --exclude='.git/' --exclude='__pycache__/' --exclude='*.pyc' \
      "$(dirname "$0")/../" ${APP_DIR}/
chown -R ${APP_USER}:${APP_USER} ${APP_DIR}

# ====== 创建虚拟环境 ======
step "创建 Python 虚拟环境..."
sudo -u ${APP_USER} python3 -m venv ${VENV_DIR}
sudo -u ${APP_USER} ${VENV_DIR}/bin/pip install --upgrade pip -q
sudo -u ${APP_USER} ${VENV_DIR}/bin/pip install -r ${APP_DIR}/requirements.txt -q

# ====== 初始化数据库 ======
step "初始化数据库..."
cd ${APP_DIR}
if [ -f "${APP_DIR}/candy_monitor.db" ]; then
    info "数据库文件已存在，跳过数据导入"
    sudo -u ${APP_USER} ${VENV_DIR}/bin/python -c "from database import init_db; init_db()" 2>/dev/null || true
else
    sudo -u ${APP_USER} ${VENV_DIR}/bin/python -c "from database import init_db; init_db()" 2>/dev/null
    if [ -f "${APP_DIR}/import_real_data.py" ]; then
        step "导入行业数据..."
        sudo -u ${APP_USER} ${VENV_DIR}/bin/python import_real_data.py || warn "数据导入失败"
    fi
fi

# ====== 配置 systemd 服务 ======
step "配置 systemd 守护进程..."
cat > /etc/systemd/system/${APP_NAME}.service << SERVICE_EOF
[Unit]
Description=可予礼品竞品监控平台
After=network.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
Environment="CANDY_HOST=127.0.0.1"
Environment="CANDY_PORT=5000"
Environment="CANDY_THREADS=4"
Environment="CANDY_DEBUG=false"
ExecStart=${VENV_DIR}/bin/python run.py
Restart=always
RestartSec=5

# 安全加固
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=${APP_DIR}
ReadOnlyPaths=/usr/lib /usr/share

[Install]
WantedBy=multi-user.target
SERVICE_EOF

systemctl daemon-reload
systemctl enable ${APP_NAME}
systemctl restart ${APP_NAME}
sleep 2

# 验证服务
if systemctl is-active --quiet ${APP_NAME}; then
    step "应用服务已启动"
else
    err "应用服务启动失败，请检查: journalctl -u ${APP_NAME} -n 20"
fi

# ====== 配置 Nginx ======
step "配置 Nginx 反向代理..."

# 移除默认站点
rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true

cat > /etc/nginx/sites-available/${APP_NAME} << NGINX_EOF
# 可予礼品竞品监控平台
server {
    listen 80;
    server_name ${DOMAIN};

    # 日志
    access_log /var/log/nginx/${APP_NAME}_access.log;
    error_log  /var/log/nginx/${APP_NAME}_error.log;

    # 上传限制
    client_max_body_size 50M;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 静态文件 (7天缓存)
    location /static/ {
        alias ${APP_DIR}/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # 反向代理
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
    }

    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
NGINX_EOF

# 启用站点
ln -sf /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/${APP_NAME}

if nginx -t 2>/dev/null; then
    systemctl reload nginx
    step "Nginx 配置生效"
else
    warn "Nginx 配置有误，请检查"
fi

# ====== 防火墙 ======
step "配置防火墙..."
ufw --force enable 2>/dev/null || true
ufw allow 22/tcp 2>/dev/null || true
ufw allow 80/tcp 2>/dev/null || true
ufw allow 443/tcp 2>/dev/null || true
ufw status verbose 2>/dev/null | grep -E '80|443' || true

# ====== 获取公网 IP ======
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ip.sb 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "YOUR_SERVER_IP")

# ====== HTTPS 配置（如果有域名） ======
if [ "${DOMAIN}" != "_" ] && [ -n "${DOMAIN}" ]; then
    step "配置 HTTPS (Let's Encrypt)..."
    apt install -y -qq certbot python3-certbot-nginx 2>&1 | tail -1
    certbot --nginx -d ${DOMAIN} --non-interactive --agree-tos --email admin@${DOMAIN} --redirect 2>/dev/null && \
        step "HTTPS 已启用" || \
        warn "HTTPS 配置失败，请手动执行: sudo certbot --nginx -d ${DOMAIN}"
fi

# ====== 完成 ======
echo ""
echo "============================================"
echo -e "  ${GREEN}部署完成！${NC}"
echo "============================================"
echo ""

if [ "${DOMAIN}" != "_" ] && [ -n "${DOMAIN}" ]; then
    echo "  访问地址: https://${DOMAIN}"
    echo "  新手引导: https://${DOMAIN}/guide"
    echo "  健康检查: https://${DOMAIN}/health"
else
    echo "  访问地址: http://${SERVER_IP}"
    echo "  新手引导: http://${SERVER_IP}/guide"
    echo "  健康检查: http://${SERVER_IP}/health"
fi

echo ""
echo "  管理命令:"
echo "    systemctl restart ${APP_NAME}    重启服务"
echo "    systemctl status  ${APP_NAME}    查看状态"
echo "    journalctl -u ${APP_NAME} -f     查看日志"
echo ""

if [ "${DOMAIN}" = "_" ] || [ -z "${DOMAIN}" ]; then
    echo "  下一步:"
    echo "    1. 将域名 A 记录指向 ${SERVER_IP}"
    echo "    2. 配置 HTTPS:"
    echo "       sudo certbot --nginx -d your-domain.com"
    echo ""
fi
