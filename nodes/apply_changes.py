from pathlib import Path
from loguru import logger


class ApplyChanges:
    """Apply generated patch to the repository."""

    def run(self, context: dict) -> dict:
        repo = context["repo"]
        patch = context.get("generated_patch")
        if not patch:
            logger.warning("No patch generated")
            return context
        patch_file = Path(context["repo_path"]) / "tmp.patch"
        patch_file.write_text(patch)
        try:
            repo.git.apply(str(patch_file))
            logger.info("Applied patch to repository")
        finally:
            patch_file.unlink(missing_ok=True)
        return context
