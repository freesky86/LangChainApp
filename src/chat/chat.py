from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatTongyi

from dotenv import load_dotenv

load_dotenv()

llm = ChatTongyi()
prompt = ChatPromptTemplate.from_messages(
    [   ("system", "你是我的人工智能助手，协助我解答问题。"),
        ("user", "{question}")
    ]
)

output = StrOutputParser()

chain = prompt | llm | output
result = chain.invoke({"question": "什么是人工智能？"})
print(result)

