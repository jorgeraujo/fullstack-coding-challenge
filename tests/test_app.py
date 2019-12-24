import os
import tempfile
from challenge import create_app, db
import pytest
from flask_testing import TestCase
from models import Translation

class TestRenderTemplates(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app
    
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_template_rendered(self):
        response = self.client.get('/')
        self.assert_template_used('index.html')
    
    def test_add_translation(self):
        # add test translation
        new_translation = Translation('test_text','test_state','fake_uid')
        expected_response = {'translations':[{'uid':'fake_uid','state':'test_state','translation':'','text_to_translate':'test_text'}]}
        db.session.add(new_translation)
        db.session.commit()
        response = self.client.get('/translations/')
        print(response.data)
        self.assertEquals(response.json, expected_response)
