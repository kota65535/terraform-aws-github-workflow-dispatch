import json
import logging
from typing import TypedDict, NotRequired

import common
from common import GitHubClient
from config import Config
from jinja2 import Template

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = Config()


class WorkflowDispatchRequest(TypedDict):
    owner: str
    repo: str
    workflow: str
    ref: NotRequired[str]
    inputs: NotRequired[dict]


# Lambda function entrypoint
def lambda_handler(event: WorkflowDispatchRequest, context):
    logger.info(f"Input: {json.dumps(event)}")

    event = render(event)

    logger.info(f"Rendered: {json.dumps(event)}")

    dispatch_workflow(event)


def render(req: WorkflowDispatchRequest) -> WorkflowDispatchRequest:
    out = {
        "owner": Template(req["owner"]).render(),
        "repo": Template(req["repo"]).render(),
        "workflow": Template(req["workflow"]).render(),
    }
    if "ref" in req:
        out["ref"] = Template(req["ref"]).render()
 
    if "inputs" in req:
        inputs = {}
        for k, v in req["inputs"].items():
            inputs[k] = Template(v).render()
        out["inputs"] = inputs

    return out


def dispatch_workflow(req: WorkflowDispatchRequest):
    client = GitHubClient(config.github_token)

    if "ref" in req:
        ref = req["ref"]
    else:
        repo = client.get_repo(req["owner"], req["repo"])
        ref = repo["default_branch"]

    if "inputs" in req:
        inputs = req["inputs"]
    else:
        inputs = {}

    client.dispatch_workflow(
        req["owner"],
        req["repo"],
        req["workflow"],
        common.DispatchWorkflowRequest(ref, inputs))
