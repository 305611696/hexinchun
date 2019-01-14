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
from nengli.Calendar import Calendar

reload(sys)
sys.setdefaultencoding('utf8')

class HeXinChun(Bot):

    def __init__(self, request_data):
        super(HeXinChun, self).__init__(request_data)
        self.title = "贺新春"
        self.list = [{"name": "小知识", "image": "http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/list_zhishi.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-22T16%3A07%3A55Z%2F-1%2F%2Fc707c5d1fb746a05537b4d7ed1eb764c55a08f6cfe645f808a705b2a75553524"},
                     {"name": "小菜谱", "image": "http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/list_meishi.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-22T16%3A07%3A55Z%2F-1%2F%2Fed79b5d3569f90ce32a1dbc0511fbf75931849ee6a9cad2a8a54309a2d00ae9b"},
                     {"name": "小日历", "image": "http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/list_rili.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2019-01-05T12%3A21%3A56Z%2F-1%2F%2Fec4e8cfdb305e19396c521952c24937d4d16513541f04308e7bb1de9f11e0851"},
                     ]
        self.current_item = self.get_session_attribute("current_item", -1)
        self.calendar = Calendar()
        self.calendar_bg = "http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/bg_zhishi.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-22T15%3A55%3A51Z%2F-1%2F%2F6fe6a206c5b1408510053d346d8bcde43c2d50d23eddd52def23dbe98c774977"
        self.zhinan = Zhinan()
        self.zhishi = Zhishi()
        self.zhishi_bg = "http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/bg_zhishi.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-22T15%3A55%3A51Z%2F-1%2F%2F6fe6a206c5b1408510053d346d8bcde43c2d50d23eddd52def23dbe98c774977"
        self.caipu = Caipu()
        self.caipu_bg = "http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/bg_meishi.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-22T15%3A49%3A03Z%2F-1%2F%2Fe2728059a31fe54c37eb6604b297365452027f2d91645741f4374835158118b8"
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('iling.backlist', self.get_to_list)
        self.add_intent_handler('iling.lbxz', self.get_select_item)
        self.add_intent_handler('iling.caipu', self.get_caipu)
        self.add_intent_handler('ai.dueros.common.next_intent', self.get_next)
        self.add_intent_handler('ai.dueros.common.previous_intent', self.get_previous)
        self.add_intent_handler('ai.dueros.common.default_intent', self.get_default)
        self.add_event_listener('Display.ElementSelected', self.get_select_item_click)
        self.add_session_ended_handler(self.ended_request)

    def launch_request(self):
        """
        打开调用名
        """
        self.wait_answer()

        self.current_item = -1
        self.set_session_attribute("current_item", -1, -1)

        list_template = self.get_list()
        v_day = self.zhinan.d_value(self.zhinan.get_current_date())
        content = r"欢迎来到贺新春，"
        if v_day > 0:
            content += "距离大年初一还有" + str(v_day) + "天。"
            if self.zhinan.has_key(self.zhinan.get_current_date()):
                content += self.zhinan.get_data(self.zhinan.get_current_date())
        elif v_day == 0:
            content += "今天是" + self.zhinan.get_data(self.zhinan.get_current_date())
        else:
            if self.zhinan.has_key(self.zhinan.get_current_date()):
                content += "今天是" + self.zhinan.get_data(self.zhinan.get_current_date())
            content += "虽然新年已经过去但是也可以了解一些新年的习俗的。"

        content += "请问要了解哪些内容呢？可以对我说第几个!"
        render_template = RenderTemplate(list_template)
        return {
            'directives': [render_template],
            'outputSpeech': content
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
            'http://dbp-resource.gz.bcebos.com/a68dacbb-a28c-83c8-354e-15c45bfea2d1/bg_index.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-22T15%3A58%3A43Z%2F-1%2F%2F08e73511b446b3e0686beca91f5834e53d611a1017cb98393042e6ae12162511')
        list_template.set_title(self.title)

        for i in range(0, len(self.list)):
            item = ListTemplateItem()
            item.set_token(i)
            item.set_plain_primary_text(self.list[i]["name"])
            item.set_plain_secondary_text(self.title + self.list[i]["name"])
            item.set_image(self.list[i]["image"])
            list_template.add_item(item)

        return list_template

    def get_select_item_click(self, req):
        """
        选择指定能力通过编号
        """
        self.wait_answer()
        # 直接选择某一个Item
        token = int(req['request']['token'])

        self.current_item = token
        self.set_session_attribute("current_item", token, -1)
        if token == 0:
            return self.get_zhishi()
        elif token == 1:
            # caipu_data = '想知道哪些春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
            caipu_data = '目前只收录了'+str(len(self.caipu.get_datas()))+'种馅料饺子的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
            render_template = self.get_template(caipu_data, self.caipu_bg)
            return {
                'directives': [render_template],
                'outputSpeech': caipu_data
            }
        elif token == 2:
            _calendar = "今天是" + self.zhinan.get_current_date() + "可以对我说下一个,查看次月日历"
            self.set_session_attribute("_year", self.calendar.get_year(), self.calendar.get_year())
            self.set_session_attribute("_month", self.calendar.get_month(), self.calendar.get_month())
            render_template = self.get_template(self.calendar.get_calendar(), self.calendar_bg)
            return {
                'directives': [render_template],
                'outputSpeech': _calendar
            }



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
                    # caipu_data = '想知道哪些春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
                    caipu_data = '目前只收录了'+str(len(self.caipu.get_datas()))+'种馅料饺子的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
                    render_template = self.get_template(caipu_data, self.caipu_bg)
                    return {
                        'directives': [render_template],
                        'outputSpeech': caipu_data
                    }
                elif num == 3:
                    _calendar = "今天是" + self.zhinan.get_current_date() + "可以对我说下一个,查看次月日历"
                    self.set_session_attribute("_year", self.calendar.get_year(), self.calendar.get_year())
                    self.set_session_attribute("_month", self.calendar.get_month(), self.calendar.get_month())
                    render_template = self.get_template(self.calendar.get_calendar(), self.calendar_bg)
                    return {
                        'directives': [render_template],
                        'outputSpeech': _calendar
                    }

            elif self.current_item == 1:
                return self.get_zhishi('=', num)
            elif self.current_item == 2:
                # caipu_data = '想知道哪些春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
                index, caipu_data = self.caipu.get_data_and_index(num)
                self.set_session_attribute("caipu_index", index, 0)
                if not caipu_data:
                    caipu_data = '目前只收录了'+str(len(self.caipu.get_datas()))+'种馅料饺子的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
                render_template = self.get_template(caipu_data, self.caipu_bg)
                return {
                    'directives': [render_template],
                    'outputSpeech': caipu_data
                }
            else:
                result_data = '我太笨了没有理解您的表达。'
                return {
                    'outputSpeech': result_data
                }
        else:

            if item == "小知识":
                self.set_session_attribute("current_item", 1, -1)
                return self.get_zhishi()
            elif item == "小菜谱":
                self.set_session_attribute("current_item", 2, -1)
                # caipu_data = '想知道哪些春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
                caipu_data = '目前只收录了'+str(len(self.caipu.get_datas()))+'种馅料饺子的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
                render_template = self.get_template(caipu_data, self.caipu_bg)
                return {
                    'directives': [render_template],
                    'outputSpeech': caipu_data
                }
            elif item == "小日历":
                self.set_session_attribute("current_item", 3, -1)
                _calendar = "今天是" + self.zhinan.get_current_date() + "可以对我说下一个,查看次月日历"
                self.set_session_attribute("_year", self.calendar.get_year(), self.calendar.get_year())
                self.set_session_attribute("_month", self.calendar.get_month(), self.calendar.get_month())
                render_template = self.get_template(self.calendar.get_calendar(), self.calendar_bg)
                return {
                    'directives': [render_template],
                    'outputSpeech': _calendar
                }
            else:
                render_template = self.get_template(r'请问你选择的是第几个呢？', self.zhishi_bg)
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
        elif self.current_item == 2:
            caipu_index = self.get_session_attribute('caipu_index', 0)
            caipu_index = int(caipu_index) + 1
            index, caipu_data = self.caipu.get_data_and_index(caipu_index)
            self.set_session_attribute("caipu_index", index, 0)
            # caipu_data = '想知道更多春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
            render_template = self.get_template(caipu_data, self.caipu_bg)
            return {
                'directives': [render_template],
                'outputSpeech': caipu_data
            }
        elif self.current_item == 3:
            _year = self.get_session_attribute("_year", self.calendar.get_year())
            _month = self.get_session_attribute("_month", self.calendar.get_month())
            if _month == 12:
                _year += 1
                _month = 1
            else:
                _month += 1
            self.set_session_attribute("_year", _year, self.calendar.get_year())
            self.set_session_attribute("_month", _month, self.calendar.get_month())
            render_template = self.get_template(self.calendar.get_calendar(_year, _month), self.calendar_bg)
            return {
                'directives': [render_template]
            }
        else:
            pass

    def get_previous(self):
        self.wait_answer()
        if self.current_item == 1:
            return self.get_zhishi('-')
        elif self.current_item == 2:
            caipu_index = self.get_session_attribute('caipu_index', 0)
            caipu_index = int(caipu_index) - 1
            index, caipu_data = self.caipu.get_data_and_index(caipu_index)
            self.set_session_attribute("caipu_index", index, 0)
            # caipu_data = '想知道更多春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
            render_template = self.get_template(caipu_data, self.caipu_bg)
            return {
                'directives': [render_template],
                'outputSpeech': caipu_data
            }
        elif self.current_item == 3:
            _year = self.get_session_attribute("_year", self.calendar.get_year())
            _month = self.get_session_attribute("_month", self.calendar.get_month())
            if _month == 1:
                _year -= 1
                _month = 12
            else:
                _month -= 1
            self.set_session_attribute("_year", _year, self.calendar.get_year())
            self.set_session_attribute("_month", _month, self.calendar.get_month())
            render_template = self.get_template(self.calendar.get_calendar(_year, _month), self.calendar_bg)
            return {
                'directives': [render_template]
            }
        else:
            pass

    def get_default(self):
        self.wait_answer()
        if self.current_item == 1:
            caipu_data = '我太笨了没有理解您的表达。'
            return {
                'outputSpeech': caipu_data
            }
        elif self.current_item == 2:
            # caipu_data = '想知道更多春节美食的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
            caipu_data = '我太笨了没有理解您的表达。目前只收录了'+str(len(self.caipu.get_datas()))+'种馅料饺子的做法，比如你可以对我说：韭菜鸡蛋饺子怎么做？'
            return {
                'outputSpeech': caipu_data
            }
        else:
            caipu_data = '我太笨了没有理解您的表达。'
            return {
                'outputSpeech': caipu_data
            }

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
        render_template = self.get_template(zhishi_data, self.zhishi_bg)
        return {
            'directives': [render_template, {
            "type": "Hint",
            "hints": [
                {
                    "type": "PlainText",
                    "text": "对我说“返回”回到列表界面"
                }
            ]
        }],
            'outputSpeech': zhishi_data
        }

    def get_caipu(self):
        self.wait_answer()
        meishi = self.get_slots("meishi")
        if meishi:
            if meishi == "饺子":
                xianliao = self.get_slots("xianliao")
                if xianliao:
                    if self.caipu.get_datas().has_key(str(xianliao)+str(meishi)):
                        caipu = self.caipu.get_data(str(xianliao)+str(meishi))
                        render_template = self.get_template(caipu, self.caipu_bg)
                        return {
                            'directives': [render_template, {
                                            "type": "Hint",
                                            "hints": [
                                                {
                                                    "type": "PlainText",
                                                    "text": "对我说“返回”回到列表界面"
                                                }
                                            ]
                                        }],
                            'outputSpeech': caipu
                        }
                    else:
                        self.ask("xianliao")
                        return {
                            'outputSpeech': '我还不知道'+xianliao+'馅饺子做法，可以换个馅料么。比如你可以对我说：韭菜鸡蛋？',
                        }
                else:
                    self.ask("xianliao")
                    return {
                        'outputSpeech': '请您告诉我要做什么馅料的呢？比如你可以对我说：韭菜鸡蛋',
                        'reprompt': '饺子有很多馅料哦，可以告诉我要做什么馅的么？比如你可以对我说：韭菜鸡蛋'
                    }
            else:
                # caipu = self.caipu.get_data(meishi)
                # render_template = self.get_template(caipu, self.caipu_bg)
                # return {
                #     'directives': [render_template],
                #     'outputSpeech': caipu
                # }
                return {
                    'outputSpeech': '你说的美食的做法正在收录中，可以换个美食么。比如你可以对我说：韭菜鸡蛋饺子怎么做？',
                }
        else:
            return {
                'outputSpeech': '你说的美食的做法正在收录中，可以换个美食么。比如你可以对我说：韭菜鸡蛋饺子怎么做？',
            }

    def get_template(self, content, bg='https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1532350870263&di=c93edb2fb9a3cfe7a632acc46cceba62&imgtype=0&src=http%3A%2F%2Ffile25.mafengwo.net%2FM00%2F0A%2FAC%2FwKgB4lMC26CAWsKoAALb5778DWg60.rbook_comment.w1024.jpeg'):
        template = BodyTemplate1()
        template.set_title(self.title)
        template.set_plain_text_content(content)
        template.set_background_image(bg)
        template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254321')
        render_template = RenderTemplate(template)
        return render_template


def handler(event, context):

    bot = HeXinChun(event)
    result = bot.run()
    return result
