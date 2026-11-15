from copy import deepcopy
from datetime import datetime, timezone
import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from server.main import app,dataset,events_in_window,percentage

class WorkflowTests(unittest.TestCase):
    def setUp(self): self.client=TestClient(app)
    def test_calculation_and_unsafe_base(self):
        self.assertEqual(percentage('8898','9677'),'-8.1')
        self.assertIsNone(percentage(1,0))
        self.assertIsNone(percentage(1,-1))
    def test_source_chain(self):
        event=self.client.get('/api/events/infy-results-20261023').json()
        source=self.client.get('/api/evidence/'+event['evidence_id']).json()
        self.assertIn('8,898',source['passage'])
        self.assertIn('9,677',source['passage'])
        self.assertEqual(source['pdf_page'],4)
        self.assertEqual(len(source['sha256']),64)
        self.assertEqual(event['metric']['change_percent'],'-8.1')
    def test_duplicates_and_windows(self):
        data=deepcopy(dataset());data['events'].append(data['events'][0])
        now=datetime(2026,11,15,tzinfo=timezone.utc)
        self.assertEqual(len(events_in_window(data,30,now)),2)
        self.assertEqual(events_in_window(data,1,now),[])
    def test_missing_evidence_and_invalid_window(self):
        self.assertEqual(self.client.get('/api/evidence/missing').status_code,404)
        self.assertEqual(self.client.get('/api/briefing?days=0').status_code,422)
        routine=self.client.get('/api/events/infy-conference-20261104').json()
        self.assertIsNone(routine['evidence_id'])
        self.assertIn('not yet extracted',routine['availability'])
    def test_historical_example_and_database_failure(self):
        result=self.client.get('/api/briefing?historical=true').json()
        self.assertTrue(result['historical'])
        self.assertEqual(result['events'][0]['published_at'],'2026-10-23T16:08:26+05:30')
        with patch('server.main.psycopg.connect',side_effect=RuntimeError('secret-value')):
            response=self.client.get('/api/briefing')
        self.assertEqual(response.status_code,503)
        self.assertNotIn('secret-value',response.text)
    def test_public_diagnostic_protection(self):
        self.assertEqual(self.client.get('/verify?job_id=54ee3a54-ff5c-4206-b1d1-77066dd28ab2').status_code,401)
        self.assertEqual(self.client.post('/step',json={'job_id':'54ee3a54-ff5c-4206-b1d1-77066dd28ab2'}).status_code,401)

if __name__=='__main__': unittest.main()
