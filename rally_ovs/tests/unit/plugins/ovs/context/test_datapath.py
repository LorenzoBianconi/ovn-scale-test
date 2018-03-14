import ddt
import mock

from rally_ovs.plugins.ovs.context import datapath
from tests.unit import test


# case 1: just lrouter
# cast 2: just lswitch
# case 3: lrouter and lswitch
# case 4: lrouter and lswitch linked


@ddt.ddt
class DatapathTestCase(test.TestCase):

    def test__init__(self):
        context = datapath.Datapath({})

    def test_validate(self):
        config = {
            "router_create_args": {
                "amount": 0,
            },
        }
        datapath.Datapath.validate(config)
