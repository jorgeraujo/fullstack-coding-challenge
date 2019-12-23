from sqlalchemy.dialects.postgresql import JSON
from database import db

class Translation(db.Model):
    __tablename__='translations'
    
    uid = db.Column(db.String(),primary_key=True)
    state = db.Column(db.String())
    text_to_translate = db.Column(db.String())
    translation = db.Column(db.String())

    def __init__(self,text_to_translate, state, uid):
        self.text_to_translate = text_to_translate
        self.state = state
        self.uid = uid
    
    def __repr__(self):
        return '<id {}, text to translate{}>'.format(self.uid, self.text_to_translate)

