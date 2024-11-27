import openai
import os

# 从环境变量中获取 API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 启动微调
response = openai.FineTune.create(
    training_file="file-HtSwTTVEMRmwBCH5b7sWPj",  # 替换为你的文件 ID
    model="gpt-3.5-turbo"  # 微调模型
)

# 打印 Fine-Tune 任务 ID
print(f"Fine-tune started with ID: {response['id']}")
