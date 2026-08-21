<!-- OWNER: Tuan Anh -- chi Tuan Anh duoc sua file nay. Ghep vao REPORT.md o T+125. -->
<!-- NOTE: So lieu code_checks va judge duoc Hieu dien tu data thuc te (results-v1, verdicts-v2). -->

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

Data nguồn: `deliverables/evidence/results-v1.jsonl` (20 câu), `deliverables/evidence/verdicts-v2.jsonl` (judge v2).

**Chi phí 1 vòng eval:** ~$0.019 tổng / 20 câu ≈ **$0.001/câu**. Avg latency: **4.9s/câu**. Tổng tokens: 110,470.

### Scorecard

**Code checks** (`python eval/code_checks.py deliverables/evidence/results-v1.jsonl`):

| Tiêu chí | Pass | Fail | Pass rate | Blocker? |
|---|---|---|---|---|
| **schema_valid** | 20 | 0 | **100%** | ✅ Blocker |
| **citation_exists** | 19 | 1 | **95%** | ✅ Blocker |
| **quote_verbatim** | 13 | 7 | **65%** ⚠️ | ✅ Blocker |
| **followup_count** | 20 | 0 | **100%** | ❌ Non-blocker |
| **quote_length** | 20 | 0 | **100%** | ❌ Non-blocker |

*`citation_exists` fail: sc-05 cite `ai-evals-m09#what-to-judge-start-with-what-you-can-teach` — section id không tồn tại trong corpus.*  
*`quote_verbatim` 7 fail: sc-05, sc-06, sc-07, sc-08, sc-11, sc-12, sc-19 — tutor dịch/paraphrase thay vì trích nguyên văn.*

**LLM judge v2** (`eval/judge.py`, model `gpt-4o-mini`, prompt v2):

| Tiêu chí | Pass | Fail | Pass rate |
|---|---|---|---|
| **groundedness** (toàn bộ 20 câu) | 18 | 2 | **90%** |

*2 case fail: sc-13 (học phí — judge v2 vẫn không tin sources rỗng là hợp lệ), sc-16 (code task — tương tự).*

### Định nghĩa Gate

| Tiêu chí | Ngưỡng ship | Hiện tại | Đạt? |
|---|---|---|---|
| schema_valid | 100% | 100% | ✅ |
| citation_exists | ≥ 95% | 95% | ✅ (vừa đủ) |
| quote_verbatim | ≥ 90% | **65%** | 🔴 FAIL |
| groundedness (judge v2) | ≥ 90% | 90% | ✅ (vừa đủ) |
| followup_count | 100% | 100% | ✅ |

*Ngưỡng 90% cho các tiêu chí blocker — lý do: dưới 90% nghĩa là 2+/20 câu có lỗi tin cậy, không chấp nhận được trong môi trường học tập.*

### Quyết định gate

**CHƯA SHIP — HOLD** — vì `quote_verbatim` **65% (7/20 fail)** vi phạm gate blocker ≥90%.

**3 lỗi lớn nhất cần fix:**

1. **Tutor paraphrase thay vì trích nguyên văn** — `quote_verbatim` fail 7/20: model dịch tiếng Anh sang tiếng Việt hoặc viết lại câu thay vì copy nguyên văn. Fix: thêm rule vào SYSTEM_PROMPT yêu cầu quote phải là copy-paste nguyên văn từ section, không dịch.

2. **Citation section_id bịa** — sc-05 cite section_id không tồn tại trong corpus. Fix: thêm code check vào pipeline; hoặc inject danh sách valid_ids vào prompt để model tự kiểm.

3. **Judge v2 chưa phân biệt "từ chối hợp lệ" vs "không có nguồn"** — sc-13/sc-16 vẫn fail dù tutor từ chối đúng cách. Fix: thêm few-shot example "out_of_scope + sources=[] = PASS" cụ thể hơn vào judge_prompt v3.
