#Modified by NH37
from openai import OpenAI
import os

class Chater:
    def __init__(self):
        self.SYSTEM_PROMPT_PATH = os.path.join(os.getcwd(),"LLMSystem","TOGPT")
        self.sys_sentences=[]
        self.sentences=None
        
        self.reply = None 

        self.client = OpenAI(
            base_url='http://10.15.88.73:5008/v1',
            api_key='ollama',
        )

        self.init_sentences1()

    def init_sentences0(self):
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'ChatStyle.txt'),'r',encoding='utf-8') as f0:
            ori_sentences=f0.read().splitlines()
        self.sys_sentences=[]
        sens=[]
        for sentence in ori_sentences:
            if sentence!='':
                sens.append(sentence)
                if len(sens)==5:
                    self.sys_sentences.append(sens)
                    sens==[]
        if len(sens)>0:
            self.sys_sentences.append(sens)

    def init_sentences1(self):
        if len(self.sys_sentences)==0:
            self.init_sentences0()
        self.sentences=[
            {
                'role': 'user',
                'content': '我现在会给你一个语料库，请你记住语料库中的说话风格。我会将语料库分成几批告诉你。'
            }
        ]
        index=0
        for sens in self.sys_sentences:
            index+=1
            sent=f'这是第{index}批语料库：\n'
            for sen in sens:
                sent+=sen+'\n'
            self.sentences.append({'role':'user','content':sent})
        
    def chat(self,sen):
        if self.reply != None:
            self.sentences.append({"role": "assistant", "content": self.reply})
        self.sentences.append({'role':'user','content':'我即将告诉你一段话，请根据我说的这段话，模仿语料库的说话风格，说一段有趣或富有哲理的回复。你说的话不一定要和语料库中的内容完全一致。你回答我的话一定只有中文，不能有英语或任何其他语言！'})
        self.sentences.append({'role':'user', 'content':sen})
        self.interaction()
        return self.reply

    def interaction(self):
        chat_completion=self.client.chat.completions.create(
            messages=self.sentences,
            model='llama3.2'
        )
        self.reply=chat_completion.choices[0].message.content