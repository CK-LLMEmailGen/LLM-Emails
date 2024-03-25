# Declaring the tone to be used
tone_dict = {
"formal":
    '''
    In addition to the previously given prompt,
    Craft a formal business email with a professional tone.
    Address the recipient with proper salutations, maintain a respectful language, and avoid overly informal expressions.
    Begin by acknowledging the <TARGET_PERSON_NAME> professional achievements, data taken from <TARGET_PERSON_DATA>, introduce your <SOURCE_COMPANY_NAME>'s services (<PRODUCT_DESCRIPTION_OF_SOURCE_COMPANY>).
    Do also highlight key points from <SOURCE_COMPANY_DATA> to highlight <SOURCE_COMPANY_NAME>'s experience, expertise to instill confidence in <TARGET_PERSON_NAME> for a potential business deal.
    Don't also forget to highlight key points from <TARGET_COMPANY_DATA> to highlight <TARGET_COMPANY_NAME>'s experience in their respective fields. (This shows that <SOURCE_PERSON> took time to research about <TARGET_COMPANY_NAME>'s data).
    Conclude with a formal expression of collaboration between <SOURCE_COMPANY_NAME> and <TARGET_COMPANY_NAME>.
    The tone must be very formal, but not too monotonic. Do not consider data that is not given in context and don't hallucinate.
    Do not include templates names such as; [Source_person_name], etc...
    ''',

"semi-formal":
    '''
    In addition to the previously given prompts,
    Generate an email with a semi-formal tone, striking a balance between professionalism and friendliness. 
    Address the <TARGET_PERSON_NAME> by expressing admiration for their achievements as given in <TARGET_PERSON_DATA> and introduce <SOURCE_COMPANY_NAME>'s \
    services <PRODUCT_DESCRIPTION_OF_SOURCE_COMPANY> in a very friendly manner, but not too-informal, whilst also highlighting key points of achievements about <TARGET_COMPANY_NAME> taken from <TARGET_COMPANY_DATA>.
    Conclude the email with a courteous invitation for further discussion or collaboration between <SOURCE_COMPANY_NAME> and <TARGET_COMPANY_NAME>,
    maintaining a tone that is respectable, but a bit fiendly and humorous, make the email different than the formal tone.
    Don't consider data that is not present in the context given and don't hallucinate.
    Do not include templates names such as; [Source_person_name], etc...
    ''',

"jovial":
    '''
    In addition to the previously given prompts,
    Compose a friendly and upbeat email in a jovial tone. Use light-hearted language, incorporate positive greetings,
    and perhaps share a relevant, industry-related joke or anecdote. Commend <TARGET_COMPANY_NAME>'s achievements, taken from <TARGET_COMPANY_DATA> and Introduce <SOURCE_COMPANY_NAME>'s services\
    present in <SOURCE_COMPANY_DATA> and its product's data present in <PRODUCT_DESCRIPTION_OF_SOURCE_DATA> in a casual,\
    engaging manner to <TARGET_PERSON_NAME>, whilst also including quips about the education, experience of <TARGET_PERSON_NAME> present in <TARGET_PERSON_DATA>,\
    and conclude the email with an invitation for further discussion or collaboration. Maintain an overall lively and friendly tone throughout.
    Include emojis wherever possible.
    Don't consider data that is not present in the context given and don't hallucinate.
    Do not include templates names such as; [Source_person_name], etc...
    '''        
}

# Original Prompt
original_prompt = '''
    The data is given below in the form of HTML tags: every tag name describes its contents within its opening and closing tags.
    You have to use the context given, to perform the task with the required specifications, using the given example.
    <SOURCE_PERSON_NAME>
        {source_person}
    </SOURCE_PERSON_NAME>
    <SOURCE_PERSON_DESIGNATION>
        {source_person_designation}
    </SOURCE_PERSON_DESIGNATION>
    <SOURCE_COMPANY_NAME>
        {source_company}
    </SOURCE_COMPANY_NAME>
    <TARGET_PERSON_NAME>
        {target_person}
    </TARGET_PERSON_NAME>
    <TARGET_COMPANY_NAME>
        {target_company}
    </TARGET_COMPANY_NAME>
    <CONTEXT>
        <PRODUCT_DESCRIPTION_OF_SOURCE_COMPANY>
            {data}
        </PRODUCT_DESCRIPTION_OF_SOURCE_COMPANY>
        <SOURCE_COMPANY_DATA>
            {data}
        </SOURCE_COMPANY_DATA>
        <TARGET_COMPANY_DATA>
            {data}
        </TARGET_COMPANY_DATA>
        <TARGET_PERSON_DATA>
            {data}
        </TARGET_PERSON_DATA>
    </CONTEXT>
    <TASK>
        1. Generate an email describing how <PRODUCT_DESCRIPTION_OF_SOURCE_COMPANY> can be useful for the <TARGET_PERSON_NAME>\
            and the <TARGET_COMPANY_NAME>.
        2. Use <SOURCE_COMPANY_DATA> to explain about <SOURCE_COMPANY_NAME> to the <TARGET_PERSON_NAME> wherever necessary.
        3. Commend the experience(s), education and achievement(s) related to the <TARGET_PERSON_NAME> and the <TARGET_COMPANY_NAME> in a few lines.
        4. Maintain the required structure of the email: subject, proper salutation, body and regards and include the <SOURCE_PERSON_NAME> wherever necessary.
        5. Using <PRODUCT_DESCRIPTION_OF_SOURCE_COMPANY>, highlight the product/service features of <SOURCE_COMPANY_NAME> to the Target Person.
        6. Start the conversation in the email in a personalized way by talking about the <TARGET_PERSON_NAME>,\
            their experiences, achievements, university education, and interests from the context provided.
        7. While considering the <TARGET_PERSON_DATA> experiences, focus mostly on latest role and working company.
        8. Do not use template names such as: [SOURCE_PERSON_NAME], [SOURCE_NAME], etc.. but use the given names in context wherever possible.
    </TASK>
    <SPECIFICATIONS>
        1. Keep the entire text within 80 words.
        2. Stick only to the data provided, do not consider any external data or hallucinate.
        3. Do not include text regarding the source or target company/person that isn't present in the given context.
        4. Do not include more than 20 words in one line and give numbered bulletpoints only when necessary.
        5. Consider the required names of Source Person, Source Company, Target Person and Target Company from the context provided.
        6. Do not include hyperlinks/placeholder text in the content of the email.
        7. Generate the email based on the tone asked.
        8. You will also be given future instructions. If they are in conflict with the present ones, then consider the future ones.
    </SPECIFICATIONS>
    '''

# System Prompt
system_prompt = "You are a professional sales outreach executive with over 15 years of experience.\
                                You leverage the use of English as a language and context about the: Source, Target Company and Target person)\
                                to write a hyper-personalized sales outreach email to the Target Person.\
                                Do not generate the email right now, you will be given further instructions."

# __delimiter for prompts and chat results.
delimiter = "\n<DELIMITER>\n"