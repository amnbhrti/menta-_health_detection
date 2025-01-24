from transformers import pipeline

# Load Hugging Face model for suggestion generation
suggestion_model = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
# Load Hugging Face model for symptom detection
symptom_detection_model = pipeline("sentiment-analysis")

# Function to detect disorder based on user input
def detect_disorder(user_input):
    result = symptom_detection_model(user_input)[0]
    detected_symptom = result['label']
    confidence_score = result['score']
    
    # Customize symptom labels if needed
    if detected_symptom == "LABEL_0":
        detected_symptom = "Depressed mood"
    elif detected_symptom == "LABEL_1":
        detected_symptom = "Frustration and irritability"
    else:
        detected_symptom = "General sadness or anxiety"

    return detected_symptom, confidence_score

# Function to generate a personalized suggestion
def generate_suggestion(user_input, detected_symptom):
    prompt = (f"The user reports feeling '{user_input}', which indicates they may be experiencing '{detected_symptom}'. "
              "Please provide detailed, empathetic advice for managing this emotional state, including practical self-care steps and next actions.")
    
    response = suggestion_model(prompt, max_length=100, do_sample=True, temperature=0.7)
    suggestion = response[0]["generated_text"]
    return suggestion
