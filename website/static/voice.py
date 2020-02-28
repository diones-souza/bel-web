# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 08:31:41 2018

@author: John
"""
from gtts import gTTS
class Voice:
    def SetVoice(sentence):
        try:
            voz = gTTS(sentence, lang ='pt')
            voz.save('website/static/website/audio/voice.mp3')
        except Exception:
            print('Permissao negada: "website/static/website/audio/voice.mp3"')