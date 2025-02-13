import os
import openai

openai.api_key = os.getenv("AIPROXY_TOKEN")

def extract_email_sender(input_file, output_file):
    """Extracts sender email using LLM."""
    with open(input_file, "r") as f:
        email_content = f.read()

    prompt = "Extract the sender's email from this email message:\n" + email_content
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    email_address = response["choices"][0]["message"]["content"].strip()

    with open(output_file, "w") as f:
        f.write(email_address)

    return f"Extracted email {email_address} to {output_file}"
