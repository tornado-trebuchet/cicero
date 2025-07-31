import torch
from transformers import MarianMTModel, MarianTokenizer
from typing import Optional
from backend.domain.services.text.base_text_service import TextService
from backend.domain.models.text.e_text_clean import CleanText
from backend.domain.models.common.v_enums import LanguageEnum
from backend.domain.services.text.translator.serv_translator_dto import TranslatedTextDTO


class TranslateCleanText(TextService):
    clean_text: CleanText
    language_code: LanguageEnum
    model_name: str
    tokenizer: MarianTokenizer
    model: MarianMTModel
    device: torch.device

    def __init__(
        self, clean_text: CleanText, language_code: LanguageEnum, device: Optional[torch.device] = None
    ) -> None:
        super().__init__(config=None)
        self.clean_text = clean_text
        self.language_code = language_code

        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))

        # load tokenizer and model
        self.model_name = self._get_model_name()
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)  # type: ignore
        self.model = MarianMTModel.from_pretrained(self.model_name).to(self.device)  # type: ignore
        self.model.eval()

    def _get_model_name(self) -> str:
        lang_map = {
            LanguageEnum.FR: "Helsinki-NLP/opus-mt-en-fr",
            LanguageEnum.DE: "Helsinki-NLP/opus-mt-en-de",
        }
        name = lang_map.get(self.language_code)
        if not name:
            raise ValueError(f"No Marian model mapping for language {self.language_code}")
        return name

    def process(self) -> TranslatedTextDTO:
        # tokenize on CPU then move inputs to device
        inputs = self.tokenizer(
            [self.clean_text.text], return_tensors="pt", padding=True, truncation=True, max_length=512
        )
        inputs_on_device = {}
        for key, tensor in inputs.items():  # type: ignore
            inputs_on_device[key] = tensor.to(self.device)  # type: ignore
        inputs = inputs_on_device

        # generate on GPU
        with torch.no_grad():
            translated_ids = self.model.generate(**inputs)  # type: ignore

        # decode on CPU
        translation = self.tokenizer.decode(translated_ids[0].cpu(), skip_special_tokens=True)  # type: ignore
        return TranslatedTextDTO(translation=translation)
