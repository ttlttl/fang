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
    house = House.query.get_or_404(id)
    form.new_or_used = house.is_new
    form.community_name.data = house.community.name
    form.type.data = house.type
    form.decoration.data = house.decoration
    form.toward.data = house.toward

    if form.validate_on_submit():
        house.title = form.title.data
        house.type = form.type.data
        house.decoration=form.decoration.data
        house.toward=form.toward.data
        house.floor=form.floor.data
        house.total_floor=form.total_floor.data
        house.shi=form.shi.data
        house.ting=form.ting.data
        house.wei=form.wei.data
        house.price=form.price.data
        house.total_area=form.total_area.data
        house.total_price=form.total_price.data
        house.down_payment=form.down_payment.data
        house.detail=form.detail.data

        db.session.add(house)
        print('dfsdfsdfsdfsdfaf')
        flash('更新成功')
        return redirect(url_for('.edit_post', id=id))

    form.title.data = house.title
    form.type.data = house.type
    form.decoration.data = house.decoration
    form.toward.data = house.toward
    form.floor.data = house.floor
    form.shi.data = house.shi
    form.ting.data = house.ting
    form.wei.data = house.wei
    form.price.data = house.price
    form.total_area.data = house.total_area
    form.total_price.data = house.total_price
    form.total_floor.data = house.total_floor
    form.down_payment.data = house.down_payment
    form.detail.data = house.detail
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
        print(session['images'])
        return jsonify({'result':'Success'})
    return jsonify({'result':'Fail'})


@edit.route('/my_posts')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    pagination = House.query.order_by(House.timestamp.desc()).paginate(
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


@edit.route('/houses/<int:id>')
@login_required
def houses(id):
    community = Community.query.get_or_404(id)
    houses = community.houses
    return render_template('edit/houses.html', community=community, houses=houses)


@edit.route('/all_houses')
@login_required
def all_houses():
    houses = House.query.all()
    return render_template('edit/all_houses.html', houses=houses)


@edit.route('/delete_house/<int:id>')
@login_required
@admin_required
def delete_house(id):
    referer = request.headers.get('Referer')
    house = House.query.get(id)
    db.session.delete(house)
    flash('删除成功！')
    return redirect(referer)