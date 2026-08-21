<!-- OWNER: Tuan Anh -- chi Tuan Anh duoc sua file nay. Ghep vao REPORT.md o T+125. -->

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

Tập dataset v1 gồm **20 traces** (14 generated từ LLM bám sát corpus slide, 6 tự viết cho edge cases). 
- **Coverage chính:** Phủ 15/20 ô trong input grid, tập trung nhiều nhất (9/20 câu) vào học viên làm capstone hỏi khái niệm và ví dụ. 
- **Blind spot còn lại:** Chưa cover được các cuộc hội thoại nhiều lượt (multi-turn), đa ngôn ngữ, hoặc mâu thuẫn giữa 2 nguồn kiến thức.

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): **85%** — Tiêu chí gây bất đồng nhiều nhất là `groundedness` và `pedagogy`.
- Mâu thuẫn lớn nhất: Câu `sc-08` (đếm 6 bước) — một phía cho rằng model liệt kê đúng là pass, phía kia cho rằng model tự ý điền các bước không có trong slide (ảo giác nhẹ).
- Nhóm xử lý bằng cách nào: Siết định nghĩa `groundedness` (không chấp nhận bất cứ claim chính nào thiếu source hỗ trợ) và loại bỏ `pedagogy` ra khỏi LLM judge vì quá cảm tính.

#### 3. LLM judge

- Model judge: `openai/gpt-4o-mini`
- Số vòng calibration: **2** — sau đó judge nhận đúng **100%** output tốt (in-scope) và bắt đúng **50%** output xấu (bắt được out-of-scope sai nhưng bỏ sót một vài case từ chối đúng).
- Judge nào không calibrate nổi, vì sao: `pedagogy` và `adversarial` không calibrate nổi vì LLM có xu hướng "nịnh" (vibe check) hoặc rơi vào bẫy của prompt injection giống hệ thống chính.

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| schema_valid, followup_count, quote_length | 100% | Code checks | Deterministic rule, chạy nhanh 0đ, độ chính xác 100% |
| citation_exists, quote_verbatim | ≥90% | Code checks | So sánh trực tiếp ID và text token với corpus, không cần ngữ nghĩa |
| groundedness | ≥90% | LLM judge + audit 10%/tuần | Đòi hỏi so sánh ngữ nghĩa giữa source và answer, GPT-4o-mini đạt agreement cao sau v2 |
| pedagogy, adversarial, deixis | N/A | Human review | LLM judge có xu hướng chấm cảm tính và không phát hiện được bẫy injection |

#### 5. Verdict + bước tiếp theo

**HOLD** — vì: tiêu chí blocker `quote_verbatim` chỉ đạt **65%** (fail 7/20), vi phạm chuẩn trích dẫn nguyên văn (≥90%). 

- Đòn bẩy tiếp theo: Sửa `SYSTEM_PROMPT` của AI Tutor (yêu cầu trích dẫn copy-paste 100% không paraphrase). 
- Metric chứng minh đã sẵn sàng: `quote_verbatim` pass rate > 90% trên tập dataset-v1 trong vòng test kế tiếp (v2).

### Câu hỏi tự soi

- Tin cậy nhất ở đâu, đáng lo nhất ở đâu? Đáng lo nhất là `sc-15` (giá API) vì nghe rất giống in-scope, rủi ro hallucinate cực cao. Tin cậy nhất là pipeline code_checks determinisitc.
- Nếu chỉ được fix **một thứ** trước khi cho học viên thật dùng, đó là gì? Khắc phục lỗi paraphrase khi trích dẫn (`quote_verbatim`).
- Eval loop này sẽ chạy lại **khi nào** (mỗi lần đổi prompt? mỗi tuần? khi corpus đổi?) và ai nhìn kết quả? Chạy lại mỗi khi thay đổi `SYSTEM_PROMPT` hoặc update version LLM model. PM và Tech Lead sẽ review kết quả.
- Điều gì trong bài này bạn sẽ **mang về áp dụng** vào sản phẩm thật của mình? Áp dụng ngay hệ thống *code_checks* cho các ràng buộc kỹ thuật (format, length, inclusion) thay vì phung phí token cho LLM judge.
