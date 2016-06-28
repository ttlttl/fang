# -*- coding=UTF-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from itsdangerous import Serializer
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, AddUserForm, ChangePasswordForm
from ..decorators import admin_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码错误...')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录')
    return redirect(url_for('main.index'))


@auth.route('/user_management', methods=['GET'])
@login_required
@admin_required
def user_management():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id).paginate(
        page, per_page=10, error_out=False
    )
    users = pagination.items
    return render_template('auth/user_management.html', users=users, pagination=pagination)


@auth.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    is_admin=form.is_admin.data)
        db.session.add(user)
        db.session.commit()
        flash('添加成功')
        return redirect(url_for('auth.user_management'))
    return render_template('auth/add_user.html', form=form)


@auth.route('/status_user/<int:id>')
@login_required
@admin_required
def status_user(id):
    user = User.query.get_or_404(id)
    user.actived = not user.actived
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('auth.user_management'))


@auth.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def change_password(id):
    user = User.query.filter_by(id=id).first()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        flash("密码修改成功！")
        return redirect(url_for('auth.user_management'))
    return render_template('auth/change_password.html', form=form)

