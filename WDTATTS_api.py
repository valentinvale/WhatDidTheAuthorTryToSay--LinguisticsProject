from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, request, jsonify
from flask_cors import CORS

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

    return jsonify({'output': decoded_output})

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

    return jsonify({'output': decoded_output})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
