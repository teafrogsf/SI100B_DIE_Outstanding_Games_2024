from openai import OpenAI
from typing import List, Dict
import dialog


def chatfunction1(messages,client,screen,liste,name=None,pict=None):
      

        
        response = client.chat.completions.create(
            model="llama3.2",      
            messages=messages,    # a list of dictionary contains all chat dictionary
        )

        # 提取模型回复
        assistant_reply = response.choices[0].message.content
        print(f"Llama: {assistant_reply}")
        liste.append(dialog.WordsOutput(assistant_reply+' ',0,500,name,pict))
        # 将助手回复添加到对话历史
        messages.append({"role": "assistant", "content": assistant_reply})


def chatfunction2():
    client = OpenAI(
    base_url='http://10.15.88.73:5006/v1',
    api_key='ollama')

    chat_completion = client.chat.completions.create(
        messages=[
            {
            'role': 'user',
            'content': 'You are a helpful teaching assitant of computer science lessons, \
                you should help CS freshman with teaching \
                how to use LLM to design and create games better. '
            },
            {
            'role': 'user',
            'content': "How we can involve LLM into a part of game?",
            }
                ],
     model='llama3.2',
    )

    print(chat_completion.choices[0].message.content)



        
        
