#!/bin/bash

# 1. 停止并删除旧的容器
docker-compose down

# 2. 重新构建并启动容器
docker-compose up --build -d
