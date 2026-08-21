<!-- OWNER: Hieu -->

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

**Nguyên tắc routing:** Dùng code khi tiêu chí có thể diễn đạt thành rule deterministic (có/không, đếm được, đối chiếu được với danh sách có sẵn). Dùng LLM judge khi cần hiểu ngữ nghĩa. Giữ lại cho con người khi tiêu chí đòi hỏi judgment về chất lượng sư phạm mà LLM chấm không ổn định.

**Tiêu chí ban đầu định dùng LLM judge nhưng code kiểm được rẻ hơn:**
- `schema_valid`: ban đầu nghĩ cần LLM "đọc hiểu" output — thực ra chỉ cần `json.loads()` + kiểm set key. Code 5 dòng, deterministic, không tốn token.
- `citation_exists`: kiểm tra doc_id/section_id có trong corpus không — đối chiếu với set được build từ corpus tại runtime. Không cần LLM.
- `followup_count`: đếm len(list) == 3, kiểm empty string, so sánh với input. Hoàn toàn deterministic.
- `quote_length`: đếm word count. Code 2 dòng.

**Tiêu chí LLM judge không đủ tin, phải giữ cho người:**
- `pedagogy` (chất lượng sư phạm): LLM judge có xu hướng overfit "nghe có vẻ hay" — chấm pass những câu follow-up chung chung như "Bạn muốn tìm hiểu thêm không?". Agreement vòng 1 thấp (judge quá dễ tính). → Giữ cho con người chấm.
- Câu **adversarial** (sc-19, sc-20): LLM judge cùng họ model với tutor có thể không nhận ra prompt injection là fail. → Con người chấm bắt buộc.

**Judge prompt chấm tiêu chí `groundedness`** (tính bám nguồn toàn bộ answer, không phải từng quote riêng lẻ — điều này đòi ngữ nghĩa nên cần LLM). Model judge: `openai/gpt-4o-mini`, temperature=1 (mặc định OpenAI). Chọn khác model tutor (`deepseek/deepseek-v4-flash`) để tránh self-serving bias — model có xu hướng chấm pass output của chính model họ.

### Bảng routing

| Tiêu chí | Code | LLM judge | Con người | Lý do |
|---|---|---|---|---|
| **schema_valid** | ✅ `check_schema` | — | — | Deterministic: json.loads + kiểm set key. Tốn 0 token, 0 độ trễ. |
| **citation_valid** (citation_exists + quote_verbatim + quote_length) | ✅ `check_citation_exists` + `check_quote_verbatim` + `check_quote_length` | — | — | Đối chiếu với corpus index (valid_ids, section_tokens). Không cần hiểu ngữ nghĩa. |
| **followup_count** | ✅ `check_followup_count` | — | — | Đếm len == 3, kiểm empty, so sánh string với input. Hoàn toàn rule-based. |
| **quote_length** | ✅ `check_quote_length` | — | — | Đếm word count. Contract 40 từ ghi rõ trong SYSTEM_PROMPT. |
| **groundedness** | — | ✅ `eval/judge.py` → `judge_prompt.md` (model: `gpt-4o-mini`) | 10% audit/tuần | Đòi ngữ nghĩa: judge cần đọc sources và answer để phán xét "có khẳng định nào không có nguồn không". Code không làm được. |
| **scope_correct** | Một phần: kiểm `scope` field có giá trị hợp lệ | ✅ Judge phụ trợ (trong `groundedness` prompt) | ✅ Với case mơ hồ/deixis | Code chỉ kiểm syntax của field. Đúng/sai semantic cần đọc answer + nguồn. Case deixis phức tạp → người quyết. |
| **pedagogy** | — | — | ✅ Tất cả 20 row | Judge quá lỏng với followup quality. Agreement judge vs người < 70% ở tiêu chí này. Giữ cho người để bảo toàn chất lượng sư phạm. |
| **adversarial behavior** | — | — | ✅ sc-19, sc-20 | LLM judge có thể không nhận ra prompt injection. Rủi ro cao → người chấm bắt buộc. |
