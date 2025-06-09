import streamlit as st
from openai import OpenAI
import datetime
from xhtml2pdf import pisa
from io import BytesIO
import pickle
import pandas as pd
import base64
import re
from PIL import Image

# --- GŁÓWNY INTERFEJS ---
# Podział aplikacja na dwie kolumny: lewa (30%) i prawa (70%).
# Aplikacja zajmuje całą stronę przeglądarki, bez duych marginesów.
# st.set_page_config() musi być piewszą komendą Streamlit.
st.set_page_config(layout="wide")

# --- CUSTOMOWE TŁO ---
st.markdown(
    """
    <style>
    body {
        background-color: #e6ffe6; /* Light green background */
    }
    .stApp {
        background-color: #e6ffe6; /* Ensures the Streamlit app container also has the background color */
    }
    /* The previous CSS selector for justification was unstable.
       We will now apply justification directly within the markdown content. */
    </style>
    """,
    unsafe_allow_html=True
)

# --- CONFIG ---
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- ŁADOWANIE MODELU ML ---
# Ta funkcja ładuje przetrenowany model i koduje dane tekstowe. 
# Komenda @st.cache_resource zapewnia, że model ładuje się tylko jeden raz.
@st.cache_resource
def load_model():
    try:
        with open("model_rekomendacji.pkl", "rb") as f:
            model = pickle.load(f)
        with open("label_encoders.pkl", "rb") as f:
            encoders = pickle.load(f)
        return model, encoders
    except FileNotFoundError:
        st.error("Nie znaleziono plików modelu ('model_rekomendacji.pkl' lub 'label_encoders.pkl'). Upewnij się, że znajdują się w tym samym folderze co aplikacja.")
        return None, None

model, encoders = load_model()

# Zainicjuj zmienne stanu sesji, jeśli nie istnieją
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False
if 'intro_content' not in st.session_state:
    st.session_state.intro_content = ""
if 'training_content' not in st.session_state:
    st.session_state.training_content = ""
if 'diet_content' not in st.session_state:
    st.session_state.diet_content = ""
if 'metrics_content' not in st.session_state:
    st.session_state.metrics_content = ""
if 'skutecznosc_planu' not in st.session_state:
    st.session_state.skutecznosc_planu = ""
if 'result_for_pdf' not in st.session_state:
    st.session_state.result_for_pdf = ""

main_col1, main_col2 = st.columns([0.3, 0.7]) # 30% for left, 70% for right

with main_col1:
    # --- GRAFIKA ---
    # Poniższy kod ładuje i wyświetla obraz.
    # Upewnij się, że plik „Gemini_Generated_Image_schdyhschdyhschd.jpg” znajduje się w tym samym folderze.
    try:
        image = Image.open('Gemini_Generated_Image_schdyhschdyhschd.jpg') 
        st.image(image, use_container_width=True) 
    except FileNotFoundError:
        st.warning("Nie można załadować obrazka. Upewnij się, że plik 'Gemini_Generated_Image_schdyhschdyhschd.jpg' jest w głównym folderze aplikacji.")

    # --- TEKST WSTĘPNY (z wbudowanym CSS do justowania tekstu w lewej kolumnie) ---
    st.markdown(
        """
        <div style="text-align: justify;">
        Aplikacja 🏋️‍♀️AI Trener Personalny + 🍎Dieta to kompleksowe narzędzie stworzone w języku Python z wykorzystaniem frameworka Streamlit. Bazuje na sztucznej inteligencji, wykorzystując:

        * przetwarzanie języka naturalnego (OpenAI GPT-4o),
        * model uczenia maszynowego (Random Forest Classifier),
        * narzędzie do kodowania danych tekstowych (LabelEncoder),
        * bibliotekę pandas do pracy z danymi w języku Python.

        Aplikacja generuje w pełni spersonalizowany plan treningowy i dietetyczny w czasie krótszym niż 30 sekund. Plan tworzony jest na podstawie szczegółowego promptu NLP, modelu GPT-4o oraz przyjaznego interfejsu użytkownika, który wyświetla odpowiedź w postaci trzech odrębnych sekcji:
        * TYGODNIOWY PLAN TRENINGOWY,
        * PLAN ŻYWIENIOWY,
        * OBLICZENIA FIZJOLOGICZNE.
        
        Wygenerowany plan zawiera również prognozę skuteczności, obliczoną na podstawie wytrenowanego modelu ML. Na potrzeby aplikacji stworzono syntetyczny zbiór danych zawierający 500 przykładów różnych kombinacji cech użytkowników: płci, wieku, wagi, wzrostu, poziomu aktywności, celu treningowego, preferowanej formy treningu, dostępności sprzętu oraz liczby posiłków. Dla każdej kombinacji przypisano etykietę „Skuteczność planu”, która posłużyła jako cel predykcyjny podczas treningu modelu. Model Random Forest nauczył się rozpoznawać zależności między tymi cechami a poziomem skuteczności, klasyfikując plan jako: wysoko, średnio lub nisko skuteczny.

        Aplikacja umożliwia również wygenerowanie i pobranie pliku PDF z kompletnym planem. Kod HTML PDF-a został zaprojektowany tak, aby plik był estetyczny i gotowy do druku.
        
        AI Trener Personalny + Dieta to narzędzie bezpieczne — dane użytkownika nie są zapisywane ani przechowywane, klucz API OpenAI nie jest przechowywany w repozytorium, a aplikację można uruchamiać zarówno lokalnie, jak i online.

        Kamil Lemański 2025©
        </div>
        """,
        unsafe_allow_html=True
    )


with main_col2:
    # --- UI ---
    st.title("🏋️‍♀️AI Trener Personalny + 🍎Dieta")

    with st.form("user_data"):
        st.markdown("**Wprowadź swoje dane, aby otrzymać spersonalizowany plan.**")
        gender = st.selectbox("Płeć", ["Mężczyzna", "Kobieta"])
        age = st.number_input("Wiek", min_value=13, max_value=100, step=1, value=30)
        weight = st.number_input("Waga (kg)", min_value=30.0, max_value=200.0, step=0.5, value=70.0)
        height = st.number_input("Wzrost (cm)", min_value=100, max_value=250, step=1, value=175)
        activity = st.selectbox("Poziom aktywności fizycznej", ["niski", "średni", "wysoki"])
        goal = st.selectbox("Cel", [
            "redukcja tkanki tłuszczowej", "budowa masy mięśniowej", "poprawa wydolności",
            "zwiększenie sprawności organizmu", "zwiększenie siły",
            "poprawa zakresu ruchu", "rehabilitacja po urazach"])
        training_pref = st.selectbox("Preferencje treningowe", [
            "trening siłowy", "cardio", "trening funkcjonalny", "trening obwodowy",
            "crossfit", "fitness", "kalistenika", "pilates", "joga", "bieganie",
            "rower", "spacery"])
        equipment = st.radio("Dostęp do sprzętu?", ["tak", "nie"], horizontal=True)
        meals = st.selectbox("Liczba posiłków dziennie", [3, 4, 5])
        submit = st.form_submit_button("🚀 Generuj plan")

    # --- AI PROMPT ---
    # Ta funkcja tworzy szczegółowy prompt dla modelu GPT na podstawie danych użytkownika.
    def build_prompt():
        return f"""
    Jesteś profesjonalnym trenerem personalnym oraz dietetykiem klinicznym z wieloletnim doświadczeniem. Twoim zadaniem jest stworzenie w pełni spersonalizowanego, realistycznego i profesjonalnego planu.

    Na podstawie poniższych danych użytkownika:
    - określ jego poziom zaawansowania,
    - wygeneruj kompletny plan składający się z 3 poniższych sekcji.

    1. Tygodniowy plan treningowy:
        - Przypisz konkretne dni tygodnia do sesji treningowych.
        - Dla treningu siłowego podaj konkretne ćwiczenia, liczbę serii i powtórzeń.
        - Określ czas trwania każdej aktywności (np. 45–60 minut).
        - Uwzględnij rozgrzewkę, ćwiczenia główne i rozciąganie.
        - Dopasuj plan do dostępności sprzętu i preferencji użytkownika.
        - Zapewnij progresję i balans między wysiłkiem a regeneracją.

    2. Plan żywieniowy – jadłospis dzienny:
        - Ustal dzienny bilans kaloryczny i rozkład makroskładników.
        - Umieść nagłówek "Przykładowy dzień jedzenia:".
        - Dodaj wiersz podsumowujący makroskładniki: Makroskładniki: XXXXkcal, Białko: XXXg, Tłuszcze: XXg, Węglowodany: XXXg.
        - Zaproponuj menu z {meals} posiłków.
        - Wymień nazwy, składniki, ilości i zamienniki.

    3. Obliczenia fizjologiczne:
        - Oblicz BMR (Basal Metabolic Rate) wzorem Mifflina-St Jeora.
        - Oblicz TDEE (Total Daily Energy Expenditure).
        - Określ dzienne zapotrzebowanie kaloryczne dostosowane do celu.
        - Na końcu dodaj profesjonalne wyjaśnienie (200–300 słów) o BMR, TDEE i ich interpretacji.

    INSTRUKCJE FORMATOWANIA ODPOWIEDZI:
    - Nie używaj znaków formatowania Markdown, takich jak # czy *.
    - Rozpocznij od krótkiego, motywującego akapitu wprowadzającego.
    - Użyj DOKŁADNIE tych 3 tytułów sekcji: 🔸 TYGODNIOWY PLAN TRENINGOWY, 🔸 PLAN ŻYWIENIOWY, 🔸 OBLICZENIA FIZJOLOGICZNE.
    - Każdy z tych tytułów musi pojawić się w odpowiedzi tylko raz.
    - Zadbaj o estetyczny i przejrzysty układ tekstu z równymi wcięciami.

    DANE UŻYTKOWNIKA:
    Płeć: {gender}
    Wiek: {age}
    Waga: {weight} kg
    Wzrost: {height} cm
    Aktywność: {activity}
    Cel: {goal}
    Trening: {training_pref}
    Sprzęt: {equipment}
    Posiłki dziennie: {meals}
    """

    # --- Rekomendacja ML ---
    # Funkcja ta wykorzystuje załadowany model do prognozowania skuteczności planu.
    def predict_plan_effectiveness():
        if not model or not encoders:
            return "Nie można przewidzieć skuteczności (błąd modelu)"
            
        input_dict = {
            "Płeć": str(gender),
            "Wiek": age,
            "Waga": weight,
            "Wzrost": height,
            "Poziom aktywności": str(activity),
            "Cel": str(goal),
            "Preferencje treningowe": str(training_pref),
            "Dostępność sprzętu": str(equipment),
            "Posiłki dziennie": str(meals)
        }
        df_input = pd.DataFrame([input_dict])

        model_features = list(model.feature_names_in_)
        df_input = df_input.reindex(columns=model_features)

        for col in df_input.select_dtypes(include=['object']).columns:
            if col in encoders:
                le = encoders[col]
                df_input[col] = df_input[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        
        df_input = df_input.fillna(0)
        prediction = model.predict(df_input)[0]
        skutecznosc = encoders["Skuteczność planu"].inverse_transform([prediction])[0]
        return skutecznosc

    # --- GŁÓWNA FUNKCJONALNOŚĆ ---
    if submit and model:
        with st.spinner("Proszę czekać, generuję Twój spersonalizowany plan..."):
            prompt = build_prompt()
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                raw_result = response.choices[0].message.content
                # Zastąp niechciane znaki odpowiednimi emoji
                raw_result = raw_result.replace("𐀀", "🔸")
                
                # Przechowuj wyniki w session_state
                st.session_state.plan_generated = True
                
                if "🔸" in raw_result:
                    sections = raw_result.split("🔸")
                    st.session_state.intro_content = sections[0].strip()
                    training_full = sections[1].strip() if len(sections) > 1 else ""
                    diet_full = sections[2].strip() if len(sections) > 2 else ""
                    metrics_full = sections[3].strip() if len(sections) > 3 else ""
                    st.session_state.result_for_pdf = f"{st.session_state.intro_content}\n\n🔸 {training_full}\n\n🔸 {diet_full}\n\n🔸 {metrics_full}"
                    st.session_state.training_content = re.sub(r"^TYGODNIOWY PLAN TRENINGOWY", "", training_full, count=1).strip()
                    st.session_state.diet_content = re.sub(r"^PLAN ŻYWIENIOWY", "", diet_full, count=1).strip()
                    st.session_state.metrics_content = re.sub(r"^OBLICZENIA FIZJOLOGICZNE", "", metrics_full, count=1).strip()
                else:
                    st.session_state.training_content = raw_result 

                st.session_state.skutecznosc_planu = predict_plan_effectiveness()
                
            except Exception as e:
                st.error(f"Wystąpił błąd podczas komunikacji z API OpenAI: {e}")
                st.session_state.plan_generated = False

    # Wyświetl wyniki, jeśli plan został wygenerowany (lub jeśli jest zapisany w session_state)
    if st.session_state.plan_generated:
        st.success("✅ Plan wygenerowany!")
        if st.session_state.intro_content:
            st.write(st.session_state.intro_content)
        if st.session_state.training_content:
            st.text_area("🔸 TYGODNIOWY PLAN TRENINGOWY", value=st.session_state.training_content, height=300, key="plan_treningowy")
        if st.session_state.diet_content:
            st.text_area("🔸 PLAN ŻYWIENIOWY", value=st.session_state.diet_content, height=300, key="plan_zywieniowy")
        if st.session_state.metrics_content:
            st.text_area("🔸 OBLICZENIA FIZJOLOGICZNE", value=st.session_state.metrics_content, height=300, key="obliczenia_fizjologiczne")

        # Informacje o skuteczności planu wyświetlane poniżej wygenerowanego planu
        st.markdown(f"📈 **Przewidywana skuteczność planu:** {st.session_state.skutecznosc_planu.upper()}")
        
        st.markdown("""
    Na podstawie zebranych danych (sztucznie wygenerowanych na potrzeby tej aplikacji) i wcześniej przygotowanego modelu uczenia maszynowego, aplikacja klasyfikuje skuteczność planu na podstawie cech użytkownika, które podał w formularzu. Poniżej znajduje się krótkie wyjaśnienie dotyczące poziomów skuteczności planu:

    - 🔴 **Niska skuteczność planu** - plan prawdopodobnie nie doprowadzi do pożądanych rezultatów, ponieważ występują czynniki ograniczające skuteczność (np. niezgodność celu z trybem życia; zbyt mało posiłków; zbyt młody wiek użytkownika; nieoptymalne połączenie cech).
    - 🟠 **Średnia skuteczność planu** - plan może zadziałać, ale wymaga wysokiej samodyscypliny lub korekty (np. ograniczony dostęp do sprzętu; przeciętna liczba posiłków i umiarkowany poziom aktywności; wiek, waga lub wzrost użytkownika mogą wymagać bardziej indywidualnego podejścia; zbyt ogólne preferencje treningowe).
    - 🟢 **Wysoka skuteczność planu** - plan jest bardzo dobrze dopasowany i prawdopodobnie doprowadzi do zamierzonego celu. Plan zawiera spójne cele, poziom aktywności i preferencje treningowe. Wygenerowana propozycja zawiera dobry bilans posiłków oraz brak ograniczeń zdrowotnych.
    """)


        # HTML PDF
        html_template = f"""
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'DejaVu Sans', Arial, sans-serif;
                padding: 30px;
                color: black;
            }}
            h1 {{
                color: black;
                margin-bottom: 30px;
                text-align: center;
                font-size: 24px;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 14px;
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
                color: black;
            }}
        </style>
        </head>
        <body>
        
        <h1>Plan Treningowy + Dieta</h1>

        <pre>{st.session_state.result_for_pdf}</pre>

        </body>
        </html>
        """
        
        try:
            pdf_filename = f"plan_{datetime.date.today()}.pdf"
            # UWAGA: Poniższa ścieżka może wymagać dostosowania w zależności od środowiska.
            # Linux/macOS: '/usr/local/bin/wkhtmltopdf'
            # Windows: 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
            def generate_pdf_from_html(html: str) -> bytes:
                buffer = BytesIO()
                pisa.CreatePDF(src=html, dest=buffer)
                return buffer.getvalue()

            pdf_bytes = generate_pdf_from_html(html_template)
            
            st.download_button(
                label="📄 Pobierz plan jako PDF",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.warning("Nie można wygenerować pliku PDF. Komponent 'wkhtmltopdf' nie został znaleziony. Sprawdź, czy jest zainstalowany i czy ścieżka w `pdfkit.configuration()` jest poprawna.")
        except Exception as e:
            st.error(f"Wystąpił nieoczekiwany błąd podczas generowania PDF: {e}")
