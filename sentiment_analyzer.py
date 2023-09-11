import flet as ft
import os
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel
from google.cloud import speech
from google.cloud import texttospeech
#from google.colab import auth as google_auth
#google_auth.authenticate_user()
def main(page: ft.Page):
    vertexai.init(project="selvanlp-1542587147199", location="us-central1")
    parameters = {
#    "candidate_count": 1,
    "max_output_tokens": 256,
    "temperature": 0.1,
    "top_p": 0.8,
    "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison")
   
    page.title = "Eloquence by Selva Jagannathan"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def text_to_speech():
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=tb2.value)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Studio-O",)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16,speaking_rate=1)
        response = client.synthesize_speech(
                request={"input": input_text, "voice": voice, "audio_config": audio_config}
                )
#       response.audio_content
        print('Audio content requested"')
        audio1 = ft.Audio(
            src=response.audio_content,
            autoplay=True,
         )
        page.overlay.append(audio1)
        lambda _:audio1.play()
        lambda _:audio1.update()
        print("played")

    def speech_to_text(
        config: speech.RecognitionConfig,
        audio: speech.RecognitionAudio,
        ) -> speech.RecognizeResponse:
        client = speech.SpeechClient()

         # Synchronous speech recognition request
        response = client.recognize(config=config, audio=audio)
        print(response)


    def get_sentiment(e):
        call_bison(tb1.value)
        page.update()

    def call_bison(e):
       response = model.predict(
            """You are a native English speaker. Rephrase the input statement to sound more confident and grammatically correct."""+tb1.value
            ,**parameters)
       print(f"Response from Model: {response.text}")
       i=response.text
       tb2.value = i
       page.update()
       text_to_speech()

    startb = ft.IconButton(icon=ft.icons.AUDIOTRACK,icon_color="red400",icon_size=20,on_click=speech_to_text)
    tb1 = ft.TextField(label="You said")
    tb2 = ft.TextField(label="A native speaker would say this",read_only=True)
    def clear_fields(e):
        tb1.value = ""
        tb2.value = ""
        page.update()
    lb = ft.Text("Size 40, w100",
            size=40,
            color=ft.colors.GREEN,
#            bgcolor=ft.colors.BLUE_600,
            weight=ft.FontWeight.W_100,)
    lb.value = "Eloquence - Find the perfect words to express in English"
    clear_fields
    page.add(lb,startb,
        ft.Column(
            [
                tb1,
                tb2, 
                ft.FilledButton("Perfect me!", on_click=call_bison),
                ft.FilledButton("Clear Fields", on_click=clear_fields),
                ft.FilledButton("Play", on_click=text_to_speech)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=main, port=int(os.environ.get("PORT", 8080)), view = ft.AppView.WEB_BROWSER)
