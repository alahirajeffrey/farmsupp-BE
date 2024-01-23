from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from config import config

output_parser = StrOutputParser()

llm = ChatOpenAI(openai_api_key=config.get('OPENAI_API_KEY'), temperature=0.4)

memory = ConversationBufferMemory(
    memory_key="chat_history", human_prefix="user_message", ai_prefix="chatbot_response", return_messages=True)


def generate_ai_response(question, conversation):

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content="You are an agricultural extension worker with decades of experience having a conversation with a farmer."),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}"),
    ])

    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory.chat_memory(conversation),
        output_parser=output_parser
    )

    reply = chat_llm_chain.invoke(question)

    return reply
