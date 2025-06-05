"""
🐻 Enhanced Scrapybara Manager
Compatibility wrapper for ScrapybaraManager with extension hooks for advanced orchestration.
"""
import logging
from .scrapybara_manager import ScrapybaraManager

logger = logging.getLogger(__name__)

class EnhancedScrapybaraManager:
    """Wraps ScrapybaraManager with future extension points."""
    def __init__(self, env_snapshot_manager=None, observability=None):
        self.manager = ScrapybaraManager()
        self.env_snapshot_manager = env_snapshot_manager
        self.observability = observability
        logger.info("EnhancedScrapybaraManager initialized (wrapping ScrapybaraManager)")

    # Example: proxy all relevant methods
    async def create_workspace(self, *args, **kwargs):
        if self.observability:
            with self.observability.tracer.start_as_current_span("create_workspace"):
                result = await self.manager.create_workspace(*args, **kwargs)
        else:
            result = await self.manager.create_workspace(*args, **kwargs)
        return result

    async def get_status(self):
        if self.observability:
            with self.observability.tracer.start_as_current_span("get_status"):
                result = await self.manager.get_status()
        else:
            result = await self.manager.get_status()
        return result

    async def stop_workspace(self, session_id, *args, **kwargs):
        # Save snapshot before stopping
        if self.env_snapshot_manager:
            # src_path should be provided or inferred; here we expect it as a kwarg
            src_path = kwargs.get('src_path')
            if src_path:
                self.env_snapshot_manager.save_snapshot(session_id, src_path)
        if self.observability:
            with self.observability.tracer.start_as_current_span("stop_workspace"):
                result = await self.manager.stop_workspace(session_id, *args, **kwargs)
        else:
            result = await self.manager.stop_workspace(session_id, *args, **kwargs)
        return result

    async def delete_workspace(self, session_id, *args, **kwargs):
        # Save snapshot before deletion
        if self.env_snapshot_manager:
            src_path = kwargs.get('src_path')
            if src_path:
                self.env_snapshot_manager.save_snapshot(session_id, src_path)
        if self.observability:
            with self.observability.tracer.start_as_current_span("delete_workspace"):
                result = await self.manager.delete_workspace(session_id, *args, **kwargs)
        else:
            result = await self.manager.delete_workspace(session_id, *args, **kwargs)
        return result

    # Add more proxy or extension methods as needed

# Export a global instance for use elsewhere
enhanced_scrapybara = EnhancedScrapybaraManager()
