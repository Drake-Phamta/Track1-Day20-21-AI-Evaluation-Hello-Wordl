# Tracing — link project

| | |
|---|---|
| Backend | Braintrust |
| Project | `ai-evaluation` |
| **Link project** | **https://www.braintrust.dev/app/HieuNM05/p/ai-evaluation** |
| Người tạo | Nguyễn Minh Hiếu |

## Trạng thái — nói thẳng

Project Braintrust **đã được tạo** và link ghi ở trên. Nhưng cần nói rõ giới hạn, vì bài này
là bài về đo lường trung thực:

- **Chưa có file evidence nào chứng minh trace đã được log.** Nếu một vòng eval chạy có
  tracing, `run_eval.py` in ra dòng `Đã log 20 trace lên braintrust (project '...')` ở cuối,
  và ta sẽ có thêm một bản `results-*.jsonl` sinh ra từ vòng chạy đó. Trong `evidence/` hiện
  không có bản nào như vậy.
- **`results-v1.jsonl` — bộ chuẩn của toàn bộ scorecard — được chạy TRƯỚC khi có key**, nên
  chắc chắn không có trace. Chạy lại để lấy trace sẽ sinh output khác và làm hỏng nhãn vàng,
  confusion matrix và mọi số liệu ở mục 5–6, nên nhóm chủ động **không** chạy lại.
- **Link project có thể yêu cầu đăng nhập.** Braintrust mặc định giới hạn project trong
  organization; người ngoài mở link có thể gặp trang đăng nhập thay vì dashboard.

**Kết luận trung thực:** hạ tầng tracing đã sẵn sàng và project đã tồn tại, nhưng nhóm
**chưa chứng minh được bằng evidence trong repo** rằng các vòng eval đã được log trace.
Đây là mục checklist duy nhất nhóm không hoàn thành trọn vẹn, và ghi lại ở đây thay vì
tuyên bố đã xong.

## Hạ tầng — đã hoàn chỉnh, không cần sửa gì

- `eval/tracing.py` tự chọn backend theo biến môi trường: `BRAINTRUST_API_KEY` → Braintrust,
  `LANGSMITH_API_KEY` / `LANGCHAIN_API_KEY` → LangSmith, không có key → `_Noop()`.
- `eval/run_eval.py` và `eval/judge.py` đều gọi `_tracer.log_run(...)` cho mỗi row, kèm
  input, output, tool calls, token, cost, latency.
- Cả hai package `braintrust` và `langsmith` đã được cài.

## Cách tái lập (cho vòng sau)

```powershell
$env:PYTHONIOENCODING="utf-8"
# .env: BRAINTRUST_API_KEY=sk-...  va  BRAINTRUST_PROJECT=ai-evaluation

Copy-Item deliverables\evidence\results-v1.jsonl results.jsonl
Copy-Item deliverables\evidence\labels.csv labels.csv
python eval/judge.py            # trace lan judge tren bo chuan, KHONG dung toi results-v1
Copy-Item verdicts.jsonl deliverables\evidence\verdicts-v4-traced.jsonl
```

⚠️ **Đừng ghi đè `deliverables/evidence/results-v1.jsonl`.** Nhãn vàng, confusion matrix và
scorecard ở mục 5–6 đều neo vào đúng bộ output đó. Mọi bản chạy mới lưu thành version riêng.
