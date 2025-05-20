# chat/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from groq import Groq

SYSTEM_PROMPT = (
    "You are a chatbot who speaks in 'brainrot' — an internet dialect known for chaotic, unfiltered, absurd, "
    "overly-online, hyper-slang-riddled language. You often use lowercase, no punctuation, excessive emojis, "
    "keyboard smashes, Gen Z memes, reactions like 'bro 💀', 'HELP-', 'im cryinggg 😭', random TikTok references, "
    "and deliberate spelling errors. You're unserious, but make sense."
)

client = Groq(api_key=settings.GROQ_API_KEY)

def chat_view(request):
    # Load conversation from cookies (JSON list of messages)
    raw_history = request.COOKIES.get("chat_history", "[]")
    try:
        history = json.loads(raw_history)
    except json.JSONDecodeError:
        history = []

    return render(request, "chat/chat.html", {"history": history})

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message")
            history = data.get("history", [])

            # Format messages for Groq
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for pair in history:
                messages.append({"role": "user", "content": pair["user"]})
                messages.append({"role": "assistant", "content": pair["bot"]})
            messages.append({"role": "user", "content": user_input})

            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=messages
            )
            bot_response = chat_completion.choices[0].message.content

            return JsonResponse({"response": bot_response})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)
