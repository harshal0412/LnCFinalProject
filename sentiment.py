from google.cloud import language_v1

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return sentiment.score, sentiment.magnitude

text = "sambhar was good but idly was raw inside."
score, magnitude = analyze_sentiment(text)
print(f"Sentiment score: {score}, Sentiment magnitude: {magnitude}")


