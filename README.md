
# This is not the original Marzban repo!

Hi! This is fork of the original Marzban repo with features i wanted to have in Marzban
Original repos is here: https://github.com/gozargah/marzban

# Important Database Change:
- Database has new table "inbound_exclude_overrides". Added via alembic (so it is automatically removed with alembic in case of downgrade).


# Changes
- Added inbound filter: new parameter in .env - MARZBAN_INBOUND_EXCLUDE - is a comma-separated list of keywords. If those keywords are found in xray inbound name, inbound would not be auto assigned to all users, but administrator still would be able to manually assign that inbound to users manually.
- Marzban no longer throws errors if xray inbound is listening on unix socket and thus doesnt have port specified. If Marzban inbound doesnt have manually specified port and listener is unix, user will get 443 by default.
-  Docker container is built using Alpine
- Added support for VLESS Encryption: you need to set decryption field in xray inbound and VLESS_ENC= with encryption key in .env file
- profile-web-page-url header in subscription is now honors XRAY_SUBSCRIPTION_URL_PREFIX if its set in .env
- xHTTP extra headers scMaxEachPostBytes, scMaxConcurrentPosts, scMinPostsIntervalMs, scMinPostsIntervalMs and noGRPCHeader are sent only if set to non-default values in xray inbound (defaults are 1000000, 100, 30, 100-1000 and False)
- Updated some python libraries:
  
PS: Oh my god how i have markdown....

## Authors / Contributors

- korn3r — implementation, testing and integration
- The Almighty ChatGPT (OpenAI) — architecture, design & code assistance

