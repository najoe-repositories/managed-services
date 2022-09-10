import json
import logging


from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

HOOK_URL = "" //MS teams connector api

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    alarm_name = message['AlarmName']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    base_data = {
        "color": "64a837",
        "title": "**%s** is resolved" % alarm_name,
        "text": "**%s** has changed from %s to %s - %s" % (alarm_name, old_state, new_state, reason)
    }
    if new_state.lower() == 'alarm':
        base_data = {
            "color": "d63333",
            "title": "Alert - There is an issue %s" % alarm_name,
            "text": "**%s** has changed from %s to %s - %s" % (alarm_name, old_state, new_state, reason)
        }

    message = {
      "@context": "https://schema.org/extensions",
      "@type": "MessageCard",
      "themeColor": base_data["color"],
      "title": base_data["title"],
      "text": base_data["text"]
    }

    req = Request(HOOK_URL, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted")
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

