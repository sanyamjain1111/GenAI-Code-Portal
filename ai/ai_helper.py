import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY =  "AIzaSyD_anS93dWH5rgUa57uMuVfse8_OnJUBcE"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_ai_solution(prompt):
    response = model.generate_content(prompt+"Don't use extra charcters like * ` etc. Don't mention this line")
    return response.text

