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
                 source_person = "John Doe",
                 source_company = None,
                 target_company = None,
                 target_person = None,
                 tone_no = 0):
        self.model_name = model_name
        self.source_person = source_person
        self.source_company= source_company
        self.target_person = target_person
        self.target_company = target_company
        self.source_path = source_path
        self.target_company_path = target_company_path
        self.target_person_path = target_person_path
        self.tone_no = tone_no


    # Declaring the tone to be used
    tone = [
    '''Jovial:\
        Compose a friendly and upbeat email in a jovial tone. Use light-hearted language, incorporate positive greetings, \
        and perhaps share a relevant, industry-related joke or anecdote. Introduce your company's services in a casual,\ 
        engaging manner, and conclude the email with an invitation for further discussion or collaboration. Maintain an overall lively and friendly tone throughout.''',       
        
    '''Formal:\
    Craft a formal business email with a professional tone. \
    Address the recipient with proper salutations, maintain a respectful language, and avoid overly informal expressions. \
    Begin by acknowledging the recipient's professional achievements, introduce your company's services clearly and concisely, \
    and conclude with a formal expression of interest in potential collaboration or discussion.''',
    
    '''Semi-formal:\
    Generate an email with a semi-formal tone, striking a balance between professionalism and friendliness. \
    Address the recipient by name, express admiration for their achievements, \
    and introduce your company's services in a straightforward yet approachable manner. \
    Conclude the email with a courteous invitation for further discussion or collaboration, \
    maintaining a tone that is both respectful and personable.'''
    ]


    # Declaring the dictionary to be used
    result = dict()
    result["model_name"] = None
    result["model_version"] = None
    result["source_person_name"] = self.source_person
    result["source_company_name"] = None
    result["target_person_name"] = None
    result["target_company_name"] = None
    result["prompt"] = None
    result["email_chat"] = {
        "formal" : "",
        "semi-formal" : "",
        "jovial" : ""
    }
    result["final_email"] = None
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
        try:
            if dotenv.load_dotenv("/workspace/LLM-Emails/.env"):    
                genai.configure(api_key = os.getenv("API_KEY"))
                return True
        except Exception as e:
            print(f"Exception occurred at Gemini API Key Authentication: {e}")
            return False



    # Getting the model version
    def get_model_version(self) -> None:
        if self.model_name != 'gemini-pro':
            model_list = self.model_name.split('-')
            version = ""
            for i in range(3,len(model_list)):
                version += model_list[i]
            return version
        return None



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



    def initialize_model(self, data_list = None):
        system_prompt = "You are a professional sales outreach executive with over 15 years of experience.\
                                    You leverage the use of English as a language and context about the: Source, Target Company and Target person)\
                                    to write a hyper-personalized sales outreach email to the Target Person."

        original_prompt = '''
            The data is given below in the form of HTML tags: every tag name describes its contents within its opening and closing tags.
            You have to use the context given, to perform the task with the required specifications, using the given example.
            <SENDER_NAME>
                {Source_person}
            </SENDER_NAME>
            <CONTEXT>
                <SOURCE_DATA>
                    {Source_data}
                </SOURCE_DATA>
                <TARGET_COMPANY_DATA>
                    {Target_company_data}
                </TARGET_COMPANY_DATA>
                <TARGET_PERSON_DATA>
                    {Target_person_data}
                </TARGET_PERSON_DATA>
            </CONTEXT>
            <TASK>
                1. Generate an email describing how Source's product can be useful for the Target Person and the Target Company.
                2. Highlight the product/service features of Source company to the Target Person.
                3. Start the conversation in the email in a personalized way by talking about the Target Person,\
                   their experiences, achievements, university education, interests and other.
            </TASK>
            <SPECIFICATIONS>
                1. Stick only to the data provided, do not consider any external data or hallucinate.
                2. Do not include text regarding the source or target company/person that isn't present in the given context.
                3. Do not include more than 25-30 words in one line and give numbered bulletpoints only when necessary.
                4. Do not give a template for filling in Source Company, Target Company and Target Person names.
                   But, take the names from the context provided.
                5. Do not include hyperlinks/placeholder text in the content of the email.
                4. Ensure that the content has the tone:
                    <TONE>
                        {tone}
                    </TONE>
            </SPECIFICATIONS>
            <EXAMPLE>
                Take this email as an example on how to generate an email in a personal way\
                Greetings <Target_Person_Name>, \
                I was attempting to stand out in your inbox with some clever, witty and impressive statements. Alas, I wrote this email instead.\
                Let me get straight to the point now. We are a software development company that has been assisting healthcare businesses and companies with their web and mobile app design and development.\
                I am including some of our amazing clientele here in the vain hope that they’ll impress you: AstraZeneca, Heartbeat Health, Valis Bioscience, Better PT, Concert Pharma, eVisit, CFG Health Systems, Merck and more. *Fingers Crossed*\
                Rather predictably, I would like a short call with you, to demonstrate how our team of engineers can help you with your healthcare services.\
                I trust this email will charm you into pressing the reply button.\
                I await your profanity filled response.\
                --\
                Have a positively wonderful day,\
                company name\
                P.S. If you don’t want to receive any more emails from us, simply reply and let us know \
            </EXAMPLE>
            '''
        
        actual_prompt =f'''
            The data is given below in the form of HTML tags: every tag name describes its contents within its opening and closing tags.
            You have to use the context given, to perform the task with the required specifications, using the given example.
            <SENDER_NAME>
                {self.source_person}
            </SENDER_NAME>
            <CONTEXT>
                <SOURCE_DATA>
                    {data_list[0]}
                </SOURCE_DATA>
                <TARGET_COMPANY_DATA>
                    {data_list[1]}
                </TARGET_COMPANY_DATA>
                <TARGET_PERSON_DATA>
                    {data_list[2]}
                </TARGET_PERSON_DATA>
            </CONTEXT>
            <TASK>
                1. Generate an email describing how Source's product can be useful for the Target Person and the Target Company.
                2. Highlight the product/service features of Source company to the Target Person.
                3. Start the conversation in the email in a personalized way by talking about the Target Person,\
                   their experiences, achievements, university education, interests and other.
            </TASK>
            <SPECIFICATIONS>
                1. Stick only to the data provided, do not consider any external data or hallucinate.
                2. Do not include text regarding the source or target company/person that isn't present in the given context.
                3. Do not include more than 25-30 words in one line and give numbered bulletpoints only when necessary.
                4. Do not give a template for filling in Source Company, Target Company and Target Person names.
                   But, take the names from the context provided.
                5. Do not include hyperlinks/placeholder text in the content of the email.
                4. Ensure that the content has the tone:
                    <TONE>
                        {tone[0]}
                    </TONE>
            </SPECIFICATIONS>
            <EXAMPLE>
                Take this email as an example on how to generate an email in a personal way\
                Greetings <Target_Person_Name>, \
                I was attempting to stand out in your inbox with some clever, witty and impressive statements. Alas, I wrote this email instead.\
                Let me get straight to the point now. We are a software development company that has been assisting healthcare businesses and companies with their web and mobile app design and development.\
                I am including some of our amazing clientele here in the vain hope that they’ll impress you: AstraZeneca, Heartbeat Health, Valis Bioscience, Better PT, Concert Pharma, eVisit, CFG Health Systems, Merck and more. *Fingers Crossed*\
                Rather predictably, I would like a short call with you, to demonstrate how our team of engineers can help you with your healthcare services.\
                I trust this email will charm you into pressing the reply button.\
                I await your profanity filled response.\
                --\
                Have a positively wonderful day,\
                company name\
                P.S. If you don’t want to receive any more emails from us, simply reply and let us know \
            </EXAMPLE>
            '''
        
        delimiter = "\n<DELIMITER>\n"
        result["prompt"] = system_prompt
        result["prompt"] += delimiter
        result["prompt"] += original_prompt + "And in semi-formal, jovial tones too"
        result["prompt"] += delimiter
        model = genai.GenerativeModel(self.model_name)
        chat = model.start_chat(history = [])
        chat.send_message(system_prompt)
        result["email_chat"]["fomal"] = chat.send_message(actual_prompt)
        result["email_chat"]["semi-formal"] = chat.send_message("Generate the mail in semi-formal tone")
        result["email_chat"]["jovial"] = chat.send_message("Generate email in jovial tone")
        for key in result["email_chat"].keys():
            result["email_chat"][key] += delimiter
        ### Last change made here
        



    # Function to get the email and other data
    def email_generation(self) -> dict:
        if self.get_gemini_api_key():
            path_list = [self.source_path, self.target_company_path, self.target_person_path]
            data_list = [None*3]

            for i in range(3):
                data_list[i] = self.get_data_from_file(path_list[i])

            # source_company = self.get_data_from_file(self.source_path)
            # target_company = self.get_data_from_file(self.target_company_path)
            # target_person = self.get_data_from_file(self.target_person_path)

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
            self.result["source_person_name"] = self.source_person
            self.result["source_company_name"] = self.source_company
            self.result["target_person_name"] = self.target_person
            self.result["target_company_name"] = self.target_company
            self.result["prompt"] = original_prompt
            self.result["email"] = response
            self.result["tone"] = email_tone
            self.result["timestamp"] = self.get_current_time()
            return self.result
        
        else:
            print("API Key authentication failed for Gemini!!!!")
            return None