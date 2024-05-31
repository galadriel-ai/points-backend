import settings
from points import api_logger

logger = api_logger.get()


class WhitelistRepository:

    def __init__(self, whitelist_file: str = settings.WHITELIST_FILE):
        self.whitelist_file = whitelist_file

    def is_whitelisted(self, twitter_id: str) -> bool:
        try:
            with open(self.whitelist_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            return twitter_id in [l.replace("\n", "").strip() for l in lines]
        except:
            logger.error(f"Failed to read whitelist file: {self.whitelist_file}")
            return False
