# Tracing — link project

**Trạng thái:** chưa gắn key. Xem phần "Việc cần làm" bên dưới.

| | |
|---|---|
| Backend | _(Braintrust hoặc LangSmith — điền sau khi tạo project)_ |
| Link project | _(dán link vào đây)_ |
| Run nào đã được trace | _(điền: judge lane / tutor lane / cả hai)_ |

## Tình trạng hạ tầng

Code tracing đã hoàn chỉnh và sẵn sàng — không cần sửa gì thêm:

- `eval/tracing.py` tự chọn backend theo biến môi trường: `BRAINTRUST_API_KEY` →
  Braintrust, `LANGSMITH_API_KEY` / `LANGCHAIN_API_KEY` → LangSmith, không có key nào →
  `_Noop()` (chạy bình thường nhưng không ghi gì).
- `eval/run_eval.py` và `eval/judge.py` đều đã gọi `_tracer.log_run(...)` cho mỗi row,
  kèm input, output, tool calls, token, cost, latency.
- Cả hai package `braintrust` và `langsmith` đã được cài trên máy.

Thiếu duy nhất: **API key**. Vì vậy mọi run cho tới thời điểm này chạy ở chế độ `_Noop` và
không sinh trace nào.

## Việc cần làm

1. Tạo project miễn phí trên [braintrust.dev](https://braintrust.dev) (hoặc
   [smith.langchain.com](https://smith.langchain.com)), lấy API key.
2. Thêm vào `.env` ở thư mục gốc:
   ```
   BRAINTRUST_API_KEY=sk-...
   BRAINTRUST_PROJECT=vlearn-tutor-eval
   ```
3. Chạy lại để sinh trace — **giữ nguyên `results-v1.jsonl`, không ghi đè**:
   ```powershell
   $env:PYTHONIOENCODING="utf-8"
   Copy-Item deliverables\evidence\results-v1.jsonl results.jsonl
   Copy-Item deliverables\evidence\labels.csv labels.csv

   python eval/judge.py                    # trace làn judge trên bộ chuẩn
   Copy-Item verdicts.jsonl deliverables\evidence\verdicts-v4-traced.jsonl

   python eval/run_eval.py                 # (tuỳ chọn) trace cả làn tutor
   Copy-Item results.jsonl deliverables\evidence\results-v3-traced.jsonl
   ```
4. Điền bảng ở đầu file này, rồi commit.

⚠️ **Đừng ghi đè `deliverables/evidence/results-v1.jsonl`.** Toàn bộ nhãn vàng, confusion
matrix và scorecard ở mục 5–6 của REPORT đều neo vào đúng bộ output đó. Chạy lại sẽ ra output
khác và làm hỏng cả chuỗi — nên mọi bản chạy mới phải lưu thành version riêng.
