from copy import deepcopy
from datetime import datetime, timezone
import unittest
from fastapi.testclient import TestClient
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

if __name__=='__main__': unittest.main()
