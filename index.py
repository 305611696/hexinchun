#!/usr/bin/env python2
# -*- encoding=utf-8 -*-


import sys
from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.ListTemplate1 import  ListTemplate1
from nengli.zhinan import Zhinan

reload(sys)
sys.setdefaultencoding('utf8')

class HeXinChun(Bot):

    def __init__(self, request_data):
        super(HeXinChun, self).__init__(request_data)
        self.title = "贺新春"
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('iling.lbxz', self.getTaxSlot)
        self.add_intent_handler('iling.select', self.getTaxSlot)
        self.add_intent_handler('ai.dueros.common.next_intent', self.getTaxSlot)
        self.add_intent_handler('ai.dueros.common.previous_intent', self.getTaxSlot)
        self.add_intent_handler('ai.dueros.common.default_intent', self.getTaxSlot)
        self.add_session_ended_handler(self.ended_request)

    def launch_request(self):
        """
        打开调用名
        """

        self.wait_answer()
        template = BodyTemplate1()
        template.set_title(self.title)
        template.set_plain_text_content('欢迎进入查询个税')
        template.set_background_image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532350870263&di=c93edb2fb9a3cfe7a632acc46cceba62&imgtype=0&src=http%3A%2F%2Ffile25.mafengwo.net%2FM00%2F0A%2FAC%2FwKgB4lMC26CAWsKoAALb5778DWg60.rbook_comment.w1024.jpeg')
        template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254')
        renderTemplate = RenderTemplate(template)
        return {
            'directives': [renderTemplate],
            'outputSpeech': r'欢迎进入查询个税，请告诉我你所在的城市是哪里呢'
        }

    def ended_request(self):
            """
            关闭技能
            """
            return {
                'outputSpeech': r'感谢您的使用'
            }


    def getTaxSlot(self):
        """
        获取槽位及逻辑处理
        """
        num = self.get_slots('sys.number')
        city = self.get_slots('sys.city')
        if num and not city:
            self.nlu.ask('sys.city')
            renderTemplate = self.getTemplate(r'你所在的城市是哪里呢')

            return {
                'directives': [renderTemplate],
                'reprompt': r'你所在的城市是哪里呢',
                'outputSpeech': r'你所在的城市是哪里呢'
            }

        if city and not num:
            self.nlu.ask('sys.number')
            renderTemplate = self.getTemplate(r'你的税前工资是多少呢')

            return {
                'directives': [renderTemplate],
                'reprompt': r'你的税前工资是多少呢',
                'outputSpeech': r'你的税前工资是多少呢'
            }

        taxNum = self.computeType(num, city)
        content = r'你需要缴纳' + str(taxNum)
        renderTemplate = self.getTemplate(content)
        return {
            'directives': [renderTemplate],
            'outputSpeech': content
        }

    def getTemplate(self, title=None, content=""):
        template = BodyTemplate1()
        template.set_title(title if title else self.title)
        template.set_plain_text_content(content)
        template.set_background_image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532350870263&di=c93edb2fb9a3cfe7a632acc46cceba62&imgtype=0&src=http%3A%2F%2Ffile25.mafengwo.net%2FM00%2F0A%2FAC%2FwKgB4lMC26CAWsKoAALb5778DWg60.rbook_comment.w1024.jpeg')
        template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254')
        renderTemplate = RenderTemplate(template)
        return renderTemplate

    def computeType(self, num, city):
        '''
        调用接口计算个税
        '''
        return 100


def handler(event, context):

    bot = HeXinChun(event)
    result = bot.run()
    return result
