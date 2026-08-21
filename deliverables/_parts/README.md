# _parts — vùng viết REPORT chống conflict

`deliverables/REPORT.md` là **1 file 7 mục**. 3 người sửa song song = conflict chắc chắn.

**Luật:** trong lúc làm, **KHÔNG AI mở `REPORT.md`**. Mỗi người chỉ sửa file mục của mình ở đây.

| File | Owner duy nhất | Phase |
|---|---|---|
| `01-input-grid.md` | **Chi** | P1 |
| `02-dataset.md` | **Chi** | P1 |
| `03-rubric.md` | **Hiếu** | P3 |
| `04-routing.md` | **Hiếu** | P3 |
| `05-calibration.md` | **Hiếu** | P4 |
| `06-scorecard.md` | **Tuấn Anh** | P5–P6 |
| `07-verdict.md` | **Tuấn Anh** | P6 |
| `00-header.md` | Tuấn Anh | — |

## Cách viết

- **Giữ nguyên** heading `## N. Tên mục` và khối blockquote hướng dẫn (đó là khung câu hỏi chấm điểm).
- Thay chỗ `...`, `___`, và các bảng rỗng `| | | |` bằng nội dung thật.
- Mỗi mục phải có **quyết định + VÌ SAO**, và số liệu phải dẫn được xuống file trong `evidence/`.
- Đừng thêm `---` ở cuối file — script ghép tự chèn.

## Ghép (chỉ Tuấn Anh chạy, ở T+125)

```powershell
$env:PYTHONIOENCODING="utf-8"
python assemble_report.py --check   # liệt kê mục nào còn placeholder chưa điền
python assemble_report.py           # ghi đè deliverables/REPORT.md
```

`--check` exit code 1 nếu còn mục chưa xong → dùng nó làm cổng kiểm trước khi nộp.
