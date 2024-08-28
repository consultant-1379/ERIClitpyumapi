##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

# -*- coding: latin-1 -*-

from litp.core.plugin import Plugin
from litp.core.execution_manager import CallbackTask
from litp.core.validators import ValidationError

class ValidationPlugin(Plugin):
    """
    LITP Mock volmgr plugin to provide snapshots tasks in ats
    """

    def _dummy_callback(self,context):
        pass
    def create_configuration(self, plugin_api_context):
        item = plugin_api_context.query("yum-repository")
        return [
            CallbackTask(item[0], "Test task",
                         self._dummy_callback, ['ms'],
                         'lv','lvs')]

    def update_model(self, plugin_api_context):
        repo = plugin_api_context.query('yum-repository')[0]

        valid_string =    '0123456789ABCDEFabcdef0000000123'

        repo.checksum = valid_string

