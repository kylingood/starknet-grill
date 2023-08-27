from asyncio import run
from src.core import start

if __name__ == '__main__':
    logger.info(f"\n---This software is written by @flextive. All right are reserved. Current version: 0.1.0---\n\n"
                f"Donate: 0x63f9716a17c751d97306289b22556b879ed8fb74")
    run(start())
    logger.info('Enter any key to exit')
    input()
