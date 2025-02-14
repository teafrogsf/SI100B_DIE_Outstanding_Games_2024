import threading
import time

import pygame
from openai import OpenAI

import Config
import I18n

CLIENT = None
MESSAGES = [{
    'role': 'system',  # 系统消息，初始化为配置的AI提示
    'content': Config.AI_PROMPT
}]
EVENTS = []  # 存储事件的列表


# 向EVENTS列表中添加新事件
def add_event(event: str):
    EVENTS.append(event)
    print(event)


# 初始化AI客户端
def init():
    global CLIENT
    try:
        CLIENT = OpenAI(
            base_url=Config.AI_URL,
            api_key='ollama',
        )
    except Exception as e:
        print(e)
        CLIENT = None


# 更新AI的回应消息
def update_ai_response(response: str):
    MESSAGES.append({
        'role': 'assistant',  # 表示AI的消息角色
        'content': response   # AI的回复内容
    })


# 获取AI响应流（异步获取）
def get_response_stream(input_text, role='user'):
    user = {
        'role': role,         # 用户的角色
        'content': input_text  # 用户输入的文本
    }
    event = {
        'role': 'system',     # 系统角色
        'content': ';'.join(EVENTS)  # 系统事件信息，连接成字符串
    }
    try:
        ret = None if CLIENT is None else CLIENT.chat.completions.create(
            messages=MESSAGES + [event, user],  # 合并消息列表
            model='llama3.2',  # 使用的AI模型
            stream=True,  # 使用流模式进行响应
            timeout=30  # 超时设定
        )
    except Exception as e:  # 异常处理
        print(e)
        ret = None
    MESSAGES.append(user)  # 添加用户消息到对话记录
    return ret  # 返回流对象


LOCK = threading.Lock()
LOCK1 = threading.Lock()


def add_response(text, color=(255, 255, 0), role='user'):

    def fetch_response():
        with LOCK:  # 获取LOCK锁
            LOCK1.acquire()
            LOCK1.release()
            if not Config.RUNNING:
                return  # 若游戏结束，返回
            thread1 = threading.Thread(target=update_response)
            thread1.start()
            Config.AI_INPUT_LOCK = True  # 锁定AI输入，避免同时多个输入
            print('You: ' + text)  # 打印用户输入
            stream = get_response_stream(text, role)  # 获取AI响应流
            if stream is None:
                response.string += 'ERROR'  # 若流为空，表示出错
                return
            for chunk in stream:
                if not Config.RUNNING:
                    return  # 若游戏结束，返回
                response.string += chunk.choices[0].delta.content  # 拼接返回的响应内容
            update_ai_response(response.string[response.string.find(': ') + 2:])  # 更新AI回复
            print('AI: ' + response.string[response.string.find(': ') + 2:])  # 打印AI回复

    # UI更新处理线程

    def update_response():
        with LOCK1:  # 获取LOCK1锁
            try:
                Config.CLIENT.current_hud.add_message(response, color)  # 更新UI上的信息
                while True:
                    if not Config.RUNNING:
                        return  # 若游戏结束，返回
                    time.sleep(0.01)
                    if Config.AI_INPUT_LOCK:  # 检查是否锁定输入
                        if not thread0.is_alive() and response.is_end():  # 判断响应是否结束
                            Config.CLIENT.current_hud.messages.insert(1, (I18n.literal(response.get()), color,
                                                                          time.time()))  # 插入消息到UI
                            Config.CLIENT.current_hud.messages.pop(0)  # 弹出旧消息
                            break
                        if response.count():
                            Config.CLIENT.current_hud.messages.insert(1, (I18n.literal(response.get()), color,
                                                                          time.time()))
                            response.st = response.cnt + 1  # 更新响应状态
                if response.string.count(str(Config.FLAG)) >= 1:  # 检查是否泄露了标记
                    Config.CLIENT.current_hud.messages.insert(0, (I18n.text('flag_leaked'), (255, 0, 0), time.time()))
                    Config.NETHER_PORTAL_LOCK = False  # 解锁传送门
                Config.AI_INPUT_LOCK = False  # 解除输入锁定
            except AttributeError:
                return
            except pygame.error:
                return

    response = I18n.ai_text(I18n.text('ai_assistant').get(), '')
    thread0 = threading.Thread(target=fetch_response)
    thread0.start()
    return response


thread = threading.Thread(target=init)
thread.start()
