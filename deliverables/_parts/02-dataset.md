<!-- OWNER: Chi -->

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

**Số câu: 20** (`evidence/dataset-v1.jsonl`), phủ 15/20 ô của lưới 4×5. Năm ô còn trống đã
được lấp ở vòng v2 — xem cuối mục này và phần tự phê ở mục 1.

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
6 câu ngoài phạm vi/adversarial do nhóm tự viết.

**Review dataset — phát hiện gì:**

1. **Kiểm retrieval trước khi tốn API.** Dùng `tutor.retrieve_corpus()` (offline, 0 đồng)
   kiểm 14 câu có slide → **14/14 câu retrieve đúng slide dự kiến trong top-4**. Nghĩa là
   không có câu nào "chết" vì corpus không chứa đáp án — nếu tutor fail thì là lỗi của tutor,
   không phải lỗi đề. Chúng tôi làm lại đúng bước này cho v2 (6/6 câu có slide đều đạt).
2. **BM25 luôn trả về top-4 kể cả với câu hỏi thời tiết** — `sc-14` vẫn nhận về s45, s62, s55.
   Retrieval không bao giờ nói "không có gì khớp". → Kỷ luật scope **phải đến từ model**,
   không thể trông vào retrieval. Điều này định hình rubric ở mục 3: `scope_correct` là tiêu
   chí riêng, không suy ra từ citation.
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

### Danh sách scenario v1

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| `sc-01-new-concept-evalloop` | Học viên mới × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s14` |
| `sc-02-new-concept-vibecheck` | Học viên mới × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s15` |
| `sc-03-new-example-golden` | Học viên mới × Xin ví dụ | `in_scope` | LLM sinh, neo vào `slide-day19-20#s16` |
| `sc-04-capstone-concept-grid` | HV làm capstone × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s27` |
| `sc-05-capstone-example-dimension` | HV làm capstone × Xin ví dụ | `in_scope` | LLM sinh, neo vào `slide-day19-20#s28` |
| `sc-06-capstone-concept-routing` | HV làm capstone × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s40` |
| `sc-07-capstone-example-3checks` | HV làm capstone × Xin ví dụ | `in_scope` | LLM sinh, neo vào `slide-day19-20#s46` |
| `sc-08-capstone-concept-calibration6` | HV làm capstone × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s56` |
| `sc-09-review-concept-tracecode` | HV ôn lại × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s35` |
| `sc-10-review-example-passrate` | HV ôn lại × Xin ví dụ | `in_scope` | LLM sinh, neo vào `slide-day19-20#s48` |
| `sc-11-pm-concept-judgetruth` | PM ngoài team × Hỏi khái niệm | `in_scope` | LLM sinh, neo vào `slide-day19-20#s55` |
| `sc-12-pm-example-startcode` | PM ngoài team × Xin ví dụ | `in_scope` | LLM sinh, neo vào `slide-day19-20#s45` |
| `sc-13-out-admin-hocphi` | Học viên mới × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-14-out-weather` | HV ôn lại × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-15-out-api-pricing` | PM ngoài team × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-16-out-code-task` | HV làm capstone × Ngoài phạm vi | `out_of_scope` | nhóm tự viết |
| `sc-17-deixis-judge-agreement` | HV làm capstone × Deixis | `unclear` | LLM sinh, neo vào `slide-day19-20#s53` |
| `sc-18-deixis-apply` | HV ôn lại × Deixis | `unclear` | LLM sinh, neo vào `slide-day19-20#s41` |
| `sc-19-adv-xin-dap-an` | HV làm capstone × Adversarial | `out_of_scope` | nhóm tự viết |
| `sc-20-adv-prompt-injection` | HV làm capstone × Adversarial | `out_of_scope` | nhóm tự viết |

---

## Dataset v2 — mở rộng, đóng blind spot

**Thêm 10 câu** (`evidence/dataset-v2-extra.jsonl`) → tổng **30 câu, phủ 20/20 ô**.

Mười câu này không phải thêm cho đủ số. Mỗi câu đóng đúng một chỗ mà báo cáo v1 đã **tự khai
là thiếu**: 5 ô lưới bỏ trống, 3 blind spot ghi ở mục 2 và 7, cộng 2 câu ép kiểm trích dẫn.

| scenario_id | ô trong lưới | expected | đóng blind spot nào |
|---|---|---|---|
| `sc-21-new-deixis-blank` | Học viên mới × Deixis | `unclear` | Ô lưới trống: học viên mới × deixis |
| `sc-22-new-adv-naive` | Học viên mới × Adversarial | `out_of_scope` | Ô lưới trống: học viên mới × adversarial |
| `sc-23-review-adv-config` | HV ôn lại × Adversarial | `out_of_scope` | Ô lưới trống: ôn lại × adversarial |
| `sc-24-pm-deixis` | PM ngoài team × Deixis | `unclear` | Ô lưới trống: PM ngoài team × deixis |
| `sc-25-pm-adv-guarantee` | PM ngoài team × Adversarial | `out_of_scope` | Ô lưới trống: PM ngoài team × adversarial |
| `sc-26-english-question` | PM ngoài team × Hỏi khái niệm | `in_scope` | Blind spot: câu hỏi tiếng Anh |
| `sc-27-multisource-conflict` | HV làm capstone × Hỏi khái niệm | `in_scope` | Blind spot: hai nguồn nói khác nhau — kiêm phép dò coverage retrieval |
| `sc-28-followup-turn` | HV làm capstone × Deixis | `in_scope` | Blind spot: hỏi nối tiếp (multi-turn) |
| `sc-29-cite-stress-kappa` | HV làm capstone × Hỏi khái niệm | `in_scope` | Ép kiểm trích dẫn: hỏi đúng số liệu cụ thể |
| `sc-30-cite-stress-tpr` | HV ôn lại × Hỏi khái niệm | `in_scope` | Ép kiểm trích dẫn: hỏi đúng số liệu cụ thể |

**Hai câu stress citation là thiết kế có chủ đích.** `sc-29` hỏi đúng con số κ ≈ 0.45–0.52 và
"33–41 điểm" trong `s55`; `sc-30` hỏi đúng TPR = 5/7 = 71% và TNR = 1/3 = 33% trong `s53`.
Số liệu cụ thể là mồi ngon nhất cho việc bịa quote — model rất dễ nhớ đúng con số nhưng viết
lại câu văn quanh nó.

### ⚠️ Bộ v2 chạy trên cấu hình KHÁC — số liệu để riêng

`results-v1.jsonl` chạy bằng `gpt-4o-mini` với tool-calling thật (model tự đặt truy vấn).
`results-v2-gateway.jsonl` chạy bằng `gemma-4` qua gateway nội bộ ở chế độ pre-retrieve
(BM25 lấy nguồn trước, model không được chọn).

**Không gộp hai bộ vào một scorecard.** Mục 6 đã chứng minh hai cấu hình cho kết quả lệch
nhau đáng kể — trộn chúng lại là mắc đúng cái lỗi mà bảng đối chứng ở đó đang cảnh báo.
Bộ v2 đứng riêng như một lần đo coverage mở rộng.

**Kết quả v2 (10 câu, 41 giây):**

| Check | Kết quả |
|---|---|
| `schema_valid` | 10/10 |
| `citation_exists` | 10/10 |
| `quote_verbatim` | **4/10** |
| `followup_count` | 10/10 |
| `quote_length` | 10/10 |
| Nhãn người | 10/10 pass |

Nội dung đúng cả 10 câu — kể cả hai câu stress citation lấy **chính xác** κ 0.45–0.52,
33–41 điểm, TPR 5/7 = 71%, TNR 1/3 = 33%. Sáu case fail `quote_verbatim` đều là **ghép mẩu**,
không có case nào bịa. Điều này **xác nhận lại phát hiện của v1 trên một bộ câu hoàn toàn
mới**: điểm yếu của tutor là kỷ luật trích dẫn nguyên văn, không phải groundedness.

Một chỗ dataset v1 đặt kỳ vọng quá chặt: `sc-25` được gán `expected_scope = out_of_scope`,
nhưng tutor trả `in_scope` và giải thích pass rate phụ thuộc rủi ro, dẫn đúng ba mốc
80% / 90% / 99,9% **có thật trong `s48`**. Đó là hành vi đúng. Kỳ vọng của chúng tôi sai,
không phải tutor sai — đã ghi vào note của `labels-v2-gateway.csv`.

### Phát hiện lớn nhất từ v2: một phần ba corpus gần như chết

`sc-27` được thiết kế làm **phép dò coverage retrieval**, không phải câu hỏi kiến thức. Nó
hỏi so sánh giữa bài của Hamel và chương 4 của Chip Huyen. Kết quả đo được:

| Tài liệu | Dung lượng | Số section | TB mỗi section | Số lần được truy ra (129 lượt ở v1) |
|---|---|---|---|---|
| `chip-huyen-ch4` | 123k ký tự | 15 | **8.213** | **1** |
| `anthropic-demystifying-evals` | 58k | 19 | 3.033 | 3 |
| `hamel-evals` | 25k | 21 | 1.201 | 2 |
| `slide-day19-20` | 65k | 66 | 977 | **63** |

Ba tài liệu tham chiếu thật cộng lại chỉ được truy ra **6/129 lượt = 4,7%**, dù chiếm hơn nửa
dung lượng corpus. Slide chiếm 49%.

Nguyên nhân là **cách chia section, không phải nội dung**: `load_corpus()` tách theo heading
`##`/`###`, mà `chip-huyen-ch4` chỉ có vài heading lớn nên ra 15 khối trung bình 8.213 ký tự —
gấp 8 lần mọi tài liệu khác. BM25 với `b=0.75` phạt độ dài rất nặng, nên những khối này gần
như không bao giờ thắng điểm.

Hệ quả cho sản phẩm: **tutor đang trả lời gần như hoàn toàn từ slide bài giảng**, còn ba
nguồn chuyên sâu thì nằm đó làm cảnh. Đây là việc cần fix ở tầng corpus (chia nhỏ section),
rẻ hơn nhiều so với đổi model — và nếu không đo thì không ai biết.

Điểm sáng: ở `sc-27` tutor **không bịa** nội dung của Chip Huyen. Nó dùng một dòng trong
`s48` vốn có trích dẫn gián tiếp "— Chip Huyen, AI Engineering ch.4" và nói rõ "dựa trên các
tài liệu được cung cấp". Trung thực, nhưng cũng cho thấy nó chưa từng đọc được tài liệu gốc.
