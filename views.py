from database import db
from models import Translation, translations_schema, translation_schema
from flask import Blueprint, request, render_template, jsonify
from unbabel.api import UnbabelApi
from sqlalchemy.sql.expression import func, or_, and_
import json 
uapi = UnbabelApi('fullstack-challenge', '9db71b322d43a6ac0f681784ebdcc6409bb83359', sandbox=True)

translation_page = Blueprint('translation_page', __name__,
                        template_folder='templates', url_prefix='',static_folder='/static', static_url_path='translation_page/static')

translation_api = Blueprint('translation_api', __name__,
                        template_folder='templates', url_prefix='',static_folder='/static', static_url_path='translation_page/static')


@translation_page.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # call the unbabel api here 
        request_data=json.loads(request.data.decode())
        print(request_data['text_to_translate'])
        # add to the db 
        try:
            result = uapi.post_translations(text=request_data['text_to_translate'],source_language='en', target_language='es',callback_url='http://9e17e987.ngrok.io/translations/')
            new_translation = Translation(text_to_translate=request_data['text_to_translate'],state=result.status,uid=result.uid)
            db.session.add(new_translation)
            db.session.commit()
        except Exception as e:
            print(e)
        return 'translation_added'

@translation_api.route('/translations/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        sql = 'select * from translations  order by length(translation) desc;'
        data = db.engine.execute(sql);
        data_ =  {'translations': translations_schema.dump(data)}
        return jsonify(data_)
    # endpoint for the translation callback 
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            translation_to_update = Translation.query.filter_by(uid=data['uid']).first()
            translation_to_update.state = data['status']
            translation_to_update.translation = data['translated_text']
            db.session.commit()
        except Exception as e:
            print(e)
        return {'message': 'Successfully updated translation'}, 200
