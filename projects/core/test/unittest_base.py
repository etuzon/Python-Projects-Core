import unittest


class UnitTestBase(unittest.TestCase):

    def _verify_exception(self, exception_class_type, expected_message):
        with self.assertRaises(exception_class_type) as e:
            raise exception_class_type(expected_message)

        self.assertTrue(e.exception.message == expected_message)
