from pathlib import Path
from loguru import logger

from . import NodeContext


class PatchValidationError(Exception):
    """Raised when git apply --check fails."""


class PatchApplyError(Exception):
    """Raised when applying the patch fails."""


class ApplyChanges:
    """Apply generated patch to the repository."""

    def run(self, context: NodeContext) -> NodeContext:
        repo = context["repo"]
        patch = context.get("generated_patch")
        logger.info(patch)
        if not patch:
            logger.warning("No patch generated")
            return context
        patch_file = Path(context["repo_path"]) / "tmp.patch"
        patch_file.write_text(patch)
        try:
            repo.git.apply("--check", str(patch_file))
            logger.info("Patch validation succeeded")
        except Exception as exc:
            patch_file.unlink(missing_ok=True)
            raise PatchValidationError(str(exc)) from exc

        try:
            repo.git.apply(str(patch_file))
            logger.success("Applied patch to repository")
        except Exception as exc:
            patch_file.unlink(missing_ok=True)
            raise PatchApplyError(str(exc)) from exc
        finally:
            patch_file.unlink(missing_ok=True)
        return context
