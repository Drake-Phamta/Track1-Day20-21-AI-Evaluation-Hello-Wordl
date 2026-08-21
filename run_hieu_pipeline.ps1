# Script chạy toàn bộ pipeline của Hiếu sau khi điền API key
# Chạy từ root repo: powershell -File run_hieu_pipeline.ps1

$env:PYTHONIOENCODING = "utf-8"

Write-Host "=== STEP 1: Verify .env ===" -ForegroundColor Cyan
python -c "
import sys; sys.path.insert(0, 'tutor'); import tutor
key = tutor.get_api_key('openai/gpt-4o-mini')
if not key or key.startswith('sk-...'):
    print('ERROR: OPENAI_API_KEY chua duoc dien vao .env!')
    sys.exit(1)
print('OK: key bat dau bang sk-***' + key[-4:])
"
if ($LASTEXITCODE -ne 0) { Write-Host "STOP: Dien API key vao .env truoc!" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "=== STEP 2: Copy dataset + run_eval (20 cau, ~5-8 phut) ===" -ForegroundColor Cyan
Copy-Item deliverables\evidence\dataset-v1.jsonl dataset.jsonl
python eval/run_eval.py
if ($LASTEXITCODE -ne 0) { Write-Host "run_eval FAILED" -ForegroundColor Red; exit 1 }
Copy-Item results.jsonl deliverables\evidence\results-v1.jsonl
Write-Host "Saved results-v1.jsonl"

Write-Host ""
Write-Host "=== STEP 3: Code checks ===" -ForegroundColor Cyan
python eval/code_checks.py | Tee-Object deliverables\evidence\code-checks-v1.txt

Write-Host ""
Write-Host "=== STEP 4: Copy labels-hieu.csv -> labels.csv (gold label) ===" -ForegroundColor Cyan
Copy-Item deliverables\evidence\labels-hieu.csv labels.csv
Write-Host "labels.csv ready (se update sau khi co gold label tu 3 nguoi)"

Write-Host ""
Write-Host "=== STEP 5: Judge v1 (dung judge_prompt ban goc v1) ===" -ForegroundColor Cyan
Copy-Item deliverables\evidence\judge-prompt-v1.md eval\judge_prompt.md
python eval/judge.py
Copy-Item verdicts.jsonl deliverables\evidence\verdicts-v1.jsonl
Write-Host "Saved verdicts-v1.jsonl"

Write-Host ""
Write-Host "=== STEP 6: Judge v2 (dung judge_prompt v2 cai tien) ===" -ForegroundColor Cyan
Copy-Item deliverables\evidence\judge-prompt-v2.md eval\judge_prompt.md
python eval/judge.py
Copy-Item verdicts.jsonl deliverables\evidence\verdicts-v2.jsonl
Write-Host "Saved verdicts-v2.jsonl"

Write-Host ""
Write-Host "=== DONE! Tat ca file da san sang ===" -ForegroundColor Green
Get-ChildItem deliverables\evidence | Format-Table Name, Length
