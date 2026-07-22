from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.fix_page_titles import fix_page_title, source_page_title


class PageTitleTests(unittest.TestCase):
    def test_reads_heading_title_without_its_anchor(self) -> None:
        with TemporaryDirectory() as directory:
            source = Path(directory) / "appendix.qmd"
            source.write_text(
                "# Python 知识桥：函数、循环与异常 {#bridge-python}\n\n正文\n",
                encoding="utf-8",
            )

            self.assertEqual(
                "Python 知识桥：函数、循环与异常",
                source_page_title(source),
            )

    def test_replaces_filename_title_and_preserves_site_suffix(self) -> None:
        with TemporaryDirectory() as directory:
            page = Path(directory) / "unit.html"
            page.write_text(
                "<html><head><title>unit – 数学分析：理论、算法与模型</title>"
                "</head><body><h1>原正文</h1></body></html>",
                encoding="utf-8",
            )

            fix_page_title(page, "数列怎样记录无限过程？")

            self.assertEqual(
                "<html><head><title>数列怎样记录无限过程？ – "
                "数学分析：理论、算法与模型</title></head>"
                "<body><h1>原正文</h1></body></html>",
                page.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
