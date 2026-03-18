import resend
from config.settings import settings
resend.api_key = settings.resend_api_key
def send_narrative_briefing(email, name, html, period):
    resend.Emails.send({"from": settings.narrative_from_email, "to": email, "subject": f"Pitch Narrative Intelligence — {period}",
        "html": f"<html><body style='font-family:sans-serif;max-width:700px;margin:auto'><h2 style='color:#1a237e'>🎤 Pitch Narrative Briefing</h2><p>{period} — {name}</p><hr/>{html}<hr/><p style='font-size:12px;color:#999'>The Faulkner Group Advisors</p></body></html>"})
