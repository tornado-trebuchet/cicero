class ProtocolText:

    def __init__(self, protocol_text: str = ""):
        self._protocol_text = protocol_text if protocol_text is not None else ""

    def __repr__(self):
        return f"ProtocolText({self._protocol_text})"
    
    @property
    def protocol_text(self) -> str:
        return self._protocol_text
    
    @protocol_text.setter
    def protocol_text(self, value: str):
        self._protocol_text = value if value is not None else ""

    def unique_character_list(self) -> list[str]:
        return list(set(self._protocol_text))