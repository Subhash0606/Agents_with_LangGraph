
import warnings
warnings.simplefilter("ignore")
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv



load_dotenv()



llm = ChatOpenAI(model="gpt-5-nano")


class State(TypedDict):
    message: List[Union[HumanMessage, AIMessage]]



def process_node(state: State) -> State:

    """Process the node and return the next state."""

    response = llm.invoke(state["message"])

    print("\nAIResponse:", response.content)

    state["message"].append(AIMessage(content=response.content))

    return state


graph = StateGraph(State)

graph.add_node('process',process_node)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

app = graph.compile()


user_input= input("User: ")

conversation_history = []

while user_input.lower() != "exit":

    print(conversation_history)

    conversation_history.append(HumanMessage(content=user_input))

    response = app.invoke({"message":conversation_history})

    conversation_history = response['message']

    user_input = input("User: ")




    






    


