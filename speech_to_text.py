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
                "content": "You are expert in answering the interview questions.",
            },
            {
                "role": "user",
                "content": final_prompt,
            },
        ],
    )

    print("here is the answer:")
    print(response.choices[0].message.content)
    return response.choices[0].message.content


def extract_question_from_text(text):
    final_prompt = """for the given text  in the backtick```{input}```,
    please extract question in the given context and 
    please do not form new question give only the question present in context.
     
    example:
     context : my self satish, i have 3 years of experiance and presenlty i 'm working in hcl as softwer devloper  how transformers work
    output : how transformers works ? 

    please give only output do not give any explanation 
    apply chain of thought """.format(
        input=text
    )
    res = call_openai_api(final_prompt)
    return res


def get_answer_for_question(text):
    # audio_file = open(file_path, "rb")
    # transcription = client.audio.transcriptions.create(
    #     model="whisper-1", file=audio_file
    # )
    print("text from audio:::::::::::::::", text)

    res = extract_question_from_text(text)
    final_prompt = """I'm preparing for a job interview and would like some help answering a potential interview question. 
    Please provide a detailed response and include your chain of thought as you work through the answer.
    Points to remeber before answering 
    1) Understand the Question
    2) Identify Relevant Knowledge related to answer
    3) Structure the Answer and organize the response for clarity and impact
    4) Give answer in simple terms so that interviewer can understand easily
    for the given question in the backtick```{input}```,
    please provide the answer  in three lines and do not give any explanation """.format(
        input=res
    )
    final_res = call_openai_api(final_prompt)

    print("here is the answer:")
    # print(final_res.choices[0].message.content)
    return final_res


