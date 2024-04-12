from flask import Flask, request, jsonify
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from flask_cors import CORS
import pandas as pd

df = pd.read_csv(
    "C:\\Users\\Admin\\OneDrive\\Desktop\\Conversational_Fashion_Outfit\\output.csv")

embedder = SentenceTransformer('all-mpnet-base-v2')
pc = Pinecone(
    api_key="a8230bbc-dac6-4f9d-871a-26e0db728c10"
)
index = pc.Index("fashion-products")

app = Flask(__name__)
CORS(app)


def vectorSearch(inputQuery, k=10):
    resultant_list = []
    qa_vector = embedder.encode(inputQuery).tolist()
    results = index.query(
        vector=qa_vector,
        top_k=k,
    )
    for i in range(k):
        id = results["matches"][i]["id"]
        id = float(id)
        id = int(id)
        resultant_list.append(id)
    return resultant_list


@app.route("/")
def health():
    return "OK"


@app.route("/queryProcessor", methods=["POST"])
def queryProcessor():
    body = request.json
    res = vectorSearch(body["query"])
    response = []
    for i in range(0, len(res)):
        dic = {}
        dic["id"] = res[i]
        dic["name"] = df["name"][res[i]]
        dic["price"] = df["price"][res[i]]
        dic["img"] = df["img"][res[i]]
        dic["ratingCount"] = df["ratingCount"][res[i]]
        dic["avg_rating"] = df["avg_rating"][res[i]]
        dic["description"] = df["description"][res[i]]
        dic["quantity"] = 1
        response.append(dic)
    mymess = {
        "data": response,
        "status": 200
    }
    return jsonify(mymess)


@app.route("/product/<int:id>", methods=["GET"])
def product(id):
    dic = {}
    id = int(id)
    dic["id"] = id
    dic["name"] = df["name"][id]
    dic["price"] = df["price"][id]
    dic["img"] = df["img"][id]
    dic["ratingCount"] = df["ratingCount"][id]
    dic["avg_rating"] = df["avg_rating"][id]
    dic["description"] = df["description"][id]
    dic["quantity"] = 1
    mymess = {
        "data": dic,
        "status": 200
    }
    return jsonify(mymess)


if __name__ == '__main__':
    app.run(debug=True)
