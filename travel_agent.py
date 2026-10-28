# -*- coding: utf-8 -*-
"""旅游攻略智能Agent核心模块

提供目的地推荐、行程规划、预算估算、旅行贴士等功能，
支持基于关键词的自然语言交互。
"""

import re

from knowledge_base import DESTINATIONS, TYPE_KEYWORDS, INTENT_KEYWORDS


class TravelAgent:
    """旅游攻略智能助手"""

    def __init__(self, name="游游"):
        self.name = name
        self.destinations = DESTINATIONS
        self.history = []

    # ==================== 对外接口 ====================

    def greet(self):
        """返回欢迎语"""
        return (
            "=" * 50 + "\n"
            f"  你好！我是旅游攻略助手「{self.name}」\n"
            "  我可以帮你：\n"
            "    1. 推荐旅游目的地\n"
            "    2. 生成详细行程规划\n"
            "    3. 估算旅行预算\n"
            "    4. 提供实用旅行贴士\n"
            "  试试对我说：「推荐一个适合秋天去的海岛」\n"
            "  或「帮我规划一个成都3天的行程」\n"
            "  输入「退出」结束对话\n" +
            "=" * 50
        )

    def chat(self, user_input):
        """自然语言对话入口，自动识别意图并响应"""
        self.history.append(("用户", user_input))
        response = self._dispatch(user_input)
        self.history.append((self.name, response))
        return response

    # ==================== 核心功能 ====================

    def recommend_destinations(self, purpose=None, budget=None, season=None, region=None):
        """根据偏好推荐目的地"""
        results = []
        for name, info in self.destinations.items():
            if region and info["region"] != region:
                continue
            if season and season not in info["best_seasons"]:
                continue
            if purpose and info["type"] != purpose:
                continue
            if budget and budget != "舒适":
                cap = {"经济": 400, "豪华": 99999}.get(budget, 99999)
                if info["budget_per_day"]["经济"] > cap and budget == "经济":
                    continue
            results.append((name, info))
        return results

    def generate_itinerary(self, destination, days=None):
        """生成按天分配的行程规划"""
        if destination not in self.destinations:
            return None
        info = self.destinations[destination]
        if days is None:
            days = info["recommended_days"]
        attractions = info["attractions"]
        itinerary = []
        per_day = max(1, len(attractions) // days)
        idx = 0
        for day in range(1, days + 1):
            spots = attractions[idx: idx + per_day]
            if day == days:
                spots = attractions[idx:]
            idx += per_day
            if not spots:
                spots = attractions[-1:]
            itinerary.append({"day": day, "spots": spots})
        return itinerary

    def estimate_budget(self, destination, days, style="舒适"):
        """估算旅行总预算"""
        if destination not in self.destinations:
            return None
        info = self.destinations[destination]
        daily = info["budget_per_day"].get(style, info["budget_per_day"]["舒适"])
        return {
            "destination": destination,
            "days": days,
            "style": style,
            "daily_budget": daily,
            "total_budget": daily * days,
        }

    def get_travel_tips(self, destination):
        """获取目的地旅行贴士"""
        if destination not in self.destinations:
            return None
        return self.destinations[destination]["tips"]

    # ==================== 意图识别与分发 ====================

    def _dispatch(self, text):
        """意图识别与分发"""
        intent = self._recognize_intent(text)
        dest = self._extract_destination(text)

        if intent == "推荐目的地":
            return self._handle_recommend(text)
        if intent == "生成行程":
            if dest:
                days = self._extract_days(text)
                return self._format_itinerary(dest, days)
            return "请告诉我想去的目的地，例如「帮我规划北京4天行程」"
        if intent == "预算估算":
            if dest:
                days = self._extract_days(text) or self.destinations[dest]["recommended_days"]
                style = self._extract_style(text)
                return self._format_budget(dest, days, style)
            return "请告诉我想去的目的地和天数，例如「去东京5天大概多少钱」"
        if intent == "旅行贴士":
            if dest:
                return self._format_tips(dest)
            return "请告诉我想了解哪个目的地的贴士，例如「去拉萨有什么注意事项」"
        if intent == "美食推荐":
            if dest:
                return self._format_foods(dest)
            return "请告诉我想去哪里吃，例如「成都有什么好吃的」"

        # 未识别意图，尝试匹配目的地直接输出概览
        if dest:
            return self._format_overview(dest)
        return (
            "我还没完全理解你的意思，你可以问我：\n"
            "  · 推荐目的地：「推荐适合春天的目的地」\n"
            "  · 行程规划：「规划杭州3天行程」\n"
            "  · 预算估算：「去三亚5天多少钱」\n"
            "  · 旅行贴士：「去西藏要注意什么」"
        )

    def _recognize_intent(self, text):
        """基于关键词的意图识别"""
        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    return intent
        return None

    def _extract_destination(self, text):
        """从用户输入中提取目的地名称"""
        for name in self.destinations:
            if name in text:
                return name
        return None

    def _extract_days(self, text):
        """提取天数"""
        m = re.search(r"(\d+)\s*[天日]", text)
        if m:
            return int(m.group(1))
        return None

    def _extract_style(self, text):
        """提取消费风格"""
        if "豪华" in text:
            return "豪华"
        if "经济" in text or "穷游" in text or "省钱" in text:
            return "经济"
        return "舒适"

    # ==================== 格式化输出 ====================

    def _handle_recommend(self, text):
        """处理推荐请求"""
        purpose = season = region = None
        for p, kws in TYPE_KEYWORDS.items():
            if any(kw in text for kw in kws):
                purpose = p
                break
        season_map = {"春天": "春季", "夏天": "夏季", "秋天": "秋季", "冬天": "冬季"}
        for s in list(season_map.keys()) + list(season_map.values()):
            if s in text:
                season = season_map.get(s, s)
                break
        if "国内" in text:
            region = "国内"
        if "国外" in text or "国际" in text or "出境" in text:
            region = "国际"
        budget = self._extract_style(text)

        # 逐步放宽筛选条件，优先保留核心偏好（类型/区域）
        results = self.recommend_destinations(purpose, budget, season, region)
        if not results:
            results = self.recommend_destinations(purpose, None, season, region)
        season_relaxed = False
        if not results:
            season_relaxed = True
            results = self.recommend_destinations(purpose, None, None, region)
        if not results:
            results = list(self.destinations.items())

        note = ""
        if season_relaxed and season:
            note = f"（注：暂无{season}最佳的目的地，以下推荐不受季节限制）\n"

        lines = [f"为你推荐以下目的地：\n{note}"]
        for name, info in results[:5]:
            lines.append(
                f"  ★ {name}（{info['type']}）\n"
                f"    最佳季节：{'、'.join(info['best_seasons'])}\n"
                f"    必去景点：{', '.join(info['attractions'][:3])}...\n"
                f"    参考预算：{info['budget_per_day']['舒适']}元/天\n"
            )
        lines.append("输入「规划{目的地}行程」获取详细攻略！")
        return "\n".join(lines)

    def _format_itinerary(self, dest, days):
        itinerary = self.generate_itinerary(dest, days)
        if not itinerary:
            return f"暂无{dest}的行程数据"
        info = self.destinations[dest]
        lines = [f"[行程] {dest}{len(itinerary)}天行程规划\n"]
        for item in itinerary:
            lines.append(f"  第{item['day']}天：")
            for spot in item["spots"]:
                lines.append(f"    · {spot}")
            lines.append("")
        lines.append(f"  美食别错过：{', '.join(info['foods'][:3])}")
        lines.append(f"  建议游玩天数：{info['recommended_days']}天")
        return "\n".join(lines)

    def _format_budget(self, dest, days, style):
        result = self.estimate_budget(dest, days, style)
        if not result:
            return f"暂无{dest}的预算数据"
        return (
            f"[预算] {dest}{days}天{style}游预算参考：\n"
            f"  每日预算：约{result['daily_budget']}元\n"
            f"  总预算：约{result['total_budget']}元\n"
            f"  （含住宿、餐饮、市内交通及门票，不含大交通）"
        )

    def _format_tips(self, dest):
        tips = self.get_travel_tips(dest)
        if not tips:
            return f"暂无{dest}的贴士"
        lines = [f"[贴士] {dest}旅行贴士：\n"]
        for i, tip in enumerate(tips, 1):
            lines.append(f"  {i}. {tip}")
        return "\n".join(lines)

    def _format_foods(self, dest):
        info = self.destinations.get(dest)
        if not info:
            return f"暂无{dest}的美食数据"
        return (
            f"[美食] {dest}必吃美食：\n"
            f"  {', '.join(info['foods'])}\n"
            f"  去了可别错过！"
        )

    def _format_overview(self, dest):
        info = self.destinations[dest]
        return (
            f"[概览] {dest}旅游信息\n"
            f"  类型：{info['type']} | 最佳季节：{'、'.join(info['best_seasons'])}\n"
            f"  必去景点：{', '.join(info['attractions'])}\n"
            f"  特色美食：{', '.join(info['foods'])}\n"
            f"  建议游玩：{info['recommended_days']}天\n"
            f"  预算参考：经济{info['budget_per_day']['经济']}元/天，"
            f"舒适{info['budget_per_day']['舒适']}元/天\n\n"
            f"  输入「规划{dest}行程」或「{dest}多少钱」获取更多信息"
        )