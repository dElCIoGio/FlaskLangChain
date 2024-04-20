import os

from dotenv import load_dotenv

load_dotenv()
import json
from typing import Optional, Type
from mytools.NotifyStaff import NotifyStaffTool
from mytools.NewAppointment import NewAppointmentTool
from mytools.GetDateAndTime import GetDateTimeTool
from mytools.GetDateAndTime import get_current_date_and_time

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader, NotionDirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS

from functions import *

# PDF Reader
file = r"knowledgebase/TeeBraids.pdf"
loader = PyPDFLoader(file)
pages = loader.load()

# Create Retriever
# loader = WebBaseLoader("https://python.langchain.com/docs/expression_language/")
# docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
splitDocs = splitter.split_documents(pages)

embedding = OpenAIEmbeddings()
vectorStore = FAISS.from_documents(pages, embedding=embedding)
retriever = vectorStore.as_retriever(search_kwargs={"k": 1})

model = ChatOpenAI(
    model='gpt-3.5-turbo-1106',
    temperature=0.7
)

system = """
You are a friendly assistant called Max. You work for TeeBraids, a braiding salon for men and women. 

The customers usually text to book an appointment, so you have to collect information about the name of the curstomer, 
the hairstyle they are looking for and the time they would like to book. Make sure that the date and time they are booking
is not earlier than {current_date}. If the user only mentions a day of the week when specifying the date of the appointment
assume they mean the upcoming day of the week they mentioned. To avoid mistakes, when confirming the date, always mention
the calendar date, not the day of the week.

Always ask for confirmation from the customer about the information about the booking before submitting it. This is important.

If you already know the customer's name, don't ask again for it. You are part of the company so talk in the first person 
when answering questions.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Tools
retriever_tools = create_retriever_tool(
    retriever,
    "TeeBraids",
    "Use this tool when searching for information about TeeBraids"
)
tools = [retriever_tools,
         NotifyStaffTool(),
         NewAppointmentTool(),
         GetDateTimeTool()]

agent = create_openai_functions_agent(
    llm=model,
    prompt=prompt,
    tools=tools
)

agentExecutor = AgentExecutor(
    agent=agent,
    tools=tools
)


def process_chat(agentExecutor, user_input, chat_history):
    response = agentExecutor.invoke({
        "input": user_input,
        "chat_history": chat_history,
        "current_date": get_current_date_and_time()
    })
    return response["output"]


def getResponse(message, log):
    chat_history = [AIMessage(log[message]["Body"])
                    if log[message]["From"] == os.environ["TWILIO_NUMBER"] else
                    HumanMessage(log[message]["Body"])
                    for message in log]
    response = process_chat(agentExecutor, message, chat_history)
    return response


if __name__ == '__main__':


    chat_history = [AIMessage("Hi, what is your name?"),
                    HumanMessage("My name is Delcio. How are you?")]
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        response = process_chat(agentExecutor, user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

        print("Assistant:", response)


