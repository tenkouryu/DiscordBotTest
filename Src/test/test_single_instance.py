import os
import unittest
import uuid

from function.security.single_instance import single_instance


class SingleInstanceTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt", "Windows named mutexes are required")
    def test_only_first_process_acquires_mutex(self):
        name = f"Local\\DiscordBot_servercontroller_test_{uuid.uuid4().hex}"

        with single_instance(name) as is_primary:
            self.assertTrue(is_primary)
            with single_instance(name) as is_duplicate:
                self.assertFalse(is_duplicate)


if __name__ == "__main__":
    unittest.main()