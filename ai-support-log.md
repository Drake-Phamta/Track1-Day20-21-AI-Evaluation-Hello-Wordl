# AI Support Log — Chi (Dataset & Coverage Lead → Slides Lead)

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | Thiết kế Input Grid 4×5 | Claude Code: gợi ý trục người dùng và trục intent, đề xuất ô nào rủi ro cao | Tự đối chiếu với slide s26/s28 về tiêu chí "đổi giá trị → hành vi đúng có đổi không"; loại các biến AI đề xuất mà không tạo khác biệt hành vi (độ dài câu, có dấu/không dấu, xưng hô) |
| 2 | Sinh 20 scenario của dataset v1 | Claude Code: sinh câu hỏi, neo mỗi câu vào một slide id có thật trong deck 66 slide | **Chạy `tutor.retrieve_corpus()` offline trước khi tốn API** — 14/14 câu có slide đều truy đúng slide dự kiến trong top-4. Câu nào trượt thì viết lại, không giữ câu chết |
| 3 | Sinh 10 scenario mở rộng của dataset v2 | Claude Code: soạn câu đóng đúng các blind spot đã ghi ở mục 2 và 7 của REPORT | Kiểm retrieval lại y hệt bước 2 (6/6 câu có slide đạt). Hai câu bị viết lại vì trượt: `sc-28` phải thêm từ khoá cụ thể, `sc-27` phải đổi thành phép dò coverage sau khi thấy corpus không cho phép so sánh hai nguồn |
| 4 | Gán nhãn 20 row (labels-chi.csv) | Claude Code hỗ trợ đọc và tóm tắt output; nhãn cuối do mình quyết | Đối chiếu từng row với `expected_behavior` trong metadata dataset và với rubric 5 tiêu chí ở mục 3; ghi lý do cho mọi nhãn `fail` và `uncertain` |
| 5 | Gán nhãn 10 row bộ v2 (labels-v2-gateway.csv) | Như trên | Với `sc-25`, tự tra lại slide s48 để xác minh ba mốc 80/90/99,9% có thật trong corpus — hoá ra **kỳ vọng của dataset sai chứ không phải tutor sai** |
| 6 | Dựng deck `slides/index.html` | Claude Code: viết HTML/CSS/JS, dựng `build.py` nạp số liệu từ `evidence/` | Chạy `build.py` rồi kiểm: thẻ đóng/mở cân, JSON parse được, không token màu nào thiếu định nghĩa, deck chạy offline không cần mạng. Lướt tay hết 14 slide |
| 7 | Viết mục 1 và 2 của REPORT | Claude Code: soạn bản nháp từ dataset | Đọc lại và sửa phần "vì sao" cho đúng lập luận của nhóm; phát hiện và sửa một kết luận sai của chính bản nháp (xem dưới) |

## Phần AI gợi ý mà mình bác bỏ

- **Lập luận "5 ô lưới trống là tổ hợp không thực tế".** Bản nháp mục 2 do AI soạn viết rằng
  năm ô còn trống được bỏ có chủ đích vì không thực tế — ví dụ "học viên mới chưa đủ vốn để
  prompt-inject", "PM không ngồi trước slide nên không hỏi deixis". Nghe rất trôi chảy, và
  **sai**. Người mới chính là nhóm hỏi trống không nhiều nhất. Đây là AI bịa một lý do hợp lý
  cho một chỗ chưa nghĩ tới, và mình suýt để nguyên. Vòng v2 lấp cả 5 ô, cả 5 đều là câu hỏi
  thật — mình giữ lại phần tự phê này trong báo cáo thay vì lặng lẽ xoá.

- **Đề xuất gộp 30 câu vào một scorecard.** Bộ v2 chạy `gemma-4` pre-retrieve, bộ v1 chạy
  `gpt-4o-mini` agentic. Gộp lại thì bảng số nhìn "đầy đặn" hơn nhưng là trộn hai sản phẩm
  khác nhau vào một con số — đúng cái lỗi mà bảng đối chứng ở mục 6 đang cảnh báo. Giữ tách
  riêng, chấp nhận báo cáo nhìn rời hơn.

- **Đề xuất bỏ `sc-27` vì "câu không trả lời được".** Retrieval không truy ra được
  `chip-huyen-ch4` nên câu này gần như chắc chắn không so sánh được hai nguồn. AI đề xuất bỏ
  hoặc viết lại thành câu dễ. Mình giữ, nhưng đổi *mục đích* của nó thành **phép dò coverage
  retrieval** và ghi rõ trong note. Nhờ giữ lại mới lòi ra phát hiện lớn nhất của vòng v2:
  một phần ba corpus gần như chết.

## Phần hoàn toàn tự làm

- Chốt tỉ lệ 12/4/2/2 của dataset v1 và lý do đằng sau nó.
- Quyết định giữ `sc-27` và đổi mục đích của nó thay vì bỏ.
- Chốt nhãn cuối cho cả 30 row — AI đọc và tóm tắt giúp, nhưng nhãn `fail` nào cũng do mình
  đối chiếu lại với rubric rồi mới ghi.
- Quyết định giữ nguyên phần tự phê về lỗi "5 ô trống" trong báo cáo, dù xoá đi thì bài
  nhìn gọn hơn.

## AI sai ở đâu

1. **Bịa lý do cho chỗ trống** (đã nói ở trên) — nguy hiểm vì nó nghe thuyết phục.
2. **Kết luận vội về `quote_verbatim`.** Lần đầu nhìn tỉ lệ 60%, AI diễn giải là "tutor có vấn
   đề groundedness". Soi từng token thì **0/8 case là bịa** — tất cả chỉ là ghép mẩu bằng dấu
   ba chấm. Nếu tin luôn kết luận đầu thì routing map đã đi sai hướng hoàn toàn.
3. **Đề xuất hai code check không phân biệt được gì.** `check_followup_count` và
   `check_quote_length` đều 20/20 pass trên bộ v1 — hữu ích làm regression guard nhưng không
   phải là eval. Bài học: một check không bao giờ fail thì chưa đo được gì.
