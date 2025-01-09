from transformers import T5Tokenizer, T5ForConditionalGeneration

def predict_t5_small(text):
    tokenizer = T5Tokenizer.from_pretrained('fine-tuned-t5_tokenizer')
    model = T5ForConditionalGeneration.from_pretrained('fine-tuned-t5')

    model.to('cuda')

    # Tokenize the input
    input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cuda")  # Move to GPU if available

    # Generate output
    outputs = model.generate(
        input_ids,
        max_length=100,         # Allow for longer outputs if needed
        num_beams=10,           # Increase beams for more refined results
        repetition_penalty=2.0, # Penalize repetitive outputs
        length_penalty=2.0,     # Encourage longer outputs
        early_stopping=True
    )

    # Decode and print the output
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Generated Output:", decoded_output)

    return decoded_output

def predict_t5_base(text):
    tokenizer = T5Tokenizer.from_pretrained('fine-tuned-t5_base_tokenizer')
    model = T5ForConditionalGeneration.from_pretrained('fine-tuned-t5_base')

    model.to('cuda')

    # Tokenize the input
    input_ids = tokenizer(text, return_tensors="pt").input_ids.to("cuda")  # Move to GPU if available

    # Generate output
    outputs = model.generate(
        input_ids,
        max_length=100,         # Allow for longer outputs if needed
        num_beams=10,           # Increase beams for more refined results
        repetition_penalty=2.0, # Penalize repetitive outputs
        length_penalty=2.0,     # Encourage longer outputs
        early_stopping=True
    )

    # Decode and print the output
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Generated Output:", decoded_output)

    return decoded_output