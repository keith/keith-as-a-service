from flask import Flask, request
from flask.views import MethodView
import hashlib
import hmac
import json
import os
import requests
import sys


class GithubHook(MethodView):
    def post(self):
        try:
            signature = request.headers["X-Hub-Signature"]
        except Exception, e:
            print "No hub signature %s : %s" % (request.headers,
                                                request.get_json())
            return "This is sketchy, I'm leaving"

        try:
            secret = os.environ["hook_secret"]
            hash_string = hmac.new(secret.encode('utf-8'),
                                   msg=request.data,
                                   digestmod=hashlib.sha1).hexdigest()
            expected_hash = "sha1=" + hash_string
        except Exception, e:
            print "Building expected hash failed: %s" % e
            return "Building expected hash failed", 500

        if signature != expected_hash:
            return "Wrong hash, gtfo"

        request_json = request.get_json()
        pull_request = request_json.get("pull_request")

        if request_json.get("action") != "opened":
            return "Meh, only care about opens"

        if pull_request.get("deletions") > 0:
            return "You deleted some stuff? Awesome!"

        if pull_request.get("additions") < 10:
            return "You didn't add much, that's probably legit!"

        if pull_request.get("changed_files") > 2:
            return "OK what are you doing?"

        links = pull_request.get("_links")
        pull_request_link = links.get("self").get("href")
        comments_url = links.get("comments").get("href")
        message = "#12199 (this was closed automatically, if your pull \
            request should not be closed based on that issue, please reopen it)"
        comment_body = {"body": message}
        close_state = {"state": "closed"}
        auth = (os.environ["github_user"], os.environ["github_pass"])

        try:
            requests.post(comments_url,
                          data=json.dumps(comment_body),
                          auth=auth)
            requests.patch(pull_request_link,
                           data=json.dumps(close_state),
                           auth=auth)
        except Exception, e:
            print "Exception: ", e

        return "42"


app = Flask(__name__)
app.add_url_rule('/', view_func=GithubHook.as_view('counter'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <PORT>" % sys.argv[0]
        sys.exit(1)

    app.run(port=sys.argv[1], host="0.0.0.0")
