from voicebox.speak import Voice

import subprocess

def piper_test():
    text = "Hello! This is Piper speaking."

    subprocess.run(
        [
            "piper",
            "--model",
            "piper-voices/en_US-lessac-medium.onnx",
            "--config",
            "piper-voices/en_US-lessac-medium.onnx.json",
            "--output_file",
            "voicebox/audio/speech.wav",
        ],
        input=text,
        text=True,
        check=True,
    )
def edge_tts_test():
    import asyncio
    import edge_tts

    async def speak():
        communicate = edge_tts.Communicate(
            "I am working",
            "en-US-AriaNeural"
        )
        await communicate.save("speech.mp3")

    asyncio.run(speak())
    
if __name__ in "__main__":
    voice = Voice()
    voice.say("I am working", change_perferred_tts="pyttsx")
    