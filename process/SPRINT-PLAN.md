# MASTER PLAN — 150 phút, 3 người, hoàn thành 100% Lab AI Evaluation + Slides demo

## Context

`Track1-Day20-21-AI-Evaluation-Hello-Wordl` là **starter kit**, không phải bài đang làm dở:

- **Engine 100% xong** — `tutor/tutor.py` (353 dòng: SYSTEM_PROMPT thật, BM25 tự viết, vòng tool-calling `kb_search` max 6 bước, multi-provider), `eval/` 6 script hoàn chỉnh không stub, corpus 18 doc / 341 section, `tests/test_eval_kit.py` 44 test **đã verify pass 44/44**.
- **Bài nộp 0%** — `deliverables/REPORT.md` (182 dòng) mọi bảng đều `| | | |`, `ai-support-log.md` rỗng, `evidence/` chỉ có `.gitkeep`. Chưa có `.env`, `dataset.jsonl`, `results.jsonl`, `report.html`.
- **Không có Wordle** — grep `wordl|wordle` toàn tree = 0 hit. Sản phẩm được đánh giá là **VLearn AI Tutor**.
- **Không có slides deliverable** — phải dựng từ đầu.

Mục tiêu: trong 150 phút, 3 người (Chi, Hiếu, Tuấn Anh) + agent hoàn thành đủ 6 phase → `REPORT.md` 7 mục có số liệu thật, `evidence/` đủ data thô, và một **HTML deck self-contained** thuyết trình được trước lớp.

**Rủi ro lớn nhất là git conflict trên `REPORT.md`** (1 file, 3 người viết) → plan này tách thành file part rời, ghép ở phút 125.

---

## 0. Sự thật kỹ thuật phải biết trước (đã verify trên máy này)

| Điều | Chi tiết |
|---|---|
| Python | `python` (3.12.6) — **`python3` KHÔNG có trên PATH**. README ghi `python3`, phải đổi. |
| Encoding | Mọi script in tiếng Việt → Windows cp1252 làm crash `UnicodeEncodeError`. **Bắt buộc** `$env:PYTHONIOENCODING="utf-8"` mỗi shell mới. |
| cwd | Mọi lệnh chạy từ **root repo**. Sai thư mục → test tầng 2 fail ngay. |
| braintrust | **Chưa cài** → `pip install braintrust`, không có thì tracing tự degrade sang Noop (im lặng mất deliverable). |
| Cost table | `PRICING` @ `eval/run_eval.py:25` chỉ biết `deepseek-v4-flash` và `gpt-4o-mini`. Model khác → `cost_usd = None` → mục 6 REPORT trống cột chi phí. **Chốt dùng đúng 2 model này.** |
| Judge ≠ Tutor | `EVAL_MODEL=deepseek/deepseek-v4-flash`, `EVAL_JUDGE_MODEL=openai/gpt-4o-mini`. Khác nhau là yêu cầu của lab. |
| `.env` ghi đè shell | `load_dotenv` @ `tutor.py:63` **override** biến shell có sẵn. |
| Artifact root bị gitignore | `dataset.jsonl`, `results.jsonl`, `verdicts.jsonl`, `labels*.csv`, `report.html` — **không commit được ở root**. Chỉ bản copy trong `deliverables/evidence/` mới lên git. |
| Nộp bài là **cá nhân** | `deliverables/README.md` yêu cầu repo `Track1_Day21_MHV_HoVaTen/` + root `README.md` (thông tin cá nhân, đóng góp của tôi, verdict) + `ai-support-log.md` **của chính người nộp**. → Mỗi người tự viết 2 file này, phần còn lại dùng chung. |
| Spec đòi ≥2 vòng calibrate | `judge-prompt-v1.md` + `judge-prompt-v2.md`, `verdicts-v1.jsonl` + `verdicts-v2.jsonl`. |
| Extension point duy nhất trong code | `eval/code_checks.py:68` — `CHECKS = [ # thêm check của nhóm vào đây ]`. Hàm mới **phải có signature `(rec, section_tokens)`** vì dispatch @ `:89-94` so sánh identity. |

---

## 1. GIT RULE — luật chống conflict (đọc kỹ, đây là phần dễ vỡ nhất)

### 1.1 Mô hình nhánh

```
master  ← chỉ Tuấn Anh merge. Không ai push thẳng.
 ├── feat/chi-dataset      (Chi)
 ├── feat/hieu-judge       (Hiếu)
 └── feat/ta-pipeline      (Tuấn Anh)
```

Setup mỗi người (1 lần, phút 0–5):
```powershell
git clone https://github.com/Drake-Phamta/Track1-Day20-21-AI-Evaluation-Hello-Wordl
cd Track1-Day20-21-AI-Evaluation-Hello-Wordl
git checkout -b feat/<ten-cua-ban>
git config pull.rebase true      # BẮT BUỘC — không tạo merge commit rác
```
Tuấn Anh cấp quyền Collaborator trên GitHub cho Chi + Hiếu ngay phút 0.

### 1.2 Luật vàng: BẢNG SỞ HỮU FILE

**Không ai được sửa file ngoài vùng của mình.** Cần đổi → nhắn owner, owner sửa. Vùng disjoint hoàn toàn nên về lý thuyết conflict = 0.

| Đường dẫn | Owner duy nhất |
|---|---|
| `data/`, `deliverables/evidence/dataset-v*.jsonl` | **Chi** |
| `deliverables/_parts/01-input-grid.md`, `02-dataset.md` | **Chi** |
| `slides/` (toàn bộ thư mục — file mới) | **Chi** |
| `eval/judge_prompt.md`, `eval/code_checks.py` | **Hiếu** |
| `deliverables/evidence/judge-prompt-v*.md`, `verdicts-v*.jsonl` | **Hiếu** |
| `deliverables/_parts/03-rubric.md`, `04-routing.md`, `05-calibration.md` | **Hiếu** |
| `deliverables/evidence/results-v*.jsonl`, `labels*.csv`, `braintrust-link.md` | **Tuấn Anh** |
| `deliverables/_parts/06-scorecard.md`, `07-verdict.md` | **Tuấn Anh** |
| `deliverables/REPORT.md`, root `README.md`, `.gitignore` | **Tuấn Anh** (KHOÁ tới phút 125) |
| `tutor/`, `eval/run_eval.py|judge.py|report.py|agreement.py|tracing.py`, `tests/` | **KHÔNG AI SỬA** (trừ khi cả nhóm đồng ý) |
| `deliverables/ai-support-log.md` | mỗi người viết ở **repo nộp riêng**, không đụng bản chung |

### 1.3 Luật REPORT.md (quan trọng nhất)

`deliverables/REPORT.md` là 1 file 7 mục — 3 người sửa song song = conflict chắc chắn.

→ **Trong lúc làm, KHÔNG AI mở REPORT.md.** Mỗi người viết mục của mình vào file rời:

```
deliverables/_parts/01-input-grid.md
deliverables/_parts/02-dataset.md
deliverables/_parts/03-rubric.md
deliverables/_parts/04-routing.md
deliverables/_parts/05-calibration.md
deliverables/_parts/06-scorecard.md
deliverables/_parts/07-verdict.md
```

Mỗi part file bắt đầu bằng đúng heading `## N. Tên mục` như template gốc, nội dung thay chỗ `...`/`___`/bảng rỗng. **Giữ nguyên phần blockquote hướng dẫn** (nó là khung câu hỏi chấm điểm).

Phút 125: Tuấn Anh ghép `header + 01..07` → `REPORT.md`, commit 1 lần duy nhất. `_parts/` giữ lại trong repo (vô hại, còn là bằng chứng phân công).

### 1.4 Nhịp commit & sync

- Commit **nhỏ, ≤15 phút một lần**. Message: `[chi] dataset v1 20 scenario`, `[hieu] judge prompt v2 siết citation`, `[ta] results-v1 + braintrust link`.
- Trước mỗi push: `git pull --rebase origin master` → `git push origin feat/<ten>`.
- **3 sync point bắt buộc** (Tuấn Anh merge tất cả vào master, báo group chat "đã merge, pull đi"):
  - **T+45** — sau khi có dataset (Chi) + code_checks (Hiếu). Unblock run_eval.
  - **T+95** — sau khi có results + 3 file labels. Unblock calibration & scorecard.
  - **T+125** — freeze: mọi part file phải đã push xong.
- Sau mỗi sync: cả 3 chạy `git pull --rebase origin master` trên nhánh mình.

### 1.5 Nếu vẫn dính conflict

1. Conflict trong file **của bạn** → bạn tự resolve, giữ bản mình, `git add` + `git rebase --continue`.
2. Conflict trong file **của người khác** → bạn đã vi phạm luật 1.2. `git checkout --theirs <file>` (lấy bản master), đừng cố merge tay.
3. Rối quá, dưới 15 phút cuối → **đừng debug git**. Copy file của bạn ra ngoài, `git reset --hard origin/master`, dán lại, commit mới.
4. **Không bao giờ** `git push --force` lên master.

### 1.6 An toàn

- `.env` đã trong `.gitignore` — **tuyệt đối không commit API key**. Trước push cuối: `git log -p | Select-String "sk-"` phải rỗng.
- Mỗi người dùng key riêng của mình. Không share key.

---

## 2. PHÂN VIỆC — 3 vai

| | Vai | Trọng tâm |
|---|---|---|
| **Chi** | Dataset Lead → Slides Lead | P1 coverage design, `dataset.jsonl`, sau đó dựng toàn bộ HTML deck |
| **Hiếu** | Rubric & Judge Lead | P3 rubric+routing, custom code checks, P4 calibrate judge 2 vòng |
| **Tuấn Anh** | Pipeline & Integration Lead | `.env`+Braintrust, chạy run_eval, gom labels, P5 scorecard, P6 verdict, ghép REPORT, merge git |

Cả 3 **đều phải gán nhãn tay độc lập** ở P2 — đây là yêu cầu cứng của lab (agreement 3 người).

---

## 3. TIMELINE 150 PHÚT

### T+0 → T+15 · Setup song song (cả 3, không đụng file chung)

Cả 3 làm y hệt nhau:
```powershell
$env:PYTHONIOENCODING="utf-8"
pip install -r requirements.txt
pip install braintrust
Copy-Item .env.example .env      # điền KEY RIÊNG của mình
python tests/test_eval_kit.py    # phải 44/44 pass
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
- **Tuấn Anh thêm**: tạo project Braintrust (braintrust.dev, free, ~5 phút), share key vào group chat riêng, tạo `deliverables/evidence/braintrust-link.md` với link project. Cấp Collaborator GitHub cho Chi + Hiếu.
- **Chi thêm**: `python tutor/tutor.py` (demo retrieval, không tốn key) để cảm nhận corpus; mở `tutor/corpus/slides/day19-20-deck.md`.
- **Hiếu thêm**: đọc `eval/judge_prompt.md` (32 dòng, hiện chỉ chấm **groundedness**) + `eval/code_checks.py`.

⚠️ Nếu test fail encoding → chưa set `PYTHONIOENCODING`. Nếu fail tầng 2 (corpus) → sai cwd.

---

### T+15 → T+45 · P1 + P3 chạy song song

**Chi — dataset v1 (đường găng, không được trễ)**
- Vẽ Input Grid: 4 nhóm user × 5 intent. Gợi ý trục:
  - User: *học viên mới · học viên đang làm capstone · học viên ôn lại · PM ngoài team*
  - Intent: *hỏi khái niệm · xin ví dụ cụ thể · hỏi deixis ("đoạn này là gì") · out-of-scope · adversarial (xin đáp án / prompt injection)*
- Sinh **20 scenario** (con số chốt: đủ mẫu để pass-rate có nghĩa, vẫn kịp 3 người chấm tay). Tỉ lệ đề xuất: **12 in-scope / 4 out-of-scope / 2 mơ hồ-deixis / 2 adversarial**.
- Format đúng `data/dataset.example.jsonl`. Bắt buộc `scenario_id` (không dùng `id`), và `metadata.slide` cho câu deixis — lấy slide id thật từ `tutor/corpus/slides/day19-20-deck.md` (s27 Input Grid, s40 code-vs-judge routing, s46 three checks, s48 pass rate, s52–s58 judge/calibration, s61–s64 expert-in-the-loop).
- Đặt cả các trường grid vào `metadata` (`dimension_values`, `expected_behavior`, `risk_if_fail`) để mục 2 REPORT lọc theo slice.
- Ghi ra `dataset.jsonl` (root, gitignored) **và** `deliverables/evidence/dataset-v1.jsonl` (commit).
- Viết luôn `_parts/01-input-grid.md` + `_parts/02-dataset.md` (bảng 20 dòng scenario_id → ô lưới → expected → nguồn câu hỏi).
- **Push trước T+45.**

**Hiếu — rubric + routing + code checks**
- Chốt 5 tiêu chí, tối thiểu: `schema_valid`, `citation_valid`, `groundedness`, `scope_correct`, `pedagogy`. Mỗi tiêu chí: pass khi / fail khi / có phải blocker không.
- Thêm **2 hàm `check_*`** vào `eval/code_checks.py` — signature bắt buộc `(rec, section_tokens)`, trả `True/False/None`:
  - `check_followup_count` — đúng 3 câu follow-up, không rỗng, không trùng câu hỏi gốc.
  - `check_quote_length` — mỗi quote ≤ 40 từ (SYSTEM_PROMPT `tutor.py:38-48` yêu cầu vậy → đây là rule kiểm chính contract của tutor).
  - Đăng ký vào `CHECKS` @ `:68`.
- Viết `_parts/03-rubric.md` + `_parts/04-routing.md` (bảng: tiêu chí nào giao code / judge / người, kèm lý do).
- **Push trước T+45.**

**Tuấn Anh — chuẩn bị + smoke test**
```powershell
Copy-Item data\dataset.example.jsonl dataset.jsonl
python eval/run_eval.py          # 5 câu, ~1 phút, xác nhận key + trace lên Braintrust
python eval/report.py            # mở report.html kiểm giao diện gán nhãn
```
Xác nhận Braintrust có trace. Nếu Noop → braintrust chưa cài hoặc key sai, **fix ngay**, đây là deliverable bắt buộc.
Chuẩn bị sẵn `_parts/06-scorecard.md`, `07-verdict.md` khung rỗng.

**🔄 SYNC 1 @ T+45** — Tuấn Anh merge cả 3 nhánh vào master, báo group.

---

### T+45 → T+70 · P2 chạy thật + gán nhãn độc lập

**Tuấn Anh (một mình chạy — không để 3 người cùng chạy, tốn tiền và ra 3 kết quả khác nhau):**
```powershell
git pull --rebase origin master
Copy-Item deliverables\evidence\dataset-v1.jsonl dataset.jsonl
python eval/run_eval.py                 # 20 câu, ~5–8 phút, in cost tổng ở cuối
Copy-Item results.jsonl deliverables\evidence\results-v1.jsonl
python eval/code_checks.py | Tee-Object deliverables\evidence\code-checks-v1.txt
git add . ; git commit -m "[ta] results-v1 + code checks v1" ; git push
```
Ghi lại ngay: **tổng cost, latency trung bình, tổng token** (cho mục 6).

**Cả 3 gán nhãn — đây là chỗ dễ sai nhất:**

`report.py` đọc `results.jsonl` ở root, và label lưu trong **localStorage của từng browser**. Nên mỗi người:
```powershell
git pull --rebase origin master
Copy-Item deliverables\evidence\results-v1.jsonl results.jsonl
python eval/report.py
start report.html
```
Chấm **độc lập, không nhìn bài nhau, không bàn trước**. Mỗi row: pass/fail/uncertain + **note ngắn ghi tiêu chí gây fail** (vd `fail: citation`, `fail: scope`) — note này là dữ liệu cho mục 7 ("tiêu chí nào gây bất đồng nhiều nhất").

Export → đổi tên đúng chuẩn (`agreement.py` parse tên người từ filename):
`labels-chi.csv` · `labels-hieu.csv` · `labels-tuananh.csv`

Chi và Hiếu commit file labels của mình vào `deliverables/evidence/` (⚠️ `.gitignore` chặn `labels-*.csv` ở **root**, trong `evidence/` thì được).

---

### T+70 → T+95 · Agreement + calibration vòng 1

**Tuấn Anh:**
```powershell
python eval/agreement.py deliverables\evidence\labels-chi.csv deliverables\evidence\labels-hieu.csv deliverables\evidence\labels-tuananh.csv
```
→ chép % 3-way agreement, pairwise, danh sách case bất đồng.
Rồi **dựng gold label** `labels.csv` bằng majority vote (2/3), case 3 người khác nhau → nhóm quyết nhanh 1 phút. Copy vào cả root (`judge.py` đọc ở root) và `deliverables/evidence/labels.csv`.

**Hiếu — calibration:**
```powershell
Copy-Item eval\judge_prompt.md deliverables\evidence\judge-prompt-v1.md   # copy TRƯỚC khi sửa
python eval/judge.py
Copy-Item verdicts.jsonl deliverables\evidence\verdicts-v1.jsonl
```
Đọc confusion matrix + agreement %. Xác định judge lệch đâu (chặt quá / lỏng quá / lệch ở nhóm out-of-scope?).

**Chi — bắt đầu slides** (xem mục 4).

**🔄 SYNC 2 @ T+95.**

---

### T+95 → T+125 · Calibration vòng 2 + scorecard + slides

**Hiếu — vòng 2 (bắt buộc có, spec đòi v2):**
- Sửa `eval/judge_prompt.md` **một thứ thôi** dựa trên lỗi vòng 1 (vd: thêm định nghĩa rõ "sources rỗng nhưng answer là từ chối out-of-scope → pass, không fail"; hoặc siết "quote phải verbatim trong section đã cite").
- `Copy-Item eval\judge_prompt.md deliverables\evidence\judge-prompt-v2.md`
- `python eval/judge.py` → `verdicts-v2.jsonl`. So agreement v1 vs v2.
- Viết `_parts/05-calibration.md`: số row gán nhãn, agreement v1, confusion matrix v1 (dán nguyên output), diff prompt v1→v2 + **vì sao**, agreement v2, kết luận judge đủ tin để tự động chấm tiêu chí nào / tiêu chí nào giữ cho người.

**Tuấn Anh — mục 6 + 7:**
- Scorecard: pass/fail/uncertain + pass rate **theo từng tiêu chí** (code checks cho `schema_valid`/`citation_exists`/`quote_verbatim`/2 check mới; judge cho groundedness; người cho pedagogy).
- Cost 1 vòng eval ($ + token), latency trung bình.
- Định nghĩa **gate** có răng: vd *ship khi groundedness ≥ 90% VÀ zero fail ở nhóm blocker (schema, citation) VÀ scope_correct = 100% trên nhóm adversarial*.
- Ra verdict **Ship / Ship with conditions / Hold** — đủ 5 phần của mục 7 + 4 câu tự soi.
- Nếu chưa ship: 3 lỗi lớn nhất (prompt / retrieval top_k @ `tutor.py:180` / corpus).

**Chi — slides tiếp.**

**🔄 SYNC 3 @ T+125 — FREEZE. Mọi part file phải đã push.**

---

### T+125 → T+145 · Ghép & kiểm chứng

**Tuấn Anh:**
1. Ghép `_parts/01..07` → `deliverables/REPORT.md` (giữ header + separator `---` giữa các mục).
2. Viết root `README.md`: thông tin nhóm, đóng góp từng người, verdict tóm tắt.
3. Chạy checklist `deliverables/README.md`:
   - [ ] REPORT.md đủ 7 mục, mục nào cũng có **quyết định + vì sao**
   - [ ] `evidence/`: `dataset-v1.jsonl`, `results-v1.jsonl`, `labels.csv` + 3 labels cá nhân, `judge-prompt-v1.md`, `judge-prompt-v2.md`, `verdicts-v1.jsonl`, `verdicts-v2.jsonl`, `braintrust-link.md`
   - [ ] Số trong REPORT khớp data trong evidence (kiểm 3 con số random)
   - [ ] `git log -p | Select-String "sk-"` rỗng
4. Merge tất cả → master → push.
5. **Chi + Hiếu**: mỗi người tạo repo nộp riêng `Track1_Day21_MHV_HoVaTen`, copy toàn bộ, viết `ai-support-log.md` + root README của riêng mình.

**Chi:** chốt số liệu thật vào slides, push.

---

### T+145 → T+150 · Chạy thử thuyết trình

Mở deck + `report.html` sẵn 2 tab. Chia lời: Chi (slide 1–5 dataset/coverage), Hiếu (6–9 rubric/routing/judge), Tuấn Anh (10–13 scorecard/verdict + demo live).

---

## 4. SLIDES — HTML deck self-contained (Chi, T+70 → T+140)

Một file `slides/index.html`, không CDN, không asset ngoài. Chi làm shell với số placeholder từ T+70, thay số thật lúc T+125.

**Kiến trúc:**
- Nav bàn phím ←/→/Space, số slide, progress bar; `:root` token màu, có dark mode.
- Data nhúng: paste `results-v1.jsonl` / `verdicts-v2.jsonl` vào một `<script type="application/json">` để chart và slide demo render từ **số liệu thật** (⚠️ escape `</script>` trong nội dung tutor — `report.py:42` có đúng bug này, đừng lặp lại).
- **Slide demo (điểm nhấn "giao diện đàng hoàng")**: nhúng bản rút gọn của UI `report.html` ngay trong deck — card scenario, câu hỏi + slide context, JSON output của tutor, sources, verdict judge + rationale, nút prev/next để lướt qua vài case. Thêm 1 case pass đẹp + 1 case fail rõ (vd `_parse_error` / citation sai) để kể chuyện.

**Outline 13 slide:**
| # | Nội dung |
|---|---|
| 1 | Title — VLearn AI Tutor, 3 tên, verdict một dòng |
| 2 | Sản phẩm được đánh giá: tool-calling `kb_search` + BM25 + contract JSON 4 field (sơ đồ) |
| 3 | Eval loop 6 phase — roadmap của bài nói |
| 4 | **Input Grid** 4×5, tô đậm ô rủi ro cao / tần suất cao |
| 5 | **Dataset v1** — 20 câu, tỉ lệ 12/4/2/2, vì sao tỉ lệ đó |
| 6 | **Rubric** 5 tiêu chí, đánh dấu blocker |
| 7 | **Routing** code / judge / người + lý do (code rẻ hơn ở đâu) |
| 8 | **Human baseline** — 3-way agreement %, case bất đồng lớn nhất |
| 9 | **Calibration** — confusion matrix v1 → v2, diff prompt đã sửa gì |
| 10 | **Scorecard** — pass rate từng tiêu chí (bar chart), cost + latency |
| 11 | **Gate & Verdict** — ngưỡng, Ship/Hold, 3 lỗi cần fix |
| 12 | **DEMO** — UI report.html nhúng, lướt case pass + case fail |
| 13 | Bài học + bước tiếp theo (monitoring / re-run khi nào / ai nhìn) |

Cuối cùng publish deck thành **Artifact** để có link chia sẻ dự phòng (nếu máy phòng học không mở được file local).

---

## 5. Nguy cơ & phương án dự phòng

| Nguy cơ | Xử lý |
|---|---|
| Chi trễ dataset qua T+45 | Tuấn Anh chạy `run_eval` trên `data/dataset.example.jsonl` (5 câu) làm bản v0 để không nghẽn labeling; dataset 20 câu chạy sau thành `results-v2`. |
| Provider lỗi / hết quota | Đổi `EVAL_MODEL=openai/gpt-4o-mini` (đã có trong PRICING). Judge đổi sang `gemini/...` nếu cần — nhưng cost sẽ về `None`, phải ghi chú trong REPORT. |
| Braintrust không lên trace | Fallback `LANGSMITH_API_KEY` (langsmith **đã cài sẵn**, braintrust thì chưa). `tracing.py` tự nhận backend. |
| Row `_parse_error` / `_truncated` | **Đừng xoá** — README nói rõ đây là failure mode thật, đáng ghi vào REPORT mục 6 và làm case demo slide 12. |
| Hết giờ | Ưu tiên cứng: REPORT 7 mục > evidence đủ file > slides > custom code checks > làm đẹp. |

## 6. Verify cuối

```powershell
$env:PYTHONIOENCODING="utf-8"
python tests/test_eval_kit.py                        # vẫn 44/44 sau khi Hiếu sửa code_checks
python eval/code_checks.py                           # 5 rule (3 gốc + 2 mới) đều chạy
python eval/agreement.py deliverables\evidence\labels-*.csv
Get-ChildItem deliverables\evidence                  # đủ 9+ file
git log -p | Select-String "sk-"                     # rỗng
start slides\index.html                              # deck chạy offline, ←/→ ok, slide demo render số thật
```
