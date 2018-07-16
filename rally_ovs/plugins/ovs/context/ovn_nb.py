# Copyright 2016 Ebay Inc.
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

import six
from rally.common.i18n import _
from rally.common import logging
from rally import consts
from rally.task import context
from rally_ovs.plugins.ovs import ovnclients

LOG = logging.getLogger(__name__)


@context.configure(name="ovn_nb", order=120)
class OvnNorthboundContext(ovnclients.OvnClientMixin, context.Context):
    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": consts.JSON_SCHEMA,
        "properties": {
            "nbctl_daemon_mode": {"type": "boolean"},
        },
        "additionalProperties": True
    }

    DEFAULT_CONFIG = {
        "nbctl_daemon_mode": False,
    }

    @logging.log_task_wrapper(LOG.info, _("Enter context: `ovn_nb`"))
    def setup(self):
        super(OvnNorthboundContext, self).setup()

        ovn_nbctl = self.controller_client("ovn-nbctl")
        ovn_nbctl.set_sandbox("controller-sandbox", self.install_method)

        nbctl_daemon_mode = self.config["nbctl_daemon_mode"]
        if nbctl_daemon_mode:
            self._run_daemon()
            self._set_daemon_mode(True)

        lswitches = ovn_nbctl.show()

        self.context["ovn_nb"] = {
            "nbctl_daemon_mode": nbctl_daemon_mode,
            "lswitches": lswitches,
        }

    @logging.log_task_wrapper(LOG.info, _("Exit context: `ovn_nb`"))
    def cleanup(self):
        pass
