import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

# 创建 Flask 实例
app = Flask(__name__)

# 实例化一个 OpenAI 客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 读取 Fine-Tuned 模型的 ID
with open("fine_tuned_model.json", "r") as f:
    FINE_TUNED_MODEL = f.read().strip()

print(f"Using model ID: {FINE_TUNED_MODEL}")
print(f"API:{os.getenv("OPENAI_API_KEY")}")

# 主页面路由
@app.route('/')
def index():
    return "Hello, this is the ChatGPT API integration demo!"

# 显示聊天页面
@app.route('/chat', methods=['GET'])
def chat_page():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat with ChatGPT</title>
    </head>
    <body>
        <h1>Chat with ChatGPT</h1>
        <div>
            <textarea id="userInput" placeholder="Enter your message here..."></textarea><br>
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

# 接收用户消息并返回 ChatGPT 的响应
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        # 使用显式实例化客户端调用 API
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
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
