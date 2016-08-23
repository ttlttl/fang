# -*- coding=UTF-8 -*-
from flask_wtf import Form
from wtforms import StringField, BooleanField, SubmitField, IntegerField,\
    SelectField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length


class AddUsedHouseForm(Form):
    new_or_used = SelectField('新旧', choices=[('-1', '新旧情况'), ('0', '二手房'), ('1', '新房')])
    community_name = StringField('小区名称', validators=[DataRequired(), Length(1,200)])
    total_area = IntegerField('面积', validators=[DataRequired()])
    price = IntegerField('价格', validators=[DataRequired()])
    total_price = IntegerField('总价', validators=[DataRequired()])
    down_payment = IntegerField('最低首付', validators=[DataRequired()])
    shi = IntegerField('室', validators=[DataRequired()])
    ting = IntegerField('厅', validators=[DataRequired()])
    wei = IntegerField('卫', validators=[DataRequired()])
    type = SelectField(choices=[('0', '房屋类型'), ('1', '公寓'), ('2', '别墅'), ('3', '普通住宅'),\
                               ('4', '老公房'), ('5', '洋房'), ('6', '平房')], validators=[DataRequired()])
    decoration = SelectField(choices=[('0','装修情况'), ('1','毛坯'), ('2','简单装修'), ('3','中等装修'), \
                                     ('4','精装修'), ('5','豪华装修')], validators=[DataRequired()])
    toward = SelectField(choices=[('0','朝向'), ('1','东'), ('2','西'), ('3','南'), ('4','北'),\
                                ('5','东南'), ('6','东北'), ('7','西南'), ('8','西北')], validators=[DataRequired()])
    floor = IntegerField('楼层')
    total_floor = IntegerField('总层数')
    title = StringField('标题', validators=[DataRequired(), Length(1, 200)])
    detail = TextAreaField('详情')
    submit = SubmitField('发布')


class AddAreaForm(Form):
    area_name = StringField('街道名称', validators=[DataRequired(), Length(1, 200)])
    en_name = StringField('拼音', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('添加')


class AddCommunityForm(Form):
    community_name = StringField('小区名称', validators=[DataRequired(), Length(1, 200)])
    en_name = StringField('拼音', validators=[DataRequired(), Length(1, 64)])
    developer = StringField('开发商', validators=[Length(1, 64)])
    property_management = StringField('物业公司', validators=[Length(1, 64)])
    property_costs = DecimalField('物业费(元/平方米)')
    greening_rate = DecimalField('绿化率')
    submit = SubmitField('添加')


