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
    """Create datapath resources (logical switches or logical routers)."""

    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "router_create_args": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "minimum": 0,
                    },
                    "batch": {
                        "type": "integer",
                        "minimum": 1,
                    }
                },
                "additionalProperties": False,
            },
            "cleanup": {"type": "boolean"},
        },
        "additionalProperties": False,
    }

    DEFAULT_CONFIG = {
        "router_create_args": {"amount": 0},
        "cleanup": True,
    }

    RESOURCE_NAME_FORMAT = "lrouter_XXXXXX_XXXXXX"

    def setup(self):
        self._init_clients()

        router_create_args = self.config["router_create_args"]
        routers = self._add_routers(router_create_args)
        self.context["datapaths"] = {
            "routers": routers,
        }

    def _add_routers(self, router_create_args):
        routers = []
        ovn_nbctl = self._get_ovn_nbctl()
        for i in range(router_create_args["amount"]):
            name = self.generate_random_name()
            lr = ovn_nbctl.lrouter_add(name)
            routers.append(lr)
        return routers

    def cleanup(self):
        if not self.config["cleanup"]:
            return

    def _init_clients(self):
        # FIXME: Already exists in:
        # - OvnNorthbound.setup()
        # - OvsScenario.__init__()

        multihost_info = self.context["ovn_multihost"]
        for k, v in six.iteritems(multihost_info["controller"]):
            cred = v["credential"]
            self._controller_clients = ovsclients.Clients(cred)

        self._install_method = multihost_info["install_method"]

    def _get_controller_client(self, client_type="ssh"):
        # Returns a remote client for the controller node
        client = getattr(self._controller_clients, client_type)
        return client()

    def _get_ovn_nbctl(self):
        # Returns ovn-nbctl client for the controller sandbox
        ovn_nbctl = self._get_controller_client("ovn-nbctl")
        ovn_nbctl.set_sandbox("controller-sandbox", self._install_method)
        return ovn_nbctl
