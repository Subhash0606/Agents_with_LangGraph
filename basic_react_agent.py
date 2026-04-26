
import warnings
warnings.simplefilter("ignore")
import os
from typing import TypedDict, List, Union, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import add_messages
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode



class AgenState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]



@tool

def add_(a:int, b:int):
    """This function adds 2 numbers together"""

    return a+b

def subt_(a:int, b:int):
    """This function subtracts second number from first number"""

    return a-b

def mult_(a:int, b:int):
    """This function multiplies 2 given numbers"""

    return a*b

tool_list = [add_,subt_,mult_]

model = ChatOpenAI(model='gpt-4o').bind_tools(tool_list)


##node

def process_node(state:AgenState)->AgenState:

    system_prompt = SystemMessage(content = 'You are a AI Assitant! Your job is to respond with best of your abilities')

    response = model.invoke([system_prompt]+state['messages'])

    return {'messages':[response]}


def tool_decision(state: AgenState)-> str:

    last_message = state['messages'][-1]

    if last_message.tool_calls:
        return "continue"
    
    else:
        return "end"
    

tool_node = ToolNode(tools=tool_list) 

graph = StateGraph(AgenState)

graph.add_node('process',process_node)
graph.add_node('tool_node',tool_node)

graph.set_entry_point('process')

graph.add_conditional_edges('process', tool_decision, {'continue':'tool_node','end':END})

graph.add_edge('tool_node','process')

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


input_message = HumanMessage(content = ('Add 2+3-6*3'))

print_stream(app.stream({'messages':input_message}, stream_mode='values'))








    


    








