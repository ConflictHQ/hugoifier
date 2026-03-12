"""Tests for utils.decapify."""
import os
import tempfile
import unittest

from hugoifier.utils.decapify import (
    _build_collections,
    _infer_fields_for_file,
    _infer_fields_for_folder,
    _parse_frontmatter,
    _sanitize_color,
    _widget_for_value,
    decapify,
)


class TestSanitizeColor(unittest.TestCase):
    def test_valid_hex6(self):
        self.assertEqual(_sanitize_color("#2e3748"), "#2e3748")

    def test_valid_hex3(self):
        self.assertEqual(_sanitize_color("#fff"), "#fff")

    def test_uppercase(self):
        self.assertEqual(_sanitize_color("#AABBCC"), "#AABBCC")

    def test_invalid_falls_back(self):
        self.assertEqual(_sanitize_color("red"), "#2e3748")
        self.assertEqual(_sanitize_color("javascript:alert(1)"), "#2e3748")
        self.assertEqual(_sanitize_color("#gggggg"), "#2e3748")


class TestWidgetForValue(unittest.TestCase):
    def test_bool(self):
        self.assertEqual(_widget_for_value(True), "boolean")
        self.assertEqual(_widget_for_value(False), "boolean")

    def test_number(self):
        self.assertEqual(_widget_for_value(42), "number")
        self.assertEqual(_widget_for_value(3.14), "number")

    def test_list(self):
        self.assertEqual(_widget_for_value([]), "list")
        self.assertEqual(_widget_for_value(["a", "b"]), "list")

    def test_string_default(self):
        self.assertEqual(_widget_for_value("hello"), "string")
        self.assertEqual(_widget_for_value(None), "string")


class TestParseFrontmatter(unittest.TestCase):
    def test_parses_yaml_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\ntitle: Hello\ndate: 2024-01-01\ndraft: false\n---\n\nBody text.\n")
            path = f.name
        try:
            result = _parse_frontmatter(path)
            self.assertEqual(result["title"], "Hello")
            self.assertEqual(result["draft"], False)
        finally:
            os.unlink(path)

    def test_empty_on_missing_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("No frontmatter here.\n")
            path = f.name
        try:
            self.assertEqual(_parse_frontmatter(path), {})
        finally:
            os.unlink(path)

    def test_empty_on_missing_file(self):
        self.assertEqual(_parse_frontmatter("/nonexistent/path.md"), {})


class TestInferFields(unittest.TestCase):
    def _make_md(self, dirpath, name, frontmatter):
        path = os.path.join(dirpath, name)
        with open(path, "w") as f:
            f.write("---\n")
            for k, v in frontmatter.items():
                f.write(f"{k}: {v!r}\n")
            f.write("---\n\nBody.\n")
        return path

    def test_folder_fields_include_known_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_md(tmp, "post1.md", {"title": "Hello", "date": "2024-01-01", "tags": ["a"]})
            fields = _infer_fields_for_folder(tmp, ["post1.md"])
            names = [f["name"] for f in fields]
            self.assertIn("title", names)
            self.assertIn("date", names)
            self.assertIn("tags", names)
            self.assertIn("body", names)

    def test_folder_fields_always_end_with_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._make_md(tmp, "post.md", {"title": "Test"})
            fields = _infer_fields_for_folder(tmp, ["post.md"])
            self.assertEqual(fields[-1]["name"], "body")
            self.assertEqual(fields[-1]["widget"], "markdown")

    def test_file_fields_include_all_frontmatter_keys(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("---\ntitle: About\nsubtitle: Us\n---\n")
            path = f.name
        try:
            fields = _infer_fields_for_file(path)
            names = [fi["name"] for fi in fields]
            self.assertIn("title", names)
            self.assertIn("subtitle", names)
            self.assertIn("body", names)
        finally:
            os.unlink(path)


class TestBuildCollections(unittest.TestCase):
    def test_folder_collection_from_md_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            blog = os.path.join(tmp, "blog")
            os.makedirs(blog)
            for i in range(3):
                with open(os.path.join(blog, f"post{i}.md"), "w") as f:
                    f.write("---\ntitle: Post\n---\n")
            collections = _build_collections(tmp)
            self.assertEqual(len(collections), 1)
            self.assertEqual(collections[0]["name"], "blog")
            self.assertIn("folder", collections[0])

    def test_file_collection_from_index_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            about = os.path.join(tmp, "about")
            os.makedirs(about)
            with open(os.path.join(about, "_index.md"), "w") as f:
                f.write("---\ntitle: About\n---\n")
            collections = _build_collections(tmp)
            self.assertEqual(len(collections), 1)
            self.assertIn("files", collections[0])

    def test_recursive_md_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            deep = os.path.join(tmp, "blog", "2024")
            os.makedirs(deep)
            with open(os.path.join(deep, "post.md"), "w") as f:
                f.write("---\ntitle: Deep Post\n---\n")
            collections = _build_collections(tmp)
            self.assertEqual(len(collections), 1)
            self.assertEqual(collections[0]["name"], "blog")

    def test_default_collection_when_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            collections = _build_collections(tmp)
            self.assertEqual(len(collections), 1)
            self.assertEqual(collections[0]["name"], "pages")

    def test_nonexistent_dir_returns_default(self):
        collections = _build_collections("/nonexistent/content")
        self.assertEqual(len(collections), 1)
        self.assertEqual(collections[0]["name"], "pages")


class TestDecapify(unittest.TestCase):
    def test_creates_admin_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            content = os.path.join(tmp, "content")
            os.makedirs(content)
            with open(os.path.join(content, "_index.md"), "w") as f:
                f.write("---\ntitle: Home\n---\n")
            result = decapify(tmp)
            self.assertIn("complete", result.lower())
            self.assertTrue(os.path.exists(os.path.join(tmp, "static", "admin", "index.html")))
            self.assertTrue(os.path.exists(os.path.join(tmp, "static", "admin", "config.yml")))

    def test_admin_index_escapes_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            decapify(tmp, cms_name='<script>alert("xss")</script>')
            with open(os.path.join(tmp, "static", "admin", "index.html")) as f:
                html = f.read()
            self.assertNotIn("<script>alert", html)
            self.assertIn("&lt;script&gt;", html)

    def test_invalid_color_falls_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            decapify(tmp, cms_color="not-a-color")
            with open(os.path.join(tmp, "static", "admin", "index.html")) as f:
                html = f.read()
            self.assertIn("#2e3748", html)


if __name__ == "__main__":
    unittest.main()
