import pyaudio
import wave
from openai import OpenAI
import os
import openai

# personal ::
os.environ["OPENAI_API_KEY"] = (
    "ask satish"
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
                "content": "You are a expericed data scientist and python devolper, sql devloper to answer all the questions related to data science and sql and python",
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


def get_answer_for_question(file_path):
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    print("text from audio:::::::::::::::", transcription.text)

    res = extract_question_from_text(transcription.text)
    final_prompt = """for the given question in the backtick```{input}```,
    please provide the answer  in two lines and do not give any explanation """.format(
        input=res
    )
    final_res = call_openai_api(final_prompt)

    print("here is the answer:")
    # print(final_res.choices[0].message.content)
    return final_res


text = """how to handle outliers in categorical column It represents the difference between the average prediction of our model and the correct value we are trying to predict. """
res = extract_question_from_text(text)

print("res:", res)
