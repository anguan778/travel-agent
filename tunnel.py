"""内网穿透：将本地8080端口暴露到公网"""
from pyngrok import ngrok

# 设置代理（如果需要）
import os
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

print("正在建立公网隧道...")
# 打开8080端口的隧道
public_url = ngrok.connect(8080, "http")
print("=" * 50)
print("部署成功！公网访问地址：")
print(public_url)
print("=" * 50)
print("按 Ctrl+C 断开连接")
print()

# 保持运行
try:
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()
except KeyboardInterrupt:
    print("正在关闭隧道...")
    ngrok.kill()
    print("已断开")