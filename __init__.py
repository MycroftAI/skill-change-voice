# Copyright 2021, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

VOICE_NORM = {
    "alan": "apope",
    "pope": "apope",
    "alan pope": "apope",
    "british male": "apope",
    "cori": "cori_samuel",
    "cori samuel": "cori_samuel",
    "british female": "cori_samuel",
    "american female": "amy",
    "american male": "kusal",
}

VOICE_SELECTION = ["british male", "british female", "american male", "american female"]


class ChangeVoiceSkill(MycroftSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._last_voice = ""

    def initialize(self):
        self.register_entity_file("voice.entity")
        self.bus.on("mycroft.tts.voice-changed", self.handle_voice_changed)

    @intent_handler("change-voice.intent")
    def handle_change_voice(self, message):
        voice = message.data.get("voice")

        if not voice:
            voice = self.ask_selection(
                VOICE_SELECTION,
            )

        self._change_voice(voice)

    def _change_voice(self, voice: str):
        if not voice:
            self.speak("I don't recognize that voice")
            return

        self._last_voice = voice
        voice_norm = VOICE_NORM.get(voice, voice)

        LOG.info("Changing voice to %s", voice_norm)
        self.speak("Changing voice")
        self.bus.emit(Message("mycroft.tts.change-voice", data={"voice": voice_norm}))

    def handle_voice_changed(self, message):
        self.speak(f"Voice has now been changed to {self._last_voice}")

    def shutdown(self):
        self.bus.remove("mycroft.tts.voice-changed", self.handle_voice_changed)


def create_skill():
    return ChangeVoiceSkill()
