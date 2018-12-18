#!/usr/bin/env python2
# -*- encoding=utf-8 -*-


import sys
import math
import random
from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem
from nengli.Zhinan import Zhinan
from nengli.Zhishi import Zhishi
from nengli.Caipu import Caipu

reload(sys)
sys.setdefaultencoding('utf8')

class HeXinChun(Bot):

    def __init__(self, request_data):
        super(HeXinChun, self).__init__(request_data)
        self.title = "贺新春"
        self.list = [{"name": "小知识", "image": "image"}, {"name": "小菜谱", "image": "image"}]
        self.current_item = self.get_session_attribute("current_item", -1)
        self.zhishi = Zhishi()
        self.caipu = Caipu()
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('iling.backlist', self.get_to_list)
        self.add_intent_handler('iling.lbxz', self.get_select_item)
        self.add_intent_handler('ai.dueros.common.next_intent', self.get_next)
        self.add_intent_handler('ai.dueros.common.previous_intent', self.get_previous)
        self.add_intent_handler('ai.dueros.common.default_intent', self.get_default)
        self.add_session_ended_handler(self.ended_request)

    def launch_request(self):
        """
        打开调用名
        """
        self.wait_answer()

        self.current_item = -1
        self.set_session_attribute("current_item", -1, -1)
        # template = BodyTemplate1()
        # template.set_title(self.title)
        # template.set_plain_text_content('欢迎进入'+self.title)
        # template.set_background_image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532350870263&di=c93edb2fb9a3cfe7a632acc46cceba62&imgtype=0&src=http%3A%2F%2Ffile25.mafengwo.net%2FM00%2F0A%2FAC%2FwKgB4lMC26CAWsKoAALb5778DWg60.rbook_comment.w1024.jpeg')
        # template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254')
        # renderTemplate = RenderTemplate(template)
        # return {
        #     'directives': [renderTemplate],
        #     'outputSpeech': r'欢迎进入，'+self.title+'请告诉我你所在的城市是哪里呢'
        # }

        list_template = self.get_list()
        render_template = RenderTemplate(list_template)
        return {
            'directives': [render_template],
            'outputSpeech': r'请选择要了解的内容，可以对我说第几个'
        }

    def get_to_list(self):
        """
        返回列表
        """
        self.wait_answer()
        self.current_item = -1
        self.set_session_attribute("current_item", -1, -1)
        list_template = self.get_list()
        render_template = RenderTemplate(list_template)
        return {
            'directives': [render_template],
            'outputSpeech': r'请选择要了解的内容，可以对我说第几个'
        }

    def ended_request(self):
            """
            关闭技能
            """
            return {
                'outputSpeech': r'感谢您的使用'
            }


    def get_list(self):
        """
        获取能力列表
        :return:
        """
        list_template = ListTemplate1()
        list_template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254')
        list_template.set_background_image(
            'https://skillstore.cdn.bcebos.com/icon/100/c709eed1-c07a-be4a-b242-0b0d8b777041.jpg')
        list_template.set_title(self.title)

        for i in range(0, len(self.list)):
            item = ListTemplateItem()
            item.set_token(i)
            item.set_plain_primary_text(self.list[i]["name"])
            item.set_plain_secondary_text(self.title + self.list[i]["name"])
            item.set_image("image")
            list_template.add_item(item)

        return list_template

    def get_select_item(self):
        """
        选择指定能力通过编号
        """

        self.wait_answer()
        # 直接选择某一个Item
        num = self.get_slots('num')
        item = self.get_slots('list')

        if num:

            num = int(num)
            if self.current_item == -1:
                self.current_item = num
                self.set_session_attribute("current_item", num, -1)
                if num == 1:
                    return self.get_zhishi()
                elif num == 2:
                    caipu_data = self.zhishi.get_datas()[math.floor(random.random() * len(self.zhishi.get_datas()))]
                    render_template = self.get_template(caipu_data)
                    return {
                        'directives': [render_template],
                        'outputSpeech': caipu_data
                    }
            elif self.current_item == 1:
                return self.get_zhishi('=', num)
        else:

            if item == "小知识":
                self.set_session_attribute("current_item", 1, -1)
                return self.get_zhishi()
            elif item == "小菜谱":
                self.set_session_attribute("current_item", 2, -1)
                content = item
                render_template = self.get_template(content)
                return {
                    'directives': [render_template],
                    'outputSpeech': content
                }
            else:
                render_template = self.get_template(r'请问你选择的是第几个呢？')
                self.nlu.ask('num')
                return {
                    'directives': [render_template],
                    'reprompt': r'你选择第几个呢',
                    'outputSpeech': r'请问你选择的是第几个呢？'
                }

    def get_next(self):
        self.wait_answer()
        if self.current_item == 1:
            return self.get_zhishi('+')
        else:
            pass

    def get_previous(self):
        self.wait_answer()
        if self.current_item == 1:
            return self.get_zhishi('-')
        else:
            pass

    def get_default(self):

        pass

    def get_zhishi(self, tag='random', num=0):
        index = self.get_session_attribute("zhishi_data", 0)
        if tag == '+':
            index += 1
        elif tag == '-':
            index -= 1
        elif tag == '=':
            index = num
        else:
            index = int(math.floor(random.random() * len(self.zhishi.get_datas())))

        _index, zhishi_data = self.zhishi.get_data(index)
        self.set_session_attribute("zhishi_data", _index, 0)
        render_template = self.get_template(zhishi_data)
        return {
            'directives': [render_template],
            'outputSpeech': zhishi_data
        }

    def get_template(self, content):
        template = BodyTemplate1()
        template.set_title(self.title)
        template.set_plain_text_content(content)
        template.set_background_image('https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532350870263&di=c93edb2fb9a3cfe7a632acc46cceba62&imgtype=0&src=http%3A%2F%2Ffile25.mafengwo.net%2FM00%2F0A%2FAC%2FwKgB4lMC26CAWsKoAALb5778DWg60.rbook_comment.w1024.jpeg')
        template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254321')
        render_template = RenderTemplate(template)
        return render_template


def handler(event, context):

    bot = HeXinChun(event)
    result = bot.run()
    return result
