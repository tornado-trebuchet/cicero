
class TranslateCleanText(TextService):
    def __init__(self, clean_text, language_code=None):
        self.clean_text = clean_text
        self.language_code = language_code
        super().__init__(config=None)


    def process(self):



        return TranslatedTextDTO(translation)