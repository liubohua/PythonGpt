# 使用官方的 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到 Docker 容器中的 /app 目录
COPY . /app

# 安装所需的依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的默认端口
EXPOSE 5000

# 设置容器启动时运行的命令
CMD ["python", "app.py"]
