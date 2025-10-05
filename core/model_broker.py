import requests, logging, os, json
import asyncio

class Broker:
    def __init__(self):
        # Ollama local API
        self.ollama_url = "http://localhost:11434"
        # Groq API key
        self.api_base = "http://localhost:11434/api/chat"
        self.model = "mistral:7b-instruct-v0.2-q4_K_M" 
        self.groq_api_key = os.getenv("GROQ_API_KEY") 
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"   

    # def __init__(self):
    #     self.local_models = {
    #         "mistral": self.local_mistral_stub,
    #         "llama8b": self.local_llama_stub
    #     }
    #     self.remote_models = {
    #         "groq": self.remote_groq_stub
    #     }
    #     self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
    #     self.groq_api = os.getenv("GROQ_API_KEY")

    def ollama_available(self) -> bool:
        try:
            # r = requests.get(f"{self.ollama_url}/v1/models", timeout=3)
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False
        
    def query_ollama(self, model: str, prompt: str) -> str:
        logging.info(f"🌀 Using Ollama model: {model}")
        payload = {
            "model": self.model,
            "messages": prompt,
        }
        response = requests.post(self.api_base, json=payload, stream=True)
        # resp = requests.post(
        #     f"{self.ollama_url}/api/chat",
        #     json={"model": model, "prompt": prompt},
        #     stream=False,
        #     timeout=120,
        # )
        response.raise_for_status()
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Headers: {response.headers}")
        full_response = ""
        done = False
        try:
            for line in response.iter_lines():
                    if line:
                        try:
                            logging.info(f"Response Line: {line}")
                            # logging.info(f"Response Line UTF-8: {line.decode("utf-8")}")
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
  
        # if resp.status_code == 200:
        #     try:
        #         logging.info(f"Response Text: {resp.text}")  # Log the raw response text
        #         response_json = resp.json()
        #         output = response_json.get("response", "").strip()
        #         logging.info(f"Parsed Output: {output}")
        #         return output
        #     except Exception as e:
        #         logging.error(f"Error processing response: {e}")
        #         return ""
        # else:
        #     logging.error(f"Request failed with status: {resp.status_code}")
        #     return ""

        # output = ""
        # for line in resp.iter_lines():
        #     if line:
        #         try:
        #             data = json.loads(line)
        #             output += data.get("response", "")
        #         except Exception as e:
        #             logging.error(f"Ollama parse error: {e}")
        # return output.strip()
        
    def query_groq(self, model: str, prompt: str) -> str:
        if not self.groq_api:
            raise ValueError("⚠️ GROQ_API_KEY missing.")
        logging.info(f"⚡ Using Groq model: {model}")
        headers = {"Authorization": f"Bearer {self.groq_api}"}
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()


    def load(self, model: str, prompt: str) -> str:
        """
        Decide route:
        - Local models: mistral, llama3, granite → Ollama if available
        - Heavy models: llama-3-70b, mixtral-8x7b → Groq
        """
        local_models = ["mistral:7b-instruct-v0.2-q4_K_M"]
        heavy_models = ["llama-3-70b", "mixtral-8x7b"]

        if model in local_models and self.ollama_available():
            return self.query_ollama(model, prompt)
        elif model in heavy_models:
            return self.query_groq(model, prompt)
        elif model in local_models:
            logging.warning("⚠️ Ollama not available, falling back to Groq")
            return self.query_groq(model, prompt)
        else:
            raise ValueError(f"❌ Unknown model requested: {model}")
        
broker = Broker()
