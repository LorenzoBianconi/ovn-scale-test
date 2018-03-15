# TODO:
# - Use constants for order?
# - Require ovn_multihost context when common validators are available

import six

from rally.common import logging
from rally.task import context
from rally.task import validation
from rally import consts

from rally_ovs.plugins.ovs import ovsclients

LOG = logging.getLogger(__name__)


@context.configure(name="datapath", order=115)
class Datapath(context.Context):
    """
    Create datapath resources (logical switches or logical routers).
    """

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "router_create_args": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "minimum": 0
                    },
                    "batch": {
                        "type": "integer",
                        "minimum": 1
                    }
                },
                "additionalProperties": False
            }
        },
        "additionalProperties": False
    }

    DEFAULT_CONFIG = {
    }

    RESOURCE_NAME_FORMAT = "lrouter_XXXXXX_XXXXXX"

    def setup(self):
        self._init_clients()

        ovn_nbctl = self.controller_client("ovn-nbctl")
        ovn_nbctl.set_sandbox("controller-sandbox", self.install_method)

        lrouters = []

        name = self.generate_random_name()
        lrouter = ovn_nbctl.lrouter_add(name)
        lrouters.append(lrouter)

        self.context["datapaths"] = { "lrouters": lrouters }

    def cleanup(self):
        pass

    def _init_clients(self):
        # FIXME: This code is duplicated in OvnNorthbound.setup() and
        # OvsScenario.__init__(). Create a helper?
        multihost_info = self.context["ovn_multihost"]

        for k, v in six.iteritems(multihost_info["controller"]):
            cred = v["credential"]
            self._controller_clients = ovsclients.Clients(cred)

        self.install_method = multihost_info["install_method"]

    def controller_client(self, client_type="ssh"):
        client = getattr(self._controller_clients, client_type)
        return client()
