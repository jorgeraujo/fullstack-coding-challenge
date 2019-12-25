from flask import request, render_template
from . import translation_page
from challenge.models import Translation
from challenge import db, uapi
from marshmallow import Schema, fields, ValidationError
from challenge.config import TRANSLATION_CALLBACK
import json 

# schema for the post request 
class RequestTranslationSchema(Schema):
    text_to_translate = fields.Str()

@translation_page.route('/', methods=['GET','POST'])
def index():
    
    if request.method == 'GET':
        return render_template('index.html')
    
    elif request.method == 'POST':
        # payload validation
        request_data=request.get_json(force=True)
      
        try:
            schema = RequestTranslationSchema()
            schema.load(request_data)
        except ValidationError as err:
            return 'Bad Request', 400
         
        # try to call unbabel api and add to the db 
        try:
             # call the unbabel API
            result = uapi.post_translations(text=request_data['text_to_translate'],source_language='en', target_language='es',callback_url=TRANSLATION_CALLBACK)
            
            new_translation = Translation(text_to_translate=request_data['text_to_translate'],state=result.status,uid=result.uid)
            db.session.add(new_translation)
            db.session.commit()
            return {'state':result.status,'uid':result.uid}, 201
        except:
            return 'Server Error', 500
