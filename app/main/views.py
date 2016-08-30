# -*- coding=UTF-8 -*-
from flask import render_template, request, redirect, url_for
from . import main
from ..models import House, District, Area, Community
import re


# total price range
a_range = ((0, 10000), (0, 101), (101, 150), (151, 201), (201, 301), \
           (301, 501), (501, 1001), (1001, 10000))
# total area range
c_range = ((0, 10000), (0, 51), (51, 71), (71, 91), (91, 111), (111, 131), \
           (131, 151), (151, 201), (201, 301), (301, 10000))


@main.route('/', methods=['GET'])
def index():
    return redirect(url_for('main.esf'))


@main.route('/detail/<int:id>')
def detail(id):
    post = House.query.get_or_404(id)
    images = post.images
    return render_template('detail.html', post=post, images=images)


@main.route('/xf/')
def xf():
    return redirect(url_for('.xf_with_location_and_args', location='all', args='a0-b0-c0'))


@main.route('/xf/<location>')
def xf_redirect_with_location(location):
        return redirect(url_for(".xf_with_location_and_args", location=location, args="a0-b0-c0"))


@main.route('/xf/<location>/<args>')
def xf_with_location_and_args(location, args):
    # args, eg: a1-b3-c2, price in range(0, 101), 3 shi, area in range(51-71)
    if not re.match(r'a[0-9]-b[0-9]-c[0-9]', args):
        arg_a, arg_b, arg_c = "a0", "b0", "c0"
    else:
        arg_a, arg_b, arg_c = args.split("-")
    num_a, num_b, num_c = int(arg_a[1:]), int(arg_b[1:]), int(arg_c[1:])
    if num_a >= len(a_range):
        num_a = 0
    if num_b > 7:
        num_b = 0
    if num_c >= len(c_range):
        num_c = 0

    page = request.args.get('page', 1, type=int)
    selected_district = "all"
    selected_area = None
    selected_location = "all"
    areas = None

    # all
    if location == "all":
        if num_b == 0:
            pagination = House.query.filter(House.is_new==True,
                                            House.total_price.between(*a_range[num_a]),
                                            House.total_area.between(*c_range[num_c])) \
                .paginate(page, per_page=10, error_out=False)
        else:
            pagination = House.query.filter(House.is_new==True,
                                            House.total_price.between(*a_range[num_a]),
                                            House.shi == num_b,
                                            House.total_area.between(*c_range[num_c]))\
                .paginate(page, per_page=10, error_out=False)
        selected_location = "all"
    # eg: changningqu-beixinjing
    elif "-" in location:
        selected_district, selected_area = location.split("-")
        if num_b == 0:
            pagination = House.query.filter(House.is_new==True,
                                            House.total_price.between(*a_range[num_a]),
                                            House.total_area.between(*c_range[num_c]),
                                            House.community_id==Community.id).\
                                    filter(Community.area_id==Area.id).\
                                    filter(Area.en_name==selected_area).\
                                    paginate(page, per_page=10, error_out=False)
        else:
            pagination = House.query.filter(House.is_new==True,
                                            House.total_price.between(*a_range[num_a]),
                                            House.shi == num_b,
                                            House.total_area.between(*c_range[num_c]),
                                            House.community_id==Community.id).\
                                    filter(Community.area_id == Area.id).\
                                    filter(Area.en_name == selected_area).\
                                    paginate(page, per_page=10, error_out=False)
        selected_location = "%s-%s" % (selected_district, selected_area)
        areas = District.query.filter_by(en_name=selected_district).first().areas.all()
    # eg: changningqu
    else:
        selected_district = location
        if num_b == 0:
            pagination = House.query.filter(House.is_new == True,
                                            House.total_price.between(*a_range[num_a]),
                                            House.total_area.between(*c_range[num_c]),\
                                            House.community_id==Community.id).\
                                    filter(Community.area_id==Area.id).\
                                    filter(Area.district_id==District.id).\
                                    filter(District.en_name==selected_district).\
                                    paginate(page, per_page=10, error_out=False)
        else:
            pagination = House.query.filter(House.is_new == True,
                                            House.total_price.between(*a_range[num_a]),
                                            House.shi == num_b,
                                            House.total_area.between(*c_range[num_c]),\
                                            House.community_id == Community.id).\
                                    filter(Community.area_id == Area.id).\
                                    filter(Area.district_id == District.id).\
                                    filter(District.en_name == selected_district).\
                                    paginate(page, per_page=10, error_out=False)
        selected_location = location
        areas = District.query.filter_by(en_name=selected_district).first().areas.all()

    posts = pagination.items
    districts = District.query.all()
    return render_template('xf.html', districts=districts, areas=areas, posts=posts, \
                           pagination=pagination, a=arg_a, b=arg_b, c=arg_c, \
                           selected_location = selected_location, \
                           selected_district=selected_district, selected_area=selected_area,\
                           current_page='xf')


@main.route('/esf/')
def esf():
    return redirect(url_for('.esf_with_location_and_args', location='all', args='a0-b0-c0'))


@main.route('/esf/<location>')
def redirect_with_location(location):
        return redirect(url_for(".esf_with_location_and_args", location=location, args="a0-b0-c0"))


@main.route('/esf/<location>/<args>')
def esf_with_location_and_args(location, args):
    # args, eg: a1-b3-c2, price in range(0, 101), 3 shi, area in range(51-71)
    if not re.match(r'a[0-9]-b[0-9]-c[0-9]', args):
        arg_a, arg_b, arg_c = "a0", "b0", "c0"
    else:
        arg_a, arg_b, arg_c = args.split("-")
    num_a, num_b, num_c = int(arg_a[1:]), int(arg_b[1:]), int(arg_c[1:])
    if num_a >= len(a_range):
        num_a = 0
    if num_b > 7:
        num_b = 0
    if num_c >= len(c_range):
        num_c = 0

    page = request.args.get('page', 1, type=int)
    selected_district = "all"
    selected_area = None
    selected_location = "all"
    areas = None

    # all
    if location == "all":
        if num_b == 0:
            pagination = House.query.filter(House.is_new==False,
                                            House.total_price.between(*a_range[num_a]),
                                            House.total_area.between(*c_range[num_c])) \
                .paginate(page, per_page=10, error_out=False)
        else:
            pagination = House.query.filter(House.is_new==False,
                                            House.total_price.between(*a_range[num_a]),
                                            House.shi == num_b,
                                            House.total_area.between(*c_range[num_c]))\
                .paginate(page, per_page=10, error_out=False)
        selected_location = "all"
    # eg: changningqu-beixinjing
    elif "-" in location:
        selected_district, selected_area = location.split("-")
        if num_b == 0:
            pagination = House.query.filter(House.is_new==False,
                                            House.total_price.between(*a_range[num_a]),
                                            House.total_area.between(*c_range[num_c]),
                                            House.community_id==Community.id).\
                                    filter(Community.area_id==Area.id).\
                                    filter(Area.en_name==selected_area).\
                                    paginate(page, per_page=10, error_out=False)
        else:
            pagination = House.query.filter(House.is_new==False,
                                            House.total_price.between(*a_range[num_a]),
                                            House.shi == num_b,
                                            House.total_area.between(*c_range[num_c]),
                                            House.community_id==Community.id).\
                                    filter(Community.area_id == Area.id).\
                                    filter(Area.en_name == selected_area).\
                                    paginate(page, per_page=10, error_out=False)
        selected_location = "%s-%s" % (selected_district, selected_area)
        areas = District.query.filter_by(en_name=selected_district).first().areas.all()
    # eg: changningqu
    else:
        selected_district = location
        if num_b == 0:
            pagination = House.query.filter(House.is_new == False,
                                            House.total_price.between(*a_range[num_a]),
                                            House.total_area.between(*c_range[num_c]),\
                                            House.community_id==Community.id).\
                                    filter(Community.area_id==Area.id).\
                                    filter(Area.district_id==District.id).\
                                    filter(District.en_name==selected_district).\
                                    paginate(page, per_page=10, error_out=False)
        else:
            pagination = House.query.filter(House.is_new == False,
                                            House.total_price.between(*a_range[num_a]),
                                            House.shi == num_b,
                                            House.total_area.between(*c_range[num_c]),\
                                            House.community_id == Community.id).\
                                    filter(Community.area_id == Area.id).\
                                    filter(Area.district_id == District.id).\
                                    filter(District.en_name == selected_district).\
                                    paginate(page, per_page=10, error_out=False)
        selected_location = location
        areas = District.query.filter_by(en_name=selected_district).first().areas.all()

    posts = pagination.items
    districts = District.query.all()
    return render_template('esf.html', districts=districts, areas=areas, posts=posts, \
                           pagination=pagination, a=arg_a, b=arg_b, c=arg_c, \
                           selected_location = selected_location, \
                           selected_district=selected_district, selected_area=selected_area,
                           current_page='esf')


