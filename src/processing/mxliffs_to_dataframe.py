import requests
import argparse
import os
import urllib.parse
import json

from load import load_mx


class MemsourceTinyClient:
    USERNAME_ENV = "MEMSOURCE_USERNAME"
    PASSWORD_ENV = "MEMSOURCE_PASSWORD"

    BASE_URL = "https://cloud.memsource.com/web/api2/v1/"

    def __init__(self):
        self.username = os.environ.get(self.USERNAME_ENV)
        self.password = os.environ.get(self.PASSWORD_ENV)
        self.token = None
        self.login()

    def _request(self, url, method, body=None, url_params=None):
        full_url = urllib.parse.urljoin(self.BASE_URL, url)
        all_url_params = {"token": self.token}
        if url_params:
            all_url_params.update(url_params)
        response = method(full_url, json=body, params=all_url_params)
        return response.json() if response.content else None

    def _post(self, url, body, url_params=None):
        return self._request(url, requests.post, body=body, url_params=url_params)

    def _get(self, url, url_params=None):
        return self._request(url, requests.get, url_params=url_params)

    def login(self):
        self.token = self._post(
            "auth/login", body={"userName": self.username, "password": self.password})['token']

    def get_conversations(self, job_uid: str):
        return self._get(f"jobs/{job_uid}/conversations")


def extract_record_phase_1(segment, conversations):
    for conv in conversations['conversations']:
        if conv['references']['segmentId'] == segment.tunit_id:
            for comment in conv['comments']:
                segment.comments.append(comment['text'])

    line_record = {
        "tunit_id": segment.tunit_id,
        "source": segment.source,
        "target": segment.target,
        "comments": "\n".join(segment.comments),
        "provided": segment.provided,
        "edit_time": segment.edit_time,
        "think_time": segment.think_time,
        "edit_time_word": segment.edit_time_word,
        "think_time_word": segment.think_time_word,
        "is_first": segment.is_first,
        "is_last": segment.is_last,
    }

    return line_record


def extract_record_phase_2(segment, conversations):

    conversation = [conv for conv in conversations['conversations']
                    if conv['references']['segmentId'] == segment.tunit_id]

    line_record = {
        "tunit_id": segment.tunit_id,
        "source": segment.source,
        "target": segment.target,
        "revision_conversation": conversation,
        "revision_provided": segment.provided,
        "revision_edit_time": segment.edit_time,
        "revision_think_time": segment.think_time,
        "revision_edit_time_word": segment.edit_time_word,
        "revision_think_time_word": segment.think_time_word,
        "revision_is_first": segment.is_first,
        "revision_is_last": segment.is_last,
    }

    return line_record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase-2', action='store_true')
    args = parser.parse_known_args()[0]

    client = MemsourceTinyClient()
    data = load_mx()

    extract_fn = extract_record_phase_2 if args.phase_2 else extract_record_phase_1

    # XXX this is not very efficient but who cares
    for doc in data:
        doc_record = {
            "user_a": doc.user_a,
            "doc_name": doc.doc_name,
            "mt_name": doc.mt_name,
            "job_uid": doc.job_uid,
        }

        conversations = client.get_conversations(doc.job_uid)
        if not conversations:
            conversations = {'conversations': []}  # fake empty conversations object

        doc.lines[0].is_first = True
        doc.lines[-1].is_last = True

        for segment in doc.lines:
            line_record = extract_fn(segment, conversations)

            print(json.dumps(
                {**doc_record, **line_record}, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()