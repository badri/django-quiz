class ScoreTamperedException(Exception):
    def __init__(self, quiz, quiz_id, score):
        self.quiz = quiz
        self.quiz_id = quiz_id
        self.score = score

    def __str__(self):
        return "Someone attempted to alter the score of quiz %s, id=%d to %d." % (self.quiz, self.quiz_id, self.score)
        
