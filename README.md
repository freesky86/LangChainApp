# LangChainApp
This is a FastAPI + LangChain(LangGraph) Application. It provides RESTFul API to leverage the power of LLMs. 
The main purpose of this project is to demonstrate how to use LangChain to build a simple application.

## How to run
**Step 1**: create virtual environment  
```bash
python -m venv myvenv
```

**Step 2**: activate virtual environment  
- **Windows**:  
  ```bash
  .\myvenv\Scripts\activate  
  ```
- **macOS/Lunix**:  
  ```bash  
  source myvenv/bin/activate
  ```
**Step 3**: install dependencies
After activating the virtual environment, install the dependencies listed in the requirememnt.txt:
```bash
pip install -r requirement.txt
```

**注**: 由于langchain的lib在国内下载比较慢，如果有下载好的，可以copy到.\myvenv目录下。

**Step 4**: config enviroment variables
1. create .env file under root path  
2. access 阿里百炼平台(https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key) to get API key 
3. add DASHSCOPE_API_KEY in .env file
```env
DASHSCOPE_API_KEY="sk-xxx"
```

**Step 5**: run application
1. open terminal and make sure it uses myvenv virtual environment
2. run '*fastapi dev main.py*' to start the application, then you can call API according the swagger docs on http://127.0.0.1:8000/docs  
```bash
fastapi dev main.py
```


