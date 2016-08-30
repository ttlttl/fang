# -*- coding=UTF-8 -*-
import os
import datetime
import random
from flask import render_template, redirect, request, url_for, flash, \
    jsonify, current_app, make_response, session
from flask_login import login_required, current_user
from . import edit
from .. import db
from .forms import AddUsedHouseForm, AddAreaForm, AddCommunityForm
from ..models import District, House, Community, Area, Image
from ..decorators import admin_required


@edit.route('/main')
@login_required
def main():
    return render_template('edit/main.html')


@edit.route('/location_info')
@login_required
def location_info():
    districts = District.query.order_by(District.id)
    return render_template('edit/location_info.html', districts=districts)


@edit.route('/get_areas_json/<int:id>')
def get_areas_json(id):
    areas = District.query.get(id).areas.all()
    return jsonify({"areas": [{ "id":area.id, "name":area.name} for area in areas]})


@edit.route('/get_communities_json/<int:id>')
def get_communities_json(id):
    communities = Area.query.get(id).communities.all()
    return jsonify({"communities": [{"id": community.id, "name":community.name} \
                                    for community in communities]})


@edit.route('/add_community', methods=['GET', 'POST'])
@login_required
def add_community():
    if request.method == 'POST':
        area_id = request.form['area_id']
        community_name = request.form['community_name']
        if area_id and community_name:
            area = Area.query.get(area_id)
            if not area:
                flash("街道信息错误")
            community = Community(name=community_name, area=area)
            db.session.add(community)
            flash("添加小区信息成功")
            return redirect(url_for('.add_community'))
    districts = District.query.all()
    return render_template('edit/add_community.html', districts=districts)


@edit.route('/communities/<int:id>', methods=['GET', 'POST'])
@login_required
def communities(id):
    form = AddCommunityForm()
    area = Area.query.get_or_404(id)
    if form.validate_on_submit():
        new_community = Community(name=form.community_name.data, en_name=form.en_name.data, area=area)
        db.session.add(new_community)
        flash('添加成功')
        return redirect(url_for('edit.communities', id=id))
    communities = area.communities
    return render_template('edit/communities.html', form=form, area=area, communities=communities)


@edit.route('/community_management/<int:id>', methods=['GET', 'POST'])
@login_required
def community_management(id):
    form = AddCommunityForm()
    community = Community.query.get_or_404(id)
    if form.validate_on_submit():
        community.name = form.community_name.data
        community.en_name = form.en_name.data
        community.developer = form.developer.data
        community.property_management = form.property_management.data
        community.property_costs = form.property_costs.data
        community.greening_rate = form.greening_rate.data
        db.session.add(community)
        flash('更新成功')
        return redirect(url_for('.community_management', id=id))
    form.community_name.data = community.name
    form.en_name.data = community.en_name
    form.developer.data = community.developer
    form.property_management.data = community.property_management
    form.property_costs.data = community.property_costs
    form.greening_rate.data = community.greening_rate
    return render_template('edit/community_management.html', form=form)


@edit.route('/publish2', methods=['GET', 'POST'])
@login_required
def publish2():
    form = AddUsedHouseForm()
    if form.validate_on_submit():
        community = Community.query.filter_by(name=form.community_name.data).first()
        if not community:
            flash("小区不存在，请先添加小区信息")
            return redirect(url_for(".add_community"))
        house = House(title = form.title.data,
                      is_new = False if form.new_or_used.data == '0' else True,
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
                      author = current_user._get_current_object(),
                      community=community)
        db.session.add(house)
        image_names = session.get('images')
        if image_names is not None:
            images = [Image(url=image_name, house=house) for image_name in image_names]
            for image in images:
                db.session.add(image)
            session['images'].clear()
        flash('发布成功')
        return redirect(url_for('.publish2'))
    return render_template('edit/publish2.html', form=form)


@edit.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    form = AddUsedHouseForm()
    post = House.query.get_or_404(id)
    form.new_or_used = post.is_new
    form.community_name.data = post.community.name
    form.type.data = post.type
    form.decoration.data = post.decoration
    form.toward.data = post.toward

    if form.is_submitted():
        post.title = form.title.data
        post.type = form.type.data
        post.decoration=form.decoration.data
        post.toward=form.toward.data
        post.floor=form.floor.data
        post.total_floor=form.total_floor.data
        post.shi=form.shi.data
        post.ting=form.ting.data
        post.wei=form.wei.data
        post.price=form.price.data
        post.total_area=form.total_area.data
        post.total_price=form.total_price.data
        post.down_payment=form.down_payment.data
        post.detail=form.detail.data

        db.session.add(post)
        flash('更新成功')
        return redirect(url_for('.edit_post', id=id))

    form.title.data = post.title
    form.type.data = post.type
    form.decoration.data = post.decoration
    form.toward.data = post.toward
    form.floor.data = post.floor
    form.shi.data = post.shi
    form.ting.data = post.ting
    form.wei.data = post.wei
    form.price.data = post.price
    form.total_area.data = post.total_area
    form.total_price.data = post.total_price
    form.total_floor.data = post.total_floor
    form.down_payment.data = post.down_payment
    form.detail.data = post.detail
    return render_template('edit/edit_post.html', form=form)


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@edit.route('/imgUpload/', methods=['POST'])
@login_required
def imgUpload():
    error = ''
    url = ''
    url = ''
    callback = request.args.get('CKEditorFuncNum')
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """
    <script type="text/javascript">
        window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
    </script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


@edit.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')
    if file:
        fext = os.path.splitext(file.filename)[-1]
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        file.save(filepath)
        if session.get('images') is None:
            session['images'] = []
        session['images'].append(rnd_name)
        # mutable structures are not picked up automatically
        session.modified = True
        return jsonify({'result':'Success'})
    return jsonify({'result':'Fail'})


@edit.route('/my_posts')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    if current_user.is_administrator:
        pagination = House.query.order_by(House.timestamp.desc()).paginate(
            page, per_page=10, error_out=False
        )
    else:
        pagination = House.query.filter_by(House.author_id==current_user.id)\
            .order_by(House.timestamp.desc()).paginate(
                    page, per_page=10, error_out=False
                )
    posts = pagination.items
    return render_template('edit/my_posts.html', posts=posts, pagination=pagination)


@edit.route('/districts')
@login_required
def districts():
    districts = District.query.all()
    return render_template('edit/districts.html', districts=districts)


@edit.route('/areas/<int:id>', methods=['GET', 'POST'])
@login_required
def areas(id):
    form = AddAreaForm()
    district = District.query.get_or_404(id)
    if form.validate_on_submit():
        new_area = Area(name=form.area_name.data, en_name = form.en_name.data, district=district)
        db.session.add(new_area)
        flash('添加成功')
        return redirect(url_for('edit.areas', id=id))
    areas = district.areas
    return render_template('edit/areas.html', form=form, district=district, areas=areas)


@edit.route('/area_management/<int:id>', methods=['GET', 'POST'])
@login_required
def area_management(id):
    form = AddAreaForm()
    area = Area.query.get_or_404(id)
    if form.validate_on_submit():
        area.name = form.area_name.data
        area.en_name = form.en_name.data
        db.session.add(area)
        flash('更新成功')
        return redirect(url_for('edit.areas', id=id))
    form.area_name.data = area.name
    form.en_name.data = area.en_name
    return render_template('edit/area_management.html', form=form)


@edit.route('/posts/<int:id>')
@login_required
def posts(id):
    community = Community.query.get_or_404(id)
    posts = community.posts
    return render_template('edit/posts.html', community=community, posts=posts)


@edit.route('/all_posts')
@login_required
def all_posts():
    posts = House.query.all()
    return render_template('edit/all_posts.html', posts=posts)


@edit.route('/delete_post/<int:id>')
@login_required
@admin_required
def delete_post(id):
    referer = request.headers.get('Referer')
    post = House.query.get(id)
    db.session.delete(post)
    flash('删除成功！')
    return redirect(referer)