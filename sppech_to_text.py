import pyaudio
import wave

# # Parameters
# FORMAT = pyaudio.paInt16  # Format of sampling
# CHANNELS = 1  # Number of audio channels
# RATE = 44100  # Sampling rate (samples per second)
# CHUNK = 1024  # Number of frames per buffer
# RECORD_SECONDS = 5  # Duration of recording
# OUTPUT_FILENAME = "output.wav"  # Output file name

# # Create an interface to PortAudio
# audio = pyaudio.PyAudio()

# # Open a new stream
# stream = audio.open(
#     format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
# )

# print("Recording...")

# frames = []

# # Store data in chunks for RECORD_SECONDS
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)

# print("Finished recording.")

# # Stop and close the stream
# stream.stop_stream()
# stream.close()
# # Terminate the PortAudio interface
# audio.terminate()

# # Save the recorded data as a WAV file
# wf = wave.open(OUTPUT_FILENAME, "wb")
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(audio.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b"".join(frames))
# wf.close()


from openai import OpenAI
import os
import openai

# personal ::
os.environ["OPENAI_API_KEY"] = "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"

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


# audio_file = open("output.wav", "rb")
# transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
# print("textt:::::::::::::::", transcription.text)


# final_prompt = """for the given question in the backtick```{input}```,
# please provide the answer """.format(
#     input=transcription.text
# )
# response = client.chat.completions.create(
#     model="gpt-4o",  # "gpt-3.5-turbo-1106",
#     # response_format={"type": "json_object"},
#     temperature=0.1,
#     seed=42,
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a expericed data scientist and python devolper, sql devloper to answer all the questions related to data science and sql and python",
#         },
#         {
#             "role": "user",
#             "content": final_prompt,
#         },
#     ],
# )

# print("here is the answer:")
# print(response.choices[0].message.content)


def get_answer_for_question(file_path):
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    print("textt:::::::::::::::", transcription.text)

    final_prompt = """for the given question in the backtick```{input}```,
    please provide the answer  and do not give any explanation """.format(
        input=transcription.text
    )
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
