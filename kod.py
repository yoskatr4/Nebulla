import cv2
import imp
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import random
import speech_recognition as sr
import sys
import time
import mediapipe as mp
import webbrowser
import numpy as np
import pyautogui

def yüz():              #Yüz tanımayı açıyoruz
    def change_pitch(sound, semitones):
        new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    tts = gTTS(text="Yüz algılama başlatılıyor", lang='tr')
    tts.save("Yüz_algılama.mp3")

    ses_dosyasi = AudioSegment.from_file("Yüz_algılama.mp3")
    ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)
    play(ses_dosyasi_changed_pitch)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            
            for (ex, ey, ew, eh) in eyes:
                center = (int(ex + ew/2), int(ey + eh/2))
                radius = int((ew + eh) / 4)
                cv2.circle(roi_color, center, radius, (0, 255, 0), 2)
        
        cv2.imshow('Face Detection', frame)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def şaka():         #Şaka oluşturucuyu açıyoruz
    def generate_joke(input_sentence):
        jokes = [
        "Neden tavuklar uçmaz? Kanatları var da ondan!",
        "Hangi kuş uçmaz? Koltuk!",
        "Adamın biri denize düşmüş, neden? Çünkü deniz kum istermiş!",
        "Hangi pil patlar? TORPİL!",
        "En çok karşıdan karşıya geçen kimdir? Dondurmacı!",
        "Hangi fare peynir yemez? Bilgisayar faresi!",
        "Temel arkadaşına demiş ki; benim bir gün karımı dünyanın en uzak yere göndereceğim. Nereye? İşe!",
        "Adamın biri güneşte yanmış, ay da düz!",
        "Hangi örtü masaya serilmez? Göz örtüsü!",
        "En çok hava alan ilimiz hangisidir? Kuşadası!",
        "Adamın biri gülmüş, saksılar düşmüş!",
        "Ay karanlık mı? Hayır, yer karanlık!",
        "Adamın biri denize düşmüş, karısı neden ağlamış? Elektrik faturası su almış!",
        "Hangi tasla su içilmez? Kafatasıyla!",
        "Hangi don durmaz? Jandarma!",
        "Adamın biri kızmış, neden? Tahterevalliyle!",
        "En hızlı yemek hangisidir? Hamburger!",
        "Bir elmanın yarısı neye benzer? Diğer yarısına!",
        "Adamın biri kırmızı tişörtlüymüş, ne olmuş? Domates!",
        "Hangi dağda çiçek yetişmez? Yanar dağda!",
        "Adamın biri dondurma yemiş, neden erimemiş? Donmuş!",
        "Temel'in kızı iğne yutmuş, neden? Babası delik olsun diye!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi fare resim yapar? Boya faresi!",
        "Hangi pil yakmaz? Aküpür!",
        "Hangi kuş uçmaz? Karakuş!",
        "Hangi kanun insanları yargılamaz? Gravitasyon kanunu!",
        "Bir fil neden bilgisayar kullanamaz? Fareler onu korkuttuğu için!",
        "Hangi fare ev yapar? Koli fare!",
        "Hangi nar ekşisidir? Şeftali ekşisi!",
        "Hangi ağaç denize düşmez? Çam ağacı!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi düğme dikilmez? Gömlek düğmesi!",
        "Hangi ilaç hiç acıtıcı değildir? Krem!",
        "Adamın biri dondurma yemiş, neden üzgün? Çünkü muhallebiyi görmüş!",
        "Bir gölün içinde ne yok? 'G' harfi!",
        "Hangi araba kör olur? Gözlüklü otobüs!",
        "Hangi araba üzgündür? Ağlıyormobil!",
        "Adamın biri denize düşmüş, neden boğulmamış? Çünkü olay yeri tatil beldesi imiş!",
        "Hangi ayı en yaşlıdır? Dünayı!",
        "Hangi kale tarihi bilir? Şato!",
        "Hangi yolda trafik kazası olmaz? Samanyolu!",
        "Hangi kedi su içmez? Kuru kedi!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi kalem silgiyi sevmez? Pilot kalem!",
        "Hangi ördekler uçarken ses çıkarmaz? Sessiz ördekler!",
        "Hangi kuşun eti yenmez? Kuş etmez!",
        "Hangi fare resim yapar? Boya faresi!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi ağaç tıraş olmaz? Dikdörtgen ağaç!",
        "Hangi yılan zehirsizdir? Dik yürüyen yılan!",
        "Hangi fare asla hasta olmaz? Sağlıkla!",
        "Hangi kalemle yazı yazılmaz? Kardan adamla!",
        "Hangi masada yemek yenmez? Ameliyat masası!",
        "Hangi yıldız gece ve gündüz görülür? Radyo yıldızı!",
        "Hangi bitki pazara gitmez? Pazar otu!",
        "Hangi telefonla konuşulmaz? Kırmızı telefonla!",
        "Hangi yolda trafik kazası olmaz? Samanyolu!",
        "Hangi at nalı düşmez? Sahte nal!",
        "Hangi kale sallanır? Mendil kalesi!",
        "Hangi dağda çiçek yetişmez? Yanar dağda!",
        "Hangi bankada para saklanmaz? Sazan bankada!",
        "Hangi dikiş dikilmez? Hamsi dikişi!",
        "Hangi kanun insanları yargılamaz? Gravitasyon kanunu!",
        "Hangi fare ağlayarak gider? Hüngür hüngür fare!",
        "Hangi ayakkabı bacaklarını kullanır? Terlik!",
        "Hangi saat doğruyu söyler? Kırık saat!",
        "Hangi fare peynir yapmaz? Bilgisayar faresi!",
        "Hangi ördekler uçarken ses çıkarmaz? Sessiz ördekler!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi ağaç denize düşmez? Çam ağacı!",
        "Hangi tahtada çizim yapılmaz? Diş tahtasında!",
        "Hangi kediler suda boğulmaz? Deniz kedisiii!",
        "Hangi dondurma sıçrar? Volcano dondurma!",
        "Hangi teneke kutuda yiyecek bulunmaz? Pencere teneke kutusunda!",
        "Hangi kedi suda boğulmaz? Deniz kedisiii!",
        "Hangi bahçede çiçek yetişmez? Sünger bahçesinde!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi fare yorulmaz? Pilli fare!",
        "Hangi fare kırmızı giyer? Kırmızı fare!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi kalemle yazı yazılmaz? Kardan adamla!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi futbol takımı korkutur? Korkuspor!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi balık yüzebilir? Karadeniz!",
        "Hangi kuş dondurma yer? Muhabbet kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi dondurma yerken kaşınmaz? Dondurma yenirken kaşınmaz!",
        "Hangi böcek savaşır? Cihangir!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi ağaç denize düşmez? Çam ağacı!",
        "Hangi kale sallanır? Mendil kalesi!",
        "Hangi bankada para saklanmaz? Sazan bankada!",
        "Hangi dondurma sıçrar? Volcano dondurma!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi balık yüzebilir? Karadeniz!",
        "Hangi kuş dondurma yer? Muhabbet kuşu!",
        "Hangi futbol takımı korkutur? Korkuspor!",
        "Hangi ağaç gözlük takar? Sığla!",
        "Hangi kuş ses çıkarmaz? Dilsiz kuş!",
        "Hangi hayvan bütün gün oturur? Koltuk!",
        "Hangi köyde deniz olur? Karpuzköy!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ay evimizin içinde kalır? Lale!",
        "Hangi yaprak soğuktur? Buz yaprağı!",
        "Hangi denizde su yoktur? Karadeniz!",
        "Hangi makasla kumaş kesilmez? Ameliyat makası!",
        "Bir vampir eczaneye girdi ve 'Kan grubum hangi rafa düşer? diye' sordu.",
        "Gece bekçisi sabaha kadar neden uyumamış? Çünkü gece nöbetindeydi!",
        "Gözlüklü hayalet ne yapar? Görünmez!",
        "Ölümsüz olmanın kötü tarafı ne? Sonsuz faturalar!",
        "Cadılar neden internet kullanamaz? Çünkü sihirli değil, sinyal zayıf!",
        "Zombi partiye neden gitmez? Herkesin ona yapışkan olduğunu düşünür.",
        "Dracula'nın sevdiği yemek nedir? Kan-yon makarnası!",
        "İntihar eden hayalet neden pişman oldu? Öteki tarafta korkunç bir kuyruk oluştu!",
        "Freddy Krueger neden bankaya gitmez? Rüyalarındaki kara günleri unutur!",
        "Korku filmi yönetmeni kız arkadaşına ne demiş? 'Seni seviyorum, ama senin yerine bir dublör düşünüyorum.'",
        "Ölümden sonra ne olur? Cenaze!",
        "Zombilere neden güvenilmez? Çünkü hep boş kafalılar!",
        "Kafası karışık vampir ne yapar? Düşüncelerini içer!",
        "Ölümsüzlük sırrı nedir? Yarım asır boyunca aynı kişiyi seçmemek!",
        "Dracula'nın en sevdiği dizi hangisi? Kan Bates Moteli!",
        "Hayaletler hangi otobüsü tercih eder? Görünmez otobüs!",
        "Cadılar neden radyo dinler? Daha fazla büyü hakkında bilgi edinmek için!",
        "Freddy Krueger neden telefon kullanamaz? Çünkü hep tuşları kaçırır!",
        "Neden mumyanlar asla yalan söylemez? Yalan söylerse sargıları çözülür!",
        "Gece yarısı en çok neye benzer? Görünmez bir jete!",
        "Vampirler neden sosyal medyada popüler? Çünkü beğenileri kanatsızdır!",
        "Cadılar neden süpürgeyle uçar? Bilet fiyatları uçakla gitmeye göre daha uygundur!",
        "Ölüler neden mezarlıkta mutlu olur? Çünkü yer altı daireleri sessizdir!",
        "Hayaletler neden asansör kullanmaz? Çünkü düğmeye basamazlar!",
        "Korku filmi canavarı spor yapınca ne yapar? Koşu-bandaj!",
        "Freddy Krueger hangi dili konuşur? Uyku dilini!",
        "Dracula hangi müzik türünü dinler? Rock'n'kan roll!",
        "Cadılar neden telefon alışverişi yapmaz? Çünkü sinyal süpürgesini alamazlar!",
        "Zombi sevgilisiyle neden ayrıldı? Kalbi atmıyordu, sadece yavaşça yürüyordu!",
        "Hayalet hangi ödülü kazandı? Saydam başarı ödülü!",
        "Korku filmi canavarı ne zaman gülümser? Kamera çekimde olduğunda!",
        "Vampirler neden pozitif düşünür? Çünkü negatif kan grubu yok!",
        "Cadılar neden sürekli grip olur? Çünkü sihirli değil, mikroplu!",
        "Ölüler neden dans etmekten hoşlanır? Çünkü kemikleri oynuyor!",
        "Zombi neden halı alışverişi yapar? Yeni beyni olmadığı için zemini hissedemez!",
        "Hayaletler neden tren kullanmaz? Raya dökülmek istemedikleri için!",
        "Freddy Krueger hangi yemekleri sever? Rüya tatlıları!",
        "Cadılar neden sürekli kitap okur? Bilgi büyüsü yapmak için!",
        "Vampirler neden borsada işlem yapmaz? Çünkü yatırımları kanla değil, kazançla ilgilenir!",
        "Zombi hangi dili konuşur? Çürükçe!",
        "Hayaletlerin en sevdiği tatil hangisi? Hallow-veeeen!",
        "Korku filmi canavarı hangi sporu yapmaz? Korku sporu!",
        "Vampirler neden araba kullanamaz? Ayakları debelenirken direksiyon tutamazlar!",
        "Cadılar neden sürekli sihirli değnek taşır? Cebinde acil durum büyüsü yapması için!",
        "Ölüler neden bilgisayar oyunu oynar? Kafaları boş olduğu için!",
        "Zombi hangi yarışmayı kazanamaz? Hız koşusu!",
        "Hayaletler neden sürekli çevreci? Çünkü geri dönüşümleri hep yapıyorlar!",
        "Freddy Krueger hangi kahveyi tercih eder? Kabuspresso!",
        "Cadılar neden sürekli gülümser? Dişleri hep sihirli beyazlatma büyüsü yapar!",
        "Vampirler neden market alışverişi yapmaz? Sadece kan ihtiyaçları vardır!",
        "Zombi hangi konuda uzmandır? Beyin yemek!",
        "Hayaletler neden asla dürüst olamaz? Hep perde arkasında saklanırlar!",
        "Korku filmi canavarı hangi takımı tutar? Korkuspor!",
        "Cadılar neden sürekli ruj sürer? Çünkü büyüleri dudaklarından yaparlar!",
        "Ölüler neden restoran açmaz? Çünkü menüde isimleri yerine numaraları yazarlar!",
        "Zombi hangi yazılım dili kullanır? Kod yem!",
        "Hayaletler neden bisiklet kullanmaz? Çünkü pedalları çiğnerler!",
        "Freddy Krueger hangi renkleri sever? Karabiber ve kan kırmızısı!",
        "Cadılar neden daima mutlu? Çünkü sihirli gülme büyüsü yaparlar!",
        "Vampirler neden tiyatroya gitmez? Kan grubu uyuşmazlığı nedeniyle!",
        "Zombi hangi spor ayakkabıları giyer? Çürükçüler!",
        "Hayaletler neden havaalanına gitmez? Check-in yapamazlar, sadece çıkış yapabilirler!",
        "Korku filmi canavarı neden internet kullanmaz? Çünkü hiçbir siteye izinsiz giremez!",
        "Cadılar neden sürekli güzellik kremleri kullanır? Genç kalmak için büyü yaparlar!",
        "Ölüler neden partilere gitmez? Çünkü çok solgun görünürler!",
        "Zombi hangi müzik türünü dinler? Death metal!",
        "Hayaletler neden gözlük kullanmaz? Hiçbir şeyi net göremedikleri için!",
        "Freddy Krueger hangi sporu yapmaz? Uyuma yarışı!",
        "Cadılar neden sürekli hava değiştirir? Sihirli havalandırma büyüsü yaparlar!",
        "Vampirler neden her zaman üşür? Kanları dondurulduğu için!",
        "Zombi hangi filmi izlemek ister? Beyin Olmazsa Olmaz!",
        "Hayaletler neden otostop yapmaz? Hiç kimse onları göremez!",
        "Korku filmi canavarı neden masa tenisi oynamaz? Top hep korkup kaçar!",
        "Cadılar neden sürekli ayna karşısında? Kendi büyüleyici yansımalarını görmek için!",
        "Ölüler neden yemek pişirmez? Çünkü tad alma yetenekleri kaybolmuştur!",
        "Zombi hangi yemekleri sever? Beyin mantarı çorbası!",
        "Hayaletler neden yazılım mühendisi olamaz? Kodları yazamazlar, sadece kodları yazarlar!",
        "Freddy Krueger hangi müzik enstrümanını çalmaz? Uykululu!",
        "Cadılar neden sürekli kedi besler? Onların da 9 canı olduğuna inandıkları için!",
        "Vampirler neden matematikte iyi? Onlar için sayılar kanları gibidir!",
        "Zombi hangi okulu bitirdi? Çürükler Üniversitesi!",
        "Hayaletler neden karikatür izlemez? Çünkü gölge karakterler yeterince korkutucu değildir!",
        "Korku filmi canavarı hangi müzik enstrümanını çalar? Korku-yun!",
        "Cadılar neden sürekli çiçek yetiştirir? Büyülü bahçe yapabilmek için!",
        "Ölüler neden parka gitmez? Onlar zaten hep solmuş görünür!",
        "Zombi hangi dergiyi okur? Çürüyüz Dergisi!",
        "Hayaletler neden sosyal medya kullanmaz? Çünkü kimse onların mesajlarını göremez!",
        "Freddy Krueger hangi bisikleti tercih eder? Kabus Bisikleti!",
        "Cadılar neden sürekli saatleri değiştirir? Zamana büyü yapabilmek için!",
        "Vampirler neden yoga yapar? Esnek olmak, daha iyi ısırabilmek içindir!",
        "Zombi hangi film karakterini örnek alır? Yürü Adam!",
        "Hayaletler neden karikatür izlemez? Çünkü gölge karakterler yeterince korkutucu değildir!",
        "Korku filmi canavarı hangi müzik enstrümanını çalar? Korku-yun!",
        "Cadılar neden sürekli çiçek yetiştirir? Büyülü bahçe yapabilmek için!",
        "Ölüler neden parka gitmez? Onlar zaten hep solmuş görünür!",
        "Zombi hangi dergiyi okur? Çürüyüz Dergisi!",
        "Hayaletler neden sosyal medya kullanmaz? Çünkü kimse onların mesajlarını göremez!",
        "Freddy Krueger hangi bisikleti tercih eder? Kabus Bisikleti!",
        "Cadılar neden sürekli saatleri değiştirir? Zamana büyü yapabilmek için!",
        "Vampirler neden bilgisayar oyunu oynar? Ekrandaki kanı hissetmek için!"
        "Hangi fare en büyük fare? Hamster!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi böcekler çok hızlı koşar? Yarım koşan böcekler!",
        "Hangi ilaç en tatlısıdır? Şurup!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi fare süt ister? Sütlü kahve fare!",
        "Hangi tavuk yumurtlayamaz? Erkek tavuk!",
        "Hangi biber süperdir? Süpermarket!",
        "Hangi kız silinmez? Tabiki dürüst kız!",
        "Hangi otobüs ünlüdür? Şöhret otobüsü!",
        "Hangi takı yemek yemez? Kolye!",
        "Hangi balık kara yolda yüzer? Karabatak!",
        "Hangi ağaç denize düşer? Muz ağacı!",
        "Hangi gemi kara yoluyla gider? Gemi kara yoluyla gitmez!",
        "Hangi kuş dondurma yemez? Vakvak kuşu!",
        "Hangi kuş takım elbise giyer? Karga!",
        "Hangi ahtapot en tehlikelisi? Çıtır ahtapot!",
        "Hangi takı takılmaz? İğne takı!",
        "Hangi karpuz ekşidir? Ekşi karpuz!",
        "Hangi takı takılmaz? Dikiş makası takı!",
        "Hangi saat en doğrusudur? Yelkovan!",
        "Hangi ayin içinde kalır? Lale!",
        "HACKLENDİN DOSTUM(şaka)",
        "HACKLENDİN DOSTUM(şaka)",
        "Hangi ampül yanmaz ap*(şaka)",
        "Hangi ampül yanmaz ap*(şaka)",
    ]
        
        random_joke = random.choice(jokes)
        return random_joke

    print("Şakalar tamamen yapay zeka tarafında raskele oluşturuldu")
    time.sleep(3)

    from gtts import gTTS
    from pydub import AudioSegment
    from pydub.playback import play
    import os

    def change_pitch(sound, semitones):
        # Örnekleme hızını semiton oranında değiştir
        new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    tts = gTTS(text="Enter tuşuna basın", lang='tr')
    tts.save("saka.mp3")  # Ses dosyasını kaydet
        
    # Ses dosyasını yükle ve çal
    ses_dosyasi = AudioSegment.from_file("saka.mp3")
    ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
    play(ses_dosyasi_changed_pitch)

    user_input = input("Enter tuşuna basın: ")


    for i in range(3):
        joke = generate_joke(user_input)
        print(f"{'-' * 20} Şaka {i + 1} {'-' * 20}")
        print("AI:", joke)

        # Şakayı ses olarak çal
        tts = gTTS(text=joke, lang='tr')
        tts.save("saka.mp3")  # Ses dosyasını kaydet
        
        # Ses dosyasını yükle ve çal
        ses_dosyasi = AudioSegment.from_file("saka.mp3")
        ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
        play(ses_dosyasi_changed_pitch)
        
    print("-" * 48)

def renkler():
    def change_pitch(sound, semitones):
        # Örnekleme hızını semiton oranında değiştir
        new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    tts = gTTS(text="Renk tanıma başlatılıyor", lang='tr')
    tts.save("renk.mp3")  # Ses dosyasını kaydet
        
    # Ses dosyasını yükle ve çal
    ses_dosyasi = AudioSegment.from_file("renk.mp3")
    ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
    play(ses_dosyasi_changed_pitch)
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Renkler : Beyaz, Kahverengi, Kırmızı, Mavi, Mor, Sarı, Turuncu, Yeşil\nNot:hangi renk tanımayı istiyorsanız o rengi söylemeniz yeterlisir")
        print("Sesli komut bekleniyor...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="tr-TR")  # Türkçe için tr-TR kullanabilirsiniz
            print("Algılanan komut:", command)

            if "beyaz" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

                tts = gTTS(text="Beyaz algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("beyaz.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("beyaz.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)

                print("Beyaz renk algılama başlatılıyor...")
                beyaz()
            elif "kahverengi" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

                tts = gTTS(text="Kahverengi algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Kahverengi.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Kahverengi.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Kahverengi renk algılama başlatılıyor...")
                kahverengi()
            elif "kırmızı" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

                tts = gTTS(text="Kırmızı algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Kırmızı.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Kırmızı.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Kırmızı renk algılama başlatılıyor...")
                kırmızı()
            elif "mavi" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

                tts = gTTS(text="Mavi algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Mavi.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Mavi.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Mavi renk algılama başlatılıyor...")
                mavi()
            elif "mor" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

                tts = gTTS(text="Mor algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Mor.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Mor.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Mor renk algılama başlatılıyor...")
                mor()
            elif "sarı" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                tts = gTTS(text="Sarı algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Sarı.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Sarı.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Sarı renk algılama başlatılıyor...")
                sarı()
            elif "turuncu" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                tts = gTTS(text="Turuncu algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Turuncu.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Turuncu.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Turuncu renk algılama başlatılıyor...")
                turuncu()
            elif "yeşil" in command:
                def change_pitch(sound, semitones):
                    # Örnekleme hızını semiton oranında değiştir
                    new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
                    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
                tts = gTTS(text="Yeşil algılama başlatılıyor lütfen bekleyiniz", lang='tr')
                tts.save("Yeşil.mp3")  # Ses dosyasını kaydet
                    
                # Ses dosyasını yükle ve çal
                ses_dosyasi = AudioSegment.from_file("Yeşil.mp3")
                ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
                play(ses_dosyasi_changed_pitch)
                print("Yeşil renk algılama başlatılıyor...")
                yeşil()


        except sr.UnknownValueError:
            print("Sesli komut anlaşılamadı.")
        except sr.RequestError:
            print("Sesli komut servisine erişilemiyor.")

def yeşil():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 100, 100])  # Yeşil rengin HSV değerleri
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('Green Color Detection', res)

        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def turuncu():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_orange = np.array([11, 150, 100])
        upper_orange = np.array([20, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_orange, upper_orange)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('Orange Color Detection', res)

        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def sarı():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Yeşil renk aralığı
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        green_res = cv2.bitwise_and(frame, frame, mask=green_mask)

        # Mavi renk aralığı
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)

        # Sarı renk aralığı
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_res = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # Yeşil ve mavi renklerin kombinasyonu
        combined_res = cv2.addWeighted(green_res, 1, blue_res, 1, 0)

        # Tüm renklerin kombinasyonu
        combined_res = cv2.addWeighted(combined_res, 1, yellow_res, 1, 0)

        cv2.imshow('Color Detection', combined_res)

        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def mor():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([35, 100, 100])  # Yeşil rengin HSV değerleri
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('Green Color Detection', res)

        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def mavi():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Yeşil renk aralığı
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        green_res = cv2.bitwise_and(frame, frame, mask=green_mask)

        # Mavi renk aralığı
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)

        combined_res = cv2.addWeighted(green_res, 1, blue_res, 1, 0)

        cv2.imshow('Color Detection', combined_res)

        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def beyaz():
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 30, 255])
            mask = cv2.inRange(hsv_frame, lower_white, upper_white)

            res = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow('White Color Detection', res)

            # ESC tuşuna basılınca çık
            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    
def kahverengi():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Yeşil renk aralığı
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        green_res = cv2.bitwise_and(frame, frame, mask=green_mask)

        # Mavi renk aralığı
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([140, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)

        # Sarı renk aralığı
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        yellow_res = cv2.bitwise_and(frame, frame, mask=yellow_mask)

        # Kırmızı renk aralığı
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([20, 255, 255])
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        red_res = cv2.bitwise_and(frame, frame, mask=red_mask)

        # Yeşil, mavi, sarı ve kırmızı renklerin kombinasyonu (kahverengi algılama)
        brown_res = cv2.addWeighted(green_res, 1, blue_res, 1, 0)
        brown_res = cv2.addWeighted(brown_res, 1, yellow_res, 1, 0)
        brown_res = cv2.addWeighted(brown_res, 1, red_res, 1, 0)

        cv2.imshow('Color Detection', brown_res)

        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def kırmızı():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv_frame, lower_red, upper_red)
        
        lower_red_dark = np.array([170, 50, 50])
        upper_red_dark = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv_frame, lower_red_dark, upper_red_dark)
        
        mask_final = mask1 + mask2
        res = cv2.bitwise_and(frame, frame, mask=mask_final)
        
        cv2.imshow('Red Color Detection', res)
        
        # ESC tuşuna basılınca çık
        if cv2.waitKey(5) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()

def parmak():
    def change_pitch(sound, semitones):
        # Örnekleme hızını semiton oranında değiştir
        new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    tts = gTTS(text="El ile uygulama açma başlatılıyor lütfen bekleyiniz", lang='tr')
    tts.save("parmak.mp3")  # Ses dosyasını kaydet

    ses_dosyasi = AudioSegment.from_file("parmak.mp3")
    ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
    play(ses_dosyasi_changed_pitch)
    print("El ile uygulama açma başlatılıyor...")
    time.sleep(3)
    print("100-100 kordinatları üst kutucuk \n100-200 kordinatları ortadaki kurucuk \n100-300 kordinatları alt kutucuk")
    time.sleep(3)
    print("Pamağınızı hangi kurucuğa götürürseniz o kutucuk için yazdığınız uygulama açılır\n (Unutmyın uygulamanın ismini tam ve doğru yazmalısınız)")
    time.sleep(5)

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Kamerayı aç
    cap = cv2.VideoCapture(0)

    # El tespiti için Mediapipe Hands modelini yükle
    with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:

        # İlgili uygulamaların pozisyon ve ad bilgilerini saklayan bir sözlük
        apps = {
            (100, 100, 150, 150): None,
            (100, 200, 150, 250): None,
            (100, 300, 150, 350): None
        }

        for (x_min, y_min, x_max, y_max), _ in apps.items():
            app_name = input(f"Lütfen {x_min}-{y_min} koordinatları arasında açmak istediğiniz uygulamanın adını girin: ")
            apps[(x_min, y_min, x_max, y_max)] = app_name

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Kamera açılamadı")
                break

            # Görüntüyü BGR den RGB ye dönüştür
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Yükseklik ve genişlik değerlerini al
            height, width, _ = image.shape
            # El tespiti yap
            results = hands.process(image)

            active_app = None  # Şu anki aktif uygulama

            if results.multi_hand_landmarks:
                # Her bir el için
                for hand_landmarks in results.multi_hand_landmarks:
                    # İşaret parmağı noktasını al
                    index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    # İşaret parmağı noktasının konumunu piksel cinsinden hesapla
                    x, y = int(index_finger_landmark.x * width), int(index_finger_landmark.y * height)
                    # Yeşil bir daire çiz
                    cv2.circle(image, (x, y), 10, (0, 255, 0), -1)

                    # İlgili uygulamaların pozisyonlarına göre işlem yap
                    for (x_min, y_min, x_max, y_max), app_name in apps.items():
                        if x_min < x < x_max and y_min < y < y_max and app_name:
                            active_app = app_name
                            break

            # Eğer aktif bir uygulama varsa, ilgili uygulamayı aç
            if active_app:
                webbrowser.open(active_app)
                active_app = None

            # Uygulama alanlarını çizdir
            for (x_min, y_min, x_max, y_max), _ in apps.items():
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Görüntüyü göster
            cv2.imshow('Mediapipe Hands', image)

            # ESC tuşuna basılınca çık
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

def fare():
    def change_pitch(sound, semitones):
        # Örnekleme hızını semiton oranında değiştir
        new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    tts = gTTS(text="El ile fare kontrolü başlatılıyor lütfen bekleyiniz", lang='tr')
    tts.save("fare.mp3")  # Ses dosyasını kaydet

    ses_dosyasi = AudioSegment.from_file("fare.mp3")
    ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
    play(ses_dosyasi_changed_pitch)
    print("El ile fare kontrolü başlatılıyor...")

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    # Kamerayı aç
    cap = cv2.VideoCapture(0)

    # El tespiti için Mediapipe Hands modelini yükle
    with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7) as hands:
        
        # Hareketi kaydetmek için bir değişken oluştur
        move_x = 0
        move_y = 0
        
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Kamera açılamadı")
                break
            
            # Görüntüyü BGR den RGB ye dönüştür
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Yükseklik ve genişlik değerlerini al
            height, width, _ = image.shape
            # El tespiti yap
            results = hands.process(image)
            
            # Eğer el tespit edildiyse
            if results.multi_hand_landmarks:
                # Her bir el için
                for hand_landmarks in results.multi_hand_landmarks:
                    # İşaret parmağı noktasını al
                    index_finger_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    # İşaret parmağı noktasının konumunu piksel cinsinden hesapla
                    x, y = int(index_finger_landmark.x * width), int(index_finger_landmark.y * height)
                    # Yeşil bir daire çiz
                    cv2.circle(image, (x, y), 10, (0, 255, 0), -1)
                    
                    # Mouse hareketini hesapla
                    move_x = (x - (width // 2)) // 10
                    move_y = ((height // 2) - y) // 10
                    
                    # Mouse hareketini uygula
                    pyautogui.moveRel(move_x, move_y, duration=0.1)
                    
            # Görüntüyü göster
            cv2.imshow('Mediapipe Hands', image)
            
            # ESC tuşuna basılınca çık
            if cv2.waitKey(5) & 0xFF == 27:
                break

        # Hareketi geri al
        pyautogui.moveRel(-move_x, -move_y, duration=0.1)

    cap.release()
    cv2.destroyAllWindows()

def main():

    recognizer = sr.Recognizer()
    def change_pitch(sound, semitones):
        # Örnekleme hızını semiton oranında değiştir
        new_sample_rate = int(sound.frame_rate * (5 ** (semitones / 12.0)))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    tts = gTTS(text="Program başlatıldı sesli komut bekleniyor", lang='tr')
    tts.save("main.mp3")  # Ses dosyasını kaydet
                    
    # Ses dosyasını yükle ve çal
    ses_dosyasi = AudioSegment.from_file("main.mp3")
    ses_dosyasi_changed_pitch = change_pitch(ses_dosyasi, semitones=3)  # Örnek olarak tonu 2 yarıton artır
    play(ses_dosyasi_changed_pitch)

    with sr.Microphone() as source:
        print("Sesli komut bekleniyor...")
        print("fare : El ile fare kontrolü \nrenk tanıma : Renk tanıma programını açar \nşaka : Şaka yapma programını açar \nel ile uygulama : El ile uygulama açar \n")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="tr-TR")  # Türkçe için tr-TR kullanabilirsiniz
            print("Algılanan komut:", command)

            if "fare" in command:
                print("El ile fare kntrolü başlatılıyor...")
                fare()
                
            
            elif "renk tanıma" in command:
                print("Renk algılama başlatılıyor...")
                renkler()

            elif "yüz tanıma" in command:
                print("Yüz algılama başlatılıyor...")
                yüz()
                
            elif "şaka" in command:
                print("Şaka programı başlatılıyor...")
                şaka()
            
            elif "el ile uygulama" in command:
                print("El ile uygulama açma başlatılıyor...")
                parmak()

            elif "fare" in command:
                print("El ile fare kontrolü başlatılıyor...")

            else:
                print("Böyle bir komut yok.")

        except sr.UnknownValueError:
            print("Sesli komut anlaşılamadı.")
        except sr.RequestError:
            print("Sesli komut servisine erişilemiyor.")

if __name__ == "__main__":
    main()

