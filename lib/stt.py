import dialogflow

def detect_intent_audio(project_id, session_id, audio_file_path, language_code):
    import dialogflow_v2 as dialogflow

    session_client = dialogflow.SessionsClient()
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_FLAC
    sample_rate_hertz = 44100
    session = session_client.session_path(project_id, session_id)

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)

    return {
   		"query": response.query_result.query_text,
      "intent": response.query_result.intent.display_name,
      "confidence": response.query_result.intent_detection_confidence,
    }
