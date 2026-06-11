import requests
import json

from .models import MetaAdInsight

from dotenv import load_dotenv
import os

load_dotenv()

META_TOKEN = os.getenv("META_ACCESS_TOKEN")


def get_fb_insights(since, until, ad_account_id) -> dict:
    url = f"https://graph.facebook.com/v20.0/{ad_account_id}/insights"

    params = {
        "fields": "ad_id,account_name,campaign_id,campaign_name,adset_name,ad_name,spend,actions,action_values,impressions,reach,clicks,cpc,cpm,frequency",
        "time_range": json.dumps({"since": since, "until": until}),
        "level": "ad",
        "limit": 10000,
        "access_token": META_TOKEN,
    }

    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.content)

    if response.status_code != 200:
        return {'status': response.status_code, 'details': f"Ошибка Meta API: {response.text}"}

    data = response.json().get("data", [])

    for item in data:
        actions = item.get("actions", [])

        lead_count = 0
        message_lead_count = 0

        for a in actions:
            action_type = a.get("action_type")
            value = int(a.get("value", 0))

            if action_type == "lead":
                lead_count += value
            elif action_type == "onsite_conversion.messaging_conversation_started_7d":
                message_lead_count += value

        try:
            insight = MetaAdInsight.objects.filter(date=since)
            insight = insight.get(ad_id=item.get('ad_id'))
        except MetaAdInsight.DoesNotExist:
            pass
        else:
            insight.delete()

        insight = MetaAdInsight.objects.create(
            ad_id=item.get('ad_id'),
            account_name=item.get("account_name"),
            campaign_id=item.get("campaign_id"),
            campaign_name=item.get("campaign_name"),
            adset_name=item.get("adset_name"),
            ad_name=item.get("ad_name"),
            spend=item.get("spend", 0),
            impressions=item.get("impressions", 0),
            reach=item.get("reach", 0),
            clicks=item.get("clicks", 0),
            cpc=item.get("cpc", 0),
            cpm=item.get("cpm", 0),
            frequency=item.get("frequency", 0),
            lead_count_form=lead_count,
            lead_count_message=message_lead_count,
            raw_actions=actions,
            date=since,
        )
        insight.save()

    return {'status': 200, 'details': "Data is saved!"}
