import asyncio
import os
import sys
import json
import base64
from dotenv import load_dotenv

from computer_use_demo.loop import sampling_loop, APIProvider
from computer_use_demo.tools import ToolResult
from anthropic.types.beta import BetaMessage, BetaMessageParam
from anthropic import APIResponse

load_dotenv()

async def main():
    # Set up your Anthropic API key and model
    api_key = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")
    if api_key == "YOUR_API_KEY_HERE":
        raise ValueError(
            "Please first set your API key in the ANTHROPIC_API_KEY environment variable"
        )
    provider = APIProvider.ANTHROPIC

    # Check if the instruction is provided via command line arguments
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
    else:
        instruction = "Save an image of a cat to the desktop."

    print(
        f"Starting Claude 'Computer Use'.\nPress ctrl+c to stop.\nInstructions provided: '{instruction}'"
    )

    # Set up the initial messages
    messages: list[BetaMessageParam] = [
        {
            "role": "user",
            "content": instruction,
        }
    ]

    # Define callbacks (you can customize these)
    def output_callback(content_block):
        if isinstance(content_block, dict) and content_block.get("type") == "text":
            print("Assistant:", content_block.get("text"))

    def tool_output_callback(result: ToolResult, tool_use_id: str):
        """도구 실행 결과 처리 - 액션 타입별 아이콘"""
        
        short_id = tool_use_id[:8]
        
        if result.output:
            # 액션 타입 추측해서 적절한 아이콘
            output_lower = result.output.lower()
            
            if "click" in output_lower:
                icon = "👆"
            elif "type" in output_lower or "text" in output_lower:
                icon = "⌨️"
            elif "key" in output_lower:
                icon = "🔑"
            elif "screenshot" in output_lower:
                icon = "📸"
            else:
                icon = "✅"
            
            print(f"{icon} [{short_id}] {result.output}")
        
        if result.error:
            print(f"❌ ERROR [{short_id}] {result.error}")
        
        if result.base64_image:
            os.makedirs("screenshots", exist_ok=True)
            image_data = result.base64_image
            with open(f"screenshots/screenshot_{tool_use_id}.png", "wb") as f:
                f.write(base64.b64decode(image_data))

    def api_response_callback(response: APIResponse[BetaMessage]):
        print(
            "\n---------------\nAPI Response:\n",
            json.dumps(json.loads(response.text)["content"], indent=4),  # type: ignore
            "\n",
        )

    # Run the sampling loop
    messages = await sampling_loop(
        model="claude-sonnet-4-5-20250929",
        provider=provider,
        system_prompt_suffix="""

<EFFICIENCY_RULES>
* BE EFFICIENT: Complete tasks quickly without over-verification
* VERIFY ONCE: After completing an action, verify success ONCE and move on
* NO REDUNDANT CHECKS: Do not re-verify the same condition multiple times
* STOP WHEN DONE: When all task requirements are met, take final screenshot and STOP immediately
* NO EXTRA SCREENSHOTS: Take screenshots only when necessary, not repeatedly
* EXAMPLE: If login is successful and correct page is shown, STOP. Do not keep checking.
</EFFICIENCY_RULES>

""",
        messages=messages,
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        api_response_callback=api_response_callback,
        api_key=api_key,
        only_n_most_recent_images=3, # 3 -> 2
        max_tokens=2048,
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Encountered Error:\n{e}")
