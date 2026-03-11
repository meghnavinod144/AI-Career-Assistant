import google.generativeai as genai

# paste your API key here
genai.configure(api_key="AIzaSyANG5zR_gq8dSQnL6DPJnlrCsaoAlfO12w")

print("API configured...")

model = genai.GenerativeModel("gemini-1.5-flash")

print("Model loaded...")

response = model.generate_content("Say hello in one short sentence")

print("Response received:")
print(response.text)