from logging_config import logger

from . import NodeContext


class CommitAndPush:
    """Commit changes and push the branch."""

    def __init__(self, commit_message: str):
        self.commit_message = commit_message

    def run(self, context: NodeContext) -> NodeContext:
        repo = context["repo"]
        branch_name = context["branch_name"]
        repo.git.add(all=True)
        if repo.is_dirty():
            repo.index.commit(self.commit_message)
            logger.info("Committed changes")
            try:
                repo.git.push("-u", "origin", branch_name)
                logger.info("Pushed branch to remote")
            except Exception as exc:
                logger.error(f"Failed to push: {exc}")
                context["push_error"] = str(exc)
        else:
            logger.info("No changes to commit")
        return context
