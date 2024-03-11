# Class to generate Emails from Gemini
import dotenv
import google.generativeai as genai
import pytz
import os
from datetime import datetime



class EmailGenFromGemini():

    def __init__(self, model_name = 'gemini-pro',
                 source_path = None,
                 target_company_path = None,
                 target_person_path = None,
                 source = None,
                 target_company = None,
                 target_person = None,
                 tone_no = 0):
        self.model_name = model_name
        self.source = source
        self.target_person = target_person
        self.target_company = target_company
        self.source_path = source_path
        self.target_company_path = target_company_path
        self.target_person_path = target_person_path
        self.tone_no = tone_no



    # Declaring the dictionary to be used
    result = dict()
    result["model_name"] = None
    result["model_version"] = None
    result["source_product_name"] = None
    result["target_person_name"] = None
    result["target_company_name"] = None
    result["prompt"] = None
    result["email"] = None
    result["tone"] = None
    result["timestamp"] = None



    # Return data from file:
    def get_data_from_file(self, file_path) -> str:
        try:
            with open(file_path, 'r') as file:
                data = file.read()
                return data
        except FileNotFoundError:
            print(f"{file_path} file is not found")
            return None



    # Function to get the API Key of Gemini
    def get_gemini_api_key(self) -> None:
        dotenv.load_dotenv("/workspace/LLM-Emails/.env")    
        api_key = os.getenv("API_KEY")
        genai.configure(api_key=api_key)



    # Function to get the current time
    def get_current_time(self) -> str:
        try:
            timezone = pytz.timezone('Asia/Kolkata')                                        # In IST
            current_time = datetime.now(timezone)
            return current_time.strftime("%Y-%m-%d_%H:%M:%S")
        except Exception as e:
            print(f"Failed to get the current time zone, exception:\n{e}")
            return None



    # Chat Completion function for Gemini
    def get_gemini_completion(self, prompt, temp = 0.5) -> str:
        try:
            genai.configure(api_key = os.getenv("API_KEY"))
            model = genai.GenerativeModel('models/'+self.model_name)
            response = model.generate_content(
                prompt,
                generation_config = genai.types.GenerationConfig(
                    candidate_count = 1,
                    stop_sequences = ['space'],
                    temperature = temp
                )
            )
            return response
        except Exception as e:
            print(f"Failed to get the answer from the model, exception:\n{e}")
            return None



    # Getting the model version
    def get_model_version(self) -> None:
        if self.model_name != 'gemini-pro':
            model_list = self.model_name.split('-')
            version = ""
            for i in range(3,len(model_list)):
                version += model_list[i]
            return version
        return None



    # Function to get the email and other data
    def email_generation(self) -> dict:
        self.get_gemini_api_key()

        source = self.get_data_from_file(self.source_path)
        target_company = self.get_data_from_file(self.target_company_path)
        target_person = self.get_data_from_file(self.target_person_path)

        original_prompt = "You are provided with 'Target Person' data and 'Target Company' data.\
            You are also given ''Source Company's product'' data.\
            Your task is to generate an email describing how Source's product can be useful for the Target Person and the Target Company.\
            Start the conversation in the email in a personalized way by talking about the Target Person,\
            their experiences, achievements, university education, interests and other.\
            But only stick to the data provided, do not consider any external data or hallucinate.\
            Do not give any hyperlinks/text regarding the source or target company/person that isn't present in the given context.\
            Do not include more than 25-30 words in one line and give bulletpoints wherever necessary.\
            Now, refer to the Target Person's data provided earlier and then introduce the services of Source Company's product."

        email_gen_prompt = f"You are provided with 'Target Person' data\n\n: {target_person} \n\n\n\n\n You are also provided with the 'Target Company' data:\n\n {target_company}\n\n\n\n\n.\
            You are also given ''Source Company's product'' data:\n\n {source} \n\n\n\n\n.\
            Your task is to generate an email describing how Source's product can be useful for the Target Person and the Target Company.\
            Start the conversation in the email in a personalized way by talking about the Target Person,\
            their experiences, achievements, university education, interests and other.\
            But only stick to the data provided, do not consider any external data or hallucinate.\
            Do not give any hyperlinks/text regarding the source or target company/person that isn't present in the given context.\
            Do not include more than 25-30 words in one line and give bulletpoints wherever necessary.\
            Now, refer to the Target Person's data provided earlier and then introduce the services of Source Company's product."

        tone = ["Maintain a tone that is respectful,\
        professional, and aligns with formal business communication standards.\
        enchance the email in 15 - 20 lines.",
        "Add a touch of humor or a witty remark,\
        leveraging the Target Person's data provided earlier. Then, introduce the services of the Source Company's product\
        in a light-hearted and engaging manner. The goal is to make the email feel friendly,\
        approachable, and maybe even a bit funny.\
        Describe how the Source Company's product can be benifitted for the Target Company in 15 - 20 lines.",
        "The goal is to make the email feel friendly, approachable, and definitely funny. \
        Ensure the tone is semi-formal, maintaining respect while incorporating humor.\
        Keep the email short in 15 - 20 lines."]

        input_prompt = original_prompt + "\n" + tone[self.tone_no]
        prompt = email_gen_prompt + "\n" + tone[self.tone_no]
        response_obj = self.get_gemini_completion(prompt, 0.5)
        response = ""
        if response_obj is not None:
            response = response + response_obj.text
            # print(response)
        email_tone = 'formal'
        if self.tone_no == 0:
            email_tone = 'formal'
        elif self.tone_no == 1:
            email_tone = 'semi-formal'
        else:
            email_tone = 'jovial'

        self.result["model_name"] = self.model_name
        self.result["model_version"] = self.get_model_version()
        self.result["source_product_name"] = self.source
        self.result["target_person_name"] = self.target_person
        self.result["target_company_name"] = self.target_company
        self.result["prompt"] = original_prompt
        self.result["email"] = response
        self.result["tone"] = email_tone
        self.result["timestamp"] = self.get_current_time()
        return self.result