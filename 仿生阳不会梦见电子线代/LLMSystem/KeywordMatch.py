import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
#from googletrans import Translator

# 创建一个 Translator 实例
#translator = Translator()

class MatchKeyword:

    def __init__(self):
        self.keyword_list = ['强大', '弱小', '光芒多', '光芒少', '光芒适中', '大费', '小费', '中费', '绿', '蓝', '紫', '金', '激进', '保守', 
                    '稳定', '不稳定', '进攻', '防守', '均衡', '多样化', '近战', '远程', '突刺', '斩击', '打击', '反击', '烧伤', '流血', '迅捷',
                    '忍耐', '易损', '破绽', '强壮', '充能', '麻痹', '守护', '振奋', '妖灵', '虚弱', '束缚', '腐蚀', '烟气', '控制', '伤害', 
                    '混乱', '恢复', '体力', '回混', '治疗','抽取书页','抽取卡牌','回复光芒','正面效果','负面效果','烧','火','回光','抽书',
                    '抽卡','回血','抽取','抗性','防御','烟']
        self.opposite=[['强大','弱小'],['光芒多','光芒少'],['大费','小费'],['激进','保守'],['进攻','防守'],['近战','远程'],['稳定','不稳定']]
        self.negation_words=['不','没','不是','没有','不怎么']
        self.same_type=[['强大','弱小'],['光芒多','光芒少','光芒适中','大费','小费','中费'],['绿','蓝','紫','金'],['激进','保守'],['稳定','不稳定'],
                        ['进攻','防守','均衡'],['近战','远程'],['烧','火','烧伤'],['正面效果','负面效果'],['回光','回复光芒'],['抽书','抽卡','抽取书页','抽取卡牌','抽取'],
                        ['回混','抗性'],['防守','防御'],['烟气','烟']]
        self.model = spacy.load('zh_core_web_md')


    # 函数：获取词的向量表示   
    def get_word_vector(self,word):
        try:
            return self.model(word).vector
        except KeyError:
            return np.zeros(self.model.vector_size)


    def match_keywords(self,user_input,neg):    
        #user_input = translator.translate(user_input, src='auto', dest='zh-cn').text
        
        #print(user_input)
        for text in self.negation_words:
            if user_input==text:
                return {'neg':1}
        for text in self.negation_words:
            if user_input.find(text)!=-1:
                neg=1
                break

        # 获取用户输入的向量
        user_input_vector = self.get_word_vector(user_input)
        
        similarities = {}
        for keyword in self.keyword_list:
            # 获取每个关键词的向量
            keyword_vector = self.get_word_vector(keyword)
            
            # 计算余弦相似度
            similarity = cosine_similarity([user_input_vector], [keyword_vector])[0][0]
            if neg:
                Flag=0
                for pairs in self.opposite:
                    if pairs[0]==keyword:
                        similarities[pairs[1]]=similarity
                        Flag=1
                        break
                    if pairs[1]==keyword:
                        similarities[pairs[0]]=similarity
                        Flag=1
                        break
                if Flag==0:
                    similarities[keyword]=similarity
            else:
                similarities[keyword]=similarity
        return similarities

    def match(self,user_input):
        max_similarity={}
        doc=self.model(user_input)
        for keyword in self.keyword_list:
            max_similarity[keyword]=0
        tmp_similarity={}
        for text in doc:
            neg=0
            if 'neg' in tmp_similarity:
                neg=1
            tmp_similarity=self.match_keywords(text.text,neg)
            if 'neg' in tmp_similarity:
                continue
            for keyword in self.keyword_list:
                max_similarity[keyword]=max(max_similarity[keyword],tmp_similarity[keyword])
        top_keywords=sorted(max_similarity.items(),key=lambda d:d[1],reverse=True)
        cnt=0
        res_keywords=[]
        #print("最匹配的关键词：")
        for keyword, similarity in top_keywords:
            if cnt==3 or similarity<0.45:
                break
            if max_similarity[keyword]!=-1:
                res_keywords.append(keyword)
                #print(f"{keyword} - 相似度: {similarity:.4f}")
                cnt+=1
                for types in self.same_type:
                    if (keyword in types):
                        for kwd in types:
                            if kwd!=keyword:
                                max_similarity[kwd]=-1
        return res_keywords

#ttt=MatchKeyword()
#ttt.match('我需要一张进攻的书页')