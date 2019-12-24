from models import Translation,translations_schema
from flask import request, jsonify
from . import translation_api
from challenge import db, socketio

@translation_api.route('/translations/', methods=['GET','POST'])
def translate():
    if request.method == 'GET':
        sql = 'select * from translations  order by length(translation) desc;'
        result = db.engine.execute(sql);
        data_ =  {'translations': translations_schema.dump(result)}
        return jsonify(data_)
    # endpoint for the translation callback 
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
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
