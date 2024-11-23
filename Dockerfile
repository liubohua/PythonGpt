# 使用官方的 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到 Docker 容器中的 /app 目录
COPY . /app

# 安装所需的依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# 暴露 Flask 应用的默认端口
EXPOSE 5000
# 使用 gunicorn 启动 Flask 应用
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
