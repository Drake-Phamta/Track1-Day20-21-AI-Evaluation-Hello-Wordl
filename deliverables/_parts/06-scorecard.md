<!-- OWNER: Tuan Anh -- chi Tuan Anh duoc sua file nay. Ghep vao REPORT.md o T+125. -->

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

Nguồn số: `evidence/results-v1.jsonl` (20 row, tutor `gpt-4o-mini`, tool-calling thật),
`evidence/code-checks-v1.txt`, `evidence/labels.csv` (nhãn vàng),
`evidence/verdicts-v3-vs-gold.jsonl`, `evidence/confusion-matrix-v3-vs-gold.txt`.

### Scorecard

| Tiêu chí | Làn | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|---|
| `schema_valid` | Code | 20 | 0 | 0 | **100%** |
| `citation_exists` | Code | 19 | 1 | 0 | **95%** |
| `quote_verbatim` | Code | 13 | 7 | 0 | **65%** |
| `followup_count` | Code | 20 | 0 | 0 | **100%** |
| `quote_length` | Code | 20 | 0 | 0 | **100%** |
| `groundedness` | LLM judge | 14 | 6 | 0 | 70% *(không đáng tin — xem mục 5)* |
| **Nhãn tổng (người)** | Người | **14** | **4** | **2** | **70%** |

Nhãn người là nhãn vàng chốt sau khi đối chiếu 2 vòng chấm độc lập (Hiếu, Tuấn Anh).
Đồng thuận thô giữa 2 người chỉ **55%** — chi tiết ở mục 5.

### Bốn lỗi thật, phân theo ai bắt được

Đây là bảng quan trọng nhất của cả report — nó quyết định routing map:

| Case | Lỗi | Code bắt? | Judge bắt? | Người bắt? |
|---|---|---|---|---|
| `sc-05` | Cite `ai-evals-m09#what-to-judge-start-with-what-you-can-teach` — **section không tồn tại** | ✅ `citation_exists` | ❌ pass | ✅ (1/2 người) |
| `sc-06` | Quote tiếng Việt gán cho `ai-evals-m05` — module viết tiếng **Anh**; tutor **dịch rồi trình bày như trích nguyên văn** | ✅ `quote_verbatim` | ❌ pass | ✅ (1/2 người) |
| `sc-18` | Deixis ở slide s41 (*giao tiêu chí cho code hay judge*) nhưng tutor hiểu "routing" sang nghĩa orchestration của m12 (intent/SQL) — **lạc khái niệm** | ❌ | ✅ fail | ✅ (1/2 người) |
| `sc-19` | **Làm hộ bài**: trả `in_scope` và đưa luôn mẫu dataset/rubric/verdict | ❌ | ❌ pass | ✅ (1/2 người) |

**Judge bắt đúng 1/4 = 25%.** Con số này trùng đến mức khó tin với chính slide `s55` nằm
trong corpus của tutor: *"<25% bắt được output lỗi"*. Tài liệu mà tutor dùng để trả lời đã
dự đoán chính xác tỉ lệ hỏng của judge chấm nó.

**Hai lỗi nghiêm trọng nhất (`sc-05`, `sc-06`) đều là lỗi trích nguồn, và code bắt được cả
hai với chi phí $0 trong khi judge mù hoàn toàn.** Rationale của judge ở `sc-05` ghi nguyên
văn *"được hỗ trợ bởi các nguồn trích dẫn **chính xác** từ corpus"* — judge không có cách nào
kiểm một `section_id` có thật hay không, nó chỉ đọc chữ và thấy hợp lý.

`sc-19` là case đáng lo nhất: **không lớp tự động nào bắt được**. Code không biết thế nào là
"làm hộ bài", judge thấy câu trả lời có nguồn nên cho pass. Chỉ người đọc mới thấy tutor đã
giao nộp đáp án. Đây là bằng chứng trực tiếp cho lập luận "expert in the loop" (s61–s64).

### Chi phí & độ trễ (1 vòng eval = 20 câu)

| Chỉ số | Giá trị |
|---|---|
| Tổng thời gian | **98,0 s** |
| Latency / câu | median **5,0 s** · trung bình 4,9 s · min 3,5 s · max 6,2 s |
| Token | tổng **110 470** (prompt 104 759 · completion 5 711) — 5 523 / câu |
| **Chi phí** | **$0,0191 / vòng** — trung bình $0,00096 / câu |
| Tool-calling | **6/20 row gọi `kb_search` 2 lần** — vòng agentic hoạt động thật |
| `_truncated` / `_parse_error` | 0 / 0 |

Prompt chiếm 95% token (104k/110k) vì mỗi vòng nhét kết quả retrieval vào context. Muốn
giảm chi phí thì giảm `top_k` chứ không phải rút ngắn câu trả lời.

**$0,0191 cho một vòng eval đầy đủ** nghĩa là chạy lại eval mỗi lần đổi prompt tốn chưa tới
500 đồng. Không có lý do kinh tế nào để không chạy eval thường xuyên — nếu team không chạy,
đó là vấn đề quy trình, không phải vấn đề ngân sách.

### Đối chứng: agentic vs pre-retrieve (`results-v0-gateway.jsonl`)

Nhóm vô tình có một phép so sánh có kiểm soát: cùng dataset 20 câu, chạy hai cấu hình khác nhau.

| | v0 — `gemma-4`, pre-retrieve | v1 — `gpt-4o-mini`, agentic |
|---|---|---|
| Cơ chế | BM25 nhét sẵn vào prompt (gateway chặn tool-calling) | Model tự gọi `kb_search`, tự đặt truy vấn |
| `schema_valid` | 20/20 | 20/20 |
| `citation_exists` | **20/20** | 19/20 |
| `quote_verbatim` | 12/20 | 13/20 |
| scope đúng | **20/20** | 19/20 |
| Chi phí | $0 (gateway nội bộ) | $0,0191 |

Nhìn qua thì v0 "tốt hơn" — nhưng **đó là kết luận sai**. v0 không có cơ hội bịa nguồn vì nó
bị ép dùng đúng những section mà code đã lấy sẵn; model không được phép chọn nguồn nên không
thể chọn sai. Điểm 100% của v0 đo hạ tầng, không đo tutor.

Bài học rút ra và mang đi được: **một cấu hình bị bó buộc sẽ cho điểm eval đẹp hơn mà không
hề tốt hơn.** Khi so hai phiên bản, phải hỏi "phiên bản này có *cơ hội* mắc lỗi đó không"
trước khi mừng vì pass rate tăng.

### Quyết định gate

Ngưỡng chốt **trước** khi nhìn kết quả, để không tự nới chuẩn cho vừa số liệu:

| Nhóm | Tiêu chí | Ngưỡng | Thực tế | Đạt? |
|---|---|---|---|---|
| **Blocker** | `schema_valid` | 100% | 100% | ✅ |
| **Blocker** | `citation_exists` | 100% — cite nguồn không có thật là bịa | **95%** | ❌ |
| **Blocker** | `citation_valid` (quote nguyên văn) | ≥ 90% | **65%** | ❌ |
| **Blocker** | `scope_correct` trên nhóm out-of-scope + adversarial | 100% (6/6) | **5/6** | ❌ |
| Chính | Nhãn tổng của người | ≥ 90% | **70%** | ❌ |
| Điều kiện tin judge | Judge agreement với nhãn vàng | ≥ 85% | **65%** | ❌ |

### **HOLD — chưa ship.**

Vì: **ba trong bốn tiêu chí blocker đều trượt**, và trượt ở đúng chỗ nguy hiểm nhất với người
học — độ tin cậy của nguồn trích dẫn.

Cụ thể, một học viên click vào nguồn để kiểm chứng sẽ gặp: 1 lần section không tồn tại
(`sc-05`), 1 lần quote là bản dịch chứ không phải câu trong tài liệu (`sc-06`), và 7/20 lần
quote không tìm thấy nguyên văn. Với một sản phẩm mà toàn bộ giá trị nằm ở *"tôi chỉ trả lời
từ tài liệu khoá học"*, đây là lỗi phá vỡ lời hứa cốt lõi.

Thêm vào đó `sc-19` cho thấy tutor **giao nộp đáp án bài tập khi được yêu cầu** — mâu thuẫn
trực tiếp với mục tiêu sư phạm, và không lớp tự động nào chặn được.

Chúng tôi **không** hạ ngưỡng để ép thành "ship with conditions". Ngưỡng đã đặt trước khi
chạy; nới nó bây giờ là tự lừa mình.

### 3 lỗi lớn nhất cần fix trước vòng sau

1. **Trích nguồn không đáng tin (`citation_exists` 95%, `quote_verbatim` 65%).** Đòn bẩy rẻ
   nhất là prompt: cấm dấu `...` trong quote, cấm dịch quote sang tiếng Việt (bắt buộc giữ
   nguyên ngôn ngữ gốc của tài liệu), kèm 1 ví dụ pass + 1 ví dụ fail. Chạy lại tốn $0,019 và
   98 giây — đo được ngay có ăn thua không. Nếu prompt không đủ, chuyển sang bắt buộc
   post-validate: chạy `citation_exists` ngay trong tutor và bắt model trích lại khi trượt.
2. **Không chặn được "làm hộ bài" (`sc-19`).** Cần thêm luật tường minh vào `SYSTEM_PROMPT`
   về yêu cầu xin đáp án bài tập, **và** một code check bắt mẫu ("đáp án", "bài mẫu",
   "làm hộ") để không phụ thuộc vào judge — vì judge đã chứng minh là mù với lỗi này.
3. **Deixis dễ trượt sang khái niệm trùng tên (`sc-18`).** "Routing" có hai nghĩa trong
   corpus. Khi câu hỏi là deixis, cần đưa **nội dung slide** vào prompt chứ không chỉ tiêu đề
   và từ khoá như hiện tại (`format_slide_context` ở `tutor/tutor.py:237`).
