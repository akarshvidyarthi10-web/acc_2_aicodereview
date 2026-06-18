import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    force=True,
)

logger = logging.getLogger("ai_code_review")
logger.setLevel(logging.INFO)
logger.propagate = True
