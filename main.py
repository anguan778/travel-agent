# -*- coding: utf-8 -*-
"""旅游攻略Agent - 命令行交互入口

运行方式：python main.py
"""

from travel_agent import TravelAgent


def main():
    agent = TravelAgent()
    print(agent.greet())
    print()
    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{agent.name}: 旅途愉快，再见！")
            break
        if not user_input:
            continue
        if user_input in ("退出", "quit", "exit", "拜拜", "再见"):
            print(f"{agent.name}: 旅途愉快，再见！")
            break
        response = agent.chat(user_input)
        print(f"{agent.name}: {response}")
        print()


if __name__ == "__main__":
    main()