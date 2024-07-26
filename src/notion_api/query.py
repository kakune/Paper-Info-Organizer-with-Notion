from typing import Dict

gNotionURL: str = 'https://api.notion.com/v1/pages'


def _makeHeader(inNotionAPIKey: str) -> Dict:
    return {
        'Notion-Version': '2022-06-28',
        'Authorization': 'Bearer ' + inNotionAPIKey,
        'Content-Type': 'application/json',
    }
