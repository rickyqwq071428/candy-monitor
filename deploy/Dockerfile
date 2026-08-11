# 可予礼品竞品监控平台 Dockerfile
# 构建: docker build -t candy-monitor .
# 运行: docker run -d -p 5000:5000 --name candy-monitor candy-monitor

FROM python:3.12-slim

LABEL maintainer="可予礼品有限公司"
LABEL description="喜糖/伴手礼竞品监控平台"

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 5000

# 环境变量
ENV CANDY_HOST=0.0.0.0
ENV CANDY_PORT=5000
ENV CANDY_THREADS=4
ENV CANDY_DEBUG=false

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 启动
CMD ["python", "run.py"]
