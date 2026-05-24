from typing import TypedDict, Literal
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# 1. 明确定义图的状态（State）
# 这是节点之间传递的数据结构
class GraphState(TypedDict):
    user_input: str
    intent: str  # 用户的意图：'translate' 或 'polish'
    response: str

class WriteAgent:
    def __init__(self):
        # 2. 初始化通义千问大模型
        # ChatTongyi 默认会读取环境变量 DASHSCOPE_API_KEY
        self.llm = ChatTongyi(model_name="qwen-turbo", temperature=0.7)

        # 编译图
        self.app = self.compile_workflow()

    # 3. 定义图的节点（Nodes）
    def intent_router_node(self, state: GraphState) -> GraphState:
        """分类节点：判断用户是想翻译还是润色"""
        user_input = state["user_input"]
        
        prompt = f"""请分析以下用户的输入，判断他们的真实意图是需要“翻译（把一种语言换成另一种语言）”还是“润色（让原本的语言文字更地道优美）”。

        请仅输出 'translate' 或 'polish' 其中一个词，不要包含任何其他字符。

        用户输入: {user_input}
        """

        # 转换为 LangChain 的消息格式进行调用
        llm_output = self.llm.invoke([HumanMessage(content=prompt)]).content.strip().lower()
    
        # 简单清洗，确保返回预期的分类
        intent = "translate" if "translate" in llm_output else "polish"
        return {"intent": intent}


    def translate_node(self,state: GraphState) -> GraphState:
        """翻译节点"""
        user_input = state["user_input"]
        system_prompt = "你是一个精通多语言的翻译官，请将用户的输入翻译为地道的英文。如果原本就是英文，则翻译为中文。"
        
        res = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ])
        return {"response": res.content}


    def polish_node(self, state: GraphState) -> GraphState:
        """润色节点"""
        # user_input = state["state" if "user_input" not in state else "user_input"]
        user_input = state["user_input"]
        system_prompt = "你是一个文学编辑，请在不改变原意的前提下，润色修正用户输入的句子，使其更高级、流畅、没有语病。"
        
        res = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ])
        return {"response": res.content}


    # 4. 路由逻辑（Conditional Edge 的分流函数）
    def route_by_intent(self, state: GraphState) -> Literal["translate", "polish"]:
        """根据分类节点的判断结果，决定下一步走哪个节点"""
        return state["intent"]

    def compile_workflow(self):
        # 5. 构建和编译 LangGraph 工作流
        workflow = StateGraph(GraphState)

        # 添加节点
        workflow.add_node("intent_router", self.intent_router_node)
        workflow.add_node("translate_helper", self.translate_node)
        workflow.add_node("polish_helper", self.polish_node)

        # 设置起点
        workflow.add_edge(START, "intent_router")

        # 设置条件条件边：从分类节点出发，根据意图流向翻译或润色
        workflow.add_conditional_edges(
            "intent_router",
            self.route_by_intent,
            {
                "translate": "translate_helper",
                "polish": "polish_helper"
            }
        )

        # 设置终点边：处理完后直接结束
        workflow.add_edge("translate_helper", END)
        workflow.add_edge("polish_helper", END)

        app = workflow.compile()
        # ✨ 新增：在编译完成后，直接在控制台打印类似图片的 ASCII 架构图
        print("\n" + "="*20 + " 工作流架构图 (Workflow Graph) " + "="*20)
        try:
            # 使用 LangGraph 内置的 ASCII 字符画图功能
            app.get_graph().print_ascii()
        except Exception as e:
            print(f"打印字符图失败: {e}")
        print("="*71 + "\n")
        return app
    
    def run(self, user_input: str) -> str:
        """对外的运行接口，输入用户文本，输出处理结果"""
        inputs = {"user_input": user_input}
        result = self.app.invoke(inputs)
        print(f"识别意图: {result['intent']}")
        print(f"最终结果: {result['response']}\n")
        return result["response"]


# 6. 测试运行
if __name__ == "__main__":
    agent = WriteAgent()
    # 测试用例 1：触发翻译
    print("--- 测试 1：翻译意图 ---")
    agent.run("今天天气真好，我想出去走走。")

    # 测试用例 2：触发润色
    print("--- 测试 2：润色意图 ---")
    agent.run("我写代码非常厉害，别人都说我是个大牛。")
