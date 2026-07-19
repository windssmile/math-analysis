"""Validate the machine-readable mathematics course outline."""

from __future__ import annotations

from collections.abc import Mapping
import sys
from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
OUTLINE = ROOT / "curriculum" / "outline.toml"

# The confirmed curriculum is deliberately stored as tuples so its structure
# cannot be changed accidentally while validating a submitted outline.
EXPECTED_BOOK_TITLE = "数学分析：理论、算法与模型"
EXPECTED_PARTS = (
    (
        ("part-01", 1, "实数、函数与分析语言", "有限符号怎样描述无限与连续？", 20, 4),
        (
            ("chapter-01", 1, "函数、集合与数学陈述"),
            ("chapter-02", 2, "实数系与完备性公理"),
            ("chapter-03", 3, "上界、下界与确界原理"),
            ("chapter-04", 4, "递推过程与无限逼近"),
        ),
    ),
    (
        ("part-02", 2, "数列极限与无限过程", "怎样判断一个无限过程最终稳定？", 26, 6),
        (
            ("chapter-05", 5, "数列极限与量词结构"),
            ("chapter-06", 6, "极限运算与序关系"),
            ("chapter-07", 7, "单调性、完备性与收敛准则"),
            ("chapter-08", 8, "子列、Cauchy 准则与上/下极限"),
        ),
    ),
    (
        ("part-03", 3, "函数极限、连续性与方程", "近似值能否保证真实解存在？", 20, 6),
        (
            ("chapter-09", 9, "函数极限与局部行为"),
            ("chapter-10", 10, "连续函数与连续运算"),
            ("chapter-11", 11, "闭区间上的整体性质"),
            ("chapter-12", 12, "零点、不动点与迭代求解"),
        ),
    ),
    (
        ("part-04", 4, "微分与局部线性化", "局部变化能告诉我们多少整体信息？", 24, 10),
        (
            ("chapter-13", 13, "导数、微分与局部线性模型"),
            ("chapter-14", 14, "求导法则、反函数与高阶导数"),
            ("chapter-15", 15, "微分中值定理"),
            ("chapter-16", 16, "Taylor 公式与余项"),
            ("chapter-17", 17, "优化、函数形态与 Newton 方法"),
        ),
    ),
    (
        ("part-05", 5, "积分、累积与数值求积", "局部贡献怎样重建整体总量？", 26, 10),
        (
            ("chapter-18", 18, "原函数与积分方法"),
            ("chapter-19", 19, "Riemann 积分与可积性"),
            ("chapter-20", 20, "微积分基本定理"),
            ("chapter-21", 21, "积分的几何与物理模型"),
            ("chapter-22", 22, "反常积分与数值求积"),
        ),
    ),
    (
        ("part-06", 6, "无穷级数与函数逼近", "无限叠加何时仍然可控？", 26, 10),
        (
            ("chapter-23", 23, "数项级数与基本判别"),
            ("chapter-24", 24, "正项、绝对与条件收敛"),
            ("chapter-25", 25, "函数列、函数项级数与一致收敛"),
            ("chapter-26", 26, "幂级数与解析表示"),
            ("chapter-27", 27, "多项式逼近与误差控制"),
        ),
    ),
    (
        ("part-07", 7, "Euclid 空间与多元微分", "多变量系统能否仍用线性对象作局部近似？", 26, 8),
        (
            ("chapter-28", 28, "Euclid 空间的几何与拓扑"),
            ("chapter-29", 29, "多元函数的极限与连续"),
            ("chapter-30", 30, "全微分、偏导数与导数映射"),
            ("chapter-31", 31, "高阶微分与多元 Taylor 公式"),
            ("chapter-32", 32, "隐函数、反函数与约束优化"),
        ),
    ),
    (
        ("part-08", 8, "重积分与空间测量", "怎样计算高维区域上的累积量？", 24, 8),
        (
            ("chapter-33", 33, "重积分的定义与可积性"),
            ("chapter-34", 34, "累次积分与计算"),
            ("chapter-35", 35, "重积分的变量代换"),
            ("chapter-36", 36, "反常重积分与质量、概率模型"),
        ),
    ),
    (
        ("part-09", 9, "曲线、曲面与向量分析", "边界上的信息怎样控制区域内部？", 24, 8),
        (
            ("chapter-37", 37, "参数曲线与曲线积分"),
            ("chapter-38", 38, "曲面与曲面积分"),
            ("chapter-39", 39, "Green 公式与平面场"),
            ("chapter-40", 40, "Gauss 公式与通量"),
            ("chapter-41", 41, "Stokes 公式与三大公式的统一"),
        ),
    ),
    (
        ("part-10", 10, "含参变量积分", "什么时候可以把极限或微分移进积分号？", 18, 6),
        (
            ("chapter-42", 42, "正常含参变量积分"),
            ("chapter-43", 43, "积分号下求导与积分"),
            ("chapter-44", 44, "含参反常积分的一致收敛"),
            ("chapter-45", 45, "Gamma、Beta 函数与参数敏感性"),
        ),
    ),
    (
        ("part-11", 11, "测度与 Lebesgue 积分", "Riemann 积分失效后，“大小”与“总量”应怎样重建？", 18, 6),
        (
            ("chapter-46", 46, "从长度问题到测度"),
            ("chapter-47", 47, "σ-代数与测度"),
            ("chapter-48", 48, "可测函数与收敛方式"),
            ("chapter-49", 49, "Lebesgue 积分"),
            ("chapter-50", 50, "三大收敛定理与 Riemann 理论比较"),
        ),
    ),
    (
        ("part-12", 12, "Fourier 级数初步", "复杂的周期现象能否分解为简单振动？", 18, 8),
        (
            ("chapter-51", 51, "正交函数系与最佳逼近"),
            ("chapter-52", 52, "Fourier 系数与逐点收敛"),
            ("chapter-53", 53, "Bessel、Parseval 与均方收敛"),
            ("chapter-54", 54, "周期模型、逼近误差与 Gibbs 现象"),
        ),
    ),
)


def load_outline(path: Path = OUTLINE) -> dict:
    """Load an outline TOML file using only the Python standard library."""
    with path.open("rb") as handle:
        return tomllib.load(handle)


def _is_strict_int(value: object) -> bool:
    """Return whether value is an int but not a bool."""
    return type(value) is int


def _hour_total(parts: list[Mapping[str, object]], key: str) -> int:
    return sum(
        value
        for part in parts
        if _is_strict_int(value := part.get(key))
    )


def _validate_string_field(
    item: Mapping[str, object], field: str, path: str, errors: list[str]
) -> None:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{field} must be a nonblank string")


def _validate_int_field(
    item: Mapping[str, object], field: str, path: str, errors: list[str]
) -> None:
    if not _is_strict_int(item.get(field)):
        errors.append(f"{path}.{field} must be an integer")


def _normalise_part(
    part: Mapping[str, object],
) -> tuple[tuple[object, ...], tuple[tuple[object, ...], ...]]:
    """Return the fields protected by the confirmed curriculum contract."""
    chapters = part.get("chapters", [])
    normalised_chapters = ()
    if isinstance(chapters, list):
        normalised_chapters = tuple(
            (chapter.get("id"), chapter.get("number"), chapter.get("title"))
            for chapter in chapters
        )
    return (
        (
            part.get("id"),
            part.get("number"),
            part.get("title"),
            part.get("question"),
            part.get("theory_hours"),
            part.get("applied_hours"),
        ),
        normalised_chapters,
    )


def _expected_part_for_chapter(chapter_id: object) -> str | None:
    for expected_part, expected_chapters in EXPECTED_PARTS:
        for expected_chapter in expected_chapters:
            if chapter_id == expected_chapter[0]:
                return expected_part[0]
    return None


def _validate_expected_contract(
    book: Mapping[str, object],
    parts: list[Mapping[str, object]],
    errors: list[str],
) -> None:
    if book.get("title") != EXPECTED_BOOK_TITLE:
        errors.append(
            "book.title must be exactly "
            f"{EXPECTED_BOOK_TITLE!r}, got {book.get('title')!r}"
        )

    for part_index, (expected_part, expected_chapters) in enumerate(EXPECTED_PARTS):
        if part_index >= len(parts):
            errors.append(f"{expected_part[0]} is missing from its required position")
            continue

        actual_part, actual_chapters = _normalise_part(parts[part_index])
        for field, expected_value, actual_value in zip(
            ("ID", "number", "title", "question", "theory_hours", "applied_hours"),
            expected_part,
            actual_part,
        ):
            if expected_value != actual_value:
                if field == "ID":
                    errors.append(
                        f"part {expected_part[1]} ID must be exactly "
                        f"{expected_value!r}, got {actual_value!r}"
                    )
                else:
                    errors.append(
                        f"{expected_part[0]} {field} must be exactly "
                        f"{expected_value!r}, got {actual_value!r}"
                    )

        if len(actual_chapters) != len(expected_chapters):
            errors.append(
                f"{expected_part[0]} must contain exactly "
                f"{len(expected_chapters)} confirmed chapters, got {len(actual_chapters)}"
            )
        for chapter_index, expected_chapter in enumerate(expected_chapters):
            if chapter_index >= len(actual_chapters):
                errors.append(
                    f"{expected_chapter[0]} is missing from {expected_part[0]}"
                )
                continue
            actual_chapter = actual_chapters[chapter_index]
            for field, expected_value, actual_value in zip(
                ("ID", "number", "title"), expected_chapter, actual_chapter
            ):
                if expected_value != actual_value:
                    if field == "ID":
                        errors.append(
                            f"chapter {expected_chapter[1]} ID must be exactly "
                            f"{expected_value!r}, got {actual_value!r}"
                        )
                    else:
                        errors.append(
                            f"{expected_chapter[0]} {field} must be exactly "
                            f"{expected_value!r}, got {actual_value!r}"
                        )

        for chapter_id, _, _ in actual_chapters:
            expected_owner = _expected_part_for_chapter(chapter_id)
            if expected_owner is not None and expected_owner != expected_part[0]:
                errors.append(
                    f"{chapter_id} must belong to {expected_owner}, got {expected_part[0]}"
                )


def validate_outline(data: object) -> list[str]:
    """Return all contract violations found in an outline data structure."""
    errors: list[str] = []
    if not isinstance(data, Mapping):
        return ["outline root must be a mapping"]

    schema_version = data.get("schema_version")
    if not _is_strict_int(schema_version) or schema_version != 1:
        errors.append("schema_version must be the integer 1")

    raw_book = data.get("book")
    if not isinstance(raw_book, Mapping):
        errors.append("book must be a mapping")
        book: Mapping[str, object] = {}
    else:
        book = raw_book
        _validate_string_field(book, "title", "book", errors)
        for field in ("theory_hours", "applied_hours", "total_hours"):
            _validate_int_field(book, field, "book", errors)

    raw_parts = data.get("parts")
    if not isinstance(raw_parts, list):
        errors.append("parts must be a list")
        raw_parts = []
    if len(raw_parts) != 12:
        errors.append("outline must contain exactly 12 parts")

    parts: list[Mapping[str, object]] = []
    for part_index, raw_part in enumerate(raw_parts):
        if not isinstance(raw_part, Mapping):
            errors.append(f"parts[{part_index}] must be a mapping")
            parts.append({"chapters": []})
            continue

        part_id = raw_part.get("id")
        part_path = (
            part_id
            if isinstance(part_id, str) and part_id.strip()
            else f"parts[{part_index}]"
        )
        _validate_string_field(raw_part, "id", part_path, errors)
        _validate_string_field(raw_part, "title", part_path, errors)
        _validate_int_field(raw_part, "number", part_path, errors)
        _validate_int_field(raw_part, "theory_hours", part_path, errors)
        _validate_int_field(raw_part, "applied_hours", part_path, errors)
        question = raw_part.get("question")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"{part_path} must have a guiding question")

        raw_chapters = raw_part.get("chapters")
        if not isinstance(raw_chapters, list):
            errors.append(f"{part_path}.chapters must be a list")
            raw_chapters = []

        chapters: list[Mapping[str, object]] = []
        for chapter_index, raw_chapter in enumerate(raw_chapters):
            chapter_path = f"{part_path}.chapters[{chapter_index}]"
            if not isinstance(raw_chapter, Mapping):
                errors.append(f"{chapter_path} must be a mapping")
                chapters.append({})
                continue
            _validate_string_field(raw_chapter, "id", chapter_path, errors)
            _validate_string_field(raw_chapter, "title", chapter_path, errors)
            _validate_int_field(raw_chapter, "number", chapter_path, errors)
            chapters.append(raw_chapter)

        safe_part = dict(raw_part)
        safe_part["chapters"] = chapters
        parts.append(safe_part)

    if [part.get("number") for part in parts] != list(range(1, 13)):
        errors.append("part numbers must be exactly 1..12")

    _validate_expected_contract(book, parts, errors)

    theory_hours = _hour_total(parts, "theory_hours")
    applied_hours = _hour_total(parts, "applied_hours")
    if theory_hours != 270:
        errors.append(f"theory hours must total 270, got {theory_hours}")
    if applied_hours != 90:
        errors.append(f"applied hours must total 90, got {applied_hours}")

    chapters: list[Mapping[str, object]] = []
    for part in parts:
        part_chapters = part.get("chapters", [])
        if isinstance(part_chapters, list):
            chapters.extend(part_chapters)

    if [chapter.get("number") for chapter in chapters] != list(range(1, 55)):
        errors.append("chapter numbers must be exactly 1..54")
    chapter_ids = [
        chapter_id
        for chapter in chapters
        if isinstance(chapter_id := chapter.get("id"), str)
    ]
    if len(chapter_ids) != len(set(chapter_ids)):
        errors.append("chapter IDs must be unique")
    for chapter in chapters:
        if not isinstance(chapter.get("title"), str) or not chapter["title"].strip():
            errors.append(f"{chapter.get('id', 'chapter-?')} must have a nonblank title")

    if book.get("theory_hours") != theory_hours:
        errors.append(
            "book.theory_hours must match summed theory hours "
            f"{theory_hours}, got {book.get('theory_hours')}"
        )
    if book.get("applied_hours") != applied_hours:
        errors.append(
            "book.applied_hours must match summed applied hours "
            f"{applied_hours}, got {book.get('applied_hours')}"
        )
    total_hours = theory_hours + applied_hours
    if book.get("total_hours") != total_hours:
        errors.append(
            "book.total_hours must match summed hours "
            f"{total_hours}, got {book.get('total_hours')}"
        )
    return errors


def main() -> int:
    errors = validate_outline(load_outline())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("outline valid: 12 parts, 54 chapters, 270+90=360 hours")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
