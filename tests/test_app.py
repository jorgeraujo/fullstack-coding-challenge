import os
import tempfile
from challenge import create_app, db, socketio
import challenge
import pytest
from flask_testing import TestCase
from models import Translation
from flask_socketio import SocketIO, send, emit
from mock import patch


db.metadata.clear()
class TestRenderTemplates(TestCase):


    def create_app(self):
        app = challenge.create_app()
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

    def test_add_translation_and_get_all(self):
        
        expected_response = {'translations': [
            {'uid': 'fake_uid', 'state': 'test_state', 'translation': '', 'text_to_translate': 'test_text'}]}
        # add test translation
        new_translation = Translation('test_text', 'test_state', 'fake_uid')
        db.session.add(new_translation)
        db.session.commit()
        response = self.client.get('/translations/')
        print(response.data)
        self.assertEquals(response.json, expected_response)

    def test_assert_callback_endpoint_update_translation(self):
         # add test translation
        new_translation = Translation('test_text', 'test_state', 'fake_uid')
        expected_response = {"message": "Successfully updated translation"}
        db.session.add(new_translation)
        db.session.commit()
        data = {'order_number':  3.2,
                'price': 2.0,
                'source_language': 'en',
                'status': 'completed',
                'target_language': 'es',
                'text': 'test_text',
                'text_format': 'text',
                'uid': 'fake_uid',
                'translated_text': 'updated translation'}
        with patch.object(socketio, 'emit') as mock:
            response = self.client.post('/translations/', data=data)
            print(response.data)
            self.assertEquals(response.json, expected_response)
            self.assertEquals(response.status, '200 OK')
            all = db.session.query(Translation).all()
        expected_updated_entry = {'state': 'completed', 'text_to_translate': 'test_text',
            'translation': 'updated translation', 'uid': 'fake_uid'}
        self.assertEquals(all[0].__to_dict__(), expected_updated_entry)
        # assert the sockets event is emited to update the translation
        mock.assert_called_once_with('translation completed', {'uid': 'fake_uid', 'status': 'completed', 'translation': 'updated translation'})
    
    def test_assert_callback_endpoint_update_translation_bad(self):
         # add test translation
        new_translation = Translation('test_text', 'test_state', 'fake_uid')
        expected_response = {"message": "Successfully updated translation"}
        db.session.add(new_translation)
        db.session.commit()
        bad_data = {'order_number':  3.2,
                'pssssrice': 2.0,
                'souasddasdrce_languageasd': 'en',
                'text': 'test_text',
                'text_format': 'text',
                'uiasssd': 'fake_uid',
                'translaasdated_text': 'updated translation'}
        with patch.object(socketio, 'emit') as mock:
            response = self.client.post('/translations/', data=bad_data)
            print(response.data)
            self.assertEquals(response.status, '400 BAD REQUEST')
        # assert the sockets event is not emited to update the translation
        mock.assert_not_called()
    
    def test_add_new_translation_request(self):
        new_translation = {'text_to_translate' : 'test_text'}
        response = self.client.post('/', json=new_translation)
        self.assertEquals(response.status, '201 CREATED')

    def test_add_new_translation_bad_request(self):
        new_translation = {'textranslate' : 'test_text'}
        response = self.client.post('/', json=new_translation)  
        print(response.data)
        self.assertEquals(response.status, '400 BAD REQUEST')