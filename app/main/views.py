from flask import render_template, request
from . import main
from ..models import House

@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = House.query.order_by(House.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, show_used_house=True)