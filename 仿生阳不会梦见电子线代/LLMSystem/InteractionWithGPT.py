import random,os
import json
from openai import OpenAI
from LLMSystem.KeywordMatch import MatchKeyword
import numpy as np

class LLMSystem:
    def __init__(self):
        self.SYSTEM_PROMPT_PATH = os.path.join(os.getcwd(),"LLMSystem","TOGPT")
        #self.SYSTEM_PROMPT_PATH='C:/Users/666/Desktop/Program/Games/LibraryOfRuina/ToGPT'
        self.ori_dict={}
        self.spe_dict={'Burn':0.8,'Haste':1.4,'Endurance':1.9,'Fragile':1,'Disarm':2.2,'Strength':2.5,'Paralysis':1.1,'Protection':0.9,'SProtection':1.5,'Bleed':1.2,'Fairy':1.7,'Feeble':1.6,
                'Bind':1.4,'Erosion':1.9,'Smoke':0.8,'Charge':0.3}
        self.pos_buffs=['Strength','Endurance','Haste','Protection','SProtection','Charge']
        self.neg_buffs=['Burn','Bleed','Fairy','Erosion','Feeble','Disarm','Bind','Fragile','Paralysis']
        self.prob_light={'0':16,'1':26,'2':48,'3':31,'4':13,'5':5}
        self.avg_pnt={'0':6.5,'1':9.5,'2':15,'3':21,'4':35,'5':45}
        self.prob_dice={'1':5,'2':9,'3':1,'4':0,'5':0}
        self.prob_sped={'0':0,'1':1,'2':0,'3':0}
        self.prob_pageeff={'有':1,'没有':1}
        self.prob_type={'Melee':90,'Ranged':10}
        self.prob_counter={'True':10,'False':90}
        self.keywords=[]
        self.keywords_list=[]
        self.keyword_trans={'烧伤':'Burn','迅捷':'Haste','忍耐':'Endurance','易损':'Fragile','破绽':'Disarm','强壮':'Strength','麻痹':'Paralysis','守护':'Protection','振奋':'SProtection',
                    '流血':'Bleed','妖灵':'Fairy','虚弱':'Feeble','束缚':'Bind','腐蚀':'Erosion','烟气':'Smoke','充能':'Charge'}
        self.dice_trans={'突刺骰子':'Pierce','斩击骰子':'Slash','打击骰子':'Blunt','闪避骰子':'Evade','格挡骰子':'Block'}
        self.dice_antitrans={'Pierce':'突刺','Slash':'斩击','Blunt':'打击','Evade':'闪避','Block':'格挡'}
        self.buff_keywords=['烧伤','迅捷','忍耐','易损','破绽','强壮','麻痹','守护','振奋','流血','妖灵','虚弱','束缚','腐蚀','烟气','充能']
        self.page={'type':'近战','light':0,'point':9.5,'page_effect':'没有','dice_num':2,'spe_dice':0,'unstable':-1,'counter':"False"}
        self.base_pnt,self.add_pnt,self.tot_pnt,self.unstable_pnt=[],[],0,0
        self.sentences=[]
        self.reply=''
        self.report_cnt=0
        self.final_dict={}
        self.page_pro=0
        self.PROC_MAX=14
        self.name_pool=[]
        self.now_page_cnt=0
        self.mc = MatchKeyword()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys1.txt'),'r',encoding='utf-8') as f1:
            self.togpt1=f1.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys2_0.txt'),'r',encoding='utf-8') as f20:
            self.togpt20=f20.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys2.txt'),'r',encoding='utf-8') as f2:
            self.togpt2=f2.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys3.txt'),'r',encoding='utf-8') as f3:
            self.togpt3=f3.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'ToGPT2.txt'),'r',encoding='utf-8') as f4:
            self.togpt4=f4.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys4.txt'),'r',encoding='utf-8') as f5:
            self.togpt5=f5.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys5.txt'),'r',encoding='utf-8') as f6:
            self.togpt6=f6.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys6.txt'),'r',encoding='utf-8') as f7:
            self.togpt7=f7.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys7.txt'),'r',encoding='utf-8') as f8:
            self.togpt8=f8.read()


    def init_sentences0(self):
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'ToGPT00.txt'),'r',encoding='utf-8') as f00:
            togpt00=f00.read()
        with open(os.path.join(self.SYSTEM_PROMPT_PATH,'ToGPT01.txt'),'r',encoding='utf-8') as f01:
            togpt01=f01.read()
        self.keywords_list=[]
        flag00,word=0,''
        for ch in togpt00:
            if flag00:
                if ch=='，' or ch=='。':
                    self.keywords_list.append(word)
                    word=''
                else:
                    word+=ch
            if ch=='\n':
                flag00=1
        self.sentences=[
            {
                'role': 'user',
                'content': togpt00
            },
            {
                'role': 'user',
                'content': togpt01
            }
        ]

    def init_sentences1(self):
        #with open(os.path.join(self.SYSTEM_PROMPT_PATH,'sys8.txt'),'r',encoding='utf-8') as f9:
            #togpt9=f9.read()
        self.sentences=[
            {
                'role': 'user',
                'content': self.togpt1
            },
            {
                'role': 'user',
                'content': self.togpt20
            },
            {
                'role': 'user',
                'content': self.togpt2
            },
            {
                'role': 'user',
                'content': self.togpt3
            },
            {
                'role': 'user',
                'content': self.togpt4
            },
            {
                'role': 'user',
                'content': self.togpt5
            },
            {
                'role': 'user',
                'content': self.togpt6
            },
            {
                'role': 'user',
                'content': self.togpt7
            },
            {
                'role': 'user',
                'content': self.togpt8
            },
            #{
            #    'role': 'user',
            #    'content': togpt9
            #}
        ]

    def get_name(self,sentence):
        self.sentences=[
            {
                'role': 'user',
                'content': '你需要给这张卡牌起个中文名字，名字长度大约为4字，最多不能超过7个字。\n以下是卡牌信息：\n'
            },
            {
                'role': 'user',
                'content': sentence
            },
            {
                'role': 'user',
                'content': '请注意，你起的名字里只能有中文，不能有英文或其他语言！！！'
            },
            {
                'role': 'user',
                'content': '请注意，请只告诉我这张卡牌的名字，其他任何多余的话都不要说！！！'
            }
        ]
        self.interaction()

    def interaction(self):
        if self.report_cnt>8:
            self.report_cnt=0
            self.init_sentences1()
            self.random_page()
        client = OpenAI(
            base_url='http://10.15.88.73:5008/v1',
            api_key='ollama',
        )
        chat_completion=client.chat.completions.create(
            messages=self.sentences,
            model='llama3.2'
        )
        self.reply=chat_completion.choices[0].message.content

    def cal_pnt(self):
        self.base_pnt,self.add_pnt,dice_cnt,self.tot_pnt=[],[],-1,0
        dice_list=self.ori_dict['list']
        for dice in dice_list:
            dice_cnt+=1
            self.base_pnt.append((dice['maxDice']**2+dice['minDice']**2)/16)
            if self.page['counter']=='True' and dice_cnt+1==len(dice_list):
                self.base_pnt[dice_cnt]*=1.2
            if dice['diceType']=='闪避骰子' or dice['diceType']=='格挡骰子':
                self.base_pnt[dice_cnt]*=0.5
            #if 'desq' in dice:
                #pass
            #else:
                #pass
            desq=dice['desq']
            self.add_pnt.append(0)
            if desq['effect']=='Light':
                self.add_pnt[dice_cnt]=4*desq['count']
            elif desq['effect']=='Page':
                self.add_pnt[dice_cnt]=4*desq['count']
            elif desq['effect']=='ExertBuffs' or desq['effect']=='GetBuffs':
                self.add_pnt[dice_cnt]=self.spe_dict[self.keyword_trans[desq['buffs'][0]]]*desq['counts'][0]
            elif desq['effect']=='Damege':
                self.add_pnt[dice_cnt]=0.3*desq['count']
            elif desq['effect']=='StaggerDamage':
                self.add_pnt[dice_cnt]=0.5*desq['count']
            elif desq['effect']=='Recover':
                self.add_pnt[dice_cnt]=0.25*desq['count']
            elif desq['effect']=='RecoverStagger':
                self.add_pnt[dice_cnt]=0.45*desq['count']
            self.tot_pnt+=self.base_pnt[dice_cnt]+self.add_pnt[dice_cnt]

    def cal_unstable(self):
        self.unstable_pnt,index=0,-1
        dice_list=self.ori_dict['list']
        for dice in dice_list:
            index+=1
            cal_f=(dice['maxDice']-dice['minDice'])/(dice['maxDice']+dice['minDice'])
            cal_g=1.5*self.add_pnt[index]/(self.add_pnt[index]+self.base_pnt[index])
            self.unstable_pnt+=(cal_f+cal_g)*(self.add_pnt[index]+self.base_pnt[index])/self.tot_pnt

    def report(self,sentence): #self.report error to LLM
        if sentence=='你的输出格式有误！请重新生成！':
            self.page_pro+=1
        else:
            self.page_pro+=2
        self.page_pro=min(self.page_pro,self.PROC_MAX-4)
        self.report_cnt+=1
        sentence+='\n如果我没有告诉你格式错误，请不要改变你输出的格式！注意你输出的所有数都应该是正整数！\n'
        #print(self.reply)
        #print(sentence)
        #sentence+='\n请只以文字的形式输出json格式内容，其他多余的解释都不要说。你应当重新阅读我告诉你的json格式内容。你的json格式应完全遵照我先前告诉你的格式。\n'
        self.sentences.append({'role':'assistant', 'content': self.reply})
        self.sentences.append({'role':'user','content': sentence})
        self.interaction()
        from LLMStorage import llmStorage
        llmStorage.modifyGenPageProcess(process=self.page_pro,processMax=self.PROC_MAX,pageCnt=self.now_page_cnt)

    def check(self):
        ''''
        dice_list=ori_dict['list']
        dice_cnt,tot_dice=0,len(dice_list)
        for dice in dice_list:
            dice_cnt+=1
            desq=dice['desq']
            if desq['effect']!='GetBuffs' and desq['effect']!='ExertBuffs' and len(desq['buffList'])!=0:
                self.report(f'第{dice_cnt}个骰子的特殊效果不是施加/获取状态，但你的"buffList"不为空。请重新阅读我告诉你的json格式内容，并重新生成卡牌！')
                return 0
            if desq['effect']=='GetBuffs':
                if len(desq['buffList'])==0:
                    self.report(f'第{dice_cnt}个骰子的特殊效果是使自身获取正面状态，但你给的"buffList"为空。请重新生成卡牌！')
                    return 0
                for buff in desq['buffList']:
                    buff_type=0
                    for buff_keyword in buff_keywords:
                        if buff==buff_keyword:
                            buff_type=1
                            break
                    if buff_type==0:
                        self.report(f'第{dice_cnt}个骰子的的特殊效果有错误！{buff}是我没跟你提到过的状态，不应出现。请重新生成卡牌！')
                        return 0
                    for pos_buff in pos_buffs:
                        if keyword_trans[buff]==pos_buff:
                            buff_type=1
                            break
                    for neg_buff in neg_buffs:
                        if keyword_trans[buff]==neg_buff:
                            buff_type=-1
                            break
                    if buff=='烟气':
                        buff_type=1
                    if buff_type==-1:
                        self.report(f'第{dice_cnt}个骰子的特殊效果有错误！{buff}是负面状态，不应使自身获得负面状态。请重新生成卡牌！')
                        return 0
            elif desq['effect']=='ExertBuffs':
                if len(desq['buffList'])==0:
                    self.report(f'第{dice_cnt}个骰子的特殊效果是对目标施加负面状态，但你给的"buffList"为空。请重新生成卡牌！')
                    return 0
                for buff in desq['buffList']:
                    buff_type=0
                    for buff_keyword in buff_keywords:
                        if buff==buff_keyword:
                            buff_type=1
                            break
                    if buff_type==0:
                        self.report(f'第{dice_cnt}个骰子的的特殊效果有错误！{buff}是我没跟你提到过的状态，不应出现。请重新生成卡牌！')
                        return 0
                    for pos_buff in pos_buffs:
                        if keyword_trans[buff]==pos_buff:
                            buff_type=1
                            break
                    for neg_buff in neg_buffs:
                        if keyword_trans[buff]==neg_buff:
                            buff_type=-1
                            break
                    if buff=='烟气':
                        buff_type=-1
                    if buff_type==1:
                        self.report(f'第{dice_cnt}个骰子的特殊效果有错误！{buff}是正面状态，不应对目标施加正面状态。请重新生成卡牌！')
                        return 0
        '''
        self.cal_pnt()
        self.cal_unstable()
        delta_req=(self.tot_pnt-self.page['point'])/self.page['point']
        if delta_req>0.4:
            self.report('请调小骰子的上下限或调小特殊效果的层数。请重新生成卡牌！')
            return 0
        elif delta_req>0.2:
            self.report('请略微调小骰子的上下限或略微调小特殊效果的层数。请重新生成卡牌！')
            return 0
        elif delta_req<-0.4:
            self.report('请调大骰子的上下限或调大特殊效果的层数。请重新生成卡牌！')
            return 0
        elif delta_req<-0.2:
            self.report('请略微调大骰子的上下限或略微调大特殊效果的层数。请重新生成卡牌！')
            return 0
        #if self.page['unstable']==1 and self.unstable_pnt<0.5:
        #    self.report('我要求你生成不稳定的卡牌，但是你生成的卡牌太稳定了。请重新生成卡牌！')
        #    return 0
        #if self.page['unstable']==-1 and self.unstable_pnt>0.6:
        #    self.report('我要求你生成稳定的卡牌，但是你生成的卡牌太不稳定了。请重新生成卡牌！')
        #    return 0
        return 1

    def get_random(self,dic):
        sum=0
        for value in dic.values():
            sum+=value
        rand=(np.random.randint(0,sum-1)+np.random.randint(0,sum-1)+np.random.randint(0,sum-1))%sum+1
        for key in dic:
            if rand<=dic[key]:
                return key
            rand-=dic[key]

    def random_page(self):
        requests=[]
        val_light,val_pnt,val_unstable,val_dice=0,0,0,0
        self.prob_type['近战'],self.prob_type['远程']=90,10
        self.prob_counter['True'],self.prob_counter['False']=10,90
        for keyword in self.keywords:
            if keyword=='强大':
                val_pnt+=5
            elif keyword=='弱小':
                val_pnt-=5
            elif keyword=='光芒多' or keyword=='大费':
                val_light+=3
            elif keyword=='光芒少' or keyword=='小费':
                val_light-=3
            elif keyword=='光芒适中' or keyword=='中费':
                val_light=100
            elif keyword=='绿':
                val_light-=2
                val_pnt-=5
            elif keyword=='蓝':
                val_light+=1
            elif keyword=='金':
                val_light+=2
                val_pnt+=5
            elif keyword=='紫':
                val_light+=1
                val_pnt+=2
            elif keyword=='激进':
                val_unstable+=1
            elif keyword=='保守':
                val_unstable-=1
            elif keyword=='稳定':
                val_unstable-=1
            elif keyword=='不稳定':
                val_unstable+=1
            elif keyword=='骰子多':
                val_dice+=1
            elif keyword=='骰子少':
                val_dice-=1
            elif keyword=='抽取书页' or keyword=='抽取卡牌' or keyword=='抽书' or keyword=='抽卡' or keyword=='抽取':
                requests.append('卡牌中尽可能包含能抽取书页的骰子')
            elif keyword=='回复光芒' or keyword=='回光':
                requests.append('卡牌中尽可能包含能回复光芒的骰子')
            elif keyword=='进攻':
                requests.append('卡牌中的骰子类型尽可能设为进攻型骰子')
            elif keyword=='防守' or keyword=='防御':
                requests.append('卡牌中的骰子类型尽可能设为防御型骰子')
            elif keyword=='均衡' or keyword=='多样化':
                requests.append('卡牌中的骰子类型尽可能多样化')
            elif keyword=='近战':
                self.prob_type['Ranged']-=8
            elif keyword=='远程':
                self.prob_type['Melee']-=86
            elif keyword=='突刺':
                requests.append('卡牌中尽可能包含突刺骰子')
            elif keyword=='斩击':
                requests.append('卡牌中尽可能包含斩击骰子')
            elif keyword=='打击':
                requests.append('卡牌中尽可能包含打击骰子')
            elif keyword=='反击':
                self.prob_counter['True']=900
            elif keyword=='控制':
                requests.append('卡牌中尽可能包含关于束缚的特殊效果或可以蓝伤')
            elif keyword=='伤害':
                requests.append('卡牌中尽可能包含能追加红伤的骰子')
            elif keyword=='混乱':
                requests.append('卡牌中尽可能包含能追加混乱伤害的骰子')
            elif keyword=='恢复' or keyword=='治疗':
                requests.append('卡牌中尽可能包含能恢复红血或恢复蓝血的骰子')
            elif keyword=='体力' or keyword=='回血':
                requests.append('卡牌中尽可能包含能恢复红血的骰子')
            elif keyword=='回混' or keyword=='抗性':
                requests.append('卡牌中尽可能包含能恢复蓝血的骰子')
            elif keyword=='正面效果':
                ran=(np.random.randint(0,5)+np.random.randint(0,5)+np.random.randint(0,5))%6
                for kwd in self.keyword_trans:
                    if self.pos_buffs[ran]==self.keyword_trans[kwd]:
                        requests.append(f'卡牌中尽可能包含特殊能力是施加{kwd}的骰子')
                        break
            elif keyword=='负面效果':
                ran=(np.random.randint(0,8)+np.random.randint(0,8)+np.random.randint(0,8))%9
                for kwd in self.keyword_trans:
                    if self.neg_buffs[ran]==self.keyword_trans[kwd]:
                        requests.append(f'卡牌中尽可能包含特殊能力是施加{kwd}的骰子')
                        break
            elif keyword=='烧' or keyword=='烧伤' or keyword=='火':
                requests.append(f'卡牌中尽可能包含特殊能力是施加烧伤的骰子')
            elif keyword=='烟' or keyword=='烟气':
                requests.append(f'卡牌中尽可能包含特殊能力是施加烟气的骰子')
            else:
                for buff_keyword in self.buff_keywords:
                    if keyword==buff_keyword:
                        requests.append(f'卡牌中尽可能包含特殊能力是施加{keyword}的骰子')
                        break
        self.prob_light['0'],self.prob_light['1'],self.prob_light['2'],self.prob_light['3'],self.prob_light['4'],self.prob_light['5']=16,26,48,31,13,5
        if val_light>50:
            self.prob_light['0'],self.prob_light['1'],self.prob_light['2'],self.prob_light['3'],self.prob_light['4'],self.prob_light['5']=5,10,50,50,5,1
        elif val_light>3:
            self.prob_light['0'],self.prob_light['1'],self.prob_light['2'],self.prob_light['3'],self.prob_light['4'],self.prob_light['5']=1,6,25,60,40,15
        elif val_light<-1:
            self.prob_light['0'],self.prob_light['1'],self.prob_light['2'],self.prob_light['3'],self.prob_light['4'],self.prob_light['5']=75,50,12,5,2,1
        elif val_light==-1:
            self.prob_light['0'],self.prob_light['1'],self.prob_light['2'],self.prob_light['3'],self.prob_light['4'],self.prob_light['5']=50,50,30,20,5,1
        elif val_light>0:
            self.prob_light['0'],self.prob_light['1'],self.prob_light['2'],self.prob_light['3'],self.prob_light['4'],self.prob_light['5']=1,5,15,40,50,25
        self.page['light']=int(self.get_random(self.prob_light))
        rand1,rand2=np.random.randint(8500,11500)/10000,np.random.randint(170,230)/10000
        self.page['point']=self.avg_pnt[str(self.page['light'])]*(rand1+val_pnt*rand2)
        self.page['type']=self.get_random(self.prob_type)
        if self.page['light']==0:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=5,9,1,0,0
        elif self.page['light']==1:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=3,19,4,0,0
        elif self.page['light']==2:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=2,22,23,1,0
        elif self.page['light']==3:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=6,5,17,3,0
        elif self.page['light']==4:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=5,5,2,1,0
        elif self.page['light']==5:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=1,2,1,1,0
        if val_dice>0:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=1,10,30,25,10
        elif val_dice<0:
            self.prob_dice['1'],self.prob_dice['2'],self.prob_dice['3'],self.prob_dice['4'],self.prob_dice['5']=50,40,15,1,0
        self.page['dice_num']=int(self.get_random(self.prob_dice))
        if self.page['dice_num']==1:
            self.prob_sped['0']=5;self.prob_sped['1']=40;self.prob_sped['2']=0;self.prob_sped['3']=0
        elif self.page['dice_num']==2:
            self.prob_sped['0']=5;self.prob_sped['1']=30;self.prob_sped['2']=20;self.prob_sped['3']=0
        elif self.page['dice_num']==3:
            self.prob_sped['0']=5;self.prob_sped['1']=20;self.prob_sped['2']=30;self.prob_sped['3']=5
        elif self.page['dice_num']==4:
            self.prob_sped['0']=5;self.prob_sped['1']=15;self.prob_sped['2']=40;self.prob_sped['3']=3
        elif self.page['dice_num']==5:
            self.prob_sped['0']=2;self.prob_sped['1']=10;self.prob_sped['2']=25;self.prob_sped['3']=45
        self.page['spe_dice']=int(self.get_random(self.prob_sped))

        self.page['page_effect']=self.get_random(self.prob_pageeff)
        if self.page['light']==0 or self.page['dice_num']==1:
            self.prob_counter['True']=0
        self.page['counter']=self.get_random(self.prob_counter)
        if val_unstable>0:
            self.page['unstable']=1
            requests.append('卡牌的稳定性要低（也就是说，骰子上限与下限的差值要比较大，或者骰子的特殊能力比较强）')
        elif val_unstable<0:
            self.page['unstable']=-1
            requests.append('卡牌的稳定性要强（也就是说，骰子上限与下限的差值要比较小，或者骰子的特殊能力比较弱）')
        else:
            self.page['unstable']=0
        sentence='请给我生成一张满足下列要求的卡牌：\n'
        requests.append(f'有{self.page["dice_num"]}个骰子')
        requests.append(f'卡牌的{self.page["dice_num"]}个骰子中，有{self.page["dice_num"]-self.page["spe_dice"]}个骰子的特殊效果是“移动1步”')
        cnt_req,tot_req=0,len(requests)
        for request in requests:
            cnt_req+=1
            sentence+=str(cnt_req)+'.'+request
            if cnt_req==tot_req:
                sentence+='。\n'
            else:
                sentence+='；\n'
        #sentence+='请只以文字的形式输出json格式内容，其他多余的解释都不要说。你应当重新阅读我告诉你的json格式内容。你的json格式应完全遵照我先前告诉你的格式。\n'
        self.sentences.append({'role': 'user', 'content': sentence})

    def check_name(self,card_name):
        while card_name[:7] in self.name_pool:
            name_ch=[]
            for ch in card_name:
                name_ch.append(ch)
            random.shuffle(name_ch)
            card_name=''
            for ch in name_ch:
                card_name+=ch
        card_name=card_name[:7]
        self.name_pool.append(card_name)
        return card_name

    def print_dict(self,num):
        from LLMStorage import llmStorage
        llmStorage.modifyGenPageProcess(process=self.PROC_MAX-3,processMax=self.PROC_MAX,pageCnt=self.now_page_cnt)
        self.ori_dict['cardName']='TBD'
        if self.page['counter']=='False':
            random.shuffle(self.ori_dict['list'])
        delta=(self.tot_pnt-self.avg_pnt[str(self.page['light'])])/self.avg_pnt[str(self.page['light'])]
        if self.unstable_pnt>0.9:
            self.ori_dict['cardQuality']='purple'
        elif delta<-0.02:
            self.ori_dict['cardQuality']='green'
        elif delta<0.12:
            self.ori_dict['cardQuality']='blue'
        else:
            self.ori_dict['cardQuality']='gold'
        self.ori_dict['mana']=self.page['light']
        dice_cnt=0
        for dice in self.ori_dict['list']:
            dice_cnt+=1
            if dice['minDice']==dice['maxDice']:
                dice['maxDice']+=1
            elif dice['minDice']>dice['maxDice']:
                dice['minDice'],dice['maxDice']=dice['maxDice'],dice['minDice']
            if self.page['counter']=='True' and dice_cnt==len(self.ori_dict['list']) and dice['maxDice']+dice['minDice']>20:
                self.page['counter']='False'
            if self.page['counter']=='True' and dice_cnt==len(self.ori_dict['list']):
                dice['isCounter']=True
                dice['desq']['effect']='None'
                dice['desq']['condition']='None'
                dice['desq']['count']=0
                dice['desq']['buffs']=[]
                dice['desq']['counts']=[]
                dice['maxDice']=min(10,dice['maxDice'])
                dice['minDice']=min(8,dice['minDice'])
            else:
                dice['isCounter']=False
            dice['diceType']=self.dice_trans[dice['diceType']]
            if dice['desq']['effect']=='None':
                dice['desq']['condition']='None'
            else:
                prob_condition={'Hit':50,'Win':50}
                if dice['diceType']=='Block' or dice['diceType']=='Evade':
                    prob_condition['Hit']=0
                if dice['desq']['effect']=='Damege' or dice['desq']['effect']=='StaggerDamage' or dice['desq']['effect']=='Recover' or dice['desq']['effect']=='RecoverStagger':
                    prob_condition['Win']=0
                if prob_condition['Hit']==0 and prob_condition['Win']==0:
                    prob_condition['Hit']=50
                    prob_newtype={'Blunt':30,'Slash':30,'Pierce':30}
                    dice['diceType']=self.get_random(prob_newtype)
                dice['desq']['condition']=self.get_random(prob_condition)
                if (dice['desq']['effect']=='Damage' or dice['desq']['effect']=='StaggerDamage') and dice['diceType']=='Evade':
                    dice['diceType']='Block'
            index=0
            for buff in dice['desq']['buffs']:
                dice['desq']['buffs'][index]=self.keyword_trans[buff]
                index+=1
            dice['desq']['isNext']=True
            if len(dice['desq']['buffs'])>0:
                if dice['desq']['buffs'][0]=='Burn' or dice['desq']['buffs'][0]=='Fairy' or dice['desq']['buffs'][0]=='Charge' or dice['desq']['buffs'][0]=='Erosion':
                    dice['desq']['isNext']=False
        self.ori_dict['pageDesq']={}
        self.ori_dict['pageDesq']['list']=self.ori_dict['list']
        self.ori_dict['pageDesq']['overall_desq']={}
        self.ori_dict['pageDesq']['overall_desq']['condition']='None'
        self.ori_dict['pageDesq']['overall_desq']['effect']='None'
        self.ori_dict['pageDesq']['overall_desq']['count']=0
        self.ori_dict['pageDesq']['overall_desq']['buffs']=[]
        self.ori_dict['pageDesq']['overall_desq']['counts']=[]
        self.ori_dict['pageDesq']['overall_desq']['isNext']=True
        del self.ori_dict['list']
        llmStorage.modifyGenPageProcess(process=self.PROC_MAX-2,processMax=self.PROC_MAX,pageCnt=self.now_page_cnt)
        #print(self.translate_to_chinese())
        self.get_name(self.translate_to_chinese())
        #print(self.reply)
        self.ori_dict['cardName']=self.check_name(self.reply)
        llmStorage.modifyGenPageProcess(process=self.PROC_MAX-1,processMax=self.PROC_MAX,pageCnt=self.now_page_cnt)
        prob_pageeff={'Yes':50,'No':50}
        if_pageeff=self.get_random(prob_pageeff)
        if if_pageeff=='Yes':
            dice_list=self.ori_dict['pageDesq']['list']
            for dice in dice_list:
                if dice['isCounter']:
                    continue
                if dice['desq']['effect']=='ExertBuffs' or dice['desq']['effect']=='GetBuffs':
                    self.ori_dict['pageDesq']['overall_desq']['condition']='Use'
                    self.ori_dict['pageDesq']['overall_desq']['effect']=dice['desq']['effect']
                    self.ori_dict['pageDesq']['overall_desq']['count']=0
                    self.ori_dict['pageDesq']['overall_desq']['buffs']=dice['desq']['buffs']
                    self.ori_dict['pageDesq']['overall_desq']['counts']=dice['desq']['counts']
                    self.ori_dict['pageDesq']['overall_desq']['isNext']=dice['desq']['isNext']
                    dice['desq']['condition']='None'
                    dice['desq']['effect']='None'
                    dice['desq']['count']=0
                    dice['desq']['buffs']=[]
                    dice['desq']['counts']=[]
                    break
                if dice['desq']['effect']=='Page' or dice['desq']['effect']=='Light':
                    self.ori_dict['pageDesq']['overall_desq']['condition']='Use'
                    self.ori_dict['pageDesq']['overall_desq']['effect']=dice['desq']['effect']
                    self.ori_dict['pageDesq']['overall_desq']['count']=dice['desq']['count']
                    self.ori_dict['pageDesq']['overall_desq']['buffs']=[]
                    self.ori_dict['pageDesq']['overall_desq']['counts']=[]
                    self.ori_dict['pageDesq']['overall_desq']['isNext']=False
                    dice['desq']['condition']='None'
                    dice['desq']['effect']='None'
                    dice['desq']['count']=0
                    dice['desq']['buffs']=[]
                    dice['desq']['counts']=[]
                    break
        #print(ori_dict)
        #print(tot_pnt)
        if num<10:
            nom='P000'+str(num)
        else:
            nom='P00'+str(num)
        self.final_dict[nom]=self.ori_dict

    def translate_to_chinese(self):
        page_des='卡牌类型：'
        if self.ori_dict['cardQuality']=='green':
            page_des+='绿卡（强度较弱的卡）'
        elif self.ori_dict['cardQuality']=='purple':
            page_des+='紫卡（比较特殊，不太稳定的卡）'
        elif self.ori_dict['cardQuality']=='gold':
            page_des+='金卡（强大的卡）'
        else:
            page_des+='蓝卡（强度较为均衡的卡）'
        dice_list=self.ori_dict['pageDesq']['list']
        page_des+='\n行动个数：'+str(len(dice_list))+'\n'
        index=0
        for dice in dice_list:
            index+=1
            page_des+=f'第{index}个行动:'
            if dice['isCounter']:
                page_des+='反击'
            page_des+=self.dice_antitrans[dice['diceType']]
            if dice['desq']['effect']=='Page':
                page_des+='，并抽取'+str(dice['desq']['count'])+'张书页'
            elif dice['desq']['effect']=='Light':
                page_des+='，并回复'+str(dice['desq']['count'])+'点光芒'
            elif dice['desq']['effect']=='Damege':
                page_des+='，并造成'+str(dice['desq']['count'])+'点伤害'
            elif dice['desq']['effect']=='StaggerDamege':
                page_des+='，并造成'+str(dice['desq']['count'])+'点混乱伤害'
            elif dice['desq']['effect']=='Recover':
                page_des+='，并回复'+str(dice['desq']['count'])+'点体力'
            elif dice['desq']['effect']=='RecoverStagger':
                page_des+='，并回复'+str(dice['desq']['count'])+'点混乱抗性'
            elif dice['desq']['effect']=='ExertBuffs':
                page_des+='，并对对方施加'+str(dice['desq']['counts'][0])+'层'
                exbuff='烧伤'
                for keyword in self.keyword_trans:
                    if self.keyword_trans[keyword]==dice['desq']['buffs'][0]:
                        exbuff=keyword
                        break
                page_des+=exbuff
            elif dice['desq']['effect']=='GetBuffs':
                page_des+='，并使自己获得'+str(dice['desq']['counts'][0])+'层'
                getbuff='守护'
                for keyword in self.keyword_trans:
                    if self.keyword_trans[keyword]==dice['desq']['buffs'][0]:
                        getbuff=keyword
                        break
                page_des+=getbuff
            page_des+='\n'
        return page_des

    def translate_to_json(self):
        self.ori_dict={'list':[]}
        lines=self.reply.splitlines()
        dice_cnt,line_cnt=-1,0
        for line in lines:
            if True:
                #print(line,line_cnt)
                if line.find('第')!=-1:
                    if line_cnt!=0:
                        self.report('你的输出格式有误！请重新生成！')
                        return 0
                    line_cnt=1
                    dice_cnt+=1
                    self.ori_dict['list'].append({})
                elif line.find('类型')!=-1:
                    if line_cnt!=1:
                        self.report('你的输出格式有误！请重新生成！')
                        return 0
                    line_cnt=2
                    if line.find('突刺')!=-1:
                        self.ori_dict['list'][dice_cnt]['diceType']='突刺骰子'
                    elif line.find('斩击')!=-1:
                        self.ori_dict['list'][dice_cnt]['diceType']='斩击骰子'
                    elif line.find('打击')!=-1:
                        self.ori_dict['list'][dice_cnt]['diceType']='打击骰子'
                    elif line.find('格挡')!=-1:
                        self.ori_dict['list'][dice_cnt]['diceType']='格挡骰子'
                    elif line.find('闪避')!=-1:
                        self.ori_dict['list'][dice_cnt]['diceType']='闪避骰子'
                    else:
                        self.report(f'第{dice_cnt+1}个骰子类型错误。骰子类型应该是“突刺骰子”，“斩击骰子”，“打击骰子”，“格挡骰子”，“闪避骰子”五种中的一种。请重新生成！')
                        return 0
                elif line.find('上限')!=-1:
                    if line_cnt!=2:
                        self.report('你的输出格式有误！请重新生成！')
                        return 0
                    line_cnt=3
                    num=''
                    for ch in line:
                        if ch>='0' and ch<='9':
                            num+=ch
                        else:
                            if num!='':
                                break
                    if num=='':
                        self.report(f'你没有告诉我第{dice_cnt+1}个骰子的上限。请重新生成！')
                        return 0
                    self.ori_dict['list'][dice_cnt]['maxDice']=int(num)
                elif line.find('下限')!=-1:
                    if line_cnt!=3:
                        self.report('你的输出格式有误！请重新生成！')
                        return 0
                    line_cnt=4
                    num=''
                    for ch in line:
                        if ch>='0' and ch<='9':
                            num+=ch
                        else:
                            if num!='':
                                break
                    if num=='':
                        self.report(f'你没有告诉我第{dice_cnt+1}个骰子的下限。请重新生成！')
                        return 0
                    self.ori_dict['list'][dice_cnt]['minDice']=max(1,int(num))
                elif line.find('特殊')!=-1:
                    if line_cnt!=4:
                        self.report('你的输出格式有误！请重新生成！')
                        return 0
                    line_cnt=0
                    self.ori_dict['list'][dice_cnt]['desq']={}
                    if line.find('移动')!=-1:
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='None'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=0
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    elif line.find('抽取')!=-1 or line.find('书页')!=-1:
                        Flag,num=0,''
                        for ch in line:
                            if Flag:
                                if ch>='0' and ch<='9':
                                    num+=ch
                                elif len(num)>0:
                                    break
                            if ch=='：':
                                Flag=1
                        if num=='':
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我抽取书页的数量！请重新生成！')
                            return 0
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='Page'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=max(1,int(num))
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    elif line.find('光芒')!=-1:
                        Flag,num=0,''
                        for ch in line:
                            if Flag:
                                if ch>='0' and ch<='9':
                                    num+=ch
                                elif len(num)>0:
                                    break
                            if ch=='：':
                                Flag=1
                        if num=='':
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我回复光芒的数量！请重新生成！')
                            return 0
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='Light'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=max(1,int(num))
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    elif line.find('红伤')!=-1:
                        Flag,num=0,''
                        for ch in line:
                            if Flag:
                                if ch>='0' and ch<='9':
                                    num+=ch
                                elif len(num)>0:
                                    break
                            if ch=='：':
                                Flag=1
                        if num=='':
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我造成红伤的伤害值！请重新生成！')
                            return 0
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='Damage'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=max(1,int(num))
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    elif line.find('蓝伤')!=-1:
                        Flag,num=0,''
                        for ch in line:
                            if Flag:
                                if ch>='0' and ch<='9':
                                    num+=ch
                                elif len(num)>0:
                                    break
                            if ch=='：':
                                Flag=1
                        if num=='':
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我造成蓝伤的伤害值！请重新生成！')
                            return 0
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='StaggerDamage'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=max(1,int(num))
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    elif line.find('红血')!=-1:
                        Flag,num=0,''
                        for ch in line:
                            if Flag:
                                if ch>='0' and ch<='9':
                                    num+=ch
                                elif len(num)>0:
                                    break
                            if ch=='：':
                                Flag=1
                        if num=='':
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我回复红血的回复值！请重新生成！')
                            return 0
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='Recover'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=max(1,int(num))
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    elif line.find('蓝血')!=-1:
                        Flag,num=0,''
                        for ch in line:
                            if Flag:
                                if ch>='0' and ch<='9':
                                    num+=ch
                                elif len(num)>0:
                                    break
                            if ch=='：':
                                Flag=1
                        if num=='':
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我回复蓝血的回复值！请重新生成！')
                            return 0
                        self.ori_dict['list'][dice_cnt]['desq']['effect']='RecoverStagger'
                        self.ori_dict['list'][dice_cnt]['desq']['count']=max(1,int(num))
                        self.ori_dict['list'][dice_cnt]['desq']['buffs']=[]
                        self.ori_dict['list'][dice_cnt]['desq']['counts']=[]
                    else:
                        FFlag=0
                        for buff_keyword in self.buff_keywords:
                            if line.find(buff_keyword)!=-1:
                                Flag,num=0,''
                                for ch in line:
                                    if Flag:
                                        if ch>='0' and ch<='9':
                                            num+=ch
                                        elif len(num)>0:
                                            break
                                    if ch=='：':
                                        Flag=1
                                if num=='':
                                    self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你没有告诉我状态的施加层数！请重新生成！')
                                    return 0
                                is_neg=1
                                for pos_buff in self.pos_buffs:
                                    if pos_buff==self.keyword_trans[buff_keyword]:
                                        is_neg=0
                                if buff_keyword=='烟气':
                                    rand=np.random.rand()
                                    if rand>0.5:
                                        is_neg=0
                                if is_neg:
                                    self.ori_dict['list'][dice_cnt]['desq']['effect']='ExertBuffs'
                                else:
                                    self.ori_dict['list'][dice_cnt]['desq']['effect']='GetBuffs'
                                if num=='':
                                    self.report('你生成的书页格式有误！请重新生成！')
                                    return 0
                                self.ori_dict['list'][dice_cnt]['desq']['count']=0
                                self.ori_dict['list'][dice_cnt]['desq']['buffs']=[buff_keyword]
                                self.ori_dict['list'][dice_cnt]['desq']['counts']=[max(1,int(num))]
                                FFlag=1
                                break
                        if FFlag==0:
                            self.report(f'第{dice_cnt+1}个骰子的特殊能力有误！你生成的特殊能力不是我告诉你的8种特殊能力中的一种。请重新生成！')
                            return 0
        if line_cnt!=0 or dice_cnt==-1:
            self.report('你生成的书页格式有误！请重新生成！')
            return 0
        return 1

    def create_page(self):
        from LLMStorage import llmStorage
        ttj=self.translate_to_json()
        if llmStorage.GENPAGE_SHUTDOWN:
            return 0
        while ttj==0:
            ttj=self.translate_to_json()
            if llmStorage.GENPAGE_SHUTDOWN:
                return 0
        while self.check()==0:
            ttj=self.translate_to_json()
            if llmStorage.GENPAGE_SHUTDOWN:
                return 0
            while ttj==0:
                ttj=self.translate_to_json()
                if llmStorage.GENPAGE_SHUTDOWN:
                    return 0
        return 1

    def create_page1(self,num):
        from LLMStorage import llmStorage
        self.report_cnt=0
        self.init_sentences1()
        self.random_page()
        self.interaction()
        if llmStorage.GENPAGE_SHUTDOWN:
            return 0
        CP=self.create_page()
        if llmStorage.GENPAGE_SHUTDOWN:
            return 0
        while CP==0:
            CP=self.create_page()
            if llmStorage.GENPAGE_SHUTDOWN:
                return 0
        self.print_dict(num)
        
    def create_page0(self,user_input,num):
        from LLMStorage import llmStorage
        from GameDataManager import gameDataManager
        if len(self.name_pool)==0:
            for page_name in gameDataManager.PAGE_POOL:
                self.name_pool.append(page_name)
        llmStorage.modifyGenPageProcess(process=0,processMax=self.PROC_MAX,pageCnt=1)
        self.keywords=self.mc.match(user_input)
        self.page_pro=2
        self.now_page_cnt=0
        llmStorage.modifyGenPageProcess(process=self.page_pro,processMax=self.PROC_MAX,pageCnt=1)
        for index in range(num):
            self.now_page_cnt+=1
            self.create_page1(index+1)
            if llmStorage.GENPAGE_SHUTDOWN:
                gen_path=os.path.join(os.getcwd(),'Assets','Gdata','Card','Gen','DYNAMICGENPAGE.json')
                with open (gen_path,'w',encoding='utf-8') as f_final:
                    json.dump(self.final_dict,f_final,ensure_ascii=False,indent=4)
                llmStorage.modifyGenPageProcess(process=0,processMax=self.PROC_MAX,pageCnt=-1)
                return 0
            llmStorage.modifyGenPageProcess(process=self.PROC_MAX,processMax=self.PROC_MAX,pageCnt=index+1)
            self.page_pro=0
            #print(index+1)
        llmStorage.modifyGenPageProcess(process=0,processMax=self.PROC_MAX,pageCnt=num+1)
        gen_path=os.path.join(os.getcwd(),'Assets','Gdata','Card','Gen','DYNAMICGENPAGE.json')
        with open (gen_path,'w',encoding='utf-8') as f_final:
            json.dump(self.final_dict,f_final,ensure_ascii=False,indent=4)

#tst=LLMSystem()
#tst.reply='骰子数量：3\n第1个骰子：\n骰子类型：闪避骰子\n骰子上限：8\n骰子下限：4\n特殊能力：移动1步\n第2个骰子：\n骰子类型：打击骰子\n骰子上限：13\n骰子下限：6\n特殊能力：对目标施加3层烧伤\n第3个骰子：\n骰子类型：突刺骰子\n骰子上限：5\n骰子下限：2\n特殊能力：抽取1张书页'
#tst.translate_to_json()
#print(tst.ori_dict)
#tst.create_page0('',5)