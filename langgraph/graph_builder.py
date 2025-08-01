from loguru import logger

from nodes.classify_intent import ClassifyIntent
from nodes.explore_repo import ExploreRepo
from nodes.generate_plan import GeneratePlan
from nodes.generate_code import GenerateCode
from nodes.apply_changes import ApplyChanges
from nodes.validate import Validate
from nodes.commit_and_push import CommitAndPush


class GraphBuilder:
    """Build and run the agent workflow using simple sequential steps."""

    def __init__(self, repo_url: str, goal: str, use_openai: bool = False):
        self.repo_url = repo_url
        self.goal = goal
        self.use_openai = use_openai

    def run(self):
        context = {"goal": self.goal}
        steps = [
            ClassifyIntent(),
            ExploreRepo(self.repo_url),
            GeneratePlan(),
            GenerateCode(use_openai=self.use_openai),
            ApplyChanges(),
            Validate(),
            CommitAndPush(commit_message=self.goal)
        ]
        for step in steps:
            logger.info(f"Running step {step.__class__.__name__}")
            context = step.run(context)
        logger.info("Workflow finished")
        return context
