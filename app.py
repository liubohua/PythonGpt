from flask import Flask, request, jsonify, render_template_string
import openai
import os
import json

from openai import OpenAI

# 从环境变量中获取 API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 读取微调后的模型 ID
def load_fine_tuned_model_id():
    try:
        with open("fine_tuned_model.json", "r") as file:
            data = json.load(file)
            id = data.get("fine_tuned_model_id")
            print(f"file read id:ID={id}")
            return data.get("fine_tuned_model_id")
    except FileNotFoundError:
        return None

# 加载微调后的模型 ID
FINE_TUNED_MODEL = load_fine_tuned_model_id()

# 创建 Flask 实例
app = Flask(__name__)

# 主页面路由
@app.route('/')
def index():
    return "Hello, this is the ChatGPT API integration with Fine-Tuned model!"

# 显示聊天页面
@app.route('/chat', methods=['GET'])
def chat_page():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat with Fine-Tuned ChatGPT FINE_TUNED_MODEL: {FINE_TUNED_MODEL}</title>
        <script>
            console.log("FINE_TUNED_MODEL: {FINE_TUNED_MODEL}");
        </script>
    </head>
    <body>
        <h1>Chat with ChatGPT (Fine-Tuned)</h1>
        <div>
            <textarea id="userInput" placeholder="Enter your message here...FINE_TUNED_MODEL: {FINE_TUNED_MODEL}"></textarea><br>
            <button onclick="sendMessage()">Send</button>
        </div>
        <div id="chatBox"></div>

        <script>
            function sendMessage() {
                const message = document.getElementById("userInput").value;
                if (!message) {
                    alert("Please enter a message!");
                    return;
                }

                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    let chatBox = document.getElementById("chatBox");
                    if (data.error) {
                        chatBox.innerHTML += `<p>Server error: ${data.error}</p>`;
                    } else {
                        chatBox.innerHTML += `<p>You: ${message}</p>`;
                        chatBox.innerHTML += `<p>ChatGPT: ${data.response}</p>`;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

# 接收用户消息并返回 Fine-Tuned ChatGPT 的响应
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        # 提取回复内容
        chat_response = response.choices[0].message["content"]

        # 返回时明确指定 utf-8 编码
        return jsonify({"response": chat_response}), 200

    except Exception as e:
        # 返回时明确指定 utf-8 编码，并转换为字符串以避免编码错误
        return jsonify({"error": str(e)}), 500

# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
