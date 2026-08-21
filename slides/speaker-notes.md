# Speaker Notes - VLearn AI Tutor Evaluation

## Slide 1: Bối cảnh (Chi)
- Xin chào mọi người, hôm nay nhóm chúng mình trình bày kết quả đánh giá vòng đầu tiên (Eval loop) cho VLearn AI Tutor.
- Trọng tâm của đợt này là đảm bảo Tutor trả lời chính xác, không ảo giác, và giữ đúng vai trò giáo dục.

## Slide 2: Input Grid (Chi)
- Về nhóm người dùng, chúng ta chia 4 nhóm: học viên mới, học viên làm capstone (quan trọng nhất), học viên ôn lại, và PM ngoài team.
- Về Intent, có 5 trục chính, nhưng quan tâm đặc biệt tới hỏi khái niệm và các câu hỏi mơ hồ (deixis).

## Slide 3: Dataset v1 (Chi)
- Từ lưới trên, chúng mình chốt 20 scenario cho tập dataset v1.
- Trong đó 60% là in-scope, 20% out-of-scope, 10% để đo deixis và 10% adversarial.
- Dataset này đủ để bắt được các lỗi điển hình, đặc biệt là lỗi ảo giác và trích dẫn sai.

## Slide 4: Rubric Đánh giá (Chi)
- Chúng mình sử dụng 5 tiêu chí: schema_valid, citation_valid, groundedness, scope_correct, và pedagogy.
- Trong đó 4 tiêu chí đầu là BLOCKER. Sai một cái là cả câu trả lời Fail ngay.

## Slide 5: Chiến lược Routing (Chi)
- Không phải mọi thứ đều vứt cho LLM judge.
- Code kiểm tra schema, đếm follow-up, đếm số từ.
- LLM Judge chỉ chấm groundedness và scope.
- Pedagogy và adversarial thì giữ cho con người chấm vì Judge chưa đủ khả năng.

## Slide 6: Kết quả Baseline (Chi)
- Vòng chấm độc lập đầu tiên, agreement của 3 người đạt 85%.
- Bất đồng lớn nhất là ở tiêu chí groundedness và pedagogy.
- Từ đó chúng mình siết chặt định nghĩa rubric lại.

## Slide 7: LLM Judge Calibration - V1 (Hiếu)
- Mình phụ trách phần Calibration cho LLM Judge.
- Ở vòng 1, judge chấm quá khắt khe với các câu out-of-scope. Nếu nguồn rỗng, nó lập tức chấm Fail.

## Slide 8: LLM Judge Calibration - V2 (Hiếu)
- Chúng mình thay đổi duy nhất một rule trong prompt: dạy judge rằng out-of-scope từ chối đúng cách với sources rỗng là PASS.
- Kết quả agreement tăng từ 55% lên 70% ở v2.

## Slide 9: Hạn chế của bộ nhãn (Hiếu)
- Tuy nhiên, 70% này chỉ phản ánh việc judge "không fail oan".
- Thực tế bộ 20 nhãn của chúng ta chưa có lỗi "trả lời sai" nào từ tutor, nên chúng ta chưa đo được recall (khả năng bắt lỗi thật) của judge.

## Slide 10: Code Checks Pipeline (Hiếu)
- Để bù đắp, hệ thống code checks tự động đã hoạt động rất hiệu quả, đạt tốc độ cao và chi phí 0 đồng.
- Nó bắt được lỗi lớn nhất của vòng này là trích dẫn không nguyên văn.

## Slide 11: Scorecard & Kết quả chung (Tuấn Anh)
- Từ số liệu thực tế, pass rate như sau: Schema 100%, Follow-up 100%, Groundedness 90%.
- Điểm trừ nặng nhất: Quote_verbatim chỉ đạt 65%. Tutor có xu hướng dịch hoặc paraphrase thay vì copy-paste nguyên văn.

## Slide 12: Quyết định Gate (Tuấn Anh)
- Dựa trên scorecard, chúng ta vi phạm Gate trích dẫn (yêu cầu >=90%).
- Quyết định cuối cùng: HOLD. Không ship version này.

## Slide 13: Các vấn đề cần giải quyết (Tuấn Anh)
- Đòn bẩy tiếp theo: Phải sửa SYSTEM_PROMPT để bắt buộc tutor copy-paste 100% khi trích quote.
- Đồng thời, cần bổ sung code check để đảm bảo section_id thực sự tồn tại trong corpus.

## Slide 14: Bài học áp dụng (Tuấn Anh)
- Bài học lớn nhất: Luôn ưu tiên Code checks (deterministic rules) trước khi dùng LLM judge. 
- Tiết kiệm token, nhanh, và không có sai số.
- Cảm ơn mọi người đã lắng nghe!
