class LCP:
    def __init__(self, threshold) -> None:
        self.threshold = threshold
    def return_complex(self, sentence, words):
        output = []
        for word in words:
            # the function should go here
            if len(word) >= self.threshold:
                output.append(1)
            else:
                output.append(0)
        
        return output