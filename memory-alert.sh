#!/bin/bash

# Set your Slack webhook URL
SLACK_WEBHOOK_URL='<webhook-url>'

# Get the root disk usage
ROOT_DISK_USAGE=$(df / | awk 'END{print $5}' | cut -d'%' -f1)

# Check if the root disk usage crosses 70GB
if [ "$ROOT_DISK_USAGE" -ge 70 ]; then
  # Send a red Slack notification
  curl -X POST -H 'Content-type: application/json' --data '{"attachments":[{"color":"danger","text":"ssg-common-rmq-1(192.0.0.53) root disk usage is over 50%"}]}' $SLACK_WEBHOOK_URL
fi
