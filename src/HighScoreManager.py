import os

def read_high_scores(file_name):
    """Reads the top 10 high scores from a file."""
    if not os.path.exists(file_name):
        return []

    with open(file_name, "r") as file:
        scores = [int(line.strip()) for line in file.readlines()]
    
    return scores

def write_high_score(new_score, file_name):
    """Writes a new score to the file if it's in the top 10."""
    scores = read_high_scores(file_name)
    if len(scores) < 10 or new_score > min(scores):
        scores.append(new_score)
        scores = sorted(scores, reverse=True)[:10]  # Keep top 10 scores

        with open(file_name, "w") as file:
            for score in scores:
                file.write(f"{score}\n")