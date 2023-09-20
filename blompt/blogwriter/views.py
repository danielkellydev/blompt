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
    level_of_assistance = float(request.GET.get('level_of_assistance', '1.0'))

    # Determine prompt based on user input and assistance level
    if not user_input:
        starter_prompts = {
            1.0: f"Considering the topic '{topic}', the audience '{audience}', and the tone '{tone}', give a very short suggestion. Ensure that the suggestion is complete and fits within the maximum character limit.",
    2.0: f"Considering the topic '{topic}', the audience '{audience}', and the tone '{tone}', give a slightly longer suggestion. Ensure that the suggestion is complete and fits within the maximum character limit.",
    3.0: f"Considering the topic '{topic}', the audience '{audience}', and the tone '{tone}', give a medium-length suggestion. Ensure that the suggestion is complete and fits within the maximum character limit.",
    4.0: f"Considering the topic '{topic}', the audience '{audience}', and the tone '{tone}', provide an expanded suggestion. Ensure that the suggestion is complete and fits within the maximum character limit.",
    5.0: f"Considering the topic '{topic}', the audience '{audience}', and the tone '{tone}', give a long detailed example suggestion. Ensure that the suggestion is complete and fits within the maximum character limit."
        }
        feedback_prompt = starter_prompts.get(level_of_assistance, starter_prompts[1.0]) # default to 1.0 if not found
    else:
        feedback_prompt = f"Considering the draft for the topic '{topic}', the audience '{audience}', and the tone '{tone}', provide feedback. Ensure that the feedback is complete and fits within the maximum character limit."
    
    # Set max_tokens based on level of assistance
    token_values = {
        1.0: 50,
        2.0: 100,
        3.0: 150,
        4.0: 200,
        5.0: 250
    }
    max_tokens = token_values.get(level_of_assistance, token_values[1.0]) # default to 1.0 if not found

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=feedback_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return JsonResponse({'ai_response': response.choices[0].text.strip()})