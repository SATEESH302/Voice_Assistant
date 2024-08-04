from openai import OpenAI
import os
import openai
from constants import open_ai_key
# personal ::
os.environ["OPENAI_API_KEY"] = (
    open_ai_key
)

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


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
    # final_prompt = """for the given text  in the backtick```{input}```,
    # please extract question in the given context and 
    # please do not form new question give only the question present in context.

    # please give only output do not give any explanation 
    # apply chain of thought """.format(
    #     input=text
    # )

    final_prompt = """
        ### Role:
        You are an advanced language model trained to assist in identifying and extracting specific types of information from text. Your task is to identify questions from a given transcript of an interview discussion.

        ### Task:
        Identify all questions present in a transcript of an interview discussion. 
        The goal is to isolate and extract the sentences that are structured as questions.

        ### Context:
        In interviews, participants often ask questions to gather information, clarify points, or prompt further discussion. These questions can range from direct queries to more nuanced or implied questions. Identifying these questions can be crucial for analyzing the interview content and understanding the flow of conversation.

        ### Guidelines:
        1. **Focus on Questions:** Only identify and extract sentences that are structured as questions.
        2. **Question Indicators:** Look for typical question indicators such as:
            - Question marks (?)
            - any difference related to questions
            - Interrogative words (who, what, when, where, why, how)
            - Phrasing that implies a question even without explicit indicators (e.g., "Can you explain...")
            - Note:Dont give general questions like "How are you?" or "What is your name?" Give only the technical questions like what is transformers etc.
            - If there are no questions present in the text, please give the output as "No questions present in the text."
                - Dont add any extra text or ask any questions. Only give the required output.
                - Give only the text present in output. Do not give any explanation or any other text. 
        3. **Ignore Statements:** Do not include statements, exclamations, or commands that do not serve as questions.
        4. **Contextual Awareness:** Be mindful of the context to differentiate between rhetorical questions and genuine inquiries.
        5. **Consistency:** Ensure consistency in the identification process to maintain accuracy.

        ### Examples:
        **Example 1:**
        - **Input:**
        Can you tell me about Transformers? Sure, I worked at XYZ Corp for five years as a software developer.
        What were your main responsibilities there?I was responsible for developing and maintaining web applications.

        - **Output:**
        Can you tell me about Transformers?

        **Example 2:**
        - **Input:**
        I see that you have a degree in computer science.
        It provided a strong foundation in programming and problem-solving skills.That's great. 
        Explain about pandas?

        - **Output:**
        Explain about pandas?

        **Example 3:**
        - **Input:**
        Hi How are you? I am good. What is your name? My name is John. What is your age? I am 25 years old.

        - **Output:**
        No questions present in the text.

        **Example 4:**
        - **Input:**
        and is a great

        - **Output:**
        No questions present in the text.

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
    # audio_file = open(file_path, "rb")
    # transcription = client.audio.transcriptions.create(
    #     model="whisper-1", file=audio_file
    # )
    print("text from audio :", text)


    res = extract_question_from_text(text)
    print("Question from Text: ", res)
    if res == "No questions present in the text.":
        return ""
    
        # final_prompt = """I'm preparing for a job interview and would like some help answering a potential interview question. 
        # Please provide a detailed response and include your chain of thought as you work through the answer.
        # Points to remeber before answering 
        # 1) Understand the Question
        # 2) Identify Relevant Knowledge related to answer
        # 3) Structure the Answer and organize the response for clarity and impact
        # 4) Give answer in simple terms so that interviewer can understand easily
        # 5) Dont give any extra text. Only give the required answer
        # 6) Dont give any book definitions. Make it in simple and explainable words. It has to look like a normal conversation
        # for the given question in the backtick```{input}```,
        # please provide the answer  in three lines and do not give any explanation """.format(
        #     input=res
        # )
    final_prompt = """
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
        limiting your responses to 3-4 sentences for the given question in the backtick```{input}```

        """.format(
        input=res
    )

    final_res = call_openai_api(final_prompt)

    print("Answer for the questions: ", final_res)
    # print(final_res.choices[0].message.content)
    return final_res


