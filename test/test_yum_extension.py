##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################


import unittest
from yum_extension.yum_extension import YumExtension
from yum_extension.yum_extension import RestrictedPathsValidator
from litp.core.validators import ValidationError



class TestYumExtension(unittest.TestCase):

    def setUp(self):
        self.ext = YumExtension()

    def test_property_types_registered(self):
        prop_types_expected = ['yum_name', 'yum_base_url', 'yum_ms_url_path']
        prop_types = [pt.property_type_id for pt in
                      self.ext.define_property_types()]
        self.assertEquals(prop_types_expected, prop_types)

    def test_item_types_registered(self):
        item_types_expected = ['yum-repository']
        item_types = [it.item_type_id for it in
                      self.ext.define_item_types()]
        self.assertEquals(item_types_expected, item_types)

    def test_RestrictedPathsValidator(self):
        # Assert that only extension's item types
        # are defined.
        validator = RestrictedPathsValidator(self.ext.restricted_props_path)

        ok1 = validator.validate("/LITP_PLUGINS/abc/")
        self.assertEquals(ok1, None)

        error1 = validator.validate("/LITP_PLUGINS/")
        ref_error1 = ValidationError(error_message = ('"/LITP_PLUGINS/" is a restricted value for this property.'))
        self.assertEquals(error1,ref_error1)

        error2 = validator.validate("/3PP")
        ref_error2 = ValidationError(error_message = ('"/3PP" is a restricted value for this property.'))
        self.assertEquals(error2,ref_error2)

        error3 = validator.validate("/litp")
        ref_error3 = ValidationError(error_message = ('"/litp" is a restricted value for this property.'))
        self.assertEquals(error3,ref_error3)

        error4 = validator.validate("/LITP/")
        ref_error4 = ValidationError(error_message = ('"/LITP/" is a restricted value for this property.'))
        self.assertEquals(error4,ref_error4)

        correct1 = validator.validate("/test/opt/")
        self.assertEquals(None,correct1)

        correct2 = validator.validate("/")
        self.assertEquals(None,correct2)

        correct3 = validator.validate("/LITP123/opt")
        self.assertEquals(None,correct3)

        correct4 = validator.validate("/litp_plugins123/opt")
        self.assertEquals(None,correct4)

        correct4 = validator.validate("/3pp123/opt")
        self.assertEquals(None,correct4)

        correct5 = validator.validate("litp_plugins123/opt") #This will fail the regex
        self.assertEquals(None,correct5)

        correct5 = validator.validate("3pp123/opt") #This will fail the regex
        self.assertEquals(None,correct5)

        correct5 = validator.validate("") #This will fail the regex
        self.assertEquals(None,correct5)

        correct6 = validator.validate("/docs/opt") #Docs is allowed
        self.assertEquals(None,correct6)


if __name__ == '__main__':
    unittest.main()
