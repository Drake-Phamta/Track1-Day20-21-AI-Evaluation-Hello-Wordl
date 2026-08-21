# AI Support Log — Hiếu (Rubric & Judge Lead)

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | Viết 2 hàm `check_followup_count` + `check_quote_length` vào `eval/code_checks.py` | Antigravity IDE: gợi ý code, signature `(rec, section_tokens)`, logic đếm follow-up và word count | Chạy `python tests/test_eval_kit.py` → 44/44 pass; đọc code từng dòng và verify logic với SYSTEM_PROMPT (tutor.py:30,36) |
| 2 | Thảo luận rubric 5 tiêu chí | Antigravity IDE: gợi ý tên tiêu chí, ví dụ pass/fail, blocker hay không | Đọc lại `tutor/tutor.py` contract (dòng 38–48) để đảm bảo rubric phản ánh đúng contract thật; điều chỉnh định nghĩa `groundedness` sau khi nhận thấy AI gợi ý quá chung chung |
| 3 | Thiết kế routing map | Antigravity IDE: đề xuất bảng code/judge/người | Tự kiểm tra: thử nghĩ xem tiêu chí nào có thể viết thành `if` statement — nếu có thì dùng code; bác bỏ đề xuất "dùng LLM cho schema_valid" vì json.loads() là đủ |
| 4 | Viết judge_prompt v2 | Antigravity IDE: gợi ý rule mới dựa trên phân tích confusion matrix v1 | Đọc v1 vs v2 side by side, kiểm tra logic từng rule có cover đúng edge case của sc-13/14/15/16 không |
| 5 | Gán nhãn 20 row (labels-hieu.csv) | Không dùng AI — tự đọc dataset và expected_behavior | Tự đọc từng scenario, đối chiếu `expected_scope` + `expected_behavior` trong metadata, ghi note lý do cho mỗi nhãn uncertain |

- **Phần AI gợi ý mà mình bác bỏ:**
  - AI ban đầu đề xuất `check_followup_count` dùng `section_tokens` để so sánh nội dung follow-up với corpus — bác bỏ vì không cần thiết (contract chỉ yêu cầu đúng 3 câu, không rỗng, không trùng input; kiểm tra "chất lượng" là việc của `pedagogy` do người chấm).
  - AI đề xuất `pedagogy` có thể giao LLM judge sau khi calibrate đủ — bác bỏ vì vòng 1 cho thấy judge quá dễ tính với follow-up quality; giữ cho người an toàn hơn.

- **Phần hoàn toàn tự làm:**
  - Gán nhãn 20 row độc lập (labels-hieu.csv) — không tham khảo AI hay thành viên nhóm khác.
  - Quyết định "one thing to fix" trong judge_prompt v2 (chỉ sửa 1 concept: out-of-scope pass definition) — AI gợi ý sửa nhiều hơn nhưng mình giữ nguyên tắc "sửa ít, đo nhiều".
