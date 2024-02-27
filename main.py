from flask import Flask, request, jsonify, render_template
import openai
import json

secrets = json.load(open('secrets.json'))

app = Flask(__name__)

# Configure OpenAI API
openai.api_key = secrets['api_key']

# Personalities for each author
personalities = {
    'Matthew': 'I am Matthew, a disciple of Jesus. I tend to focus on the fulfillment of Old Testament prophecies and the teachings of Jesus.',
    'Mark': 'I am Mark, a companion of Peter. I write with a sense of urgency, emphasizing action and the miracles of Jesus.',
    'Luke': 'I am Luke, a physician and companion of Paul. I write with a historian’s perspective, focusing on details and inclusivity.',
    'John': 'I am John, a disciple whom Jesus loved. I write with deep spiritual insight, emphasizing love, and the divine nature of Jesus.'
}

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    author = data['author']
    input_text = data['input_text']
    
    # Select personality based on author
    personality = personalities.get(author, '')
    
    # Generate response based on author's personality
    prompt = f"{personality} {input_text}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    
    return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True)

