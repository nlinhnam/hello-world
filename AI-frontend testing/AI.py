import websockets
import asyncio
import fitz
import pymongo
from transformers import pipeline

qa_model = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')


def mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # can be changed to the actual database
    db = client["IDB"]  # can be changed to a database name
    col = db["pdf"]  # subject to change collection name


def extract_pdf(pdf):
    document = fitz.open(pdf)
    text = []
    for page in document:
        text.append((page.get_text("text")))
    return text


# function to call the question answer model
def answer(q, c):
    result = qa_model(question=q, context=c)
    return result


async def new_client_connected(client_socket, path):
    print("New Client Connected")
    while True:
        message = await client_socket.recv()
        print("Client sent: ", message)
        c = "My name is Linhnam Nguyen. I am currently 21 years old. My hobbies are playing video games and watching " \
            "anime. I am the oldest out of my 4 brothers and a sister."
        q = str(message)
        a = str(answer(q, c))
        await client_socket.send(a)


async def start_server():
    print("Server Start")
    await websockets.serve(new_client_connected, "localhost", 8000)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()
