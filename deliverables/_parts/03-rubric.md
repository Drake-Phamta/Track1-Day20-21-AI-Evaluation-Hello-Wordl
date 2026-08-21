<!-- OWNER: Hieu -- chi Hieu duoc sua file nay. Ghep vao REPORT.md o T+125. -->

## 3. Rubric v1

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

**Định nghĩa "đủ tốt":** Tutor trả lời một câu in-scope là đủ tốt khi câu trả lời bám hoàn toàn vào corpus, trích dẫn đúng nguồn, giữ đúng vai trò trợ giảng (không bịa, không làm hộ bài), và cung cấp đúng 3 câu follow-up có giá trị để học viên đào sâu thêm.

**Với câu out-of-scope:** pass khi tutor từ chối khéo léo (không cố trả lời), gợi ý 1–2 chủ đề liên quan trong corpus, và vẫn trả 3 câu follow-up dẫn học viên quay lại bài học. Fail nếu tutor cố trả lời (hallucinate) hoặc từ chối cụt lủn mà không gợi ý gì.

**Chấm chéo:** Sau vòng gán nhãn độc lập, các case bất đồng chủ yếu ở tiêu chí `groundedness` (Hiếu và Tuấn Anh: mức độ "có nguồn hỗ trợ" chấp nhận được là bao nhiêu?) và `pedagogy` (mức độ "vừa đủ" hay "quá chung chung"). Đã siết định nghĩa: `groundedness` fail khi có bất kỳ khẳng định chính nào **không có** source hỗ trợ trực tiếp (không chỉ "trông hợp lý").

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|
| **schema_valid** | Output parse được JSON; có đủ 4 field: `scope`, `answer`, `sources`, `followup_questions` | JSON vỡ (có `_parse_error`); thiếu bất kỳ field nào | ✅ **Blocker** — nếu schema vỡ, các tiêu chí khác không kiểm được |
| **citation_valid** | Mọi `doc_id`/`section_id` trong `sources` tồn tại thật trong corpus; quote ≤ 40 từ; quote là trích nguyên văn (token subsequence) | Có nguồn bịa (doc_id/section_id không tồn tại); quote > 40 từ; quote không khớp section | ✅ **Blocker** — trích nguồn sai là lỗi tin cậy nghiêm trọng nhất |
| **groundedness** | Mọi khẳng định chính trong `answer` đều được `sources` hỗ trợ; out-of-scope được từ chối đúng cách | Có nội dung suy diễn/bịa không trong sources; câu out-of-scope bị trả lời bừa; câu in-scope bị từ chối oan | ✅ **Blocker** — đây là tiêu chí trung tâm của RAG tutor |
| **scope_correct** | `scope` field đúng với thực tế (in_scope/out_of_scope); với câu mơ hồ: hoặc hỏi lại hoặc dùng slide context đúng | `scope` = "in_scope" nhưng câu thực ra out-of-scope (hoặc ngược lại); bỏ qua hoàn toàn slide context với câu deixis | ✅ **Blocker** — routing sai scope phá vỡ logic kiểm soát của tutor |
| **pedagogy** | `followup_questions` có đúng 3 câu, không rỗng, không trùng câu hỏi gốc; câu hỏi giúp học viên đào sâu (so sánh, áp dụng, mở rộng) — không hỏi xã giao | Ít/nhiều hơn 3 câu; câu follow-up rỗng hoặc trùng input; câu hỏi chung chung kiểu "Bạn có muốn tìm hiểu thêm không?" | ❌ **Không blocker** — ảnh hưởng trải nghiệm học, không ảnh hưởng tính đúng đắn thông tin |

**Ví dụ pass (sc-01):** Answer giải thích đúng eval loop, cite `slide-day19-20#s14`, quote ≤ 40 từ, 3 followup: "Vibe check khác gì eval loop?", "Khi nào mình nên chạy lại eval?", "Golden outputs được tạo ra như thế nào?"

**Ví dụ fail (sc-15):** Input hỏi giá API GPT-5 vs Claude — tutor hallucinate một bảng giá cụ thể (nguồn không tồn tại trong corpus) → fail `groundedness` + `citation_valid` cùng lúc.
