# AI Trener Personalny i Dietetyk

To aplikacja AI zbudowana w Streamlit, która tworzy spersonalizowany plan treningowy i żywieniowy na podstawie danych użytkownika, przy użyciu GPT-4o oraz uczenia maszynowego.

## Funkcje
- Generowanie tygodniowego planu treningowego
- Jadłospis dzienny z makroskładnikami
- Obliczenia BMR, TDEE, zapotrzebowania kalorycznego
- System rekomendacyjny ML (skuteczność planu)
- Eksport wyników do PDF
- Podgląd PDF w aplikacji
- Powiadomienia SMS (Twilio)

## Jak uruchomić
1. Upewnij się, że masz `Python 3.8+`
2. Zainstaluj wymagane biblioteki:
```
pip install -r requirements.txt
```
3. Uruchom aplikację:
```
streamlit run Ai_Trainer_Agent.py
```

## Model ML
Model uczy się na 500 fikcyjnych profilach użytkowników i przewiduje skuteczność wygenerowanego planu.

## Autor
Projekt AI jako portfolio do pracy w konsultingu AI.
