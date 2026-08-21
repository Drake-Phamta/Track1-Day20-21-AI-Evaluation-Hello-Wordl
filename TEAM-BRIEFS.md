# Brief cho agent — dán thẳng vào Claude Code của bạn

Đọc [SPRINT-PLAN.md](SPRINT-PLAN.md) trước để nắm bối cảnh. File này là prompt sẵn cho agent
của từng người. Copy nguyên khối của mình, dán vào agent, bắt đầu luôn.

**Setup chung, làm trước (cả 3 người, 5 phút):**

```powershell
git clone https://github.com/Drake-Phamta/Track1-Day20-21-AI-Evaluation-Hello-Wordl
cd Track1-Day20-21-AI-Evaluation-Hello-Wordl
git config pull.rebase true
git checkout -b feat/<ten-cua-ban>          # chi | hieu | ta

$env:PYTHONIOENCODING="utf-8"               # BẮT BUỘC, thiếu là crash UnicodeEncodeError
pip install -r requirements.txt
pip install braintrust
Copy-Item .env.example .env                 # điền KEY RIÊNG của bạn
python tests/test_eval_kit.py               # phải ra "44 pass, 0 fail"
```

`.env` tối thiểu:
```
DEEPSEEK_API_KEY=...
OPENAI_API_KEY=...
EVAL_MODEL=deepseek/deepseek-v4-flash
EVAL_JUDGE_MODEL=openai/gpt-4o-mini
BRAINTRUST_API_KEY=...
BRAINTRUST_PROJECT=vlearn-tutor-eval
```

⚠️ Dùng `python`, **không phải `python3`** (không có trên PATH). Mọi lệnh chạy từ **root repo**.

---

## BRIEF — CHI (Dataset Lead → Slides Lead)

```
Tôi là Chi, làm bài lab AI Evaluation trong repo này. Đọc SPRINT-PLAN.md để nắm bối cảnh.

Vai của tôi: Dataset Lead → Slides Lead.

LUẬT GIT — TUYỆT ĐỐI: tôi CHỈ được sửa các file sau, không đụng file nào khác:
  - deliverables/evidence/dataset-v1.jsonl
  - deliverables/_parts/01-input-grid.md
  - deliverables/_parts/02-dataset.md
  - slides/  (thư mục mới, toàn quyền)
Không mở deliverables/REPORT.md. Không sửa eval/ hay tutor/. Nếu cần đổi file của người
khác thì báo tôi, đừng tự sửa.

VIỆC 1 (làm ngay, ~15 phút) — review dataset:
dataset-v1.jsonl đã có sẵn 20 câu do Tuấn Anh sinh, và _parts/01 + 02 đã có draft đầy đủ.
Đọc kỹ cả 3 file. Việc của tôi là REVIEW chứ không viết lại:
  - Câu hỏi có nghe giống học viên VinUni thật viết không? Sửa lại giọng cho tự nhiên.
  - Có câu nào trùng ý nhau không? Có ô nào trong lưới đáng lẽ phải phủ mà đang trống?
  - Phần "vì sao" trong _parts/01 và 02 có phải giọng của nhóm tôi không? Chỉnh lại.
Nếu sửa dataset thì chạy lại kiểm tra retrieval để chắc câu vẫn trả lời được:
  python -c "import sys;sys.path.insert(0,'tutor');import tutor,json,io;[print(r['scenario_id'],[h['doc_id']+'#'+h['section_id'] for h in tutor.retrieve_corpus(r['input']+' '+(r['metadata'].get('slide') or {}).get('keyword',''),top_k=4)]) for r in map(json.loads,io.open('deliverables/evidence/dataset-v1.jsonl',encoding='utf-8'))]"
Commit + push trước phút 45.

VIỆC 2 (từ phút 70 đến hết) — dựng slides/index.html:
Một file HTML self-contained, KHÔNG dùng CDN, không asset ngoài, mở bằng double-click là chạy.
  - Nav bàn phím ←/→/Space, số slide, progress bar, có dark mode (@media prefers-color-scheme)
  - Nhúng data thật: đọc deliverables/evidence/results-v1.jsonl và verdicts-v2.jsonl, paste
    vào <script type="application/json"> để chart và slide demo render từ số liệu thật.
    QUAN TRỌNG: escape chuỗi "</script>" trong nội dung tutor trước khi nhúng, không là vỡ trang.
  - Slide DEMO là điểm nhấn: nhúng bản rút gọn giao diện report.html ngay trong deck —
    card scenario, câu hỏi + slide context, JSON output của tutor, sources, verdict judge +
    rationale, nút prev/next lướt qua case. Chọn sẵn 1 case pass đẹp + 1 case fail rõ.
  - 13 slide theo outline ở mục 4 của SPRINT-PLAN.md.
Trước phút 125 thì số liệu còn là placeholder cũng được; phút 125 Tuấn Anh chốt số, tôi thay số thật.

Nhịp: commit nhỏ mỗi 15 phút, message dạng "[chi] ...".
Trước mỗi push: git pull --rebase origin master, rồi git push origin feat/chi
```

---

## BRIEF — HIẾU (Rubric & Judge Lead)

```
Tôi là Hiếu, làm bài lab AI Evaluation trong repo này. Đọc SPRINT-PLAN.md để nắm bối cảnh.

Vai của tôi: Rubric & Judge Lead.

LUẬT GIT — TUYỆT ĐỐI: tôi CHỈ được sửa các file sau, không đụng file nào khác:
  - eval/judge_prompt.md
  - eval/code_checks.py
  - deliverables/evidence/judge-prompt-v1.md, judge-prompt-v2.md, verdicts-v1.jsonl, verdicts-v2.jsonl
  - deliverables/_parts/03-rubric.md, 04-routing.md, 05-calibration.md
Không mở deliverables/REPORT.md. Không sửa eval/run_eval.py, eval/judge.py, eval/report.py,
eval/agreement.py, eval/tracing.py, tutor/, tests/. Không sửa dataset.

VIỆC 1 (làm ngay, ~30 phút) — rubric + routing + custom code checks:

a) Chốt 5 tiêu chí chấm, viết vào _parts/03-rubric.md (mỗi tiêu chí: pass khi / fail khi /
   có phải blocker không / ví dụ pass / ví dụ fail). Gợi ý bộ tiêu chí:
   schema_valid, citation_valid, groundedness, scope_correct, pedagogy.
   LƯU Ý QUAN TRỌNG từ khâu dataset: BM25 luôn trả về top-4 kể cả với câu hỏi thời tiết,
   nên retrieval không bao giờ nói "không khớp". Vì vậy scope_correct PHẢI là tiêu chí
   riêng, không được suy ra từ việc có citation hay không.

b) Thêm 2 hàm check vào eval/code_checks.py. Signature BẮT BUỘC là (rec, section_tokens)
   và trả True/False/None — vì dispatch ở dòng 89-94 so sánh identity của hàm, sai
   signature là rơi nhầm nhánh. Đăng ký vào list CHECKS ở dòng 68.
   - check_followup_count: đúng 3 câu follow-up, không rỗng, không lặp lại câu hỏi gốc
   - check_quote_length: mỗi quote ≤ 40 từ (SYSTEM_PROMPT trong tutor/tutor.py:38-48 yêu cầu vậy)
   Chạy `python tests/test_eval_kit.py` sau khi sửa — phải vẫn 44 pass, 0 fail.

c) Viết _parts/04-routing.md: bảng tiêu chí nào giao cho code / LLM judge / con người,
   kèm lý do. Nêu rõ tiêu chí nào ban đầu định cho judge nhưng code kiểm được rẻ hơn.

Commit + push trước phút 45.

VIỆC 2 (từ phút 70) — calibrate judge 2 vòng. Bắt buộc phải có v1 VÀ v2, spec đòi.
  Copy-Item eval\judge_prompt.md deliverables\evidence\judge-prompt-v1.md   # COPY TRƯỚC KHI SỬA
  Copy-Item deliverables\evidence\results-v1.jsonl results.jsonl
  # cần labels.csv (gold, majority vote) — Tuấn Anh đưa, copy vào root
  python eval/judge.py
  Copy-Item verdicts.jsonl deliverables\evidence\verdicts-v1.jsonl
Đọc confusion matrix + agreement %. Xác định judge lệch đâu: chặt quá hay lỏng quá, lệch ở
nhóm in-scope hay out-of-scope. Rồi sửa judge_prompt.md ĐÚNG MỘT THỨ, copy ra
judge-prompt-v2.md, chạy lại → verdicts-v2.jsonl, so agreement v1 vs v2.

VIỆC 3 — viết _parts/05-calibration.md: số row gán nhãn, agreement v1, dán NGUYÊN confusion
matrix từ output, diff prompt v1→v2 và VÌ SAO sửa thế, agreement v2, kết luận judge đủ tin
để tự động chấm tiêu chí nào và tiêu chí nào phải giữ cho người.

Nhịp: commit nhỏ mỗi 15 phút, message dạng "[hieu] ...".
Trước mỗi push: git pull --rebase origin master, rồi git push origin feat/hieu
```

---

## Việc chung cả 3 người: gán nhãn tay (phút 45–70)

Đây là **yêu cầu cứng** của lab — phải có nhãn của 3 người chấm độc lập.

Sau khi Tuấn Anh push `results-v1.jsonl`:

```powershell
git pull --rebase origin master
Copy-Item deliverables\evidence\results-v1.jsonl results.jsonl
python eval/report.py
start report.html
```

- Chấm **độc lập** — không nhìn bài nhau, không bàn trước. Bàn trước là hỏng con số agreement.
- Mỗi row: pass / fail / uncertain + **note ngắn ghi tiêu chí gây fail** (vd `fail: citation`,
  `fail: scope`, `fail: bịa số`). Note này là dữ liệu cho mục 7 của REPORT.
- Bấm **Export labels.csv** → đổi tên thành `labels-chi.csv` / `labels-hieu.csv` /
  `labels-tuananh.csv` (script `agreement.py` parse tên người từ **tên file**, đặt sai là hỏng).
- Copy vào `deliverables/evidence/` rồi commit. Đừng để ở root — root bị `.gitignore` chặn.

Label lưu trong `localStorage` của **từng browser**, nên mỗi người phải chấm trên máy mình.
