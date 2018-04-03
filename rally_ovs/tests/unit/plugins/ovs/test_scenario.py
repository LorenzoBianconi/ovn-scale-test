from tests.unit import test

from rally_ovs.plugins.ovs.scenarios import ovn_sandbox
from rally_ovs.tests.unit.plugins.ovs import utils

class ExploratoryScenarioTestCase(test.TestCase):

    def test_ovn_sandbox(self):
        context = utils.get_fake_context()
        scenario_inst = ovn_sandbox.OvnSandbox(context)
