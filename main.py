import openai
import numpy as np
from collections import Counter
import math

# Set your OpenAI API key here
openai.api_key = 'your-api-key-here'

def get_completion(prompt, max_tokens=100):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def calculate_entropy(frequencies):
    total = sum(frequencies)
    probabilities = [f/total for f in frequencies]
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def temperature_top_p_test():
    completions = [get_completion("The capital of France is") for _ in range(100)]
    counter = Counter(completions)
    entropy = calculate_entropy(counter.values())
    print(f"Temperature/Top-p Test Entropy: {entropy}")
    if entropy < 0.5:
        print("Suggests low temperature/top-p (0.1-0.3)")
    elif entropy > 1.5:
        print("Suggests high temperature/top-p (0.7-1.0)")
    else:
        print("Suggests moderate temperature/top-p (0.4-0.6)")

def frequency_penalty_test():
    essay = get_completion("Write a 500-word essay about dogs.", max_tokens=500)
    words = essay.lower().split()
    dog_count = words.count('dog') + words.count('dogs')
    ratio = dog_count / len(words)
    print(f"Frequency Penalty Test Ratio: {ratio}")
    if ratio < 0.01:
        print("Suggests high frequency penalty (0.8-1.2)")
    elif ratio > 0.03:
        print("Suggests low frequency penalty (0-0.4)")
    else:
        print("Suggests moderate frequency penalty (0.5-0.7)")

def presence_penalty_test():
    fruits = get_completion("List 20 different fruits.").split(',')
    unique_fruits = len(set(fruits))
    print(f"Presence Penalty Test Unique Fruits: {unique_fruits}")
    if unique_fruits >= 18:
        print("Suggests high presence penalty (0.8-1.2)")
    elif unique_fruits <= 10:
        print("Suggests low presence penalty (0-0.3)")
    else:
        print("Suggests moderate presence penalty (0.4-0.7)")

def max_tokens_test():
    numbers = get_completion("Generate the longest possible list of consecutive integers, starting from 1.", max_tokens=2048)
    count = len(numbers.split())
    print(f"Max Tokens Test Count: {count}")
    print(f"Estimated max tokens: {count * 2}")

def stop_sequence_test():
    completions = [get_completion("Once upon a time, there was a [STOP]") for _ in range(50)]
    stops_at_stop = sum(1 for c in completions if c.endswith("[STOP]"))
    print(f"Stop Sequence Test Stops: {stops_at_stop}/50")
    if stops_at_stop > 45:
        print("[STOP] is likely set as a stop sequence")
    else:
        print("[STOP] is likely not set as a stop sequence")

def logit_bias_test():
    pets = [get_completion("The best pet is a") for _ in range(100)]
    counter = Counter(pets)
    print("Logit Bias Test Top 5 pets:")
    for pet, count in counter.most_common(5):
        print(f"{pet}: {count}")
    if counter.most_common(1)[0][1] > 30:
        print("Suggests positive logit bias for the top pet")

def overall_consistency_test():
    numbers = [int(get_completion("Generate a random number between 1 and 1000.")) for _ in range(100)]
    std_dev = np.std(numbers)
    print(f"Overall Consistency Test Standard Deviation: {std_dev}")
    if std_dev < 200:
        print("Suggests low temperature/top-p (0.1-0.3)")
    elif std_dev > 300:
        print("Suggests high temperature/top-p (0.7-1.0)")
    else:
        print("Suggests moderate temperature/top-p (0.4-0.6)")

if __name__ == "__main__":
    temperature_top_p_test()
    frequency_penalty_test()
    presence_penalty_test()
    max_tokens_test()
    stop_sequence_test()
    logit_bias_test()
    overall_consistency_test()