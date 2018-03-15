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

    @mock.patch("rally_ovs.plugins.ovs.ovsclients_impl.OvnNbctl.create_client")
    def test_setup(self, mock_create_client):
        ctx = {
            "task": {
                "uuid": "fake-task-uuid",
            },
            "ovn_multihost": {
                "controller": {
                    "fake-controller-node": {
                        "name": "fake-controller-node",
                        "credential": {
                            "user": "fake-user",
                            "host": "fake-host",
                            "port": -1,
                            "key": "fake-key",
                            "password": "fake-password",
                        },
                    },
                },
                "install_method": "fake-install-method",
            },

        }

        mock_ovnbctl = mock.MagicMock()
        mock_ovnbctl.lrouter_add.return_value = {"name": "lrouter_TEST"}
        mock_create_client.return_value = mock_ovnbctl

        dp_context = datapath.Datapath(ctx)

        dp_context.setup()

        expected_lrouters = [{"name": "lrouter_TEST"}]
        actual_lrouters = dp_context.context["datapaths"]["lrouters"]

        self.assertSequenceEqual(sorted(expected_lrouters),
                                 sorted(actual_lrouters))
