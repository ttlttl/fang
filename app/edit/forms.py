# -*- coding=UTF-8 -*-
from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddUsedHouseForm(Form):
    total_area = IntegerField('面积')
    price = IntegerField('价格')
    total_price = IntegerField('总价')
    down_payment = IntegerField('最低首付')
    shi = IntegerField('室')
    ting = IntegerField('厅')
    wei = IntegerField('卫')
    type = SelectField(choices=[('0', '房屋类型'), ('1', '公寓'), ('2', '别墅'), ('3', '普通住宅'),\
                               ('4', '老公房'), ('5', '洋房'), ('6', '平房')])
    decoration = SelectField(choices=[('0','装修情况'), ('1','毛坯'), ('2','简单装修'), ('3','中等装修'), \
                                     ('4','精装修'), ('5','豪华装修')])
    toward = SelectField(choices=[('0','朝向'), ('1','东'), ('2','西'), ('3','南'), ('4','北'),\
                                ('5','东南'), ('6','东北'), ('7','西南'), ('8','西北')])
    floor = IntegerField('楼层')
    total_floor = IntegerField('总层数')
    title = StringField('标题', validators=[DataRequired(), Length(1, 200)])
    detail = TextAreaField('详情')
    submit = SubmitField('发布')


