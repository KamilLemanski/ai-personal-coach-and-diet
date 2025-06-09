🏋️‍♀️AI Trener Personalny + 🍎Dieta

Live App ➤ https://trener-presonalny-dieta-ai-kamil-lemanski.streamlit.app

AI Trener Personalny + Dieta to kompleksowa aplikacja webowa stworzona w Pythonie z wykorzystaniem frameworka Streamlit. Aplikacja generuje w pełni spersonalizowany plan treningowy i dietetyczny w mniej niż 30 sekund. Wykorzystuje zaawansowane modele sztucznej inteligencji, w tym przetwarzanie języka naturalnego (OpenAI GPT-4o) oraz model uczenia maszynowego (Random Forest Classifier), aby dostarczyć dostosowany do potrzeb użytkownika plan treningowy i dietę.

------------
✨ Właściwości:

🗓️ Generowanie kompleksowych planów treningowych i żywieniowych

⚡ Szybkość i Personalizacja (plan na podstawie szczegółowych danych użytkownika w czasie krótszym niż 30 sekund)

📈 Prognoza skuteczności (Wykorzystanie modelu ML do przewidywania skuteczności wygenerowanego planu)

📊 Obliczenia fizjologiczne (BMR, TDEE oraz dzienne zapotrzebowanie kaloryczne)

📄 Eksport do pliku PDF

🔒 Bezpieczeństwo danych (dane użytkownika nie są zapisywane, a klucz API OpenAI jest bezpiecznie używany)

-------------
🧪 Zastosowane technologie:

Python 3.8+

Streamlit

OpenAI GPT-4o

ML (Random Forest Classifier)

Pandas

LabelEncoder

PDFKit/wkhtmltopdf (do generowania plików PDF z HTML)

------------
👉 Uruchomienie aplikacji online:

https://trener-presonalny-dieta-ai-kamil-lemanski.streamlit.app

------------
📂 Folder structure:

ai-personal-coach-and-diet/

├── app.py                      # Główna logika aplikacji Streamlit

├── requirements.txt            # Biblioteki Pythona

├── packages.txt                # Zależności systemowe (wkhtmltopdf dla Streamlit Cloud)

├── model_rekomendacji.pkl      # Przetrenowany model uczenia maszynowego

├── label_encoders.pkl          # Obiekty LabelEncoder do kodowania danych tekstowych

├── Gemini_Generated...jpg      # Obrazek używany w aplikacji

├── dane_rekomendacyjne_500.csv # Sztucznie wygenerowane dane wejściowe

├── train_model.py              # Skrypt do trenowania modelu

└── README.md                   # Ten plik


------------
⚙️ Instalacja i uruchomienie aplikacji lokalnie:

1. Sklonuj repozytorium: https://github.com/KamilLemanski/ai-personal-coach-and-diet

2. Zainstaluj wymagane biblioteki: pip install -r requirements.txt

3. Zainstaluj wkhtmltopdf (niezbędne do generowania PDF): https://wkhtmltopdf.org/downloads.html

4. Skonfiguruj i dodaj swój klucz OpenAI

5. Uruchom aplikację: streamlit run main.py

------------
🔐 Zmienne środowiskowe:

Lokalnie: Ustaw zmienną środowiskową OPENAI_API_KEY w pliku .env: OPENAI_API_KEY=sk-...twój-klucz...

Streamlit: Użyj Streamlit Secrets w ustawieniach aplikacji.

------------
☁️ Deployment na platformie Streamlit Cloud:

1. Połącz swoje repozytorium GitHub ze Streamlit Cloud.
   
2. Upewnij się, że w repozytorium znajdują się następujące pliki: main.py, requirements.txt, packages.txt, model_rekomendacji.pkl, label_encoders.pkl
   
3. W ustawieniach aplikacji Streamlit Cloud, w sekcji "Secrets", dodaj swój klucz API OpenAI jako OPENAI_API_KEY.
   
4. Streamlit Cloud automatycznie zainstaluje zależności systemowe z packages.txt (wkhtmltopdf) oraz zależności Pythona z requirements.txt.
  
5.  Aplikacja zostanie uruchomiona pod wygenerowanym adresem URL.

------------
📌 Przykład użycia:

1. Wypełnij formularz, podając swoje dane, takie jak płeć, wiek, waga, wzrost, poziom aktywności, cel treningowy, preferencje, dostępność sprzętu i liczbę posiłków.

2. Kliknij przycisk "🚀 Generuj plan".

3. Aplikacja wygeneruje spersonalizowany plan treningowy, dietetyczny oraz obliczenia fizjologiczne.

4. Sprawdź prognozę skuteczności Twojego planu i przeczytaj przypisany do niej opis.

5. Kliknij "📄 Pobierz plan jako PDF", aby zapisać swój spersonalizowany plan.

------------
📝 Licencja:

© 2025 Kamil Lemański. Projekt edukacyjny i demonstracyjny.

------------
🙏 Credits:

OpenAI (GPT-4o), 
Streamlit Cloud, 
Scikit-learn,
wkhtmltopdf & PDFKit.
