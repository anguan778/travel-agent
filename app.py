# -*- coding: utf-8 -*-
"""旅游攻略Agent - Flask Web应用

运行方式：python app.py
访问地址：http://127.0.0.1:7860

部署说明：Hugging Face Spaces要求应用监听7860端口并绑定0.0.0.0。
"""

import os

from flask import Flask, render_template, request, jsonify, session

from travel_agent import TravelAgent

app = Flask(__name__)
app.secret_key = "travel-agent-secret-key-change-in-production"

# 全局Agent实例
agent = TravelAgent()


@app.route("/")
def index():
    """聊天主页面"""
    if "greeted" not in session:
        session["greeted"] = True
    return render_template("index.html", agent_name=agent.name)


@app.route("/chat", methods=["POST"])
def chat():
    """对话接口"""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "请提供message字段"}), 400

    message = data["message"].strip()
    if not message:
        return jsonify({"error": "消息不能为空"}), 400

    response = agent.chat(message)
    return jsonify({"reply": response, "agent_name": agent.name})


@app.route("/greet", methods=["GET"])
def greet():
    """欢迎语接口"""
    return jsonify({"greeting": agent.greet(), "agent_name": agent.name})


if __name__ == "__main__":
    # Hugging Face Spaces要求监听7860端口并绑定0.0.0.0
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)