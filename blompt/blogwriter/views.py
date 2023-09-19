from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'blogwriter/index.html')

def get_ai_assistance(request):
    audience = request.GET.get('audience', 'an unknown audience')
    topic = request.GET.get('topic', 'an unspecified topic')
    tone = request.GET.get('tone', 'an unspecified tone')
    user_input = request.GET.get('text', '')
    openai.api_key = settings.OPENAI_API_KEY 

    if not user_input:
        feedback_prompt = f"How about starting with something like: 'Writing a blog post about '{topic}' intended for '{audience}' with a '{tone}' tone.' Give me an introductory paragraph or some opening lines to kickstart this."
    else:
        feedback_prompt = f"I have a draft text intended for '{audience}' about '{topic}' with a '{tone}' tone. The draft is: '{user_input}'. Can you provide feedback, suggestions, or improvements?"
    
    temperature = float(request.GET.get('temperature', '0.7'))

    response = openai.Completion.create(
      engine="gpt-3.5-turbo-instruct",
      prompt=feedback_prompt,
      max_tokens=150,
      temperature=temperature,
    )

    return JsonResponse({'ai_response': response.choices[0].text})

