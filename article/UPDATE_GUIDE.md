# 论文 Markdown → Word 快速更新指南

## 核心原则

每次修改 `论文初稿.md` 后，根据改动范围选择最小代价的更新方式。

---

## 方式一：局部文字修改（最快，< 2 分钟）

**适用场景**：修改某段文字、调整表述、补充几句话

**步骤**：

1. 找到 md 中修改的段落，确认其在 Word 中的位置（属于哪一节）
2. 用 `search_and_replace` 精准替换：

```
mcp__word-document-server__search_and_replace
filename: article/2120223396.docx
old_text: <旧文字（取改动段落的前20字）>
new_text: <新文字>
```

3. 完成，无需重建文档。

---

## 方式二：替换整个段落块（中等，5 分钟）

**适用场景**：某个二级标题下的内容大幅重写

**步骤**：

1. 用 `find_text_in_document` 定位目标段落所在行号
2. 用 `delete_paragraph` 删除旧段落（可能需多次）
3. 用 `insert_line_or_paragraph_near_text` 在指定位置插入新段落：

```
mcp__word-document-server__insert_line_or_paragraph_near_text
filename: article/2120223396.docx
anchor_text: <该段落前一行的文字>
position: after
text: <新段落内容>
font_name: 仿宋
font_size: 12
```

---

## 方式三：新增/修改表格（10 分钟）

**适用场景**：表格数据更新、新增表格

**步骤**：

1. 用 `find_text_in_document` 找到表格标题位置（如"表1"）
2. 删除旧表格相关段落（表标题 + 旧表 + 数据来源）
3. 重新插入：

```
# 表标题
mcp__word-document-server__add_paragraph（在锚点后插入）

# 新表格
mcp__word-document-server__add_table
rows: N
cols: M
data: [[...], [...], ...]

# 数据来源
mcp__word-document-server__add_paragraph
```

---

## 方式四：全文重建（最彻底，30 分钟）

**适用场景**：结构大调整（新增/删除整章）、初稿改动 > 30%

**步骤**：

1. 删除旧文件（备份为 `2120223396_backup.docx`）
2. 重新执行建档流程（参照本次建档记录）
3. 可让 Claude 直接读取最新 `论文初稿.md` 全量写入

**建档 prompt 模板**：

```
请读取 article/论文初稿.md，
将全文按南京财经大学经管法文格式规范（参考 article/参考模板.md）
写入新的 Word 文件 article/2120223396.docx。
格式要求：
- 论文题目：二号黑体加粗
- 一级标题：四号黑体加粗
- 二级标题：小四仿宋加粗
- 正文/三级及以下：小四仿宋
- 摘要/参考文献：五号仿宋（10pt）
- 英文：Times New Roman
- 页边距：上下2.5cm，左3.0cm，右2.0cm
- 行距：28pt
```

---

## 快速定位工具

修改前先用以下工具确认位置，避免改错地方：

```
# 搜索关键词位置
mcp__word-document-server__find_text_in_document
filename: article/2120223396.docx
search_text: <关键词>

# 查看文档大纲（确认章节结构）
mcp__word-document-server__get_document_outline
filename: article/2120223396.docx

# 获取全文文本（确认当前内容）
mcp__word-document-server__get_document_text
filename: article/2120223396.docx
```

---

## 常见修改场景速查

| 改动类型 | 推荐方式 | 大概用时 |
|---------|---------|---------|
| 改几个词/句 | 方式一 search_and_replace | < 2 min |
| 改一整段 | 方式二 delete + insert | 5 min |
| 改摘要 | 方式一（摘要较短，全量替换） | 2 min |
| 更新参考文献 | 方式二（按序号定位删改） | 5~10 min |
| 更新表格数据 | 方式三 | 10 min |
| 新增一节 | 方式二（在章节末插入） | 10 min |
| 删除/新增整章 | 方式四 全文重建 | 30 min |

---

## 备份建议

每次大改前执行：

```bash
cp article/2120223396.docx article/2120223396_$(date +%Y%m%d).docx
```
