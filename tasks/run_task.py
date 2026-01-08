"""
Helper to run tasks easily
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()


async def run_task(instruction: str):
    """Run a task with given instruction"""
    from main import main as run_main
    sys.argv = ["run_task", instruction]
    await run_main()
