import unittest
from server.market import normalise,alert_values,classify
from server.research import validate_answer
from server.documents import safe_url

class FeatureTests(unittest.TestCase):
    def test_duplicate_and_revised_filings(self):
        row={'symbol':'INFY','an_dt':'23-Oct-2026 16:00:00','attchmntFile':'https://nsearchives.nseindia.in/a.pdf','desc':'Financial Results'}
        self.assertEqual(len(normalise([row,row],'INFY')),1)
        self.assertEqual(len(normalise([row,dict(row,attchmntFile='https://nsearchives.nseindia.in/revised.pdf')],'INFY')),2)
        self.assertEqual(classify('Unrecognised disclosure'),'review')
    def test_alert_baseline_excludes_latest(self):
        rows=[{'date':f'2026-10-{i+1:02}','close':100,'volume':100} for i in range(20)]
        rows.append({'date':'2026-10-21','close':104,'volume':250})
        a=alert_values({'rows':rows})
        self.assertEqual(a['price_change_percent'],4)
        self.assertEqual(a['volume_multiple'],2.5)
        self.assertEqual(a['volume_baseline'],100)
        self.assertTrue(a['price_triggered']);self.assertTrue(a['volume_triggered'])
        self.assertFalse(alert_values({'rows':rows[:20]})['available'])
        self.assertFalse(alert_values({'rows':rows,'corporate_actions':{'splits':{'1792454400':{}}}})['available'])
    def test_source_quotes_reject_invented_citations(self):
        evidence=[{'id':'real','text':'Revenue increased during the reported period.'}]
        good={'claims':[{'source_id':'real','quote':'Revenue increased during the reported period.','text':'Revenue increased.','kind':'reported'}]}
        self.assertEqual(len(validate_answer(good,evidence)['claims']),1)
        with self.assertRaises(ValueError):validate_answer({'claims':[dict(good['claims'][0],source_id='invented')]},evidence)
        with self.assertRaises(ValueError):validate_answer({'claims':[dict(good['claims'][0],quote='This quotation does not exist in the source.')]},evidence)
    def test_arbitrary_fetch_rejected(self):
        for url in ['http://127.0.0.1/a','https://evil.example/a.pdf','https://www.bseindia.com@evil.example/a','https://www.bseindia.com:8443/a']:
            with self.assertRaises(ValueError):safe_url(url)
