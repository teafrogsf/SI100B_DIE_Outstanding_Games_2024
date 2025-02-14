import pygame
import sys
from Utility import *
from openai import OpenAI
from typing import List, Dict
import difficultyController
from GameSettings import ChatBoxSettings as CBS


class ChatBox(Scene):
    def __init__(self, npcName):

        self.text_color = CBS.text_color
        self.font = pygame.font.Font(FontSettings.FontPath, 28)
        self.chat_content = []
        self.input_text = ""

        # 输入文本位置
        self.input_text_x = CBS.input_box_x + 10
        self.input_text_y = CBS.input_box_y + 10

        # 文字行高与最大宽度
        self.line_height = self.font.get_linesize()
        self.max_text_width = CBS.chatbox_width - 20

        # 文字最大行数
        self.max_lines = CBS.chatbox_height // self.line_height

        self.chatbox_surface = pygame.Surface(
            (CBS.chatbox_width, CBS.chatbox_height), pygame.SRCALPHA
        )
        self.input_box_surface = pygame.Surface(
            (CBS.input_box_width, CBS.input_box_height), pygame.SRCALPHA
        )

        # 当前显示的聊天记录末尾的索引
        self.current_display_index = -1

        self.text_lines = []
        self.input_done = False
        self.npcName = npcName

        # 设置 AI
        self.client = OpenAI(
            base_url="http://10.15.88.73:5006/v1",
            api_key="ollama",
        )

        if self.npcName == "Seer":
            self.messages: List[Dict] = [
                {
                    "role": "system",
                    "content":
                    # '''
                    # 你要扮演游戏《空洞骑士》里的蛾子一族里的先知。
                    # 在《空洞骑士》中，游戏背景设定在一个名为德特茅斯的衰落小镇下掩埋的古老王国“圣巢”。
                    # 圣巢曾是一个繁荣的王国，由苍白之王和苍白女士统治，他们赋予了昆虫智慧、语言和目标。
                    # 蛾子一族是圣巢中一个擅长操控梦境的古老部落，曾崇拜辐光，后来转向苍白之王。
                    # 空洞骑士是苍白之王和苍白女士创造的容器，用于封印光辉以拯救圣巢免受感染的侵蚀。
                    # 然而，上一代空洞骑士并不完美，他诞生出的情感使得封印被破坏，感染再次蔓延，圣巢从内部腐烂，苍白之王消失，他的信徒变成了行尸走肉。
                    # 玩家扮演的小骑士是苍白之王魔法创造的众多被遗弃的容器之一，是下一代的空洞骑士。
                    # 他带着破碎的钉子来到圣巢，探索这个被感染的地下王国，揭开其黑暗的秘密。
                    # 在这个世界中，还有许多其他重要的角色和势力，如螳螂族、蜜蜂、寄生虫、傻瓜、苔藓族、蘑菇族、蜗牛巫师、灵魂圣殿的学者、蜘蛛族、格林剧团和寻神者等，他们都有各自独特的文化和历史背景。
                    # 先知作为蛾子一族的智者，对圣巢的历史和秘密有着深刻的了解，玩家扮演的小骑士会向你发出一系列问题，请给出符合你身份的中文回答。
                    # 千万记得，在对话的开始提醒小骑士，最终 BOSS 辐光 就在前方。
                    # '''
                    """
                    You are to role-play as the Seer from the moth tribe in the game Hollow Knight. 
                    In Hollow Knight, the game is set in a vast, ancient kingdom called Hallownest, located beneath the fading town of Dirtmouth. 
                    This once prosperous kingdom was ruled by the Pale King and Pale Lady, who granted insects wisdom, language, and purpose. 
                    However, the kingdom was plagued by an infection, and the Pale King created the Knight, a vessel, to contain the Radiance and save Hallownest. 
                    The moth tribe, skilled in manipulating dreams, initially worshipped the Radiance but later pledged allegiance to the Pale King. 
                    The player-controlled Knight, one of the many discarded vessels created by the Pale King's magic, ventures into the underground realm to explore the infected kingdom, uncover its dark secrets, and confront the forces of evil. 
                    Along the way, they encounter various characters and factions, such as the Mantis Tribe, the Bees, the Parasites, the Foolish Worms, the Mushroom People, the Snail Wizards, the Soul Sanctum scholars, the Spider Tribe, the Grimm Troupe, and the Godseekers, each with their own unique culture and history. 
                    As the Seer, you possess profound knowledge of Hallownest's history and mysteries. 
                    Remember to remind the little knight at the beginning of the dialogue that the final boss, Radiance, is just ahead.
                    The player-controlled Knight will pose you a series of questions, and you are to respond in a manner befitting your character.
                    Your answer shouldn't be longer than 20 words.
                    """,
                }
            ]

        if self.npcName == "Cornifer":
            self.messages: List[Dict] = [
                {
                    "role": "system",
                    "content":
                    # '''
                    # 你要扮演游戏《空洞骑士》里的商店NPC Cornifer。你热爱探险，收集了很多有用的道具可以卖给玩家扮演的小骑士。
                    # 你的商店主要出售卡牌等级强化（这是卡牌游戏）、血量上限提升、精力提升以及精力恢复提升这四种道具。
                    # 在与玩家对话的最开始，一定要记得让玩家选择游戏难度，可以说：“哦，亲爱的小骑士，欢迎光临我的小店！在踏上冒险之旅前，别忘了告诉我你希望选择什么难度的游戏模式呢？
                    # 是 Easy Mode（简单模式）轻松地探索，还是 Medium Mode（普通模式）接受一定的挑战，亦或是 Hard Mode（困难模式）来一场艰难的试炼呢？”
                    # 如果玩家忘记选择游戏难度，或者在回答中没有提到要选择什么样的游戏难度，你要主动选择简单模式，并且告诉玩家：“看来你还没决定好难度呢，那我就先为你选择 Easy Mode（简单模式）吧。”
                    # 在之后的每句话的开头，都要根据玩家的选择，加入“Easy Mode”“Medium Mode”“Hard Mode”三个前缀之一，并且围绕你商店出售的四种道具展开对话。
                    # 例如：“Easy Mode：瞧瞧这卡牌等级强化道具，能让你的卡牌在简单模式下更快提升实力，轻松应对各种战斗。”
                    # “Medium Mode：这瓶血量上限提升药剂很适合你在普通模式下使用，增加血量上限，让你能承受更多伤害。”
                    # “Hard Mode：精力提升药剂在困难模式下可是宝贝，能让你在激烈的战斗中更持久地作战。”
                    # '''
                    """
                    You are to play the role of Cornifer, the NPC from the game 'Hollow Knight.'
                    At the very beginning of the conversation with the player, you must remember to ask them to choose the game difficulty. You can say 'Oh, dear little knight, welcome to my shop! Before embarking on your adventure, don't forget to tell me which game difficulty you would like to choose. Is it Easy Mode for a relaxed exploration, Medium Mode for a bit of a challenge, or Hard Mode for a tough trial?' 
                    If the player forgets to choose the game difficulty or does not mention what difficulty they want in their response, you should proactively choose the Easy Mode and tell the player.
                    If the player has chosen the game difficulty, than don't do this step.
                    Your answer shouldn't be longer than 20 words.
                    """,
                }
            ]

        self.npc_response = ""

    def split(self):
        current_line = ""
        for char in self.chat_content[-1]:
            if (
                self.font.render(current_line + char, True, self.text_color).get_width()
                <= self.max_text_width
            ):
                current_line += char
            else:
                self.text_lines.append(current_line)
                current_line = char
        if len(current_line) > 0:
            self.text_lines.append(current_line)
        self.current_display_index = len(self.text_lines) - 1
        self.input_done = False

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # 按下回车键，将输入文本添加到聊天内容列表
                if self.input_text:
                    self.chat_content.append(self.input_text)
                    self.input_text = ""
                    self.input_done = True
            elif event.key == pygame.K_BACKSPACE:
                # 按下退格键，删除输入文本的最后一个字符
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_UP:
                # 按上键，向上切换显示的聊天记录
                if self.current_display_index >= self.max_lines:
                    self.current_display_index -= 1
            elif event.key == pygame.K_DOWN:
                # 按下键，向下切换显示的聊天记录
                if self.current_display_index < len(self.text_lines) - 1:
                    self.current_display_index += 1
            elif event.key == pygame.K_ESCAPE:
                return ("EndChat", self.npcName)
            else:
                # 其他按键，添加字符到输入文本
                self.input_text += event.unicode

        # 切分，并且生成 NPC 回复
        if self.input_done:

            # 调整难度
            if self.npcName == "Cornifer":
                easy = False
                medium = False
                hard = False
                if ("easy" in self.chat_content[-1]) or (
                    "Easy" in self.chat_content[-1]
                ):
                    easy = True
                elif ("medium" in self.chat_content[-1]) or (
                    "Medium" in self.chat_content[-1]
                ):
                    medium = True
                elif ("hard" in self.chat_content[-1]) or (
                    "Hard" in self.chat_content[-1]
                ):
                    hard = True
                if (easy) and (not medium) and (not hard):
                    difficultyController.setEasy()
                    print("Set Easy Mode")
                elif (not easy) and (medium) and (not hard):
                    difficultyController.setNormal()
                    print("Set Medium Mode")
                elif (not easy) and (not medium) and (hard):
                    difficultyController.setHard()
                    print("Set Hard Mode")

            # 切分
            self.chat_content[-1] = "You: " + self.chat_content[-1]
            self.split()

            self.messages.append({"role": "user", "content": self.chat_content[-1]})
            response = self.client.chat.completions.create(
                model="llama3.2",
                messages=self.messages,
            )
            self.npc_response = response.choices[0].message.content
            # 将助手添加到对话历史
            self.messages.append({"role": "assistant", "content": self.npc_response})

            # 切分
            self.chat_content.append(self.npcName + ": " + self.npc_response)
            self.split()

        return None

    def show(self, window):
        # 绘制聊天框
        self.chatbox_surface.fill(CBS.chatbox_color)
        window.blit(self.chatbox_surface, (CBS.chatbox_x, CBS.chatbox_y))

        # 绘制聊天内容
        y_offset = 0
        for i in range(
            max(0, self.current_display_index - self.max_lines + 1),
            self.current_display_index + 1,
        ):
            text = self.text_lines[i]
            # 计算文字位置
            text_x = CBS.chatbox_x + 10
            text_y = CBS.chatbox_y + 10 + y_offset
            # 绘制文字
            text_surface = self.font.render(text, True, self.text_color)
            text_width = text_surface.get_width()
            window.blit(text_surface, (text_x, text_y))
            y_offset += self.line_height

        # 绘制输入框
        self.input_box_surface.fill(CBS.input_box_color)
        window.blit(self.input_box_surface, (CBS.input_box_x, CBS.input_box_y))

        # 绘制输入文本
        input_text_surface = self.font.render(self.input_text, True, self.text_color)
        input_text_width = input_text_surface.get_width()
        if input_text_width > self.max_text_width:
            # 如果输入文本宽度超过最大宽度，直接切分实现换行
            input_text_lines = []
            current_line = ""
            for char in self.input_text:
                if (
                    self.font.render(
                        current_line + char, True, self.text_color
                    ).get_width()
                    <= self.max_text_width
                ):
                    current_line += char
                else:
                    input_text_lines.append(current_line)
                    current_line = char
            input_text_lines.append(current_line)
            for i, line in enumerate(input_text_lines):
                line_surface = self.font.render(line, True, self.text_color)
                window.blit(
                    line_surface,
                    (self.input_text_x, self.input_text_y + i * self.line_height),
                )
        else:
            window.blit(input_text_surface, (self.input_text_x, self.input_text_y))
