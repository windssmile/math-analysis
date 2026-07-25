from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "content/chapters/chapter-12"
EXPECTED = [
 ("u-03-12-01","连续函数怎样保证取遍中间值？",1.75,.25,"intermediate-value-theorem"),
 ("u-03-12-03","有固定点是否意味着简单迭代会收敛？",1.5,.5,"fixed-points-and-iteration"),
 ("u-03-12-02","怎样把有根证明变成误差可证的算法？",1.25,.75,"certified-bisection"),
 ("u-03-12-04","不同存在与计算证书各自保证什么？",1.5,.5,"certificate-comparison"),
]
ANCHORS = {
 "u-03-12-01":("thm-u-03-12-01-zero","thm-u-03-12-01-intermediate-value"),
 "u-03-12-03":("thm-u-03-12-03-fixed-point","ex-u-03-12-03-oscillation"),
 "u-03-12-02":("alg-u-03-12-02-bisection","thm-u-03-12-02-bisection-error"),
 "u-03-12-04":("tbl-u-03-12-04-certificates","thm-u-03-12-04-certificate-boundary"),
}

class ChapterTwelveTests(unittest.TestCase):
 def test_final_units_hours_v2_and_anchors(self):
  th=ap=0
  for uid,title,t,a,suffix in EXPECTED:
   p=CHAPTER/f"{uid}-{suffix}.md"; self.assertTrue(p.is_file())
   text=p.read_text(); meta=yaml.safe_load(text.split("---\n",2)[1])
   self.assertEqual((title,t,a,2),(meta["title"],meta["hours"]["theory"],meta["hours"]["applied"],meta["content_standard"]))
   for anchor in ANCHORS[uid]: self.assertIn(f"{{#{anchor}}}",text)
   th+=t; ap+=a
  self.assertEqual((6,2),(th,ap))

 def test_navigation_and_map_use_final_order(self):
  config=(ROOT/"mkdocs.yml").read_text(); cmap=(ROOT/"content/course-map.md").read_text()
  chapter=cmap[cmap.index("### [第 12 章"):]
  self.assertIn("本章学时：8 小时（理论 6，应用 2）。",chapter)
  np=[]; mp=[]
  for uid,title,_,__,suffix in EXPECTED:
   path=f"chapters/chapter-12/{uid}-{suffix}.md"
   self.assertEqual(1,config.count(f"{title}: {path}"))
   self.assertEqual(1,chapter.count(f"[{title}]({path})"))
   np.append(config.index(path)); mp.append(chapter.index(path))
  self.assertEqual(sorted(np),np); self.assertEqual(sorted(mp),mp)

 def test_bisection_reuses_source_and_later_methods_are_absent(self):
  text=(CHAPTER/"u-03-12-02-certified-bisection.md").read_text()
  self.assertIn("mathbook_examples.bisection",text)
  self.assertNotIn("def bisect(",text)
  all_text="\n".join(p.read_text() for p in CHAPTER.glob("u-*.md"))
  for term in ("Newton","导数","中值定理","收敛阶"):
   self.assertNotIn(term,all_text.split("## 常见误区与后续")[0])

if __name__=="__main__": unittest.main()
