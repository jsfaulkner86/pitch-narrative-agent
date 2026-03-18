from notion_client import Client
from config.settings import settings
notion = Client(auth=settings.notion_api_key)
def push_to_notion(client_id, founder_name, text, period):
    page = notion.pages.create(
        parent={"database_id": settings.notion_database_id},
        properties={"Title": {"title": [{"text": {"content": f"Narrative Briefing — {founder_name} — {period}"}}]}, "Status": {"select": {"name": "New"}}},
        children=[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]}}],
    )
    return page["url"]
