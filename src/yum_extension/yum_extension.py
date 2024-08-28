##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

from litp.core.extension import ModelExtension
from litp.core.model_type import ItemType, Property, PropertyType
from litp.core.validators import RestrictedPropertiesValidator
from litp.core.validators import PropertyValidator, ItemValidator
from litp.core.validators import ValidationError

import re


class YumExtension(ModelExtension):
    """
    Allows for the modelling of a 'yum-repository' on a node.
    """
    restricted_properties = ["LITP", "OS", "3PP",
                             "UPDATES", "CBA",
                             "LITP_PLUGINS"]
    restricted_props_path = [r"/3pp",
                             r"/6(\.6)?/(os|updates)/x86_64/Packages",
                             r"/litp",
                             r"/litp_plugins"]

    def define_property_types(self):
        property_types = [
            PropertyType(
                "yum_name",
                regex=r'^[a-zA-Z0-9\-\._]+$',
                validators=[
                    RestrictedPropertiesValidator(self.restricted_properties),
                ]
            ),
            PropertyType(
                "yum_base_url",
                regex=r'^((http|https|file|ftp)://[a-zA-Zf0-9\./\-_:]+)$'
            ),
            PropertyType(
                "yum_ms_url_path",
                regex=r"^/[A-Za-z0-9\-\._/#:\s*]+$",
                validators=[
                    RestrictedPathsValidator(self.restricted_props_path),
                ]
            )
        ]
        return property_types

    def define_item_types(self):
        item_types = []

        item_types.append(
            ItemType(
                "yum-repository",
                extend_item="software-item",
                name=Property(
                    "yum_name",
                    prop_description="Yum Repository Name.",
                    required=True,
                    updatable_plugin=False,
                    updatable_rest=False
                ),
                base_url=Property(
                    "yum_base_url",
                    prop_description="Yum Repository URL.",
                ),
                ms_url_path=Property(
                    "yum_ms_url_path",
                    site_specific=True,
                    prop_description="Yum Repository Path on MS."
                ),
                cache_metadata=Property(
                    "basic_boolean",
                    prop_description="Enables Yum metadata caching. "
                    "If false, sets metadata_expire to 0 seconds, "
                    "if true the property "
                    "defaults to "
                    "the value in yum.conf ",
                    default="false",
                ),
                checksum=Property(
                    "checksum_hex_string",
                    prop_description="Checksum for yum repository",
                    updatable_plugin=True,
                    updatable_rest=False
                ),
                validators=[MutuallyExclusivePropertyValidator(
                    ['base_url', 'ms_url_path'])],
                item_description=(
                    "The client-side Yum repository configuration."
                ),
            ))
        return item_types


class RestrictedPathsValidator(PropertyValidator):
    """Validates that restricted property values are not supplied.
    """

    default_message = '"%s" is a restricted value for this property.'

    def __init__(self, restricted_prop_values, custom_message=None):
        """
        Restricts the allowed property values.

        :param restricted_prop_values: Restricted property values.
        :type  restricted_prop_values: list

        :param custom_message: Custom message, must have 1 str argument.
        :type  custom_message: str

        :returns: None or ValidationError

        """
        super(RestrictedPathsValidator, self).__init__()
        self.prop_values = restricted_prop_values
        self.message_template = custom_message or self.default_message

    def validate(self, property_value):
        for prop in self.prop_values:
            if (re.match(prop + r'/?$', property_value, re.I)):
                prop_print = '/' + property_value.split('/', 1)[1]
                msg = (self.message_template % prop_print)
                err = ValidationError(error_message=msg)
                return err


class MutuallyExclusivePropertyValidator(ItemValidator):
    """Validates that exactly one of the properties is defined.
    """

    def __init__(self, prop_names):
        """
        MutuallyExclusivePropertyValidator.

        Validates that neither or one of the required properties is defined.

        :param prop_names: Names of the mutually exclusive properties.
        :type  prop_names: list

        :returns: None or ValidatonError

        """
        super(MutuallyExclusivePropertyValidator, self).__init__()
        self.prop_set = set(prop_names)

    def validate(self, properties):
        values = [x for x in self.prop_set if properties.get(x)]
        if set(values) == self.prop_set:
            msg = 'Only one of "%s" property must be set.' % \
                  '" or "'.join(self.prop_set)
            err = ValidationError(error_message=msg)
            return err
