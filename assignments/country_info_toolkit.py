from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
import requests
from agents.run import RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = "gemini-2.0-flash"

client = AsyncOpenAI(
    api_key = GEMINI_API_KEY,
    base_url = BASE_URL
)

model = OpenAIChatCompletionsModel(
    model = MODEL,
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)


def get_country_data(country):
    if not country:
        return None
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()[0]
    capital = data.get("capital", ["Unknown"])[0]
    languages = ", ".join(data.get("languages", {}).values())
    population = data.get("population", "Unknown")

    return{
        "capital": capital,
        "languages": languages,
        "population": population
    }
        
@function_tool
def get_capital(country):
    data = get_country_data(country)
    return data.get("capital", ["Unknown"]) if data else "Unknown"

@function_tool
def get_population(country):
    data = get_country_data(country)
    return data.get("population", "Unknown") if data else "Unknown"

@function_tool
def get_languages(country):
    if data := get_country_data(country):
        return  data.get("languages", {})
    return "Unknown"

    
country_info_agent = Agent(
    name="Country Info Agent",
    instructions="""
        You are a smart and helpful assistant.

        When a user asks about a specific country, use the available tools one at a time.
        - Use `get_capital` to get the capital
        - Use `get_languages` to get the languages
        - Use `get_population` to get the population

        Then combine the results into a simple English sentence.

        If the user asks about something other than countries, politely say that this assistant only provides country information.

        Be concise, helpful, and polite.
    """,
    tools=[get_capital, get_languages,get_population]
)

user_input = str(input("Which country do you want to ask about? : "))
result = Runner.run_sync(country_info_agent, input=user_input, run_config=config)
print(result.final_output)

