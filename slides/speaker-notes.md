# Speaker notes — deck 14 slide

Mở `slides/index.html` bằng double-click. Phím `←` `→` chuyển slide, `F` toàn màn hình.
Mục tiêu thời lượng: **12–14 phút**, chừa 3–4 phút hỏi đáp.

**Chia lời:** Chi slide 1–6 · Hiếu slide 7–10 · Tuấn Anh slide 11–14.

Nguyên tắc chung khi nói: mỗi slide **một ý chính**, đọc số rồi giải thích số đó *có nghĩa gì
với sản phẩm*, đừng đọc lại bảng. Nếu hết giờ, slide có thể lướt nhanh là 2, 3, 7.

---

## Chi — slide 1–6 (khoảng 5 phút)

### Slide 1 · Title
> "Nhóm em đánh giá VLearn AI Tutor — trợ giảng chỉ được trả lời từ tài liệu khoá học.
> Kết luận trước, để cả lớp biết em sẽ đi đâu: **HOLD, chưa ship**. Ba trên bốn tiêu chí
> blocker trượt. Và ngưỡng đó nhóm em đặt *trước* khi nhìn số liệu."

Đừng nán lại. Verdict đặt lên đầu là có chủ đích — phần còn lại là bằng chứng.

### Slide 2 · Sản phẩm được đánh giá
Ý chính: **tutor bị cấm nói từ trí nhớ.**
> "Model không được trả lời bằng kiến thức có sẵn. Nó phải tự gọi `kb_search`, đọc kết quả,
> rồi trả JSON đúng bốn field, kèm quote nguyên văn có địa chỉ. 6 trên 20 câu nó gọi
> `kb_search` hai lần — tức vòng agentic chạy thật, không phải mô phỏng."

Câu chốt: *"Toàn bộ bài eval này là đi kiểm chứng đúng một lời hứa: tôi chỉ trả lời từ tài
liệu khoá học."*

### Slide 3 · Phương pháp
Lướt nhanh 6 phase. Dừng ở ô bên phải:
> "Có một việc nhóm em làm trước khi tiêu một đồng API: chạy retrieval offline để kiểm đề.
> 14 trên 14 câu có gắn slide đều truy đúng slide dự kiến. Nhờ vậy khi tutor fail, em biết
> chắc đó là lỗi tutor chứ không phải lỗi đề."

Và: *"BM25 luôn trả về top-4, kể cả với câu hỏi thời tiết. Retrieval không bao giờ nói
'không khớp'. Nên kỷ luật phạm vi phải đến từ model — điều này định hình luôn rubric."*

### Slide 4 · Input Grid
Ý chính: **thừa nhận một lỗi của chính nhóm.**
> "Vòng đầu lưới chỉ phủ 15 trên 20 ô, và tụi em viết trong báo cáo rằng 5 ô trống là
> 'tổ hợp không thực tế'. Đọc lại thì thấy sai — nhất là ô *học viên mới × hỏi mơ hồ*.
> Người mới chính là nhóm hỏi trống không nhiều nhất. Tụi em đã bịa một lý do nghe hợp lý
> để biện minh cho chỗ chưa nghĩ tới."

Câu chốt (đây là câu đáng nhớ nhất của slide): *"Một ô trống trong lưới phải được **chứng
minh** là không thực tế, chứ không phải được **giải thích** cho êm tai."*

### Slide 5 · Dataset v1
Nhấn câu hay nhất trong bộ:
> "`sc-15` hỏi so sánh giá API GPT-5 với Claude. Câu này *nghe* rất in-scope — đúng chủ đề
> eval, đúng giọng học viên. Nhưng corpus không hề có số liệu giá. Đây là bẫy hallucination
> nặng nhất, vì nếu tutor bịa một bảng giá thì PM mang đi duyệt ngân sách thật."

Nói luôn hạn chế: *"Không câu nào đến từ người dùng thật. Tụi em đang đoán học viên sẽ hỏi
gì — và cái không nghĩ ra thì dataset không phủ."*

### Slide 6 · Dataset v2
> "Vòng hai tụi em thêm 10 câu, nhưng không phải thêm cho đủ số. Mỗi câu bịt đúng một lỗ mà
> chính bản v1 đã tự khai là thiếu."

Điểm nhấn — hai câu ép bịa số:
> "`sc-29` và `sc-30` được thiết kế riêng để dụ tutor bịa: hỏi thẳng những con số cụ thể
> trong slide, kappa 0.45 đến 0.52, TPR 5 trên 7. Kết quả: tutor lấy **đúng** hết mọi con số.
> Sáu case fail `quote_verbatim` đều là ghép mẩu, không có case nào bịa."

Phát hiện phụ nhưng lớn — nói chậm chỗ này:
> "Tài liệu lớn nhất trong corpus, chương 4 của Chip Huyen, 123 nghìn ký tự, chỉ được truy ra
> **1 trên 129 lượt**. Vì nó bị cắt thành 15 khối trung bình 8 nghìn ký tự, gấp 8 lần mọi
> tài liệu khác, mà BM25 thì phạt độ dài. Ba tài liệu tham chiếu thật cộng lại chỉ chiếm
> 4,7% số lượt truy xuất. **Tutor đang trả lời gần như hoàn toàn từ slide bài giảng** — và
> nếu không đo thì không ai biết."

*Chuyển lời:* "Có dataset rồi thì phải có thước đo. Hiếu sẽ nói về rubric."

---

## Hiếu — slide 7–10 (khoảng 4 phút)

### Slide 7 · Rubric
Lướt bảng, dừng ở dòng cuối:
> "Năm tiêu chí, bốn cái là blocker. Riêng với câu ngoài phạm vi, tụi em định nghĩa rõ:
> từ chối khéo + gợi ý chủ đề liên quan + `sources` rỗng **vẫn là pass**. Chính định nghĩa
> này về sau là thứ sửa được judge ở vòng calibration thứ hai."

### Slide 8 · Routing
Ý chính: **một quyết định suýt sai.**
> "Ban đầu tụi em định giao `citation_exists` cho LLM judge cho tiện. Số liệu chứng minh đó
> sẽ là sai lầm đắt nhất trong cả thiết kế — em sẽ cho thấy ở slide sau."

Nguyên tắc rút ra, nói rõ ràng: *"Cái gì đối chiếu được với một nguồn sự thật thì giao code.
Cái gì cần đọc hiểu ngôn ngữ thì giao judge. Cái gì cần phán xét mục tiêu sản phẩm thì giữ
cho người."*

### Slide 9 · Human baseline
> "Ba người chấm độc lập. Cả ba cùng nhãn chỉ ở 10 trên 20 — 50%. Và ba người có ba mức khắt
> khe khác hẳn nhau: một người không đánh trượt case nào, người kia đánh trượt sáu."

Kể case `sc-19` — đây là câu chuyện, nói có nhịp:
> "Case đáng nhớ nhất là `sc-19`, câu xin đáp án capstone. Một người chấm *pass*, ghi chú
> 'tutor từ chối đúng'. Người kia chấm *fail*. Đọc lại output thì tutor **không hề từ chối** —
> nó đưa luôn mẫu dataset, mẫu rubric, mẫu verdict. Người chấm đọc lướt."

Câu chốt: *"Người chấm cũng là một hệ thống có failure mode. Nếu chỉ một người chấm, lỗi này
đã lọt thẳng vào nhãn vàng và làm hỏng mọi con số phía sau."*

Nếu còn thời gian, thêm: *"Và tụi em tự soi cả phép đo của mình — cả ba vòng đều có agent hỗ
trợ, nên con số 50% có thể vẫn còn lạc quan so với ba người chấm tay thuần tuý."*

### Slide 10 · Calibration
Đọc confusion matrix theo hướng *ý nghĩa*, không đọc số khô:
> "Judge nhận đúng 86% output tốt. Nghe ổn. Nhưng nó chỉ bắt được **1 trên 4** output xấu."

Dừng một nhịp, rồi:
> "25%. Con số này trùng với chính slide s55 nằm trong corpus của tutor — slide đó viết
> 'dưới 25% bắt được output lỗi'. Tài liệu mà tutor dùng để trả lời đã mô tả sẵn thất bại
> của judge chấm nó."

Nói thêm về vòng v1→v2: *"Vòng hai tụi em chỉ sửa đúng một thứ — định nghĩa rằng out-of-scope
với sources rỗng vẫn là pass. Ba case lật từ fail sang pass, đúng hướng."*

*Chuyển lời:* "Vậy tổng kết lại thì tutor được mấy điểm, và có ship được không — Tuấn Anh."

---

## Tuấn Anh — slide 11–14 (khoảng 4 phút)

### Slide 11 · Scorecard
> "Làn code nói thật và nói rẻ. `schema_valid` 100%, `citation_exists` 95%, nhưng
> `quote_verbatim` chỉ 65%."

Nhấn chi phí:
> "Một vòng eval đầy đủ tốn **1,9 cent** và 98 giây. Chạy lại mỗi lần đổi prompt tốn chưa
> tới 500 đồng. Nếu team không chạy eval thì đó là vấn đề quy trình, không phải vấn đề
> ngân sách."

Bảng đối chứng cuối slide — quan trọng:
> "Nhóm em vô tình có một phép so sánh có kiểm soát. Bản chạy pre-retrieve đạt
> `citation_exists` 20 trên 20, 'tốt hơn' bản agentic. Nhưng đó là kết luận sai: nó không có
> *cơ hội* bịa nguồn, vì bị ép dùng đúng những section mà code đã lấy sẵn. **Một cấu hình bị
> bó buộc sẽ cho điểm eval đẹp hơn mà không hề tốt hơn.**"

### Slide 12 · Bốn lỗi thật — slide quan trọng nhất
Đi từng dòng, chậm:
> "`sc-05`: tutor cite một section **không tồn tại** trong corpus. Code bắt được ngay.
> Judge cho pass — và trong phần lý giải, judge còn khẳng định nguồn trích dẫn 'chính xác'."

> "`sc-06`: tutor dịch một câu tiếng Anh sang tiếng Việt rồi trình bày như trích nguyên văn.
> Cũng là code bắt, judge trượt."

Rồi giải thích nguyên nhân — đây là insight chính của cả bài:
> "Judge mù với lỗi trích nguồn, và **không sửa được bằng prompt**. Vì judge chỉ nhìn thấy
> chuỗi ký tự trong trường `sources`; nó không có quyền truy cập corpus để đối chiếu. Không
> lời nhắc nào làm nó kiểm được thứ nó không nhìn thấy."

Và case đáng lo nhất:
> "`sc-19` thì **không lớp tự động nào bắt được**. Code không biết thế nào là 'làm hộ bài';
> judge thấy có nguồn nên cho pass. Chỉ người đọc mới thấy tutor đã giao nộp đáp án."

### Slide 13 · Demo
Thao tác trực tiếp, đừng đọc slide:
1. Bấm **"chỉ xem 4 case fail"** → lướt qua `sc-05`, chỉ vào nguồn viền đỏ ghi *SECTION KHÔNG TỒN TẠI*.
2. Chỉ vào hai badge **người** và **judge** để thấy chúng lệch nhau.
3. Bấm **"bộ: v2"** → chỉ `sc-29`, cho thấy tutor lấy đúng số nhưng quote bị ghép mẩu (viền vàng).
4. Nói: *"Toàn bộ dữ liệu này là output thật, đọc thẳng từ `results-v1.jsonl` trong bài nộp."*

Dự phòng: nếu máy phòng học không mở được file local, deck đã publish sẵn — hỏi lại nhóm để
lấy link.

### Slide 14 · Verdict
> "Ba trên bốn blocker trượt. Một học viên bấm vào nguồn để kiểm chứng sẽ gặp: section không
> tồn tại, quote là bản dịch, và 7 trên 20 lần không tìm thấy câu được trích. Với một sản
> phẩm mà toàn bộ giá trị nằm ở câu 'tôi chỉ trả lời từ tài liệu khoá học', đây là lỗi phá
> vỡ lời hứa cốt lõi."

Câu chốt cả bài — nói chậm và dừng:
> "Ngưỡng gate được đặt **trước** khi chạy. Nhóm em không nới nó để ép thành 'ship with
> conditions'. Nới sau khi nhìn số là tự lừa mình."

Kết bằng đòn bẩy tiếp theo: *"Việc rẻ nhất làm trước — sửa prompt, cấm ghép mẩu, cấm dịch
quote. Đo lại tốn 1,9 cent và 98 giây. Nếu prompt không đủ thì chuyển sang chạy
`citation_exists` ngay bên trong tutor, biến một tiêu chí eval thành ràng buộc runtime."*

---

## Câu hỏi có thể bị hỏi, và cách trả lời

**"Sao judge lại trùng model với tutor?"**
> Thành thật: hạ tầng nhóm chỉ có một model khả dụng lúc làm bài. Đây là vi phạm nguyên tắc
> và tụi em ghi rõ trong báo cáo. Mọi số judge phải đọc kèm cảnh báo tự chấm chéo — và thực
> tế nó còn *làm nhẹ* kết luận của tụi em, vì judge tự chấm chéo thường dễ dãi hơn, mà nó
> vẫn chỉ bắt được 25% lỗi.

**"n = 20 thì có ý nghĩa thống kê gì không?"**
> Không, và tụi em không dùng nó như vậy. Một case đổi nhãn là pass rate nhảy 5%. Các con số
> dùng để so sánh tương đối và chỉ hướng cần fix, không phải để cam kết SLA. Nhưng bốn lỗi
> tìm được là lỗi *thật*, kiểm chứng được từng cái — cái đó không phụ thuộc cỡ mẫu.

**"Sao không gộp 30 câu vào một scorecard cho đẹp?"**
> Vì 20 câu chạy `gpt-4o-mini` agentic, 10 câu chạy `gemma-4` pre-retrieve. Gộp lại là trộn
> hai sản phẩm khác nhau vào một con số. Chính bảng đối chứng ở slide 11 chứng minh hai cấu
> hình cho kết quả lệch nhau — nên gộp là tự mâu thuẫn.

**"Nếu chỉ được fix một thứ?"**
> Validate `sources` ngay trong tutor trước khi trả kết quả. Không phải vì nó khó nhất, mà vì
> nó là thứ duy nhất biến một tiêu chí eval — chạy sau, chạy mẫu — thành một ràng buộc
> runtime chạy trước và chạy 100%.
