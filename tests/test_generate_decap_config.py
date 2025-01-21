import unittest
from src.utils.generate_decap_config import generate_decap_config, analyze_theme, optimize_for_decap, create_config_yaml
import os

class TestGenerateDecapConfig(unittest.TestCase):

    def setUp(self):
        # Set up a temporary directory for testing
        self.test_dir = 'test_theme'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, 'index.html'), 'w') as f:
            f.write('<html><nav>Menu</nav><div class="hero">Welcome</div><footer>Footer</footer></html>')

    def tearDown(self):
        # Clean up the temporary directory after tests
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_analyze_theme(self):
        elements = analyze_theme(self.test_dir)
        self.assertIn('index.html', elements['navigation'])
        self.assertIn('index.html', elements['hero'])
        self.assertIn('index.html', elements['footer'])

    def test_optimize_for_decap(self):
        optimize_for_decap(self.test_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'data', 'navigation.yaml')))

    def test_create_config_yaml(self):
        config = create_config_yaml(self.test_dir)
        self.assertIn('backend', config)
        self.assertIn('collections', config)

    def test_generate_decap_config(self):
        result = generate_decap_config(self.test_dir)
        self.assertEqual(result, "Decap CMS config generation complete")
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'config.yml')))

if __name__ == '__main__':
    unittest.main() 