from openai import OpenAI
import os
import openai
from constants import open_ai_key
import re
# personal ::
os.environ["OPENAI_API_KEY"] = (
    open_ai_key
)

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


messages = None

def initialize_messages():
    global messages
    if messages is None: 
        Chat_System_Message = """
                ### Role:
                You are an advanced language model trained to assist in providing concise and casual answers to interview questions. Your task is to answer questions from an interview transcript in a simple, conversational manner, avoiding complex definitions and limiting responses to 3-4 sentences.

                ### Task:
                Answer each interview question provided in the transcript. Your answers should be straightforward, using casual language that is easy to understand. Keep the answers short, ideally 3-4 sentences.

                ### Context:
                In interviews, concise and clear answers are valued. The goal is to provide responses that are easy to understand, avoid jargon, and sound natural in a conversational setting.

                ### Guidelines:
                1. **Simplicity:** Use simple language and avoid technical jargon or complex definitions.
                2. **Casual Tone:** Maintain a conversational tone, as if you are chatting with a friend.
                3. **Brevity:** Keep your responses short, ideally 3-4 sentences.
                4. **Clarity:** Ensure that your answers are clear and directly address the question asked.
                5. **Avoid Book Definitions:** Provide explanations in your own words, avoiding textbook-like definitions.
                6. Dont give any extra text. Only give the required answer

                ### Examples:
                **Example 1:**
                - **Question:** Can you explain what RESTful APIs are?
                - **Answer:** Sure! RESTful APIs are a way for different software applications to talk to each other over the web. They use standard HTTP methods like GET and POST. It's like giving commands and getting responses.

                ### Chain of Thought:
                1. **Identify Questions:** Break down the transcript to identify each interview question.
                2. **Formulate Answers:** Formulate simple, casual answers for each question, keeping in mind the guidelines.
                3. **Ensure Brevity:** Make sure the answers are limited to 3-4 sentences.
                4. **Review for Clarity:** Review the answers to ensure they are clear and easy to understand.

                Note: Only output 3-4 sentences for each question. Do not provide any additional information or explanations.

                ### Prompt:
                Given the following interview transcript, answer each question in simple, casual terms, 
                limiting your responses to 3-4 sentences for the given user question

                """


        messages=[
            {"role": "system", "content": Chat_System_Message}
            ]

def update_chat(messages, role, content):
  messages.append({"role": role, "content": content})
  return messages

def get_chatgpt_response(messages):
  response = client.chat.completions.create(
  model="gpt-4o",
  temperature=0.1,
  seed=42,
  messages=messages
)
  return response.choices[0].message.content



def call_openai_api(final_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # "gpt-3.5-turbo-1106",
        # response_format={"type": "json_object"},
        temperature=0.1,
        seed=42,
        messages=[
            {
                "role": "system",
                "content": "You are expert in answering the interview questions or identifying questions from text",
            },
            {
                "role": "user",
                "content": final_prompt,
            },
        ],
    )

    # print("here is the answer:")
    # print(response.choices[0].message.content)
    return response.choices[0].message.content


def extract_question_from_text(text):

    final_prompt = """
        ### Role:
        You are an advanced language model trained to assist in identifying and extracting specific types of information from text. Your task is to identify technical interview questions only from a given transcript of an interview discussion.

        ### Task:
        Identify all the techincal interview questions present in a transcript of an interview discussion. 
        The goal is to isolate and extract the sentences that are structured as  techincal interview questions.

        ### Context:
        In interviews, participants often ask questions to gather information, clarify points, or prompt further discussion. These questions can range from direct queries to more nuanced or implied questions. Identifying these  techincal interview questions can be crucial for analyzing the interview content and understanding the flow of conversation.

        ### Guidelines:
        1. **Focus on Questions:** Only identify and extract sentences that are structured as  techincal interview questions.
        2. **Question Indicators:** Look for typical question indicators such as:
            - Question marks (?)
            - any difference related to questions
            - Interrogative words (who, what, when, where, why, how)
            - Phrasing that implies a question even without explicit indicators (e.g., "Can you explain...")
            - Note:Dont give general questions like "How are you?" or "What is your name?" Give only the technical questions like what is transformers etc.
            - If there are No Technical questions present in the text, please give the output as "No Technical questions present in the text."
                - Dont add any extra text or ask any questions. Only give the required output.
                - Give only the text present in output. Do not give any explanation or any other text. 
        3. **Ignore Statements:** Do not include statements, exclamations, or commands that do not serve as questions.
        4. **Contextual Awareness:** Be mindful of the context to differentiate between rhetorical questions and genuine inquiries.
        5. **Consistency:** Ensure consistency in the identification process to maintain accuracy.

        ### Examples:
        **Example 1:**
        - **Input:**
        Can you tell me about Transformers? 

        - **Output:**
        Can you tell me about Transformers?

        **Example 2:**
        - **Input:**
        I see that you have a degree in computer science.
        Explain about pandas?

        - **Output:**
        Explain about pandas?

        **Example 3:**
        - **Input:**
        Hi How are you?  What is your name?  What is your age? 

        - **Output:**
        No Technical questions present in the text.

        **Example 4:**
        - **Input:**
        and is a great

        - **Output:**
        No Technical questions present in the text.

        ### Chain of Thought:
        1. **Identify Sentences:** Break down the transcript into individual sentences.
        2. **Check for Indicators:** Examine each sentence for question indicators such as question marks, interrogative words, and questioning phrasing.
        3. **Context Analysis:** Consider the context to ensure the identified sentence is a genuine question, not a rhetorical one or a statement.
        4. **Extract Questions:** Extract and list all identified questions, maintaining the original wording and structure.

        ### Prompt:
        Given the following interview transcript, identify and list all the questions present in the backtick```{input}```

        """.format(
        input=text
    )

    res = call_openai_api(final_prompt)
    return res


def get_answer_for_question(text):
    global messages
    print("text from audio :", text)

    # if there are less than 3 words in the text then return empty string
    if len(text.split()) < 3:
        return ""

    res = extract_question_from_text(text)
    lower_res = res.lower()
    print("Question from Text: ", res)
    if res.lower() == "".lower():
        return ""
    
    # use regular expression to find the No and Technical and questionswords in "No Technical questions present in the text" in res
    if re.search("no", lower_res) and re.search("technical", lower_res) and re.search("question", lower_res):
        return ""
    
    # Initialize messages if not already done
    if messages is None:
        initialize_messages()
    

    messages = update_chat(messages, "user", res)
    chat_response = get_chatgpt_response(messages)
    messages = update_chat(messages, "assistant", chat_response)


    print("Answer for the questions: ", chat_response)
    return chat_response