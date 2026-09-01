"""
BhagvadGPT Telegram Bot
Receives messages from users, runs them through the same pipeline as the web app,
and sends the Gita response back on Telegram.
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# ── Telegram API helpers ──────────────────────────────────────────────────────

async def send_message(chat_id: int, text: str):
    """Send a text message to a Telegram chat."""
    try:
        transport = httpx.AsyncHTTPTransport(retries=2)
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=15.0), transport=transport) as client:
            resp = await client.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            })
            return resp.json()
    except Exception as e:
        print(f"send_message error: {e}")
        # Try without parse_mode as fallback
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                await client.post(f"{TELEGRAM_API}/sendMessage", json={
                    "chat_id": chat_id,
                    "text": text
                })
        except Exception as e2:
            print(f"send_message fallback error: {e2}")

async def send_typing(chat_id: int):
    """Show typing indicator."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(f"{TELEGRAM_API}/sendChatAction", json={
            "chat_id": chat_id,
            "action": "typing"
        })

async def set_webhook(webhook_url: str):
    """Register the webhook URL with Telegram."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{TELEGRAM_API}/setWebhook", json={"url": webhook_url})
        return resp.json()

# ── Core message handler ──────────────────────────────────────────────────────

async def handle_telegram_message(update: dict):
    """
    Process an incoming Telegram update.
    Runs the full BhagvadGPT pipeline and sends the response back.
    """
    # Only handle text messages
    message = update.get("message") or update.get("edited_message")
    if not message or "text" not in message:
        return

    chat_id = message["chat"]["id"]
    user_text = message["text"].strip()
    user_name = message.get("from", {}).get("first_name", "Friend")

    # Handle commands
    if user_text.startswith("/start"):
        await send_message(chat_id,
            f"🙏 *Radhe Radhe, {user_name}!*\n\n"
            "Welcome to *BhagvadGPT* — your AI spiritual companion powered by the Bhagavad Gita.\n\n"
            "Simply send me any question about life, emotions, relationships, career, or spirituality "
            "and I will share relevant wisdom from the Gita.\n\n"
            "You can also visit us at: bhagvadgpt.in\n\n"
            "_\"You have a right to perform your duties, but not to the fruits of action.\"_ — Gita 2.47"
        )
        return

    if user_text.startswith("/help"):
        await send_message(chat_id,
            "*BhagvadGPT Commands:*\n\n"
            "/start — Welcome message\n"
            "/help — Show this help\n\n"
            "Or just type any question and I'll answer with Gita wisdom 🙏"
        )
        return

    # Show typing while processing
    await send_typing(chat_id)

    try:
        # Import here to avoid circular imports at module load time
        from main import (
            okf_graph,
            extract_semantic_tags,
            search_by_semantic_tags,
            format_verses_to_context,
            translate_query_to_english,
            get_most_common_tags,
            prompt_template,
            create_llm_with_key,
            get_next_api_key,
            strip_think_tags,
            increment_question_counter,
        )
        from groq import RateLimitError

        # Step 1: Translate if needed
        search_query, _ = await translate_query_to_english(user_text)

        # Step 2: Tag matching (fast path first, then LLM)
        if okf_graph.priority_index:
            tag_list = list(okf_graph.priority_index.keys())
        else:
            tag_list = get_most_common_tags(limit=100)

        semantic_tags = okf_graph.fast_tag_match(search_query)
        if not semantic_tags:
            semantic_tags = await extract_semantic_tags(search_query, tag_list)

        # Step 3: Verse retrieval — top 3 for LLM, rest as appendix
        context_str = ""
        extra_nodes = []
        if semantic_tags:
            if hasattr(okf_graph, 'search_by_priority_index'):
                all_nodes = okf_graph.search_by_priority_index(semantic_tags, top_k=10)
                if all_nodes:
                    llm_nodes = all_nodes[:3]
                    extra_nodes = all_nodes[3:]
                    context_str = format_verses_to_context(llm_nodes, include_related=False)
            if not context_str:
                context_str = search_by_semantic_tags(semantic_tags, top_k=3, include_related=False)
        if not context_str:
            context_str = okf_graph.search(search_query, top_k=3, include_related=False)
        if not context_str:
            context_str = "No specific verses found. Provide general spiritual guidance."

        # Step 4: LLM response (non-streaming for Telegram)
        formatted_prompt = prompt_template.format(
            context=context_str,
            question=user_text,
            username=user_name
        )

        response_text = ""
        for attempt in range(5):
            try:
                api_key = get_next_api_key()
                llm = create_llm_with_key(api_key)
                response = await llm.ainvoke(formatted_prompt)
                response_text = strip_think_tags(response.content).strip()
                increment_question_counter()
                break
            except RateLimitError:
                if attempt < 4:
                    await asyncio.sleep(0.5)
                    continue
                response_text = "Namaste! BhagvadGPT is experiencing high traffic. Please try again in a moment. 🙏"
                break

        # Build related shlokas appendix
        if extra_nodes:
            appendix_lines = ["\n\n📚 *Also from the Gita on this topic:*\n"]
            for node in extra_nodes:
                content = node["content"]
                lines = content.split('\n')
                sanskrit = ""
                translation = ""
                current_section = None
                for line in lines:
                    if "**Sanskrit" in line or "Sanskrit (" in line:
                        current_section = "sanskrit"
                    elif "**English Translation" in line or "**Translation" in line:
                        current_section = "translation"
                    elif "**Meaning" in line:
                        break
                    elif current_section == "sanskrit" and line.strip():
                        sanskrit += line + "\n"
                    elif current_section == "translation" and line.strip():
                        translation += line + "\n"
                appendix_lines.append(
                    f"\n_{node['title']}_\n"
                    f"_{sanskrit.strip()}_\n"
                    f"_Translation: {translation.strip()}_\n"
                )
            response_text += "\n".join(appendix_lines)

        # Fix markdown for Telegram (convert ** to * for bold, fix --- separators)
        import re
        response_text = re.sub(r'\*\*(.+?)\*\*', r'*\1*', response_text)  # **bold** → *bold*
        response_text = response_text.replace('\n---\n', '\n──────────\n')
        response_text = response_text.replace('---\n', '──────────\n')
        response_text = response_text.replace('\n### ', '\n*')  # ### heading → *bold
        response_text = re.sub(r'\n### (.+)', r'\n*\1*', response_text)

        # Telegram 4096 char limit — split if needed
        if len(response_text) > 4000:
            parts = [response_text[i:i+4000] for i in range(0, len(response_text), 4000)]
            for part in parts:
                await send_message(chat_id, part)
                await asyncio.sleep(0.3)
        else:
            await send_message(chat_id, response_text)

    except Exception as e:
        print(f"Telegram handler error: {e}")
        await send_message(chat_id,
            "🙏 Namaste! Something went wrong on our end. Please try again or visit bhagvadgpt.in"
        )
