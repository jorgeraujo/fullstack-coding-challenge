from flask import Blueprint


translation_api = Blueprint('translation_api', __name__,
                        template_folder='templates', url_prefix='',static_folder='/static', static_url_path='translation_page/static')
from . import routes