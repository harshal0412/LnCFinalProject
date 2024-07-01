# sentiment_analyzer.py

class SentimentAnalyzer:
    word_weights = {
        "good": 1, "great": 2, "awesome": 3, "fantastic": 4, "amazing": 3, "love": 2, "like": 1, "liked": 2, "happy": 2, "wonderful": 3,
        "excellent": 3, "positive": 2, "joy": 2, "pleasure": 2, "delight": 2, "satisfying": 2, "best": 3, "beautiful": 2, "brilliant": 3,
        "charming": 2, "cheerful": 2, "delicious": 3, "elegant": 2, "enjoyable": 2, "fabulous": 3, "friendly": 2, "glorious": 3, "graceful": 2,
        "honest": 2, "impressive": 3, "kind": 2, "lovely": 2, "magnificent": 4, "marvelous": 3, "nice": 1, "outstanding": 4, "peaceful": 2,
        "perfect": 3, "pleasant": 2, "remarkable": 3, "spectacular": 4, "splendid": 3, "superb": 3, "terrific": 3, "thrilling": 3, "top": 2,
        "unique": 2, "valuable": 3, "vibrant": 2, "vivacious": 2, "wonder": 2, "wow": 3, "yes": 1, "zealous": 2, "can't complain": 2, "won't disappoint": 2,
        "bad": -1, "terrible": -2, "awful": -3, "horrible": -4, "hate": -3, "dislike": -1, "sad": -2, "poor": -1, "worst": -3, "negative": -2,
        "oily": -1, "boring": -2, "useless": -3, "disappointed": -2, "annoyed": -2, "unsatisfied": -2, "mediocre": -1, "ridiculous": -3,
        "abysmal": -3, "appalling": -3, "atrocious": -3, "cheap": -1, "crappy": -2, "crummy": -2, "dreadful": -3, "gross": -2, "horrendous": -4,
        "inferior": -2, "lousy": -2, "nasty": -2, "pathetic": -3, "poor": -1, "rotten": -2, "shoddy": -2, "sucky": -2, "substandard": -2,
        "terrible": -2, "unacceptable": -2, "unpleasant": -2, "worthless": -3, "wrong": -1, "yuck": -2, "no": -1, "dull": -2, "hurt": -2,
        "pain": -2, "mess": -2, "useless": -3, "fail": -2, "failure": -2, "faulty": -2, "forget": -1, "forgotten": -2, "gloomy": -2, "grim": -2,
        "hard": -1, "harm": -2, "hate": -3, "hideous": -3, "horrible": -4, "hurt": -2, "messy": -2, "miserable": -3, "offensive": -2, "painful": -2,
        "poor": -1, "rude": -2, "scary": -2, "shocking": -2, "stressful": -2, "tired": -1, "ugly": -2, "unhappy": -2, "unjust": -2, "upset": -2,
        "weak": -1, "weary": -1, "wicked": -2, "yucky": -2, "unforgiving": -3, "unforgivable": -3, "untrustworthy": -2, "vain": -2, "vicious": -2,
        "villainous": -3, "violent": -2, "vulgar": -2, "waste": -2, "wasted": -2, "wretched": -3, "don't": -2, "can't": -1, "won't": -2, "soggy": -1,
        "salty": -1, "bitter": -1, "sour": -1, "bland": -1, "bitterness": -1, "sourness": -1, "blandness": -1,
    }
    punctuation = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

    @classmethod
    def analyze_sentiment(cls, comment):
        comment = ''.join([char for char in comment if char not in cls.punctuation])
        comment = comment.lower()
        words = comment.split()
        sentiment_score = 0

        for word in words:
            if word in cls.word_weights:
                sentiment_score += cls.word_weights[word]

        for i, word in enumerate(words):
            if word == "not" and i + 1 < len(words) and words[i + 1] in cls.word_weights:
                sentiment_score -= 2 * cls.word_weights[words[i + 1]]

        return sentiment_score
