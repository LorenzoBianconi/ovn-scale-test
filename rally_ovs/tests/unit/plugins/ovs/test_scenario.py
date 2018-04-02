from tests.unit import test

from rally_ovs.plugins.ovs.scenarios.ovn_sandbox import OvnSandbox


class ExploratoryScenarioTestCase(test.TestCase):

    def get_fake_context(self, **config):
        fake_credential = {
            "user": "fake_user",
            "host": "fake_host",
            "port": -1,
            "key": "fake_key",
            "password": "fake_password",
        }

        return {
            "task": {
                "uuid": "fake_task_uuid",
            },
            "ovn_multihost": {
                "controller": {
                    "fake-controller-node": {
                        "name": "fake-controller-node",
                        "credential": fake_credential,
                    },
                },
                "farms": {
                    "fake-farm-node-0": {
                        "name": "fake-farm-node-0",
                        "credential": fake_credential,
                    },
                },
                "install_method": "fake_install_method",
            },
            "config": config,
        }

    def test_get_default_context(self):
        pass

    def test_ovn_sandbox(self):
        context_inst = self.get_fake_context(config={})
        scenario_inst = OvnSandbox(context_inst)
