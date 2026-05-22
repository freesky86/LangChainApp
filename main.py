from src.services.gpt_service import GPTService

if __name__ == "__main__":
    print("This is a LangChain Application")
    gpt_service = GPTService()
    response = gpt_service.ask("What is LangChain?")
    print(response)