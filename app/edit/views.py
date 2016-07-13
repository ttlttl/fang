# -*- coding=UTF-8 -*-
import os
import datetime
import random
from flask import render_template, redirect, request, url_for, flash, \
    jsonify, current_app, make_response, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from . import edit
from .. import db
from .forms import AddUsedHouseForm
from ..models import District, House, Community, Area


@edit.route('/location_info')
@login_required
def location_info():
    districts = District.query.order_by(District.id)
    return render_template('edit/location_info.html', districts=districts)


@edit.route('/get_areas_by_district/<int:id>', methods=['GET'])
def get_areas_by_district_id(id):
    areas = District.query.get(id).areas.all()
    return jsonify({"areas": [{ "id":area.id, "name":area.name} for area in areas]})


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
    form = AddUsedHouseForm(csrf_enabled=False)
    if form.validate_on_submit():
        community = Community.query.filter_by(name=form.community_name.data).first()
        if not community:
            flash("小区不存在，请先添加小区信息")
            return redirect(url_for(".add_community"))
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
                      author = current_user._get_current_object(),
                      community=community)
        db.session.add(house)
        flash('发布成功')
        return redirect(url_for('.publish2'))
    return render_template('edit/publish2.html', form=form)


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@edit.route('/imgUpload/', methods=['POST'])
@login_required
def imgUpload():
    error = ''
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


@edit.route('/test')
def test():
    return render_template('edit/test.html')

@edit.route('/upload', methods=['POST'])
@login_required
def upload():
    upload_files = request.files.getlist('file[]')
    filenames = []
    for file in upload_files:
        if file:
            fext = os.path.splitext(file.filename)[-1]
            rnd_name = '%s%s' % (gen_rnd_filename(), fext)
            filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
            file.save(filepath)
            filenames.append(rnd_name)
    return render_template('edit/upload.html', filenames=filenames)


@edit.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.static_folder, 'upload'), filename)