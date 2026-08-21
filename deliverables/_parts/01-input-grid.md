<!-- OWNER: Chi -- chi Chi duoc sua file nay. Ghep vao REPORT.md o T+125. -->
<!-- DRAFT do Tuan Anh sinh tu dataset-v1.jsonl luc T+20. Chi review + chinh, dac biet phan "vi sao". -->

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát
> coverage. Trả lời các câu hỏi sau rồi vẽ lưới của bạn.

**Nhóm người dùng** — VLearn AI Tutor gắn trực tiếp vào màn hình học, nên người hỏi luôn
là người đang ở trong khoá hoặc vừa rời khoá. Chúng tôi chốt 4 nhóm:

| Nhóm | Vì sao tách riêng |
|---|---|
| **Học viên mới** | Hỏi khái niệm nền, chưa có từ vựng chuyên môn, câu hỏi ngắn và tổng quát |
| **Học viên đang làm capstone** | Nhóm đông nhất và gấp nhất — hỏi để nộp bài, sai là hỏng bài nộp |
| **Học viên ôn lại** | Đã học rồi, hỏi để nhớ lại; hay hỏi kiểu deixis ("cái này", "chỗ này") |
| **PM ngoài team** | Áp kiến thức sang sản phẩm của họ — dễ kéo tutor ra ngoài corpus |

**Ý định (intent)** — 5 trục, chọn theo tiêu chí *hành vi đúng của tutor phải khác nhau*
(slide s26, s28): hỏi khái niệm · xin ví dụ/how-to · hỏi mơ hồ cần slide context ·
hỏi ngoài phạm vi · adversarial (xin đáp án, prompt injection).

Chúng tôi **loại** các biến không tạo khác biệt hành vi: độ dài câu hỏi, có dấu/không dấu,
xưng hô — tutor phải trả lời như nhau, nên không phải dimension.

### Lưới của bạn

| Nhóm user \ Intent | Hỏi khái niệm | Xin ví dụ / how-to | Hỏi mơ hồ (deixis) | Ngoài phạm vi | Adversarial |
|---|---|---|---|---|---|
| **Học viên mới** | 01, 02 🔥 | 03 | — | 13 | — |
| **HV đang làm capstone** | 04, 06, 08 🔴 🔥 | 05, 07 🔥 | 17 🔴 | 16 | 19, 20 🔴 |
| **HV ôn lại** | 09 | 10 | 18 | 14 | — |
| **PM ngoài team** | 11 | 12 | — | 15 🔴 | — |

🔴 = ô rủi ro cao · 🔥 = ô tần suất cao

**Ô rủi ro cao nhất — 4 ô, và vì sao:**

1. **HV làm capstone × hỏi khái niệm** — học viên chép thẳng câu trả lời vào bài nộp.
   Tutor bịa "6 bước calibration" thành 5 bước là hỏng bài của người ta.
2. **HV làm capstone × adversarial** — `sc-20` là prompt injection thật: nếu tutor bỏ
   contract JSON hoặc lộ system prompt thì đây là lỗi bảo mật, không chỉ lỗi chất lượng.
3. **PM ngoài team × ngoài phạm vi** — `sc-15` hỏi giá API. Câu này **nghe rất in-scope**
   (đúng chủ đề eval) nhưng corpus không có số liệu giá. Đây là bẫy hallucination nặng nhất
   trong cả dataset: bịa bảng giá → PM ra quyết định ngân sách sai.
4. **HV làm capstone × hỏi mơ hồ** — deixis không có slide context thì vô nghĩa; đoán nhầm
   chủ đề là trả lời lạc đề 100%.

**Ô tần suất cao nhất:** HV làm capstone × (hỏi khái niệm + xin ví dụ) — 9/20 câu, vì đây là
lúc học viên hỏi nhiều nhất trong đời một khoá học.

**Blind spot còn lại (thành thật):** chưa phủ hỏi nối tiếp nhiều lượt (multi-turn), chưa phủ
câu hỏi tiếng Anh, chưa phủ câu hỏi về nội dung có trong corpus nhưng **mâu thuẫn giữa 2
nguồn** (vd Hamel vs Chip Huyen nói khác nhau).
