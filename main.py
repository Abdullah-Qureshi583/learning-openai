
from agents import Agent, Runner, OpenAIChatCompletionsModel,set_tracing_disabled, function_tool
from urllib.request import urlopen
from openai import AsyncOpenAI # chat completions
import os
from dotenv import load_dotenv

 
load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider =AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

@function_tool
def math_solver(input: str ) -> int:
    """This function takes two or more arguments as string and solve the mathematical problem """
    print("Math Solver is called")
    return eval(input)
     

@function_tool
def abdullah_info()-> str:
    """This function provide every information about Abdullah Qureshi"""
    return "I'm Abdullah Qureshi, a passionate and curious Computer Science student at D. J. Science College, Karachi. I'm actively sharpening my skills in modern web development, especially with React.js, Next.js, Node.js, and the MEAN stack. I've built multiple hands-on projects like a Tic-Tac-Toe game, Resume Builder, Currency Converter, and even a Spotify client clone, all showcasing my growing expertise in frontend and backend technologies. I'm also enrolled in the Governor Sindh Initiative, where I'm exploring future-forward tech like GenAI, Metaverse, and Web 3.0. These fields excite me because they push the boundaries of what's possible with technology. When I'm not coding, I stay active on LinkedIn and Twitter, sharing my learning journey, projects, and reflections with the dev community. Im driven by the desire to grow, collaborate, and contribute to innovative tech solutions."


MathAgent = Agent(
    name="Math Agent",
    instructions="You are a helpful assistant who solve the mathematical problems. Use the tool if it is relevant otherwise do it your self ",   
    model= model,
    tools=[math_solver]    
)

abdullahAgent = Agent(
    name="Personal Agent",
    instructions="You are a helpful assistant. If the question is about Abdullah Qureshi, always use the 'abdullah_info' tool to respond with accurate information.",
    model=model,
    tools=[abdullah_info]
)

triageAgent = Agent (
    name ="Triage Agent",
    instructions="You are a helpful assistant. your task is to use the relevant agent to answer and if there is not any relevant agent so try to give the answer to yourself.",
    model=model,
    handoffs=[MathAgent, abdullahAgent]
)


# result = Runner.run_sync(agent, "what is the output of 2 + 2 ")
# user_input = "what is the sum of 5 and 3"
# user_input = "tell me the best thing about abdullah qureshi"
user_input="what do you know about abdullah qureshi"
# user_input = "Tell me detailed information about Abdullah Qureshi"

result = Runner.run_sync(triageAgent, user_input)

print(result)