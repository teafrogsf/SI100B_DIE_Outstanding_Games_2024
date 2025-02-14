from openai import OpenAI
from typing import List, Dict


def LLM_chat(input_text: str, chat_history: List[Dict]) -> str:
    client = OpenAI(
        base_url='http://10.15.88.73:5001/v1',
        api_key='ollama',  # required but ignored
    )

    # 将用户输入添加到对话历史
    chat_history.append({"role": "user", "content": input_text})

    # 调用模型
    response = client.chat.completions.create(
        model="llama3.2",
        messages=chat_history,
    )

    # 提取模型回复
    assistant_reply = response.choices[0].message.content

    # 将助手回复添加到对话历史
    chat_history.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

'''
while True:
    input_text = input("You: ")
    if input_text.lower() in ["exit", "quit"]:
        print("Chat ends.")
        break

    # 调用函数并保持对话历史
    reply = LLM_chat(input_text, messages)
    print(f"NPC: {reply}")
'''