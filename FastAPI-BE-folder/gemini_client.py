import asyncio
import httpx

# --- Configuration ---
API_KEY = "AIzaSyCkNLwnE7N0R4pGd5HluJ9eAZB17LMGl5s"
MODEL_NAME = "gemini-2.5-flash-preview-05-20"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

async def call_gemini_api(prompt: str):
    """
    Calls the Gemini API with exponential backoff for retries.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }
    max_retries = 5
    base_delay = 1.0  # seconds

    async with httpx.AsyncClient(timeout=60.0) as client:
        for attempt in range(max_retries):
            try:
                response = await client.post(API_URL, json=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                result = response.json()

                if (
                    result.get("candidates")
                    and result["candidates"][0].get("content", {}).get("parts")
                ):
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    return "Error: Received an unexpected response from the API."

            except httpx.HTTPStatusError as e:
                print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code >= 500 and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Retrying in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
                else:
                    return f"Error: Failed to get a response from the API after {max_retries} attempts."
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"Retrying in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
                else:
                    return "Error: An unexpected error occurred while contacting the API."
        return "Error: Failed to get a response after several retries."
