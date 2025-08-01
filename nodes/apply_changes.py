from pathlib import Path
from loguru import logger


class ApplyChanges:
    """Apply generated patch to the repository."""

    def run(self, context: dict) -> dict:
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
        except Exception as exc:  # GitCommandError or others
            logger.error(f"Patch validation failed: {exc}")
            context["patch_error"] = str(exc)
            patch_file.unlink(missing_ok=True)
            return context
        try:
            repo.git.apply(str(patch_file))
            logger.success("Applied patch to repository")
        except Exception as exc:
            logger.error(f"Failed to apply patch: {exc}")
            context["apply_error"] = str(exc)
        finally:
            patch_file.unlink(missing_ok=True)
        return context
