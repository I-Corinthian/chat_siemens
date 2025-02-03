from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from siemens_vbload import Vectordbquery

vb = Vectordbquery()
model = ChatOllama(model='deepseek-coder:33b', temperature=0.6)

system_msg = '''<think>You are a helpful bot who answers questions asked by the user based on the given context.</think>'''

prompt_temp = '''
Context:
{context}

PLC used:
{plc}

Question:
<action> Give a concise answer to this based of the Context: {question} </action>
'''

sysmsg = SystemMessage(content=system_msg)
prompt = ChatPromptTemplate.from_template(prompt_temp)

chat_history = [sysmsg]

def set_path(plc_model):
    if plc_model == "S7-1200":
        path = 'vdb_projects/s7-1200/vector_db'
        return path
    elif plc_model == "S7-1500":
        path = 'vdb_projects/s7-1500/vector_db'
        return path

def call(input, plc_model):
    query_results = vb.query(input, path=set_path(plc_model))
    
    context = "\n".join([res[0] for res in query_results])  
    
    call_input = prompt.format(context=context, plc = plc_model,question=input)
    if len(chat_history)>1:
        chat_history.pop(1)
        chat_history.append(HumanMessage(call_input))
    else:
        chat_history.append(HumanMessage(call_input))

    response = ""
    for chunks in model.stream(chat_history):
        response += chunks.content
        yield response