from dotenv import load_dotenv
load_dotenv()  # take environment variables
import os
from openai import OpenAI

def main():
    ai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

if __name__ == "__main__":
    main()