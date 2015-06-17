from flask import Flask, request
from flask.views import MethodView
import json
import os
import requests
import sys


class GithubHook(MethodView):
    def post(self):
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

        comment_body = {"body": "#40 hello"}
        close_state = {"state": "closed"}
        auth = (os.environ["github_user"], os.environ["github_pass"])

        try:
            requests.post(comments_url,
                          data=json.dumps(comment_body),
                          auth=auth)
            requests.patch(pull_request_link,
                           data=json.dumps(close_state),
                           auth=auth)
        except:
            pass

        return "42"


app = Flask(__name__)
app.add_url_rule('/', view_func=GithubHook.as_view('counter'))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s <PORT>" % sys.argv[0]
        sys.exit(1)

    app.run(port=sys.argv[1], host="0.0.0.0")
