"""
PERSO AI QA Task 01: Login and Homepage Access
Logout if logged in, then login and verify access to workspace/vt
"""
import os
import asyncio
from run_task import run_task
from dotenv import load_dotenv

load_dotenv()

PERSO_EMAIL = os.getenv("PERSO_EMAIL")
PERSO_PASSWORD = os.getenv("PERSO_PASSWORD")
PERSO_URL = os.getenv("PERSO_URL", "https://perso.ai/ko/workspace/vt")

if not PERSO_EMAIL or not PERSO_PASSWORD:
    raise ValueError("PERSO_EMAIL and PERSO_PASSWORD must be set in .env file")

INSTRUCTION = f"""
PERSO AI Task 01: Login and Homepage Access Test

Goal: Verify successful login and access to {PERSO_URL}

Steps:
1) Check if Chrome is running, if yes focus it, if no open it
2) Press Cmd+T to open new tab
3) Press Cmd+L to focus address bar
4) Type: {PERSO_URL}
5) Press Enter
6) Wait for page to finish loading (about 2 seconds)

7) Check current login state:
   
   [Case A] Already logged in:
   - If user profile visible in top-left corner: logged in
   - Click profile area to open dropdown menu
   - Click "로그아웃" (logout) at bottom of menu
   - Wait 2 seconds
   
   [Case B] Not logged in:
   - Proceed directly to next step

8) Login process:
   - Press Cmd+L to focus address bar
   - Type: https://perso.ai/ko/login
   - Press Enter
   - Wait 2 seconds
   - Click email field, type: {PERSO_EMAIL}
   - Click "계속" button
   - Click password field, type: {PERSO_PASSWORD}
   - Click "로그인" button
   - Wait 2 seconds

9) Final verification (DO ONLY ONCE):
   - Check: URL contains "workspace/vt"? 
   - Check: User profile visible?
   - If BOTH YES: Take ONE screenshot and STOP
   
STOP IMMEDIATELY after step 9. Do not re-verify.
"""

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 PERSO AI Task 01: Login and Homepage Access Test")
    print("=" * 60)
    print(f"📧 Email: {PERSO_EMAIL}")
    print(f"🔗 Target URL: {PERSO_URL}")
    print("=" * 60)
    asyncio.run(run_task(INSTRUCTION))
    print("\n✅ Task 01 Complete!")
