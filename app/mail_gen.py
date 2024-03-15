# Class to generate Emails from Gemini
import os
import pytz
import dotenv
import google.generativeai as genai
from datetime import datetime
from google.generativeai.generative_models import ChatSession, GenerativeModel




class EmailGenFromGemini():

    def __init__(self, model_name = 'gemini-pro',
                 source_path = None,
                 target_company_path = None,
                 target_person_path = None,
                 source_person = "John Doe",
                 source_person_designation = "Sales Executive",
                 source_company = None,
                 target_company = None,
                 target_person = None
                 ):
        self.model_name = model_name
        self.source_person = source_person
        self.source_person_designation = source_person_designation
        self.source_company = source_company
        self.target_person = target_person
        self.target_company = target_company
        self.source_path = source_path
        self.target_company_path = target_company_path
        self.target_person_path = target_person_path


    # Declaring the tone to be used
    __tone_list = [
    '''Formal:
        Craft a formal business email with a professional tone.
        Address the recipient with proper salutations, maintain a respectful language, and avoid overly informal expressions.
        Begin by acknowledging the recipient's professional achievements, introduce your company's services clearly and concisely,
        and conclude with a formal expression of interest in potential collaboration or discussion.''',
    
    '''Semi-formal:
        Generate an email with a semi-formal tone, striking a balance between professionalism and friendliness.
        Address the recipient by name, express admiration for their achievements,
        and introduce your company's services in a straightforward yet approachable manner.
        Conclude the email with a courteous invitation for further discussion or collaboration,
        maintaining a tone that is both respectful and personable.''',

    '''Jovial:
        Compose a friendly and upbeat email in a jovial tone. Use light-hearted language, incorporate positive greetings,
        and perhaps share a relevant, industry-related joke or anecdote. Introduce your company's services in a casual,
        engaging manner, and conclude the email with an invitation for further discussion or collaboration. Maintain an overall lively and friendly tone throughout.
        Include emojis wherever possible.''',        
    ]

    # Original Prompt
    __original_prompt = '''
        The data is given below in the form of HTML tags: every tag name describes its contents within its opening and closing tags.
        You have to use the context given, to perform the task with the required specifications, using the given example.
        <SOURCE_PERSON_NAME>
            {Source_person}
        </SOURCE_PERSON_NAME>
        <SOURCE_COMPANY_NAME>
            {Source_company}
        </SOURCE_COMPANY_NAME>
        <TARGET_PERSON_NAME>
            {Target_person}
        </TARGET_PERSON_NAME>
        <TARGET_COMPANY_NAME>
            {Target_company}
        </TARGET_COMPANY_NAME>
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
            1. Generate an email describing how Source company's product(s) can be useful for the Target Person and the Target Company.
            2. Maintain the required structure of the email: subject, proper slautation, body and regards and include the source person's name wherever necessary.
            2. Highlight the product/service features of Source company to the Target Person.
            3. Start the conversation in the email in a personalized way by talking about the Target Person,\
               their experiences, achievements, university education and interests from the context provided.
            5. While considering the target person's experiences, focus mostly on latest role and working company.
            6. Do not use template names such as: [SOURCE_PERSON_NAME], [SOURCE_NAME], etc... but use the given names in context wherever possible.
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
            5. You will also be given future instructions. If they are in conflict with the present ones, then consider the future ones.
        </SPECIFICATIONS>
        '''

    # System Prompt
    __system_prompt = "You are a professional sales outreach executive with over 15 years of experience.\
                                    You leverage the use of English as a language and context about the: Source, Target Company and Target person)\
                                    to write a hyper-personalized sales outreach email to the Target Person."

    # __delimiter for prompts and chat results.
    __delimiter = "\n<DELIMITER>\n"

    # Declaring the dictionary to be used
    __result = dict()
    __result["model_name"] = None
    __result["model_version"] = None
    __result["source_person_name"] = None
    __result["source_company_name"] = None
    __result["target_person_name"] = None
    __result["target_company_name"] = None
    __result["prompt"] = {
        "formal" : "",
        "semi-formal" : "",
        "jovial" : ""
    }
    __result["email_chat"] = {
        "formal" : "",
        "semi-formal" : "",
        "jovial" : ""
    }
    __result["final_email"] = None
    __result["timestamp"] = None



    # Return data from file:
    def __get_data_from_file(self, file_path) -> str:
        try:
            with open(file_path, 'r') as file:
                data = file.read()
                return data
        except FileNotFoundError:
            print(f"{file_path} file is not found")
            return ""



    # Function to get the API Key of Gemini
    def __get_gemini_api_key(self) -> None:
        try:
            if dotenv.load_dotenv("/workspace/LLM-Emails/Secrets/.env"):    
                genai.configure(api_key = os.getenv("API_KEY"))
                return True
        except Exception as e:
            print(f"Exception occurred at Gemini API Key Authentication: {e}")
            return False



    # Getting the model version
    def __get_model_version(self) -> None:
        if self.model_name != 'gemini-pro':
            model_list = self.model_name.split('-')
            version = ""
            for i in range(3,len(model_list)):
                version += model_list[i]
            return version
        return None



    # Function to get the current time
    def __get_current_time(self) -> str:
        try:
            timezone = pytz.timezone('Asia/Kolkata')                                        # In IST
            current_time = datetime.now(timezone)
            return current_time.strftime("%Y-%m-%d_%H:%M:%S")
        except Exception as e:
            print(f"Failed to get the current time zone, exception:\n{e}")
            return None



    # # Chat Completion function for Gemini
    # def get_gemini_completion(self, prompt, temp = 0.5) -> str:
    #     try:
    #         genai.configure(api_key = os.getenv("API_KEY"))
    #         model = genai.GenerativeModel('models/'+self.model_name)
    #         response = model.generate_content(
    #             prompt,
    #             generation_config = genai.types.GenerationConfig(
    #                 candidate_count = 1,
    #                 stop_sequences = ['space'],
    #                 temperature = temp
    #             )
    #         )
    #         return response
    #     except Exception as e:
    #         print(f"Failed to get the answer from the model, exception:\n{e}")
    #         return None



    # Function to initialize the model
    def __initialize_model(self, chat : ChatSession = None, data_list : list = None) -> None:
        try:
            actual_prompt =f'''
                The data is given below in the form of HTML tags: every tag name describes its contents within its opening and closing tags.
                You have to use the context given, to perform the task with the required specifications, using the given example.
                <SOURCE_PERSON_NAME>
                    {self.source_person}
                </SOURCE_PERSON_NAME>
                <SOURCE_COMPANY_NAME>
                    {self.source_company}
                </SOURCE_COMPANY_NAME>
                <TARGET_PERSON_NAME>
                    {self.target_person}
                </TARGET_PERSON_NAME>
                <TARGET_COMPANY_NAME>
                    {self.target_company}
                </TARGET_COMPANY_NAME>
                <CONTEXT>
                    <SOURCE_COMPANY_DATA>
                        {data_list[0]}
                    </SOURCE_COMPANY_DATA>
                    <TARGET_COMPANY_DATA>
                        {data_list[1]}
                    </TARGET_COMPANY_DATA>
                    <TARGET_PERSON_DATA>
                        {data_list[2]}
                    </TARGET_PERSON_DATA>
                </CONTEXT>
                <TASK>
                    1. Generate an email describing how Source company's product(s) can be useful for the Target Person and the Target Company.
                    2. Maintain the required structure of the email: subject, proper salutation, body and regards and include the source person's name wherever necessary.
                    3. Highlight the product/service features of Source company to the Target Person.
                    4. Start the conversation in the email in a personalized way by talking about the Target Person,\
                    their experiences, achievements, university education, and interests from the context provided.
                    5. While considering the target person's experiences, focus mostly on latest role and working company.
                    6. Do not use template names such as: [SOURCE_PERSON_NAME], [SOURCE_NAME], etc.. but use the given names in context wherever possible.
                </TASK>
                <SPECIFICATIONS>
                    1. Stick only to the data provided, do not consider any external data or hallucinate.
                    2. Do not include text regarding the source or target company/person that isn't present in the given context.
                    3. Do not include more than 25-30 words in one line and give numbered bulletpoints only when necessary.
                    4. Consider the required names of Source Person, Source Company, Target Person and Target Company from the context provided.
                    5. Do not include hyperlinks/placeholder text in the content of the email.
                    4. Ensure that the content has the tone:
                        <TONE>
                            {self.__tone_list[0]}
                        </TONE>
                    5. You will also be given future instructions. If they are in conflict with the present ones, then consider the future ones.
                </SPECIFICATIONS>
                '''
            
            # Setting the prompts in the result dictionary
            for key in self.__result["prompt"].keys():
                self.__result["prompt"][key] = self.__system_prompt + self.__delimiter

            # Initializing the chat class
            self.__result["email_chat"]["formal"] = chat.send_message(actual_prompt).text
            self.__result["email_chat"]["semi-formal"] = chat.send_message(f"Generate the mail in Semi-formal tone:\n{self.__tone_list[1]}\n. Generate it different from the previous mails.").text
            self.__result["email_chat"]["jovial"] = chat.send_message(f"Generate email in Jovial tone:\n{self.__tone_list[2]}\n. Generate it different from the previous mails.").text

        except Exception as e:
            print(f"Exception occurred: {e}")
        
        

    # Function to get the email and other data
    def email_generation(self) -> dict:
        if self.__get_gemini_api_key():
            path_list = [self.source_path, self.target_company_path, self.target_person_path]
            data_list = []

            for i in range(3):
                data_list.append(self.__get_data_from_file(path_list[i]))

            model = genai.GenerativeModel(self.model_name)
            chat = model.start_chat(history = [])
            self.__initialize_model(chat, data_list)

            # Display for the formal, semi-formal and jovial-tones for the initial stage.
            # result["email"]["formal"]
            # result["email"]["semi-formal"]
            # result["email"]["jovial"]

            # User will select one of the tones and then make necessary changes.

            self.__result["model_name"] = self.model_name
            self.__result["model_version"] = self.__get_model_version()
            self.__result["source_person_name"] = self.source_person
            self.__result["source_company_name"] = self.source_company
            self.__result["target_person_name"] = self.target_person
            self.__result["target_company_name"] = self.target_company
            self.__result["timestamp"] = self.__get_current_time()
            self.__result["final_email"] = self.__result["email_chat"]["formal"]
            return self.__result
        
        else:
            print("API Key authentication failed for Gemini!!!!")
            return None