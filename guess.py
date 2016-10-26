class GuessError(RuntimeError):
    pass

class Guess:
    def __init__(self, initial_guess):
        self.data = [{'guess': initial_guess}]

    def expand(self, old_guess, new_guess, question, answer_for_new):
        old_guess_id = self._get_guess_id(old_guess)
        if old_guess_id is None:
            raise GuessError(old_guess+ ' is unknown.')
        if self._get_guess_id(new_guess) is not None:
            raise GuessError(new_guess+ ' is already known.')
        last_index = len(self.data)
        if answer_for_new:
            self.data.append({'guess': new_guess})
            self.data.append({'guess': old_guess})
        else:
            self.data.append({'guess': old_guess})
            self.data.append({'guess': new_guess})
        self.data[old_guess_id] = {'question': question, 'yes': last_index, 'no': last_index + 1}

    def get_question(self, id=0):
        return self.data[id].get('question')

    def get_guess(self, id=0):
        return self.data[id].get('guess')

    def answer_question(self, answer, id=0):
        if answer:
            new_id = self.data[id].get('yes')
        else:
            new_id = self.data[id].get('no')
        if new_id is None:
            raise GuessError('Not a question')
        return new_id

    def _get_guess_id(self, guess):
        for i in range(len(self.data)):
            if self.data[i].get('guess') == guess:
                return i
        return None
