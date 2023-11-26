import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    message: dict


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        print(os.getenv("OPENAI_API_KEY"))  # This should print your API key

        message_json = json.dumps(chat_request.message)

        prompt_text = (
                "Pretend that you are an incredibly experienced therapist who is "
                "trying to help someone break negative thought patterns. "
                "Given the dictionary input, return a few alternative activity suggestions in point form "
                "that the user can do to help them break their negative thought patterns. "
                "Your response should also consider the limitations in the given dictionary input. "
                "For example, if the user is in a wheelchair, do not suggest activities that require walking. "
                "If the user is in a low income bracket, suggest affordable activities. "
                "Consider the user's preferences, location, and age. "
                "For instance, for an introverted user in a rural area, suggest suitable activities. "
                "Keep your response short and concise,  in point form, and within 2 works MAX. "
                "Here is the user's information: " + message_json
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}]
        )

        gpt_response = response.choices[0].message['content']
        return ChatResponse(response=gpt_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
