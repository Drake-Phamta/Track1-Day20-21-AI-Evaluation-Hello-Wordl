# AI Support Log — Tuấn Anh

Buổi capstone này tôi làm cùng một agent (Claude Code) gần như toàn bộ thời gian. Ghi lại
trung thực chỗ nào AI làm, chỗ nào tôi bác, chỗ nào tôi tự quyết.

## Tôi dùng AI ở đâu

| Việc | AI làm gì | Tôi làm gì |
|---|---|---|
| Đọc hiểu repo | Quét toàn bộ `tutor/`, `eval/`, `deliverables/`, dựng bản đồ "cái gì xong / cái gì trống" | Đọc lại README và `deliverables/README.md` để tự xác nhận yêu cầu nộp bài |
| Kế hoạch 150 phút | Soạn SPRINT-PLAN, phân việc 3 người, luật git chống conflict | Chốt mô hình nhánh, chọn cách tách `_parts/` |
| Dataset v1 | Sinh 20 scenario neo vào slide id thật, viết script kiểm retrieval offline | Chốt lưới 4×5, chốt tỉ lệ 12/4/2/2, duyệt lại từng câu hỏi |
| Gỡ lỗi gateway | Smoke test phát hiện tool-calling trả 400, viết fallback pre-retrieve | Quyết định chấp nhận fallback thay vì chờ admin bật tool parser |
| Gán nhãn | Đọc 20 output, đề xuất nhãn kèm lý do | Duyệt từng nhãn; đây là nơi tôi kiểm kỹ nhất vì nhãn sai là hỏng cả bài |
| Merge nhánh Hiếu | So sánh 2 bộ results, chỉ ra chúng khác nhau hoàn toàn | Quyết định lấy results của Hiếu làm chuẩn |
| REPORT mục 1,2,6,7 + slides | Soạn nội dung và dựng deck | Chốt verdict HOLD và các ngưỡng gate |

## Phần nào AI gợi ý mà tôi bác bỏ? Vì sao?

**1. Hai code check đầu tiên AI đề xuất — tôi bác sau khi thấy số liệu.**
AI đề xuất `check_followup_count` và `check_quote_length`. Chạy thử: cả hai **20/20 pass**,
tức không phân biệt được gì. Tôi yêu cầu đổi sang `check_quote_stitched` (tách "ghép mẩu"
khỏi "bịa") vì nó bám đúng failure mode thật đã tìm ra. Bài học: một check không bao giờ fail
thì không phải là eval, nó chỉ là regression guard.

**2. AI ban đầu định để verdict là "SHIP WITH CONDITIONS" — tôi ép về HOLD.**
Ở bản scorecard đầu (chạy trên gateway `gemma-4`), mọi blocker đều 100% và AI viết verdict
"ship with conditions". Tôi thấy sai: điểm 100% đó là vì gateway chặn tool-calling nên tutor
bị ép dùng nguồn có sẵn — **nó không có cơ hội bịa nguồn**. Điểm đo hạ tầng, không đo tutor.
Sau khi chuyển sang results agentic thật của Hiếu, verdict về đúng HOLD.

**3. AI suýt để tôi tin con số 100% của bản pre-retrieve là "tutor tốt".**
Đây là chỗ tôi phải tự bắt. Nó dạy tôi một câu hỏi mang về được: *phiên bản này có **cơ hội**
mắc lỗi đó không?* — hỏi trước khi mừng vì pass rate tăng.

**4. Tôi bác việc nới ngưỡng gate cho khớp kết quả.**
Khi thấy 3/4 blocker trượt, phản xạ đầu tiên là hạ ngưỡng `quote_verbatim` từ 90% xuống 60%
để "vẫn ship được". Tôi giữ nguyên ngưỡng vì nó đã được đặt **trước** khi chạy. Nới sau khi
nhìn số là tự lừa mình — và đó đúng là thứ slide s50 ("verdict phải có răng") cảnh báo.

## Phần nào tôi hoàn toàn tự làm?

- Quyết định lấy `results-v1` của Hiếu làm chuẩn thay vì bản của mình, dù bản của mình có
  điểm đẹp hơn. Lý do: bản của Hiếu chạy đúng sản phẩm mà bài lab yêu cầu đánh giá.
- Toàn bộ các ngưỡng gate và verdict cuối.
- Cách xử lý 9 case bất đồng: không bỏ phiếu mà **kiểm chứng lại** — 4 case là sự thật kiểm
  được bằng code nên chốt theo kiểm chứng, 2 case mơ hồ thật thì giữ `uncertain` chứ không ép.
- Quyết định ghi thẳng các hạn chế vào bài (judge trùng model tutor, chỉ 2 người chấm, chưa
  có tracing) thay vì giấu đi.

## AI sai ở đâu

- Đề xuất check không phân biệt được gì (mục 1 ở trên).
- Đọc `code-checks-v1.txt` của Hiếu và không nhận ra ngay nó bị lưu UTF-16 (git báo binary);
  tôi phải chỉ ra thì mới sinh lại bằng UTF-8.
- Ở vòng đầu, AI diễn giải `quote_verbatim` 60% là "tutor có vấn đề về groundedness". Soi kỹ
  từng token thì **0/8 case là bịa** — chỉ là ghép mẩu. Kết luận vội ban đầu đã sai về bản chất
  lỗi, và nếu tin luôn thì routing map đã đi sai hướng.
