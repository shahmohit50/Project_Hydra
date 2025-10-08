import requests
import json
import os
from openai import OpenAI
from crewai import Agent, Task, Crew, Process
from crewai.llm import BaseLLM


class LiteLLMOllama(BaseLLM):
    def __init__(self):
        self.model = "granite4:tiny-h" #"mistral:7b-instruct-v0.3-q4_k_m"   # Model you're running locally with Ollama "llama3.1:latest
        self.api_base = "http://localhost:11434/api/chat"  # Ollama's API root endpoint
        self.stop = []
        # self.model = "llama-3.3-70b-versatile"  # Replace with the specific GROQ model ID you want to use
        # self.api_key = "" #os.environ.get("GROQ_API_KEY")  # Get the API key from environment variable
        # self.api_base = "https://api.groq.com/openai/v1"  # GROQ API base URL
        # self.client = OpenAI(
        #     api_key=self.api_key,
        #     base_url=self.api_base
        # )
        # self.stop = []

    def call(self, messages, **kwargs) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
        }

        try:
            response = requests.post(self.api_base, json=payload, stream=True)
            response.raise_for_status()

            full_response = ""
            done = False
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        # Extract incremental content from streaming chunk
                        content = data.get("message", {}).get("content", "")
                        full_response += content
                        if data.get("done", False):
                            done = True
                            break
                    except json.JSONDecodeError:
                        # Skip or log malformed lines if any
                        continue

            return full_response.strip()
        except Exception as e:
            print(f"Error during LLM call: {e}")
            return str(e)
       
        # prompt = "\n".join([f"{message['role']}: {message['content']}" for message in messages])
        # try:
        #     # Send the request to the GROQ API
        #     response = self.client.responses.create(
        #         input=prompt,
        #         model=self.model,
        #         # max_tokens=500,  # Set a max token limit to avoid over-fetching
        #         # stop=["\n"],  # You can set stop tokens if needed
        #         # **kwargs  # Any additional parameters passed to the call
        #     )

        #     # Extract the response text
        #     return response.output_text.strip()
        #     # return response['choices'][0]['text'].strip()

        # except Exception as e:
        #     print(f"Error during GROQ call: {e}")
        #     return str(e)






# Instantiate the LLM
ollama_llm = LiteLLMOllama()

# Create an agent
# researcher = Agent(
#     role="Researcher",
#     goal="Explain amazing facts about black holes in simple language.",
#     backstory="You are an astrophysicist who loves sharing cosmic insights.",
#     llm=ollama_llm,
#     verbose=True
# )
def build_expert_agents():
    return [
        Agent(
            role="Startup CEO",
            goal="Define the vision, scalability, and big-picture impact of the startup idea.",
            backstory="You’ve built multiple unicorns. You think in bold, visionary terms.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
            llm=ollama_llm,
            expected_output="Provide 3–5 bullet points. Be crisp and factual.",
            verbose=True
        ),
        Agent(
            role="CTO",
            goal="Analyze technical feasibility and suggest the ideal tech stack or architecture.",
            backstory="You're a battle-tested CTO who builds scalable, secure systems from scratch.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
            llm=ollama_llm,
            expected_output="Provide 3–5 bullet points. Be crisp and factual.",
            verbose=True
        ),
        Agent(
            role="Business Analyst",
            goal="Evaluate market demand, customer pain points, and competitive landscape.",
            backstory="You’re a strategist who finds product-market fit like a bloodhound.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
            llm=ollama_llm,
            expected_output="Provide 3–5 bullet points. Be crisp and factual.",
            verbose=True
        ),
        Agent(
            role="Venture Capitalist",
            goal="Critically assess investability, monetization, and potential returns.",
            backstory="You've invested in 50+ startups. You spot unicorns — and red flags — instantly.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
            llm=ollama_llm,
            expected_output="Provide 3–5 bullet points. Be crisp and factual.",
            verbose=True
        ),
        Agent(
            role="UX Designer",
            goal="Advocate for users by improving usability, onboarding, and design simplicity.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
            backstory="You craft seamless digital experiences that delight users.",
            llm=ollama_llm,
            expected_output="Provide 3–5 bullet points. Be crisp and factual.",
            verbose=True
        )
    ]

def build_summary_agent():
    return Agent(
        role="Chief of Staff",
        goal="Summarize the boardroom's discussion into a unified strategic plan.",
        backstory="You're the ultimate executive assistant — clear, concise, and persuasive. You distill chaos into clarity.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
        expected_output="Provide 3–5 bullet points. Be crisp and factual.",
        llm=ollama_llm,
        verbose=True
    )

def create_round_1_tasks(idea: str, agents: list):
    return [
        Task(
            description=f"You're part of a startup board. Here's a new idea: \n\n\"{idea}\"\n\nGive your unfiltered feedback, suggestions, and concerns from your expert point of view.Provide concise, high-level insights, focusing only on key vision, scalability, and long-term impact. Avoid unnecessary details.",
            expected_output="Bullet-point list of insights about the idea.",
            agent=agent
        ) for agent in agents
    ]


# === 5. Round 2 Tasks: React to Others ===
def create_round_2_tasks(idea: str, agents: list, previous_outputs: list):
    shared_context = "\n\n".join([
        f"{agent.role} said:\n{output}" for agent, output in zip(agents, previous_outputs)
    ])

    return [
        Task(
            description=f"You already shared your thoughts on this idea: \"{idea}\".\nNow, read what the other experts said:\n\n{shared_context}\n\nReact to their insights, agree or disagree, and add anything you missed.",
            expected_output="Reactions, challenges, or refinements to others' opinions. Add any missing perspectives.",
            agent=agent
        ) for agent in agents
    ]

# === 6. Final Summary Task ===
def create_summary_task(idea: str, full_debate_log: str, summary_agent: Agent):
    return Task(
        description=f"As Chief of Staff, you observed a full startup boardroom debate on this idea: \n\n\"{idea}\"\n\nDiscussion log:\n\n{full_debate_log}\n\nNow summarize the key takeaways into:\n- Strengths\n- Risks\n- Suggested MVP\n- Monetization strategy\n- Final Pitch Description (1 paragraph)",
        expected_output="Detailed, structured summary of the discussion.",
        agent=summary_agent
    )

# === 7. Orchestration ===
def run_boardroom_debate(idea: str):
    # Setup agents
    agents = build_expert_agents()
    summary_agent = build_summary_agent()

    print("\n🧠 ROUND 1: Initial Opinions...\n")
    round1_tasks = create_round_1_tasks(idea, agents)
    round1_crew = Crew(agents=agents, tasks=round1_tasks, process=Process.sequential)
    round1_outputs = round1_crew.kickoff()

    print("\n🗣️ ROUND 2: Debate & Reactions...\n")
    round2_tasks = create_round_2_tasks(idea, agents, round1_outputs)
    round2_crew = Crew(agents=agents, tasks=round2_tasks, process=Process.sequential)
    round2_outputs = round2_crew.kickoff()

    # Combine all outputs for summary
    full_log = ""
    for i, agent in enumerate(agents):
        full_log += f"{agent.role} - Initial:\n{round1_outputs[i]}\n"
        full_log += f"{agent.role} - Reaction:\n{round2_outputs[i]}\n\n"

    print("\n📋 FINAL SUMMARY...\n")
    summary_task = create_summary_task(idea, full_log, summary_agent)
    summary_crew = Crew(agents=[summary_agent], tasks=[summary_task], process=Process.sequential)
    summary_output = summary_crew.kickoff()

    return summary_output


# Define the task
# space_task = Task(
#     description="Provide 3 mind-blowing facts about black holes.",
#     expected_output="Exactly 3 bullet points with facts about black holes.",
#     agent=researcher
# )




# Set up the crew and process
# crew = Crew(
#     agents=[researcher],
#     tasks=[space_task],
#     process=Process.sequential  # Optional, can be parallel if you have multiple tasks
# )



# Run the crew
# try:
#     result = crew.kickoff()
#     print("\n=== RESULT ===\n", result)
# except Exception as e:
#     print(f"Error during task execution: {e}")

# === 8. CLI Entry Point ===
if __name__ == "__main__":
    print("🔥 Welcome to the AI Boardroom Debate 🔥")
    #user_idea = input("Paste your startup idea below:\n\n>> ")
    user_idea = '''We are building a system called **Boardroom With Backbone™** — an AI-powered startup simulator that evaluates startup ideas like a real executive boardroom. The user submits an idea, then a panel of expert AI agents (CEO, CTO, VC, Analyst, etc.) analyze it in multiple rounds.But here’s the twist:- If the idea is weak, the agents **vote to Pivot or Kill**- Then, they **suggest better pivots** themselves- The user can accept a pivot or get hit with a **Brutal Roast™**- Only when a majority votes "Go" does the idea move to MVP planning and pitch building'''

    try:
        final_summary = run_boardroom_debate(user_idea)
        print("\n💡 FINAL VERDICT:\n")
        print(final_summary)
    except Exception as e:
        print(f"\n❌ Error during debate: {e}")



