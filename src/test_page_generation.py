from unittest import TestCase
from page_generation import GeneratePage


class TestGeneratePageExtractTitle(TestCase):
    def test_valid_header_basic(self):
        result = GeneratePage.extract_title("# Hello World")
        self.assertEqual(result, "Hello World")

    def test_valid_header_with_extra_spaces(self):
        result = GeneratePage.extract_title("#   Title with spaces  ")
        self.assertEqual(result, "Title with spaces")

    def test_valid_header_with_numbers(self):
        result = GeneratePage.extract_title("#123")
        self.assertEqual(result, "123")

    def test_valid_header_with_extra_hashes(self):
        result = GeneratePage.extract_title("# ### Multiple hashes")
        self.assertEqual(result, "### Multiple hashes")

    def test_no_header_raises_error(self):
       with self.assertRaises(ValueError):
            GeneratePage.extract_title("No header here")

    def test_subheader_raises_error(self):
        with self.assertRaises(ValueError):
            GeneratePage.extract_title("## Subheader")

    def test_empty_string_raises_error(self):
        with self.assertRaises(ValueError):
            GeneratePage.extract_title("")

    def test_whitespace_only_raises_error(self):
        with self.assertRaises(ValueError):
            GeneratePage.extract_title("   ")
