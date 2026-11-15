"""Offline HTTP boundary tests. Do NOT establish cloud/database integration."""
import json
import os
import threading
import unittest
from http.server import HTTPServer
from unittest.mock import patch
import requests
from scripts.host_probe import Handler

class ProbeBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1',0),Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health_does_not_claim_integration(self):
        with patch.dict(os.environ,{},clear=True):
            response = requests.get(self.base+'/healthz',timeout=3)
        self.assertEqual(response.status_code,200)
        self.assertFalse(response.json()['configured'])

    def test_unauthorised_write_rejected(self):
        with patch.dict(os.environ,{'PROBE_TOKEN':'x'*32},clear=True):
            response = requests.post(self.base+'/step',json={},timeout=3)
        self.assertEqual(response.status_code,401)

    def test_missing_credentials_report_names_only(self):
        with patch.dict(os.environ,{'PROBE_TOKEN':'x'*32},clear=True):
            response = requests.post(self.base+'/step',json={},headers={'Authorization':'Bearer '+'x'*32},timeout=3)
        self.assertEqual(response.status_code,503)
        self.assertIn('DATABASE_URL',response.json()['missing_keys'])
        self.assertNotIn('x'*32,response.text)

    def test_invalid_identifier_rejected_before_database(self):
        fake={key:'test-only-not-a-credential' for key in ['DATABASE_URL','AWS_ENDPOINT_URL_S3','AWS_REGION','AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY','DOCUMENT_BUCKET']}
        fake['PROBE_TOKEN']='x'*32
        with patch.dict(os.environ,fake,clear=True):
            response=requests.post(self.base+'/step',json={'job_id':'not-a-uuid'},headers={'Authorization':'Bearer '+'x'*32},timeout=3)
        self.assertEqual(response.status_code,400)

if __name__ == '__main__':
    unittest.main()
