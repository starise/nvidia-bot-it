# nvidia-bot-it

Controlla automaticamente la disponibilità delle nuove schede Nvidia GeForce RTX 3080, RTX 3090 e RTX 3070, direttamente dal sito web dello [store Nvidia](https://www.nvidia.com/it-it/shop/).

Ricevi notifiche in tempo reale sulla disponibilità dei prodotti:

- **SMS** via Twilio (anche con saldo di prova gratuito)
- **E-mail** via SendGrid (100 e-mail gratuite al giorno)

## Requisiti

- [Python 3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/) (per installare le dipendenze)

## Requisiti opzionali

- Supporto SMS: [Account Twilio](https://www.twilio.com/try-twilio)
- Supporto E-mail: [Account SendGrid](https://sendgrid.com/free/)

## Installazione

1. Clone/Download del repository
2. Installare le dipendenze con pip
    -  `pip install -r requirements.txt` o `python -m pip install -r requirements.txt`
    - Su Windows, usare `win-requirements.txt`.
3. Rinominare il file `.env_template` in `.env`. Usare un editor di testo per configurare il bot.
    - Alcune variabili sono opzionali, se lasciate in bianco verranno ignorate.
4. Aprire il file `sites.json` per personalizzare le variabili dello store Nvidia.

## Avvio del bot

Da riga di comando:

```
python nvidia-bot.py
```

Su alcuni sistemi Mac e Linux, il comando corretto è:
```
python3 nvidia-bot.py
```

## Test per le notifiche (Toast/Twilio/SendGrid)

```
python nvidia-bot.py test
```
