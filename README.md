# This is not the original Marzban repo!

Hi! This is fork of the original Marzban repo with features i wanted to have in Marzban
Original repos is here: https://github.com/gozargah/marzban

# Important Database Change:

- Database has new table "inbound_exclude_overrides".  Added automatically.

  In case of downgrade it is NOT REMOVED automatically, but that doesnt stop database from working - alembic will give error, but will start anyway.

  > ERROR [alembic.util.messaging] Can't locate revision identified by 'inbound_exclude_overrides'
  > FAILED: Can't locate revision identified by 'inbound_exclude_overrides'

## Downgrade DB :

(assuming you using updated container and not the original)

```
docker exec -it <containername> alembic downgrade 2b231de97dc3
```

then shutdown container and attach DB to original Marzban

### Downgrade DB manually (needs more testing):

```
DROP TABLE IF EXISTS inbound_exclude_overrides;
UPDATE alembic_version SET version_num = '2b231de97dc3';
.quit
```

# (un)Important Api Change:

- Xray Inbound (not host!) can now have port as Null. Either this or unix socket listener will have to have port set for panel to not throw error (default Marzban behavior)

# Changes

- HTTP_WEBROOT_PATH - env variable that makes panel serve content from this path (including /api, /statics and so on). Does not effect subscription because you can set subscription path with separate env.

- Added inbound filter: new parameter in .env - MARZBAN_INBOUND_EXCLUDE - is a comma-separated list of keywords. If those keywords are found in xray inbound name, inbound would not be auto assigned to all users, but administrator still would be able to manually assign that inbound to specific users.

- Panel no longer throws errors if xray inbound is listening on unix socket and thus doesnt have port specified. If Marzban inbound doesnt have manually specified port and listener is unix socket, user will get 443 port by default.

- Docker container is built using Alpine

- Added support for VLESS Encryption: you need to set "decryption=" field in xray inbound and VLESS_ENC= with encryption key in .env file

- profile-web-page-url header in subscription response now honors XRAY_SUBSCRIPTION_URL_PREFIX if its set in .env and doesnt send internal request url instead.

- xHTTP extra headers scMaxEachPostBytes, scMaxConcurrentPosts, scMinPostsIntervalMs, scMinPostsIntervalMs and noGRPCHeader are sent only if set to non-default values in xray inbound (defaults are 1000000, 100, 30, 100-1000 and False)

- Updated some python libraries and dashboard modules (at least no more critical security issues during dashboard build, yay!).

## Authors / Contributors

- korn3r — implementation, testing and integration
- The Almighty ChatGPT (OpenAI) — architecture, design & code assistance
