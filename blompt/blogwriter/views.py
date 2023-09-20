from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings

# Render the index view
def index(request):
    return render(request, 'blogwriter/index.html')

def get_ai_assistance(request):
    audience = request.GET.get('audience', 'an unknown audience')
    topic = request.GET.get('topic', 'an unspecified topic')
    tone = request.GET.get('tone', 'an unspecified tone')
    user_input = request.GET.get('text', '')
    openai.api_key = settings.OPENAI_API_KEY 
    temperature = float(request.GET.get('temperature', '0.7'))


    # Determine prompt based on user input and assistance level
    feedback_prompt = f"You are a writing assistant. The ethos behind this application is that instead of getting AI to do all the work, your role is to assist and prompt the writer. The writer's input will be found in {user_input}. First of all, consider what the writer's audience is. The audience is {audience}. Next, consider what the writer's topic is. The topic is {topic}. Finally, consider what the writer's tone is. The tone is {tone}. Now, based on the writer's input, audience, topic, and tone, provide the writer with some feedback. If the {user_input} is empty, please ask the writer some questions to get them started. If the {user_input} is not empty, please consider what the writer has written, how it relates to the audience, topic, and tone, and provide the writer with some feedback."
    
    max_tokens = 300

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=feedback_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return JsonResponse({'ai_response': response.choices[0].text.strip()})