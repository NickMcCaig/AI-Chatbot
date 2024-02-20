import csv

# Load sentiment scores from CSV file into a dictionary
sentiment_scores = {}
with open('sentiment.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    for row in reader:
        sentiment_scores[row[0]] = float(row[1])

# Load emphasis words and their scores from CSV file into a dictionary
emphasis_scores = {}
with open('emphasis.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    for row in reader:
        emphasis_scores[row[0]] = float(row[1])

# Define function to calculate sentiment score
def calculate_sentiment(text):
    words = text.lower().split()
    sentiment_score = 0
    negation = False
    
    for i in range(len(words)):
        # Check for negation words
        if words[i] in ['not', 'no', 'never', 'none', 'neither', 'nor']:
            negation = True
        # Check for sentiment words
        elif words[i] in sentiment_scores:
            sentiment_word = words[i]
            emphasis_word = None
            if i > 0 and words[i-1] in emphasis_scores:
                emphasis_word = words[i-1]
            elif i > 1 and words[i-2] in emphasis_scores:
                emphasis_word = words[i-2]
            if emphasis_word:
                sentiment_score += sentiment_scores[sentiment_word] * emphasis_scores[emphasis_word]
            else:
                sentiment_score += sentiment_scores[sentiment_word]
            # Apply negation if present
            if negation:
                sentiment_score *= -1
                negation = False
                
        # Check for emphasis words
        elif words[i] in emphasis_scores:
            emphasis_word = words[i]
            # Check for preceding sentiment words to apply emphasis
            for j in range(i-1, max(i-6, -1), -1):
                if words[j] in sentiment_scores:
                    sentiment_score += emphasis_scores[emphasis_word] * sentiment_scores[words[j]]
                    break
        # Check if the current word ends in an exclamation point
        if words[i][-1] == '!':
            # If so, increase the emphasis score for any preceding words
            for j in range(max(i-5, 0), i):
                if words[j] in emphasis_scores:
                    sentiment_score *= 1.1

    return sentiment_score
def store_comment(comment, number, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([comment, number])