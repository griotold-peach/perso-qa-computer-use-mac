"""
Test task: Open Chrome and navigate to Naver
"""
import asyncio
from run_task import run_task

INSTRUCTION = """
Test: Chrome + Naver Navigation

1) Check if Chrome is running, if yes focus it, if no open it
2) Press Cmd+T to open new tab
3) Press Cmd+L to focus address bar
4) Type: https://naver.com
5) Press Enter
6) Wait for page to finish loading (about 2 seconds)
7) Take ONE final screenshot to verify Naver homepage
"""

if __name__ == "__main__":
    print("🧪 Testing Chrome + Naver navigation...")
    asyncio.run(run_task(INSTRUCTION))
