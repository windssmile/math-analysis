import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "content" / "chapters"
MATRIX = ROOT / "docs" / "reviews" / "2026-07-31-parts-01-09-interface-matrix.md"

# Stable chapter-level witnesses selected from actual prerequisites.book declarations.
# These are deliberately semantic witnesses, not a brittle equality check over prose.
CHAPTER_CONTRACT = {
    1: (), 2: (), 3: ("chapter-02",), 4: ("chapter-03",),
    5: ("chapter-04",), 6: ("chapter-05",), 7: ("chapter-03", "chapter-05"),
    8: ("chapter-05", "chapter-07"), 9: ("chapter-05",), 10: ("chapter-09",),
    11: ("u-02-08-02", "u-03-10-01"), 12: ("u-02-07-03", "u-03-10-01"),
    13: ("u-03-09-02", "u-03-10-01"), 14: ("u-04-13-03",),
    15: ("u-03-11-02", "u-04-13-02"), 16: ("u-04-14-04", "u-04-15-01"),
    17: ("u-04-15-02", "u-04-16-02"), 18: ("u-04-14-05",),
    19: ("u-01-03-02", "u-02-05-02"), 20: ("u-05-19-04",),
    21: ("u-05-19-04", "u-05-20-03"), 22: ("u-05-19-04", "u-05-20-03"),
    23: ("数列极限",), 24: ("Cauchy 尾部",), 25: ("上确界", "一致收敛"),
    26: ("根值判别", "上极限"), 27: ("一致连续", "一致收敛"),
    28: ("邻域",), 29: ("Fréchet 微分", "多元极限与连续"),
    30: ("Fréchet 微分", "链式法则"), 31: ("Fréchet 微分", "Jacobian"),
    32: ("紧致性", "隐函数定理"), 33: ("Riemann 积分", "紧致性"),
    34: ("一元 Riemann 积分",), 35: ("Fréchet 微分", "Jacobian"),
    36: ("反常积分", "累次积分"), 37: ("Riemann 积分", "向量函数微分"),
    38: ("局部参数化", "叉积"), 39: ("Jacobian", "u-09-37-03"),
    40: ("u-09-38-04", "u-09-39-01"), 41: ("u-09-37-03", "u-09-38-01"),
}


def metadata(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---\n", 2)[1])


def matrix_rows() -> list[list[str]]:
    text = MATRIX.read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        if re.match(r"^\|\s*\d+\s*\|", line):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


class Parts0109CrossConsistencyTests(unittest.TestCase):
    def test_matrix_covers_each_real_chapter_once_with_complete_contract_fields(self):
        guides = sorted(CHAPTERS.glob("chapter-*/index.md"))
        self.assertEqual(41, len(guides))
        rows = matrix_rows()
        self.assertEqual(list(range(1, 42)), [int(row[0]) for row in rows])
        self.assertTrue(all(len(row) == 7 for row in rows))
        for row in rows:
            self.assertTrue(all(row[i] and row[i] != "—" for i in range(2, 7)), row)

    def test_real_core_pages_ids_counts_and_publication_order_match_matrix(self):
        pages = sorted(CHAPTERS.glob("chapter-*/u-*.md"))
        ids = [metadata(page)["unit_id"] for page in pages]
        # Parse every physical unit front matter.  The current tree has 189 such
        # pages while the publication contract says 186; the matrix records that
        # discrepancy for human review instead of silently redefining core scope.
        self.assertEqual(189, len(pages))
        self.assertEqual(189, len(set(ids)))
        self.assertIn("186 个学习单元、337 学时", (ROOT / "README.md").read_text(encoding="utf-8"))

        matrix_order = [int(row[0]) for row in matrix_rows()]
        course_map = (ROOT / "content" / "course-map.md").read_text(encoding="utf-8")
        map_order = [int(n) for n in re.findall(r"\{#chapter-(\d{2})\}", course_map)]
        nav = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        nav_order = [int(n) for n in re.findall(r"chapters/chapter-(\d{2})/index\.md", nav)]
        # Every published course-map chapter stays in matrix order.  Missing
        # headings are separately surfaced in the matrix's human-review notes.
        self.assertEqual(map_order, [n for n in matrix_order if n in set(map_order)])
        self.assertEqual(matrix_order, nav_order)

    def test_chapter_contract_witnesses_are_declared_and_recorded(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        for chapter, witnesses in CHAPTER_CONTRACT.items():
            declared = []
            for page in (CHAPTERS / f"chapter-{chapter:02d}").glob("u-*.md"):
                declared.extend(str(x) for x in metadata(page)["prerequisites"]["book"])
            if not witnesses:
                self.assertFalse(declared, f"chapter {chapter} unexpectedly declares book prerequisites")
                self.assertIn("无", rows[chapter][3])
            for witness in witnesses:
                self.assertIn(witness, declared, f"chapter {chapter}: registry drift")
                self.assertIn(witness, rows[chapter][3], f"chapter {chapter}: matrix misses witness")

    def test_locked_cross_part_interfaces_and_boundaries(self):
        rows = {int(row[0]): row for row in matrix_rows()}
        def joined(chapter):
            return " ".join(rows[chapter][2:])

        for consumer in (5, 7): self.assertIn("第 3 章", joined(consumer))
        for consumer in (12, 15, 19, 28): self.assertIn("第 11 章", joined(consumer))
        for consumer in (20, 22, 33): self.assertIn("第 19 章", joined(consumer))
        for consumer in (26, 27): self.assertIn("第 25 章", joined(consumer))
        self.assertNotIn("第 26", rows[25][3]); self.assertNotIn("第 27", rows[25][3])
        for consumer in (31, 35, 38): self.assertIn("第 29 章", joined(consumer))
        for chapter in range(37, 42): self.assertIn("第 33–35 章", joined(chapter))
        for consumer in (39, 40, 41): self.assertRegex(joined(consumer), r"第 (37|38) 章")
        self.assertIn("第 39 章", joined(41))
        self.assertNotIn("第 41", rows[40][3])

        text = MATRIX.read_text(encoding="utf-8")
        self.assertIn("附录不作为任何核心章节或单元的前置", text)
        self.assertNotRegex(text, r"第\s*42\s*章|chapter-42|u-\d{2}-42-")


if __name__ == "__main__":
    unittest.main()
