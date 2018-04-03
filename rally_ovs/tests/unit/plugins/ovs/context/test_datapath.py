# Copyright 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ddt
import mock

from jsonschema.exceptions import ValidationError
from rally_ovs.plugins.ovs.context.datapath import Datapath
from rally_ovs.tests.unit.plugins.ovs import utils
from tests.unit import test

@ddt.ddt
class DatapathTestCase(test.TestCase):

    @ddt.data({},
              {"amount": 0},
              {"amount": 1},
              {"amount": 2},
              {"amount": 0, "batch": 1},
              {"amount": 1, "batch": 1},
              {"amount": 2, "batch": 1},
              {"amount": 2, "batch": 2})
    def test_valid_router_config(self, router_create_args):
        config = {"router_create_args": router_create_args}
        Datapath.validate(config)

    @ddt.data({"amount": -1},
              {"amount": 0, "batch": 0},
              {"amount": 1, "batch": -1})
    def test_invalid_router_config(self, router_create_args):
        config = {"router_create_args": router_create_args}
        with self.assertRaisesRegexp(ValidationError, ""): # Ignore message
              Datapath.validate(config)

    def test_init_default(self):
        context = utils.get_fake_context(datapath={})
        Datapath(context)

    @ddt.data({"router_create_args": {"amount": 1},
               "routers": [{"name": "lrouter_1"}]},
              {"router_create_args": {"amount": 2},
               "routers": [{"name", "lrouter_1"},
                           {"name": "lrouter_2"}]},
              {"router_create_args": {"amount": 3},
               "routers": [{"name": "lrouter_1"},
                           {"name": "lrouter_2"},
                           {"name": "lrouter_3"}]})
    @ddt.unpack
    @mock.patch("rally_ovs.plugins.ovs.ovsclients_impl.OvnNbctl.create_client")
    def test_add_only_routers(self, mock_create_client,
                              router_create_args, routers):
        mock_client = mock_create_client.return_value
        mock_client.lrouter_add.side_effect = routers

        config = {
            "datapath": {
                "router_create_args": router_create_args,
            },
        }
        context = utils.get_fake_context(**config)
        dp_context = Datapath(context)
        dp_context.setup()

        expected_routers = routers
        actual_routers = dp_context.context["datapaths"]["routers"]
        self.assertSequenceEqual(sorted(expected_routers),
                                 sorted(actual_routers))
