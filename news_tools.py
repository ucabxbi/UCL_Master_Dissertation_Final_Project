from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_core.retrievers import BaseRetriever
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool
from langchain_community.document_loaders import WebBaseLoader
import requests, os
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

embedding_function = OpenAIEmbeddings()

class DBNewsSearch:
    @tool("News DB Tool")
    def databasenews(query: str):
        """Fetch industry news articles and process their contents."""
        API_KEY = os.getenv('NEWSAPI_KEY')  # Fetch API key from environment variable
        base_url = "https://newsapi.org/v2/everything"
        
        params = {
            'q': query,
            'sortBy': 'publishedAt',
            'apiKey': API_KEY,
            'language': 'en',
            'pageSize': 10,
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return "Failed to retrieve news."
        
        articles = response.json().get('articles', [])
        all_splits = []
        for article in articles:
            loader = WebBaseLoader(article['url'])
            docs = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)
            all_splits.extend(splits) 
            for split in splits:
                split.metadata['source_url'] = article['url']

        if all_splits:
            vectorstore = Chroma.from_documents(all_splits, embedding=embedding_function, persist_directory="./chroma_db")
            retriever = vectorstore.similarity_search(query)
            return retriever
        else:
            return "Nothing available for processing."

class GetNews:
    @tool("Get News Tool")
    def news(query: str) -> str:
        """Search Chroma DB for relevant news information based on the industry from customer input."""
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
        retriever = vectorstore.similarity_search(query)
        return retriever        
class NewsSearchTools:

    @tool("Search for news articles")
    def search_news(query):
        """Useful for finding additional perspectives and analyses on specific topics.

        """
        search_tool = DuckDuckGoSearchRun()
        return search_tool.run(query)
    