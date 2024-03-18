# Declaring the tone to be used
tone_dict = {
"formal":
    '''
    Craft a formal business email with a professional tone.
    Address the recipient with proper salutations, maintain a respectful language, and avoid overly informal expressions.
    Begin by acknowledging the recipient's professional achievements, introduce your company's services clearly and concisely,
    and conclude with a formal expression of interest in potential collaboration or discussion.
    ''',

"semi-formal":
    '''
    Generate an email with a semi-formal tone, striking a balance between professionalism and friendliness.
    Address the recipient by name, express admiration for their achievements,
    and introduce your company's services in a straightforward yet approachable manner.
    Conclude the email with a courteous invitation for further discussion or collaboration,
    maintaining a tone that is both respectful and personable.
    ''',

"jovial":
    '''
    Compose a friendly and upbeat email in a jovial tone. Use light-hearted language, incorporate positive greetings,
    and perhaps share a relevant, industry-related joke or anecdote. Introduce your company's services in a casual,
    engaging manner, and conclude the email with an invitation for further discussion or collaboration. Maintain an overall lively and friendly tone throughout.
    Include emojis wherever possible.
    '''        
}

# Original Prompt
original_prompt = '''
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
system_prompt = "You are a professional sales outreach executive with over 15 years of experience.\
                                You leverage the use of English as a language and context about the: Source, Target Company and Target person)\
                                to write a hyper-personalized sales outreach email to the Target Person.\
                                Do not generate the email right now, you will be given further instructions."

# __delimiter for prompts and chat results.
delimiter = "\n<DELIMITER>\n"