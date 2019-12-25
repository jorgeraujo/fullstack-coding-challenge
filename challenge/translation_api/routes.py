from challenge.models import Translation,translations_schema
from flask import request, jsonify
from . import translation_api
from marshmallow import Schema, fields, ValidationError
from challenge import db, socketio

class ApiResponseSchema(Schema):
    order_number = fields.Float()
    price = fields.Float()
    source_language = fields.Str()
    status = fields.Str()
    target_language = fields.Str()
    text = fields.Str()
    text_format = fields.Str() 
    uid = fields.Str()
    translated_text = fields.Str()


@translation_api.route('/translations/', methods=['GET','POST'])
def translate():
    if request.method == 'GET':
        sql = 'select * from translations order by length(translation) desc;'
        result = db.engine.execute(sql);
        data_ =  {'translations': translations_schema.dump(result).data}
        return jsonify(data_)
    # endpoint for the translation callback 
    if request.method == 'POST':
        data = request.form.to_dict()
        # payload validation
        try:
            validated = ApiResponseSchema().load(data)
        except ValidationError as err:
            return 'Bad Request', 400

        try:
            translation_to_update = Translation.query.filter_by(uid=data['uid']).first()
            translation_to_update.state = data['status']
            translation_to_update.translation = data['translated_text']
            db.session.commit()
            msg = data
            socketio.emit('translation completed',{'uid':data['uid'],'status':data['status'],'translation':data['translated_text']})
        except Exception as e:
            print(e)
        return {'message': 'Successfully updated translation'}, 200
