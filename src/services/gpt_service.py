from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatTongyi

from dotenv import load_dotenv

load_dotenv()

class GPTService:
    def __init__(self):
        self.llm = ChatTongyi()
        self.prompt = ChatPromptTemplate.from_messages(
            [   ("system", "你是我的人工智能助手，协助我解答问题。"),
                ("user", "{question}")
            ]
        )
        self.output = StrOutputParser()

    def ask(self, question: str) -> str:
        chain = self.prompt | self.llm | self.output
        # question = "什么是人工智能？"
        result = chain.invoke({"question": question})
        return result


if __name__ == "__main__":
    service = GPTService()
    result = service.ask("什么是人工智能？")
    print(result)
