with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'telegram/webhook' not in content:
    telegram_code = """

# Telegram Bot Webhook

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        from telegram_bot import handle_telegram_message
        asyncio.create_task(handle_telegram_message(update))
        return {"ok": True}
    except Exception as e:
        print(f"Telegram webhook error: {e}")
        return {"ok": False}


@app.get("/telegram/set-webhook")
async def telegram_set_webhook(url: str):
    from telegram_bot import set_webhook
    result = await set_webhook(url)
    return result
"""
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(content + telegram_code)
    print("Added telegram endpoints")
else:
    print("Already present")
