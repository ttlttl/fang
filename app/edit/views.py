# -*- coding=UTF-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import edit
from .. import db
from .forms import AddUsedHouseForm
from ..models import District, House


@edit.route('/location_info')
@login_required
def location_info():
    districts = District.query.order_by(District.id)
    return render_template('edit/location_info.html', districts=districts)


@edit.route('/publish2', methods=['GET', 'POST'])
@login_required
def publish2():
    form = AddUsedHouseForm(csrf_enabled=False)
    print(form.errors)
    if form.validate_on_submit():
        house = House(title = form.title.data,
                      is_new = False,
                      type = form.type.data,
                      decoration = form.decoration.data,
                      toward = form.toward.data,
                      floor = form.floor.data,
                      total_floor = form.total_floor.data,
                      shi = form.shi.data,
                      ting = form.ting.data,
                      wei = form.wei.data,
                      price = form.price.data,
                      total_area = form.total_area.data,
                      total_price = form.total_price.data,
                      down_payment = form.down_payment.data,
                      detail = form.detail.data,
                      author = current_user._get_current_object() )
        db.session.add(house)
        db.session.commit()
        return redirect(url_for('.publish2'))
    return render_template('edit/publish2.html', form=form)