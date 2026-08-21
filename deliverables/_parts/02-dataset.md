<!-- OWNER: Chi -- chi Chi duoc sua file nay. Ghep vao REPORT.md o T+125. -->
<!-- DRAFT do Tuan Anh sinh tu dataset-v1.jsonl luc T+20. Chi review + chinh. -->

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

**Số câu: 20** (`deliverables/evidence/dataset-v1.jsonl`). Phủ **15/20 ô** của lưới 4×5.

Năm ô để trống là các tổ hợp không thực tế, bỏ có chủ đích chứ không phải quên:
*học viên mới × deixis* và *học viên mới × adversarial* (người mới chưa đủ vốn để hỏi trống
không hay để prompt-inject), *HV ôn lại × adversarial*, *PM ngoài team × deixis* và
*PM ngoài team × adversarial* (PM không ngồi trước slide nên không hỏi deixis).

**Tỉ lệ và lý do chọn:**

| Loại | Số câu | Vì sao tỉ lệ này |
|---|---|---|
| `in_scope` | 12 (60%) | Đây là công việc chính của tutor — cần đủ mẫu để pass rate có nghĩa |
| `out_of_scope` | 4 (20%) | Đủ để đo scope discipline, không cần nhiều hơn vì hành vi đúng chỉ có một |
| `unclear` (deixis) | 2 (10%) | Ít nhưng bắt buộc — đây là chỗ duy nhất kiểm được `metadata.slide` có được dùng không |
| `adversarial` | 2 (10%) | Ít về số lượng, cao về rủi ro: 1 câu xin đáp án + 1 câu prompt injection |

Cắt theo mức rủi ro: **8 câu `high_risk`**, 7 `core`, 3 `out_of_scope` thuần, 2 `adversarial`.

**Nguồn câu hỏi:** 14 câu do LLM sinh nhưng **neo vào slide có thật** trong
`tutor/corpus/slides/day19-20-deck.md` (mỗi câu gắn `metadata.slide` với slide id thật);
6 câu ngoài phạm vi/adversarial do nhóm tự viết. Nhóm chưa có trace người dùng thật —
đây là hạn chế đã ghi nhận, vòng sau phải thay dần bằng câu hỏi thật.

**Review dataset — phát hiện gì:**

1. **Chạy kiểm tra retrieval trước khi tốn API.** Dùng `tutor.retrieve_corpus()` (offline,
   0 đồng) kiểm 14 câu có slide → **14/14 câu retrieve đúng slide dự kiến trong top-4**.
   Nghĩa là không có câu nào "chết" vì corpus không chứa đáp án — nếu tutor fail thì là lỗi
   của tutor, không phải lỗi đề.
2. **Phát hiện quan trọng:** BM25 **luôn** trả về top-4 kể cả với câu hỏi thời tiết —
   `sc-14` vẫn nhận về s45, s62, s55. Retrieval không bao giờ nói "không có gì khớp".
   → Kỷ luật scope **phải đến từ model**, không thể trông vào retrieval. Điều này định hình
   luôn rubric mục 3 (`scope_correct` là tiêu chí riêng, không suy ra từ citation).
3. Đã bỏ các câu quá dễ kiểu "AI evaluation là gì" — không phân biệt được tutor tốt/xấu.
4. `sc-15` (giá API) là câu tốt nhất trong bộ: nghe in-scope, thực ra out-of-scope.

**Nếu chỉ được giữ 10 câu** — giữ 10 câu này, vì chúng phủ đủ mọi *hành vi đúng khác nhau*
mà tutor phải làm được, mỗi câu bắt một failure mode riêng:

1. `sc-04-capstone-concept-grid`
2. `sc-06-capstone-concept-routing`
3. `sc-08-capstone-concept-calibration6`
4. `sc-07-capstone-example-3checks`
5. `sc-10-review-example-passrate`
6. `sc-12-pm-example-startcode`
7. `sc-15-out-api-pricing`
8. `sc-14-out-weather`
9. `sc-17-deixis-judge-agreement`
10. `sc-20-adv-prompt-injection`

### Danh sách scenario (bảng tóm tắt)

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| `sc-01-new-concept-evalloop` | Học viên mới × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s14` |
| `sc-02-new-concept-vibecheck` | Học viên mới × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s15` |
| `sc-03-new-example-golden` | Học viên mới × Xin ví dụ / how-to | `in_scope` | LLM sinh, neo vào `slide-day19-20#s16` |
| `sc-04-capstone-concept-grid` | HV đang làm capstone × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s27` |
| `sc-05-capstone-example-dimension` | HV đang làm capstone × Xin ví dụ / how-to | `in_scope` | LLM sinh, neo vào `slide-day19-20#s28` |
| `sc-06-capstone-concept-routing` | HV đang làm capstone × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s40` |
| `sc-07-capstone-example-3checks` | HV đang làm capstone × Xin ví dụ / how-to | `in_scope` | LLM sinh, neo vào `slide-day19-20#s46` |
| `sc-08-capstone-concept-calibration6` | HV đang làm capstone × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s56` |
| `sc-09-review-concept-tracecode` | HV ôn lại × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s35` |
| `sc-10-review-example-passrate` | HV ôn lại × Xin ví dụ / how-to | `in_scope` | LLM sinh, neo vào `slide-day19-20#s48` |
| `sc-11-pm-concept-judgetruth` | PM ngoài team × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s55` |
| `sc-12-pm-example-startcode` | PM ngoài team × Xin ví dụ / how-to | `in_scope` | LLM sinh, neo vào `slide-day19-20#s45` |
| `sc-13-out-admin-hocphi` | Học viên mới × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-14-out-weather` | HV ôn lại × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-15-out-api-pricing` | PM ngoài team × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-16-out-code-task` | HV đang làm capstone × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-17-deixis-judge-agreement` | HV đang làm capstone × Hỏi mơ hồ (deixis) | `unclear` | LLM sinh, neo vào `slide-day19-20#s53` |
| `sc-18-deixis-apply` | HV ôn lại × Hỏi mơ hồ (deixis) | `unclear` | LLM sinh, neo vào `slide-day19-20#s41` |
| `sc-19-adv-xin-dap-an` | HV đang làm capstone × Adversarial | `out_of_scope` | nhóm tự viết |
| `sc-20-adv-prompt-injection` | HV đang làm capstone × Adversarial | `out_of_scope` | nhóm tự viết |
