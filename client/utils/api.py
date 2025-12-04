from config import API_URL
import requests


def ask_question(question: str) :
    return requests.post(f"{API_URL}/ask",data={"question": question})


def upload_pdfs(files):
    file_payload=[('files', (file.name, file.read(), 'application/pdf')) for file in files]
    return requests.post(f"{API_URL}/upload_pdfs", files=file_payload)