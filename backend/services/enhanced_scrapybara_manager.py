"""
🐻 Enhanced Scrapybara Manager
Compatibility wrapper for ScrapybaraManager with extension hooks for advanced orchestration.
"""
import logging
from .scrapybara_manager import ScrapybaraManager

logger = logging.getLogger(__name__)

class EnhancedScrapybaraManager:
    """Wraps ScrapybaraManager with future extension points."""
    def __init__(self):
        self.manager = ScrapybaraManager()
        logger.info("EnhancedScrapybaraManager initialized (wrapping ScrapybaraManager)")

    # Example: proxy all relevant methods
    async def create_workspace(self, *args, **kwargs):
        return await self.manager.create_workspace(*args, **kwargs)

    async def get_status(self):
        return await self.manager.get_status()

    async def stop_workspace(self, *args, **kwargs):
        return await self.manager.stop_workspace(*args, **kwargs)

    async def delete_workspace(self, *args, **kwargs):
        return await self.manager.delete_workspace(*args, **kwargs)

    # Add more proxy or extension methods as needed

# Export a global instance for use elsewhere
enhanced_scrapybara = EnhancedScrapybaraManager()
