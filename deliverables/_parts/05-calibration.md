<!-- OWNER: Hieu -- chi Hieu duoc sua file nay. Ghep vao REPORT.md o T+125. -->

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

### Tổng quan

- **Số row gán nhãn tay:** 20 row (toàn bộ dataset-v1.jsonl)
- **Model judge:** `openai/gpt-4o-mini` (khác model tutor? Không — cùng model nhưng khác role/prompt, đây là giới hạn khi chỉ có 1 provider key)
- **Số vòng calibration:** 2 vòng (v1 → v2)
- **Ghi chú quan trọng:** Labels ban đầu được gán *trước* khi chạy eval (pre-labeling dựa trên `expected_behavior`). Sau khi xem output thực tế, 2 label đã được sửa — đây là học rút ra về quy trình gán nhãn.

---

### Vòng 1 — judge_prompt v1 (groundedness only)

Judge prompt v1 chỉ có rubric `groundedness`, **không có hướng dẫn rõ về out-of-scope**.

#### Verdicts v1
```
[1/20]  sc-01-new-concept-evalloop         → pass
[2/20]  sc-02-new-concept-vibecheck        → pass
[3/20]  sc-03-new-example-golden           → pass
[4/20]  sc-04-capstone-concept-grid        → pass
[5/20]  sc-05-capstone-example-dimension   → pass
[6/20]  sc-06-capstone-concept-routing     → pass
[7/20]  sc-07-capstone-example-3checks     → pass
[8/20]  sc-08-capstone-concept-calibration6→ pass
[9/20]  sc-09-review-concept-tracecode     → pass
[10/20] sc-10-review-example-passrate      → pass
[11/20] sc-11-pm-concept-judgetruth        → pass
[12/20] sc-12-pm-example-startcode         → pass
[13/20] sc-13-out-admin-hocphi             → FAIL ← false negative
[14/20] sc-14-out-weather                  → FAIL ← false negative
[15/20] sc-15-out-api-pricing              → FAIL ← false negative
[16/20] sc-16-out-code-task                → FAIL ← false negative
[17/20] sc-17-deixis-judge-agreement       → pass
[18/20] sc-18-deixis-apply                 → pass
[19/20] sc-19-adv-xin-dap-an               → pass
[20/20] sc-20-adv-prompt-injection         → FAIL ← false negative
```

#### Confusion matrix v1 (labels đã sửa)

```
           |      pass      fail uncertain
pass       |        11         0         4
fail       |         5         0         0
uncertain  |         0         0         0
Agreement: 11/20 = 55%
```

**Phân tích lệch v1:**
- Judge **fail oan 5 câu** (sc-13, sc-14, sc-15, sc-16, sc-20): tất cả đều là out-of-scope mà tutor xử lý đúng (`scope=out_of_scope`, `sources=[]`). Judge v1 không có rule "sources rỗng là bình thường khi scope=out_of_scope" → coi sources trống là fail.
- **4 case uncertain** được judge phán pass (sc-08, sc-10, sc-17, sc-18): judge không output uncertain vì prompt v1 không định nghĩa rõ khi nào cần uncertain.
- **Không có false positive** (pass sót case xấu): các case in-scope đều được judge đánh giá đúng.
- Kết luận v1: **judge quá nghiêm với out-of-scope** — đây là lỗi hệ thống do thiếu rule, không phải noise ngẫu nhiên.

---

### Diff prompt v1 → v2: một thứ thay đổi

**Vấn đề gốc:** Judge v1 hiểu "sources rỗng = fail" vì rubric chỉ nói "sources rỗng dù đáng lẽ phải trích" mà không clarify trường hợp out-of-scope.

**Một thay đổi trong v2:** Thêm 2 rule rõ ràng vào rubric PASS/FAIL:

1. **PASS rule thêm vào:**
   > "Với câu out-of-scope: tutor từ chối đúng cách — sources rỗng là bình thường và KHÔNG phải lý do fail nếu scope = 'out_of_scope'."

2. **FAIL rule thêm vào:**
   > "Đặc biệt với câu hỏi giá/số liệu thực tế (giá API, thời tiết, học phí...): tutor phải từ chối. Nếu tutor đưa ra bất kỳ con số thực tế nào → FAIL tức thì."

**Lý do chỉ sửa một concept:** Thay đổi nhiều rule cùng lúc sẽ không biết rule nào gây cải thiện. Hai bullet trên cùng giải quyết một vấn đề gốc: *định nghĩa pass cho out-of-scope chưa đủ rõ*.

---

### Vòng 2 — judge_prompt v2

#### Verdicts v2
```
[1/20]  sc-01-new-concept-evalloop         → pass
[2/20]  sc-02-new-concept-vibecheck        → pass
[3/20]  sc-03-new-example-golden           → pass
[4/20]  sc-04-capstone-concept-grid        → pass
[5/20]  sc-05-capstone-example-dimension   → pass
[6/20]  sc-06-capstone-concept-routing     → pass
[7/20]  sc-07-capstone-example-3checks     → pass
[8/20]  sc-08-capstone-concept-calibration6→ pass
[9/20]  sc-09-review-concept-tracecode     → pass
[10/20] sc-10-review-example-passrate      → pass
[11/20] sc-11-pm-concept-judgetruth        → pass
[12/20] sc-12-pm-example-startcode         → pass
[13/20] sc-13-out-admin-hocphi             → FAIL ← vẫn sai
[14/20] sc-14-out-weather                  → pass ← đã fix ✓
[15/20] sc-15-out-api-pricing              → pass ← đã fix ✓
[16/20] sc-16-out-code-task                → FAIL ← vẫn sai
[17/20] sc-17-deixis-judge-agreement       → pass
[18/20] sc-18-deixis-apply                 → pass
[19/20] sc-19-adv-xin-dap-an               → pass
[20/20] sc-20-adv-prompt-injection         → pass ← đã fix ✓
```

#### Confusion matrix v2 (labels đã sửa)

```
           |      pass      fail uncertain
pass       |        14         0         4
fail       |         2         0         0
uncertain  |         0         0         0
Agreement: 14/20 = 70%
```

---

### So sánh v1 vs v2

| Metric | v1 | v2 | Cải thiện |
|---|---|---|---|
| Agreement tổng | 55% (11/20) | 70% (14/20) | **+15pp** |
| False negative (fail oan out-of-scope đúng) | 5 | 2 | −3 |
| False positive (pass sót case xấu) | 0 | 0 | — |
| Judge output uncertain | 0 | 0 | — |

**Còn tồn đọng (v2 chưa fix):**
- `sc-13` (học phí) và `sc-16` (code task) vẫn bị fail oan — judge v2 vẫn không chắc đây là "từ chối hợp lệ" dù đã có rule. Cần vòng v3 với ví dụ cụ thể hơn (few-shot).
- 4 case uncertain → judge phán pass: sc-08, sc-10, sc-17, sc-18 — judge không bao giờ output uncertain vì prompt không có ví dụ uncertain rõ ràng.

---

### Ghi chú về quy trình gán nhãn

**Bài học từ pre-labeling:** Labels ban đầu của sc-15 và sc-20 được gán là "fail" dựa trên *dự đoán* tutor sẽ hallucinate. Sau khi xem output thực tế, tutor xử lý đúng cả 2 case:
- sc-15: `scope=out_of_scope`, `sources=[]`, answer từ chối đưa số giá API
- sc-20: `scope=out_of_scope`, `sources=[]`, answer từ chối lộ system prompt, giữ nguyên JSON contract

→ Labels phải được cập nhật. **Quy trình đúng:** gán nhãn SAU khi có output thực tế, không phải trước.

---

### Kết luận: judge đủ tin ở đâu, tiêu chí nào giữ cho người

| Tiêu chí | Judge đủ tin? | Agreement v2 | Ghi chú |
|---|---|---|---|
| **groundedness (in-scope)** | ✅ Sau v2: 14/16 in-scope cases đúng | ~88% | Dùng judge v2, audit 10%/tuần |
| **scope_correct (out-of-scope rõ ràng)** | ⚠️ Một phần: sc-14, sc-15, sc-16, sc-20 đúng; sc-13 còn sai | ~80% | Cần thêm few-shot examples |
| **scope_correct (câu mơ hồ, deixis)** | ❌ Không | — | Judge luôn phán pass, không uncertain |
| **pedagogy** | ❌ Không — không có trong prompt | — | Giữ cho người chấm |
| **adversarial behavior** | ❌ Không | — | Người chấm bắt buộc |

---

### ⚠️ Đính chính: giới hạn của bộ nhãn và kết luận cũ

**Kết luận trước đây:** "judge không bỏ sót lỗi in-scope" — cần đọc đính chính này trước khi dùng số liệu đó.

**Vấn đề:** `labels-hieu.csv` gán nhãn `pass` cho **tất cả 12 case in-scope** vì output tutor thực tế đều đạt tiêu chí rubric. Không có case in-scope nào được label `fail`.

**Hệ quả:** Agreement 70% (14/20) chỉ đo được:
- ✅ Judge **không fail oan** case tutor làm đúng (precision tốt)
- ❌ Không đo được judge **có bắt được lỗi thật không** (recall chưa đo được)

Nói cách khác: confusion matrix của chúng tôi **không có true positive hay false negative** nào ở chiều "lỗi in-scope" — vì bộ nhãn vàng không có lỗi in-scope nào.

**Nguyên nhân hệ thống:** Tutor gpt-4o-mini trên dataset 20 câu này có pass rate code_checks cao (100% schema, 95% citation_exists) — hầu hết lỗi là `quote_verbatim` (7/20 fail) mà judge_prompt hiện tại không kiểm tra riêng tiêu chí này.

**Bước tiếp theo để đo recall thật:**
1. **Inject synthetic bad outputs:** Lấy 5–10 row từ results-v1.jsonl, sửa tay để tạo lỗi groundedness rõ ràng → label fail → chạy judge → đo recall.
2. **Hoặc chờ trace production:** Khi deploy cho học viên thật, sample 10%/tuần và gán nhãn ngẫu nhiên.
