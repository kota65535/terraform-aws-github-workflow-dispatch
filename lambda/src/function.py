import json
import logging
from typing import TypedDict

import common
from common import GitHubClient
from config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = Config()


class WorkflowDispatchRequest(TypedDict):
    owner: str
    repo: str
    workflow: str
    ref: str
    inputs: dict


# Lambda function entrypoint
def lambda_handler(event: WorkflowDispatchRequest, context):
    logger.info(f"Input: {json.dumps(event)}")

    dispatch_workflow(event)


def dispatch_workflow(req: WorkflowDispatchRequest):

    client = GitHubClient(config.github_token)

    if not req["ref"]:
        repo = client.get_repo(req["owner"], req["repo"])
        req["ref"] = repo["default_branch"]

    client.dispatch_workflow(
        req["owner"],
        req["repo"],
        req["workflow"],
        common.DispatchWorkflowRequest(req["ref"], req["inputs"]))
