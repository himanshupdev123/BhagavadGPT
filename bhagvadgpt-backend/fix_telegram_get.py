with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '@app.post("/telegram/webhook")'
new = '''@app.get("/telegram/webhook")
async def telegram_webhook_get():
    """Telegram verification ping"""
    return {"ok": True}


@app.post("/telegram/webhook")'''

content = content.replace(old, new)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done, telegram GET handler added")
