import unittest
from systemd_order_audit import audit
def unit(**kw):return {k:kw.get(k,[]) for k in ('after','before','requires','wants')}
class Contract(unittest.TestCase):
    def run_data(self,units,root='app.service'):return audit({'roots':[root],'units':units})
    def test_require_not_order(self):self.assertEqual(self.run_data({'app.service':unit(requires=['db.service']),'db.service':unit()})['edges'],[])
    def test_after_not_pull(self):self.assertEqual(self.run_data({'app.service':unit(after=['db.service']),'db.service':unit()})['active'],['app.service'])
    def test_after(self):self.assertEqual(self.run_data({'app.service':unit(after=['db.service'],requires=['db.service']),'db.service':unit()})['order'],['db.service','app.service'])
    def test_before(self):self.assertEqual(self.run_data({'app.service':unit(before=['db.service'],wants=['db.service']),'db.service':unit()})['order'],['app.service','db.service'])
    def test_cycle(self):
        r=self.run_data({'app.service':unit(after=['db.service'],requires=['db.service']),'db.service':unit(after=['app.service'])})
        self.assertFalse(r['acyclic']);self.assertEqual(r['cycle'],['app.service','db.service','app.service']);self.assertIsNone(r['order'])
    def test_self_cycle(self):self.assertEqual(self.run_data({'app.service':unit(after=['app.service'])})['cycle'],['app.service','app.service'])
    def test_missing_pull(self):self.assertFalse(self.run_data({'app.service':unit(requires=['db.service'])})['complete'])
    def test_missing_order(self):self.assertEqual(self.run_data({'app.service':unit(after=['db.service'])})['inactive_order_targets'],['db.service'])
    def test_transitive(self):self.assertEqual(self.run_data({'app.service':unit(requires=['db.service']),'db.service':unit(wants=['net.target']),'net.target':unit()})['active'],['app.service','db.service','net.target'])
    def test_pull_cycle_not_order_cycle(self):self.assertTrue(self.run_data({'app.service':unit(requires=['db.service']),'db.service':unit(requires=['app.service'])})['acyclic'])
    def test_unreachable_cycle(self):self.assertTrue(self.run_data({'app.service':unit(),'db.service':unit(after=['db.service'])})['acyclic'])
    def test_unknown_root(self):
        with self.assertRaises(ValueError):self.run_data({'db.service':unit()})
    def test_invalid_unit(self):
        with self.assertRaises(ValueError):self.run_data({'app.service':unit(wants=['../../etc/passwd'])})
    def test_duplicate_dependency(self):
        with self.assertRaises(ValueError):self.run_data({'app.service':unit(wants=['db.service','db.service'])})
    def test_snapshot_fields(self):
        with self.assertRaises(ValueError):audit({'roots':[],'units':{}})
    def test_downstream_blocked(self):
        r=self.run_data({'app.service':unit(after=['db.service'],requires=['db.service','child.service']),'db.service':unit(after=['app.service']),'child.service':unit(after=['app.service'])})
        self.assertEqual(r['blocked'],['app.service','child.service','db.service'])
