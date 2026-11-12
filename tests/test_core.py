import unittest,copy,json
from hermes_decision_expiry import run
DEMO={'now': '2026-11-12T12:00:00Z', 'evidence': [{'id': 'delivery-days', 'value': 30, 'observed_at': '2026-11-11T12:00:00Z', 'expires_at': '2026-11-13T12:00:00Z'}], 'decisions': [{'id': 'supplier-A', 'requirements': [{'evidence': 'delivery-days', 'operator': 'lte', 'expected': 20}]}]}
class DomainTests(unittest.TestCase):
 def test_changed_reason_invalidates(self):
  self.assertEqual(run(DEMO)['decisions'][0]['state'],'invalidated')
 def test_expired_does_not_mean_failed(self):
  x=run(dict(DEMO,now='2026-11-13T12:00:00Z'));self.assertEqual(x['decisions'][0]['state'],'unconfirmed');self.assertEqual(x['decisions'][0]['conditions'][0]['reason'],'expired_evidence')
 def test_missing_evidence_is_unknown(self):
  x=run(dict(DEMO,evidence=[]));self.assertEqual(x['decisions'][0]['state'],'unconfirmed');self.assertFalse(x['notifications_sent'])
