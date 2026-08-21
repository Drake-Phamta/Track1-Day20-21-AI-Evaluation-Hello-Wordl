# Braintrust Tracing Link

Project: **ai-evaluation**  
Model: `openai/gpt-4o-mini`  
Dataset: `dataset-v1.jsonl` (20 scenarios)

## Link project Braintrust

<!-- Điền link vào đây sau khi chạy python eval/run_eval.py với BRAINTRUST_API_KEY -->
> **TODO:** Chạy bước dưới rồi paste link vào đây.

**Project URL:** https://www.braintrust.dev/app/[org]/p/ai-evaluation

---

## Hướng dẫn chạy (15 phút)

### Bước 1: Lấy API key Braintrust

1. Vào https://www.braintrust.dev → **Sign up** (hoặc Sign in nếu đã có)
2. Sau khi vào dashboard → click **Settings** (góc trên phải)
3. Vào tab **API Keys** → **Create new key**
4. Copy key (bắt đầu bằng `sk-...`)

### Bước 2: Điền key vào .env

Mở file `.env` trong thư mục gốc, bỏ comment dòng BRAINTRUST:

```
BRAINTRUST_API_KEY=sk-...        # paste key vào đây
BRAINTRUST_PROJECT=ai-evaluation
```

### Bước 3: Chạy eval có tracing

```powershell
# Từ thư mục gốc của project:
python eval/run_eval.py
```

Output sẽ thấy cuối cùng:
```
Đã log 20 trace lên braintrust (project 'ai-evaluation').
```

### Bước 4: Lấy link project

1. Vào https://www.braintrust.dev/app → chọn project **ai-evaluation**
2. Copy URL trình duyệt
3. Paste vào đây (phần "Project URL" ở trên)

---

## Lưu ý quan trọng

> ⚠️ ĐỪNG ghi đè `deliverables/evidence/results-v1.jsonl` — scorecard neo vào bộ đó.
> File mới từ `python eval/run_eval.py` sẽ ghi vào `results.jsonl` ở root — OK.
