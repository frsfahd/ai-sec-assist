import os 
import asyncio

from typing import Annotated
from openai import AsyncOpenAI
from iso639 import Lang

from dotenv import load_dotenv

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

from scanner import ScanFile, ScanURL
from news import GetRandomNews, ListNews

from util.Types import NewsArticle

# Create the plugin
class ScannerPlugin:

    @staticmethod
    @kernel_function(description="Scan a given URL and provides an explanation whether it is safe or not according to the result")
    async def scan_url(url: str) -> Annotated[str, "Returns a scan result and explanation whether it is safe or not."]:
        result = await ScanURL(url)
        return result
    
    @staticmethod
    @kernel_function(description="Scan a given file (file path) and provides an explanation whether it is safe or not according to the result")
    async def scan_file(url: str) -> Annotated[str, "Returns a scan result and explanation whether it is safe or not."]:
        result = await ScanFile(url)
        return result

class NewsPlugin:
    @staticmethod
    @kernel_function(description="provide user with a Cybersecurity news/update article in spesific language (use ISO 639-1 as language code input)")
    async def get_random_news(language: str) -> Annotated[NewsArticle, "returns an object containing details of the article (title, url, date of published, name of publisher)"]:
        # lg = Lang(language.capitalize())
        result = await GetRandomNews(lang=language)
        return result
    
    @staticmethod
    @kernel_function(description="provide user with a list of 5 Cybersecurity news/update articles in spesific language (use ISO 639-1 as language code input) based on given keyword")
    async def list_of_news(keyword: str, language: str) -> Annotated[list[NewsArticle], "returns a list of article objects"]:
        # lg = Lang(language.capitalize())
        result = await ListNews(keyword=keyword, lang=language)
        return result

# Create Client
load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get("GITHUB_TOKEN"), 
    base_url="https://models.inference.ai.azure.com/",
)

# Create an AI Service that will be used by the `ChatCompletionAgent`
chat_completion_service = OpenAIChatCompletion(
    ai_model_id="gpt-4.1-mini",
    async_client=client,
)

# Create an agent

agent = ChatCompletionAgent(
    service=chat_completion_service, 
    name="SecurityAgent",
    plugins=[ScannerPlugin(), NewsPlugin()],
    instructions="""
    You are a helpful AI Agent that can help answer general digital security questions and scan user's links and files

    Important: when users specify the link and file to scan use that value to scan.
    
    """,
)

# Dictionary to store threads per user
user_threads: dict[str, ChatHistoryAgentThread] = {}

async def RunAgent(user_inputs: list[tuple[str, str]]):
    """
    user_inputs: List of (user_id, message) tuples
    """
    user_id, user_input = user_inputs
    
    # Get or create a thread for this user
    thread = user_threads.get(user_id)
    if thread is None:
        thread = ChatHistoryAgentThread()

    ##################################
        # STREAM OUTPUT
        # print(f"# User ({user_id}): {user_input}\n")
        # first_chunk = True
        # async for response in agent.invoke_stream(
        #     messages=user_input, thread=thread,
        # ):
        #     if first_chunk:
        #         print(f"# {response.name}: ", end="", flush=True)
        #         first_chunk = False
        #     print(f"{response}", end="", flush=True)
        #     thread = response.thread
        # print()
        #################################

        # Use non-streaming call
    response = await agent.get_response(
        messages=user_input, thread=thread,
    )

    # Save the updated thread for this user
    user_threads[user_id] = thread

    return response
    # Optional: Clean up threads if needed
    # for thread in user_threads.values():
    #     await thread.delete()


if __name__ == '__main__':
    user_inputs = [
        # ("alice", "is this url safe, http://ruehrdich.dnsdojo.org/.newsle/ ?"),
        # ("alice", "tell me more about malware."),
        ("john", "give a data news in french")
    ]
    for chat in user_inputs:
        response = asyncio.run(RunAgent(chat))
        print("okay")
        print(response.content)

    # for user_id in user_threads:
    #     print(user_threads.get(user_id)._chat_history.messages)