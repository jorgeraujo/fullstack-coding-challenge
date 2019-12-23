from database import db
from models import Translation
from flask import Blueprint, request, render_template
from unbabel.api import UnbabelApi
import json 
uapi = UnbabelApi('fullstack-challenge', '9db71b322d43a6ac0f681784ebdcc6409bb83359', sandbox=True)

translation_page = Blueprint('translation_page', __name__,
                        template_folder='templates', url_prefix='')

@translation_page.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # call the unbabel api here 
        
        # add to the db 
        try:
            result = uapi.post_translations(text=request.form['text_to_translate'],source_language='en', target_language='es')
            new_translation = Translation(text_to_translate=request.form['text_to_translate'],state=result.status,uid=result.uid)
            db.session.add(new_translation)
            db.session.commit()
        except Exception as e:
            print(e)
        return 'translation_added'