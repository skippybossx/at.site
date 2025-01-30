#!/bin/bash
curl -H "X-Auth-Token: ${librenms_api_key}" "${librenms_domain_name}/api/v0/devices" | jq -r '.devices[] | select(.type=="network") | "\(.hostname) (\(.ip)) - \(.hardware) [\(.version)]"'
