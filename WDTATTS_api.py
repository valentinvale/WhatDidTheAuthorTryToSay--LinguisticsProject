from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import spacy
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from keybert import KeyBERT

app = Flask(__name__)

CORS(app)

@app.route('/predict_t5_small', methods=['POST'])
def predict_t5_small():
    text = request.json['text']

    tokenizer = T5Tokenizer.from_pretrained('fine_tuned_t5_tokenizer')
    model = T5ForConditionalGeneration.from_pretrained('fine_tuned_t5')
    model.to('cuda')

    input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(
        input_ids,
        max_new_tokens=100,          
        num_beams=3,                 
        temperature=0.7,             
        top_p=0.85,                 
        repetition_penalty=3.0,      
        length_penalty=1.5,          
        early_stopping=True 
    )
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Generated Output:", decoded_output)

    def get_t5_embeddings(text):
        input_ids = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=256).input_ids.to("cuda")
        with torch.no_grad():
            embeddings = model.get_encoder()(input_ids).last_hidden_state
            mean_pooled = embeddings.mean(dim=1)
        return mean_pooled.cpu().numpy().squeeze()

    kw_model = KeyBERT()
    def extract_key_phrases(text):
        return [phrase for phrase, _ in kw_model.extract_keywords(text, top_n=10)]

    key_phrases = extract_key_phrases(text)

    phrase_embeddings = np.array([get_t5_embeddings(phrase) for phrase in key_phrases])

    num_clusters = 5
    clustering_model = AgglomerativeClustering(n_clusters=num_clusters)
    cluster_labels = clustering_model.fit_predict(phrase_embeddings)

    clusters = {i: [] for i in range(num_clusters)}
    for i, label in enumerate(cluster_labels):
        clusters[label].append(key_phrases[i])

    theme_representatives = []
    for cluster_id, phrases in clusters.items():
        cluster_embeddings = np.array([get_t5_embeddings(phrase) for phrase in phrases])
        cluster_centroid = cluster_embeddings.mean(axis=0)
        distances = np.linalg.norm(cluster_embeddings - cluster_centroid, axis=1)
        representative_idx = np.argmin(distances)
        theme_representatives.append(phrases[representative_idx])

    print("\nIdentified Themes:")
    for cluster_id, phrases in clusters.items():
        print(f"Theme {cluster_id + 1}: {phrases}")
        print(f"Representative for Theme {cluster_id + 1}: {theme_representatives[cluster_id]}")

    return jsonify({'output': decoded_output, 'themes': clusters, 'representatives': theme_representatives})

@app.route('/predict_t5_base', methods=['POST'])
def predict_t5_base():
    text = request.json['text']

    tokenizer = T5Tokenizer.from_pretrained('fine_tuned_t5_base_tokenizer')
    model = T5ForConditionalGeneration.from_pretrained('fine_tuned_t5_base')
    model.to('cuda')

    input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(
        input_ids,
        max_length=100,         
        num_beams=5,           
        repetition_penalty=3.0, 
        length_penalty=1.0,     
        top_k=50,               
        top_p=0.95,             
        early_stopping=True 
    )
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Generated Output:", decoded_output)

    def get_t5_base_embeddings(text):
        input_ids = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=256).input_ids.to("cuda")
        with torch.no_grad():
            embeddings = model.get_encoder()(input_ids).last_hidden_state
            mean_pooled = embeddings.mean(dim=1)
        return mean_pooled.cpu().numpy().squeeze()

    kw_model = KeyBERT()
    def extract_key_phrases(text):
        return [phrase for phrase, _ in kw_model.extract_keywords(text, top_n=10)]

    key_phrases = extract_key_phrases(text)

    phrase_embeddings = np.array([get_t5_base_embeddings(phrase) for phrase in key_phrases])

    num_clusters = 5
    clustering_model = AgglomerativeClustering(n_clusters=num_clusters)
    cluster_labels = clustering_model.fit_predict(phrase_embeddings)

    clusters = {i: [] for i in range(num_clusters)}
    for i, label in enumerate(cluster_labels):
        clusters[label].append(key_phrases[i])

    theme_representatives = []
    for cluster_id, phrases in clusters.items():
        cluster_embeddings = np.array([get_t5_base_embeddings(phrase) for phrase in phrases])
        cluster_centroid = cluster_embeddings.mean(axis=0)
        distances = np.linalg.norm(cluster_embeddings - cluster_centroid, axis=1)
        representative_idx = np.argmin(distances)
        theme_representatives.append(phrases[representative_idx])

    print("\nIdentified Themes:")
    for cluster_id, phrases in clusters.items():
        print(f"Theme {cluster_id + 1}: {phrases}")
        print(f"Representative for Theme {cluster_id + 1}: {theme_representatives[cluster_id]}")

    return jsonify({'output': decoded_output, 'themes': clusters, 'representatives': theme_representatives})


@app.route('/predict_gpt2', methods=['POST'])
def predict_gpt2():
    text = request.json['text']

    tokenizer = GPT2Tokenizer.from_pretrained('fine_tuned_gpt2_tokenizer')
    model = GPT2LMHeadModel.from_pretrained('fine_tuned_gpt2')

    model.to('cuda')

    input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(
        input_ids,
        max_new_tokens=100,         
        num_beams=3,               
        temperature=0.7,             
        top_p=0.85,                 
        repetition_penalty=3.0,      
        length_penalty=1.5,          
        early_stopping=True 
    )
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Generated Output:", decoded_output)

    def get_gpt2_embeddings(text):
        input_ids = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=256).input_ids.to("cuda")
        with torch.no_grad():
            embeddings = model.transformer(input_ids).last_hidden_state
            mean_pooled = embeddings.mean(dim=1)
        return mean_pooled.cpu().numpy().squeeze()

    kw_model = KeyBERT()
    def extract_key_phrases(text):
        return [phrase for phrase, _ in kw_model.extract_keywords(text, top_n=10)]

    key_phrases = extract_key_phrases(text)

    phrase_embeddings = np.array([get_gpt2_embeddings(phrase) for phrase in key_phrases])

    num_clusters = 5
    clustering_model = AgglomerativeClustering(n_clusters=num_clusters)
    cluster_labels = clustering_model.fit_predict(phrase_embeddings)

    clusters = {i: [] for i in range(num_clusters)}
    for i, label in enumerate(cluster_labels):
        clusters[label].append(key_phrases[i])

    theme_representatives = []
    for cluster_id, phrases in clusters.items():
        cluster_embeddings = np.array([get_gpt2_embeddings(phrase) for phrase in phrases])
        cluster_centroid = cluster_embeddings.mean(axis=0)
        distances = np.linalg.norm(cluster_embeddings - cluster_centroid, axis=1)
        representative_idx = np.argmin(distances)
        theme_representatives.append(phrases[representative_idx])

    print("\nIdentified Themes:")
    for cluster_id, phrases in clusters.items():
        print(f"Theme {cluster_id + 1}: {phrases}")
        print(f"Representative for Theme {cluster_id + 1}: {theme_representatives[cluster_id]}")

    return jsonify({'output': decoded_output, 'themes': clusters, 'representatives': theme_representatives})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
