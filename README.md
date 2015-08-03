# keith as a service

This repo (and heroku app) exist to close pull requests on the CocoaPods
[specs repo](https://github.com/CocoaPods/Specs) that don't follow the
[guidelines](https://github.com/CocoaPods/Specs/pull/12199)

## Local usage

```sh
make setup

# You also need to add this on the webhook on github
openssl rand -hex 32 | pbcopy
export hook_secret=`pbpaste`
export github_user=<USER>
export github_pass=<PASS>
export message="This is the close message"
make verify # Check to make sure your env is correct
make serve

# In a different window
make ngrok
```

## Heroku usage

```sh
# Generate a secret for use with the webhook
openssl rand -hex 32 | pbcopy

# Export these env vars on Heroku
hook_secret=<SECRET>
github_user=<USER>
github_pass=<PASS>
message=<MESSAGE>
```
