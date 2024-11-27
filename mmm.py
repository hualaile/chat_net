import os
import requests
from flask import Flask, request, jsonify, render_template

# 初始化 Flask 应用
app = Flask(__name__)

# 获取 LM stdio API 密钥和 URL（可以在环境变量中设置）
API_KEY = "lm-studio"  # 使用环境变量存储 API 密钥
API_URL = "http://llll.natapp1.cc/v1/chat/completions" # 默认本地 URL
MODEL_NAME = "llama-3.2-3b-instruct"  # 默认模型名称

# 检查 API 密钥和模型名称是否设置
if not API_KEY:
    raise ValueError("LM_STDIO_API_KEY is not set in environment variables.")
if not MODEL_NAME:
    raise ValueError("MODEL_NAME is not set in environment variables.")

# 聊天路由
@app.route("/api/chat", methods=["POST"])
def chat():
    # 获取用户消息
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # 请求 LM stdio API 获取响应
    try:
        response = requests.post(
            API_URL,
            json={
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": user_message}]
            },
            headers={"Authorization": f"Bearer {API_KEY}"},
        )

        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get("choices")[0].get("message").get("content")
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"error": f"API call failed with status code {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# 首页路由，显示聊天界面
@app.route("/")
def index():
    return render_template("index.html")

# 运行 Flask 应用
if __name__ == "__main__":
    app.run(debug=True)
