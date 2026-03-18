"""Tests for utils.enhance."""
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from hugoifier.utils.enhance import (
    _chunks,
    _find_baseof,
    _parse_ai_json,
    _parse_frontmatter,
    _read_body,
    _read_site_context,
    _seo_og_tags,
    _update_frontmatter,
    alt_text,
    generate,
    seo,
)


class TestReadSiteContext(unittest.TestCase):
    def test_reads_title_from_hugo_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "My Test Site"\n')
            ctx = _read_site_context(tmp)
            self.assertEqual(ctx["title"], "My Test Site")

    def test_reads_title_from_config_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "config.toml"), "w") as f:
                f.write('title = "Legacy Config"\n')
            ctx = _read_site_context(tmp)
            self.assertEqual(ctx["title"], "Legacy Config")

    def test_hugo_toml_takes_precedence_over_config_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Hugo"\n')
            with open(os.path.join(tmp, "config.toml"), "w") as f:
                f.write('title = "Config"\n')
            ctx = _read_site_context(tmp)
            self.assertEqual(ctx["title"], "Hugo")

    def test_reads_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Site"\ndescription = "A fine site"\n')
            ctx = _read_site_context(tmp)
            self.assertEqual(ctx["description"], "A fine site")

    def test_finds_content_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "content", "blog"))
            os.makedirs(os.path.join(tmp, "content", "about"))
            ctx = _read_site_context(tmp)
            self.assertIn("blog", ctx["content_sections"])
            self.assertIn("about", ctx["content_sections"])

    def test_defaults_when_no_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx = _read_site_context(tmp)
            self.assertEqual(ctx["title"], "My Hugo Site")
            self.assertEqual(ctx["description"], "")
            self.assertEqual(ctx["content_sections"], [])

    def test_handles_missing_content_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx = _read_site_context(tmp)
            self.assertEqual(ctx["content_sections"], [])
            self.assertEqual(ctx["sample_content"], "")

    def test_reads_sample_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = os.path.join(tmp, "content")
            os.makedirs(content)
            with open(os.path.join(content, "page.md"), "w") as f:
                f.write("---\ntitle: Test\n---\n\nSome content.\n")
            ctx = _read_site_context(tmp)
            self.assertIn("Some content.", ctx["sample_content"])


class TestParseFrontmatter(unittest.TestCase):
    def test_parses_yaml_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "page.md")
            with open(path, "w") as f:
                f.write("---\ntitle: Hello\ndate: 2024-01-01\ndraft: false\n---\n\nBody.\n")
            result = _parse_frontmatter(path)
            self.assertEqual(result["title"], "Hello")
            self.assertFalse(result["draft"])

    def test_returns_empty_dict_for_missing_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bare.md")
            with open(path, "w") as f:
                f.write("Just some text.\n")
            self.assertEqual(_parse_frontmatter(path), {})

    def test_returns_empty_dict_for_missing_file(self):
        self.assertEqual(_parse_frontmatter("/nonexistent/path.md"), {})

    def test_returns_empty_dict_for_empty_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty_fm.md")
            with open(path, "w") as f:
                f.write("---\n\n---\nBody.\n")
            self.assertEqual(_parse_frontmatter(path), {})


class TestUpdateFrontmatter(unittest.TestCase):
    def test_adds_new_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "post.md")
            with open(path, "w") as f:
                f.write("---\ntitle: Hello\n---\nBody text here.\n")
            _update_frontmatter(path, {"description": "A great post"})
            fm = _parse_frontmatter(path)
            self.assertEqual(fm["description"], "A great post")
            self.assertEqual(fm["title"], "Hello")

    def test_preserves_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "post.md")
            with open(path, "w") as f:
                f.write("---\ntitle: Hello\n---\nBody text here.\n")
            _update_frontmatter(path, {"description": "desc"})
            body = _read_body(path)
            self.assertIn("Body text here.", body)

    def test_updates_existing_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "post.md")
            with open(path, "w") as f:
                f.write("---\ntitle: Old Title\n---\nBody.\n")
            _update_frontmatter(path, {"title": "New Title"})
            fm = _parse_frontmatter(path)
            self.assertEqual(fm["title"], "New Title")

    def test_noop_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bare.md")
            with open(path, "w") as f:
                f.write("No frontmatter here.\n")
            _update_frontmatter(path, {"description": "test"})
            with open(path, "r") as f:
                self.assertEqual(f.read(), "No frontmatter here.\n")


class TestReadBody(unittest.TestCase):
    def test_extracts_body_after_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "post.md")
            with open(path, "w") as f:
                f.write("---\ntitle: Test\n---\n\nThe body content.\n")
            body = _read_body(path)
            self.assertEqual(body, "The body content.")

    def test_returns_full_content_without_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bare.md")
            with open(path, "w") as f:
                f.write("Just text, no frontmatter.\n")
            body = _read_body(path)
            self.assertIn("Just text", body)

    def test_returns_empty_for_missing_file(self):
        self.assertEqual(_read_body("/nonexistent/path.md"), "")


class TestFindBaseof(unittest.TestCase):
    def test_finds_baseof_in_layouts(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseof = os.path.join(tmp, "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(baseof))
            with open(baseof, "w") as f:
                f.write("<html></html>")
            self.assertEqual(_find_baseof(tmp), baseof)

    def test_finds_baseof_in_themes(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseof = os.path.join(tmp, "themes", "mytheme", "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(baseof))
            with open(baseof, "w") as f:
                f.write("<html></html>")
            self.assertEqual(_find_baseof(tmp), baseof)

    def test_prefers_layouts_over_themes(self):
        with tempfile.TemporaryDirectory() as tmp:
            layouts_baseof = os.path.join(tmp, "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(layouts_baseof))
            with open(layouts_baseof, "w") as f:
                f.write("<html>layouts</html>")
            theme_baseof = os.path.join(tmp, "themes", "t", "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(theme_baseof))
            with open(theme_baseof, "w") as f:
                f.write("<html>theme</html>")
            self.assertEqual(_find_baseof(tmp), layouts_baseof)

    def test_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(_find_baseof(tmp))


class TestParseAiJson(unittest.TestCase):
    def test_parses_valid_json(self):
        result = _parse_ai_json('{"key": "value"}')
        self.assertEqual(result, {"key": "value"})

    def test_parses_fenced_json(self):
        result = _parse_ai_json('```json\n{"key": "value"}\n```')
        self.assertEqual(result, {"key": "value"})

    def test_parses_json_embedded_in_prose(self):
        result = _parse_ai_json('Here is the result:\n{"title": "Hello"}\nDone.')
        self.assertEqual(result, {"title": "Hello"})

    def test_returns_none_for_invalid(self):
        self.assertIsNone(_parse_ai_json("not json at all"))

    def test_returns_none_for_json_list(self):
        self.assertIsNone(_parse_ai_json('[1, 2, 3]'))

    def test_returns_none_for_empty_string(self):
        self.assertIsNone(_parse_ai_json(""))

    def test_parses_fenced_json_without_language(self):
        result = _parse_ai_json('```\n{"a": 1}\n```')
        self.assertEqual(result, {"a": 1})


class TestChunks(unittest.TestCase):
    def test_splits_evenly(self):
        result = list(_chunks([1, 2, 3, 4], 2))
        self.assertEqual(result, [[1, 2], [3, 4]])

    def test_handles_remainder(self):
        result = list(_chunks([1, 2, 3, 4, 5], 2))
        self.assertEqual(result, [[1, 2], [3, 4], [5]])

    def test_empty_list(self):
        result = list(_chunks([], 3))
        self.assertEqual(result, [])

    def test_chunk_larger_than_list(self):
        result = list(_chunks([1, 2], 10))
        self.assertEqual(result, [[1, 2]])

    def test_chunk_size_one(self):
        result = list(_chunks([1, 2, 3], 1))
        self.assertEqual(result, [[1], [2], [3]])


class TestSeoOgTags(unittest.TestCase):
    def test_injects_og_tags(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseof = os.path.join(tmp, "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(baseof))
            with open(baseof, "w") as f:
                f.write("<html><head><title>Test</title></head><body></body></html>")
            result = _seo_og_tags(tmp)
            self.assertIn("OG tags", result)
            with open(baseof, "r") as f:
                html = f.read()
            self.assertIn("og:title", html)
            self.assertIn("og:description", html)
            self.assertIn("og:url", html)

    def test_skips_if_already_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseof = os.path.join(tmp, "layouts", "_default", "baseof.html")
            os.makedirs(os.path.dirname(baseof))
            with open(baseof, "w") as f:
                f.write('<html><head><meta property="og:title" content="x" /></head></html>')
            result = _seo_og_tags(tmp)
            self.assertIn("already present", result)

    def test_returns_message_when_no_baseof(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _seo_og_tags(tmp)
            self.assertIn("No baseof.html found", result)


class TestGenerate(unittest.TestCase):
    @patch("hugoifier.utils.enhance.call_ai")
    def test_creates_content_files(self, mock_ai):
        ai_response = json.dumps({
            "blog/first-post.md": "---\ntitle: First Post\ndate: 2026-03-17\ndescription: A post\n---\n\nHello world.\n",
            "blog/second-post.md": "---\ntitle: Second Post\ndate: 2026-03-17\ndescription: Another post\n---\n\nGoodbye world.\n",
        })
        mock_ai.return_value = ai_response

        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            result = generate(tmp, prompt="Write blog posts")
            self.assertIn("Generated 2", result)
            self.assertTrue(os.path.exists(os.path.join(tmp, "content", "blog", "first-post.md")))
            self.assertTrue(os.path.exists(os.path.join(tmp, "content", "blog", "second-post.md")))
            with open(os.path.join(tmp, "content", "blog", "first-post.md"), "r") as f:
                self.assertIn("Hello world.", f.read())

    @patch("hugoifier.utils.enhance.call_ai")
    def test_handles_invalid_ai_response(self, mock_ai):
        mock_ai.return_value = "not valid json"
        with tempfile.TemporaryDirectory() as tmp:
            result = generate(tmp, prompt="Write posts")
            self.assertIn("Could not generate content", result)

    @patch("hugoifier.utils.enhance.call_ai")
    def test_from_file_reads_example(self, mock_ai):
        ai_response = json.dumps({
            "page.md": "---\ntitle: New Page\ndate: 2026-03-17\ndescription: New\n---\n\nContent.\n",
        })
        mock_ai.return_value = ai_response

        with tempfile.TemporaryDirectory() as tmp:
            example = os.path.join(tmp, "example.md")
            with open(example, "w") as f:
                f.write("---\ntitle: Example\n---\n\nExample content.\n")
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            result = generate(tmp, from_file=example)
            self.assertIn("Generated 1", result)
            # Verify call_ai was called with the example content
            prompt_arg = mock_ai.call_args[0][0]
            self.assertIn("Example content.", prompt_arg)


class TestSeo(unittest.TestCase):
    @patch("hugoifier.utils.enhance.call_ai")
    def test_finds_missing_descriptions(self, mock_ai):
        mock_ai.return_value = json.dumps({"My Post": "A short description."})
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            content = os.path.join(tmp, "content")
            os.makedirs(content)
            path = os.path.join(content, "post.md")
            with open(path, "w") as f:
                f.write("---\ntitle: My Post\n---\n\nSome body text.\n")
            result = seo(tmp)
            self.assertIn("Added meta descriptions to 1", result)
            fm = _parse_frontmatter(path)
            self.assertEqual(fm["description"], "A short description.")

    @patch("hugoifier.utils.enhance.call_ai")
    def test_skips_files_with_descriptions(self, mock_ai):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            content = os.path.join(tmp, "content")
            os.makedirs(content)
            with open(os.path.join(content, "post.md"), "w") as f:
                f.write("---\ntitle: My Post\ndescription: Already set\n---\n\nBody.\n")
            result = seo(tmp)
            self.assertIn("already have descriptions", result)
            mock_ai.assert_not_called()

    def test_handles_missing_content_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = seo(tmp)
            self.assertIn("No content/", result)


class TestAltText(unittest.TestCase):
    @patch("hugoifier.utils.enhance.call_ai")
    def test_finds_images_without_alt(self, mock_ai):
        mock_ai.return_value = json.dumps({"logo.png": "Company logo"})
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            layouts = os.path.join(tmp, "layouts")
            os.makedirs(layouts)
            tpl = os.path.join(layouts, "index.html")
            with open(tpl, "w") as f:
                f.write('<html><body><img src="logo.png"></body></html>')
            result = alt_text(tmp)
            self.assertIn("Added alt text to 1", result)
            with open(tpl, "r") as f:
                html = f.read()
            self.assertIn('alt="Company logo"', html)

    @patch("hugoifier.utils.enhance.call_ai")
    def test_skips_images_with_alt(self, mock_ai):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            layouts = os.path.join(tmp, "layouts")
            os.makedirs(layouts)
            tpl = os.path.join(layouts, "index.html")
            with open(tpl, "w") as f:
                f.write('<html><body><img src="logo.png" alt="A logo"></body></html>')
            result = alt_text(tmp)
            self.assertIn("All images already have alt text", result)
            mock_ai.assert_not_called()

    @patch("hugoifier.utils.enhance.call_ai")
    def test_finds_images_with_empty_alt(self, mock_ai):
        mock_ai.return_value = json.dumps({"photo.jpg": "A photo"})
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            layouts = os.path.join(tmp, "layouts")
            os.makedirs(layouts)
            tpl = os.path.join(layouts, "page.html")
            with open(tpl, "w") as f:
                f.write('<html><body><img src="photo.jpg" alt=""></body></html>')
            result = alt_text(tmp)
            self.assertIn("Added alt text to 1", result)

    def test_no_templates_returns_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "hugo.toml"), "w") as f:
                f.write('title = "Test"\n')
            result = alt_text(tmp)
            self.assertIn("All images already have alt text", result)


if __name__ == "__main__":
    unittest.main()
