from sqlalchemy.dialects.postgresql import JSON
from flask import Flask
from challenge import db, ma


class Translation(db.Model):
    __tablename__='translations'
    
    uid = db.Column(db.String(),primary_key=True)
    state = db.Column(db.String())
    text_to_translate = db.Column(db.String())
    translation = db.Column(db.String(),default='')

    def __init__(self,text_to_translate, state, uid):
        self.text_to_translate = text_to_translate
        self.state = state
        self.uid = uid
    
    def __repr__(self):
        return '<id {}, text to translate{}>'.format(self.uid, self.text_to_translate)
    
    def __to_dict__(self):
        return {
            'uid' : self.uid,
            'state' : self.state,
            'text_to_translate' : self.text_to_translate,
            'translation': self.translation
        }


class TranslationSchema(ma.Schema):
    class Meta:
        fields=("uid","state","text_to_translate", "translation")

translation_schema = TranslationSchema()
translations_schema = TranslationSchema(many=True)
