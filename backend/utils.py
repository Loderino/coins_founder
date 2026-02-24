import cyrtranslit

def transcript(text: str) -> str:
    """
    Transcribes given text from Cyrillic to Latin alphabet, replaces some symbols and corrects some words.

    Args:
        text (str): Text to be transcripted.

    Returns:
        str: Transcripted text.
    """
    """"""
    transcripted = cyrtranslit.to_latin(text, 'ru')
    transcripted = transcripted.replace("'", "")
    transcripted = transcripted.replace("ejn", "eyn")
    transcripted = transcripted.replace("cz", "ts")
    transcripted = transcripted.replace("j", "y")
    transcripted = transcripted.replace(" ", "_")
    transcripted = transcripted.replace("-", "_")
    if transcripted == "Bahreyn":
        transcripted = "Bakhreyn"
    elif transcripted == "Kazahstan":
        transcripted = "Kazakhstan"
    elif transcripted.endswith("j"):
        transcripted = transcripted[:-1]+"y"
    return transcripted