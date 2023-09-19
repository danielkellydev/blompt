document.addEventListener('DOMContentLoaded', function() {
    const blogInput = document.getElementById('textInput');
    const getAssistanceBtn = document.querySelector('button[onclick="requestAIAssistance()"]');
    const heading = document.querySelector('header h1');
    heading.style.opacity = "1";
    
    // Additional input fields
    const audienceInput = document.getElementById('audience');
    const toneInput = document.getElementById('tone');
    const topicInput = document.getElementById('topic');

    getAssistanceBtn.addEventListener('click', async () => {
        if(blogInput.value.trim().length === 0) {
            alert('Please write something in the blog input first.');
            return;
        }

        // Get values from the additional fields
        const audience = encodeURIComponent(audienceInput.value);
        const tone = encodeURIComponent(toneInput.value);
        const topic = encodeURIComponent(topicInput.value);

        try {
            let response = await fetch(`/get_ai_assistance?text=${encodeURIComponent(blogInput.value)}&audience=${audience}&tone=${tone}&topic=${topic}`);
            if (response.ok) {
                let data = await response.json();
                let aiText = data.ai_response;  // assuming 'ai_response' is the key for the AI's output in the returned JSON
                
                // Instead of appending directly to the blog input, show the suggestions in an alert:
                alert(`Suggestions from AI:\n${aiText}`);
            } else {
                console.error('Failed to fetch AI assistance.', response);
                alert('There was an error getting AI assistance. Please check the console for details.');
            }
        } catch (error) {
            console.error('There was an error:', error);
            alert('There was an error getting AI assistance. Please check the console for details.');
        }
    });
});