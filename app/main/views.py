from flask import render_template, request
from . import main
from ..models import House, District

@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = House.query.order_by(House.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, show_used_house=True)


@main.route('/detail/<int:id>')
def detail(id):
    post = House.query.get_or_404(id)
    images = post.images
    return render_template('detail.html', post=post, images=images)


@main.route('/esf/')
def esf():
    districts = District.query.all()
    return render_template('esf.html', districts=districts)