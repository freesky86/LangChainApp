import os
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi

from dotenv import load_dotenv

load_dotenv()

class CalculateAgent:
    def __init__(self):
        # 1. 确保环境变量已加载
        if "DASHSCOPE_API_KEY" not in os.environ:
            raise ValueError("请先设置环境变量 DASHSCOPE_API_KEY")

        # 2. 定义 Agent 可以使用的 Tool（工具）
        # 必须加上简洁清晰的 Docstring，大模型靠它来判断何时使用该工具
        @tool
        def calculate_multiply(a: int, b: int) -> int:
            """当需要计算两个整数相乘（乘法）时，使用此工具。"""
            print(f"工具被调用: calculate_multiply({a}, {b})")
            return a + b

        tools = [calculate_multiply]

        # 3. 初始化通义千问大模型
        # 推荐使用 qwen-turbo、qwen-plus 或最新版的智能体基座模型
        llm = ChatTongyi(model="qwen-plus", temperature=0.0)

        # 4. 使用 LangChain 1.x 推荐的全新 API 构建高级 Agent
        # 该方法底层基于 LangGraph，自动处理了循环思考、工具调用与状态持久化
        print("正在初始化 Agent...")
        self.agent_executor = create_agent(
            model=llm,
            tools=tools,
            # 如果需要开启 LangSmith 追踪，可在此处或通过环境变量配置
        )

    def ask_agent(self, query: str) -> str:
        print(f"\n用户提问: {query}")
        print("-" * 50)

        # 构造消息列表：强行把系统提示词作为第一条消息喂进去
        messages = [
            (
                "system", 
                "你是一个严格的数据报告员。在回答用户的数学问题时，你必须且只能使用工具返回的数值，"
                "绝对不允许自己进行二次计算或修正，即使你觉得工具的结果是错的，也必须以工具返回的结果为准！"
            ),
            ("user", query)
        ]
        
        # 执行并获取响应
        response = self.agent_executor.invoke({"messages": messages})
        
        # 打印最终模型输出的结果
        final_message = response["messages"][-1]  #langchain_core.messages.ai.AIMessage
        print(f"Agent 回复: {final_message.content}")
        return final_message.content


if __name__ == "__main__":
    # 测试场景 1：不需要工具，直接闲聊
    agent = CalculateAgent()
    agent.ask_agent("你好，你是谁？")
    
    # 测试场景 2：需要触发工具调用进行数学计算
    agent.ask_agent("请问 123 乘以 456 的结果是多少？")