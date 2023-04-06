import requests
import time
from api_secrets import API_KEY_ASSEMBLYAI

# 1. 로컬에 있는 파일을 어셈블리 AI에 업로드
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {"authorization": API_KEY_ASSEMBLYAI}


def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint, headers=headers, data=read_file(filename)
    )

    audio_url = upload_response.json()["upload_url"]
    return audio_url


# 2. 텍스트 변환
def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=headers
    )

    job_id = transcript_response.json()["id"]
    return job_id


# 3. 어셈블리 api계속 끌어오기
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


# 이후 출력의 status를 확인하여 완료여부를 알아낼 수 있다. 현 시점에서는 처리중이다.
# 그래서 반복적으로 status를 물어보는 코드를 작성할 것이다.


def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while 1:
        data = poll(transcript_id)
        # polling_response = requests.get(polling_endpoint, headers=headers)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]
        print("Waiting 30 seconds...")
        time.sleep(30)


# 변환된거 저장


def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)
    if data:
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data["text"])
        print("텍스트로 저장.")
    else:
        print("Error!", error)
    print(data)
