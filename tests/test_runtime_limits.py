import os
import unittest
from unittest.mock import patch
from contextlib import contextmanager
from server import research

@contextmanager
def available_lock(name):
    yield True

class RuntimeLimits(unittest.TestCase):
    def test_prediction_rejected_before_evidence_or_model(self):
        with patch.object(research.documents,'passages') as retrieve,patch.object(research,'reserve') as reserve:
            with self.assertRaisesRegex(ValueError,'tomorrow'):
                research.run('INFY','stock prediction tomorrow?','test')
            retrieve.assert_not_called();reserve.assert_not_called()

    def test_ready_sources_with_unmatched_question_are_not_processing_error(self):
        with patch.object(research,'configured',return_value=True),patch.object(research.documents,'readiness',return_value={'ready':True}),patch.object(research.documents,'passages',return_value=[]),patch.object(research,'reserve') as reserve:
            with self.assertRaisesRegex(ValueError,'Documents are ready'):
                research.run('INFY','Unmatched fundamental topic','test')
            reserve.assert_not_called()

    def test_quota_exhaustion_prevents_request(self):
        with patch.dict(os.environ,{'GEMINI_REQUESTS_PER_DAY':'20','GEMINI_REQUESTS_PER_MINUTE':'2'}),patch.object(research.store,'lock',available_lock),patch.object(research.store,'get',return_value={'count':20,'times':[]}),patch.object(research.store,'put') as write:
            with self.assertRaisesRegex(ValueError,'Daily free-tier'):
                research.reserve()
            write.assert_not_called()

    def test_billing_confirmation_and_fixed_model_required(self):
        with patch.dict(os.environ,{'GEMINI_API_KEY':'test-only-placeholder','GEMINI_FREE_TIER_CONFIRMED':'false'}):
            self.assertFalse(research.configured())
        with patch.dict(os.environ,{'GEMINI_API_KEY':'test-only-placeholder','GEMINI_FREE_TIER_CONFIRMED':'true','GEMINI_MODEL':'unapproved-model'}):
            self.assertFalse(research.configured())
