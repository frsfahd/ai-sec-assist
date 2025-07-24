# AI Security Assistant

A Chatbot-utilizing-LLM to assist general user in digital security area.

Core Features :

- [x] File Scanning
- [x] URL Scanning
- [x] Security News and Updates
- [ ] Graphical cybersecurity information
- [ ] Interactive Quiz
- [ ] General Security Tips

## How it Works

```mermaid
---
title: File & URL Scanning
---

stateDiagram-v2

    [*] --> RECEIVE_MESSAGE: message
    [*] --> WAITING_COMMAND: file upload

    WAITING_COMMAND --> RECEIVE_FILE:[bot] plz upload a file
    WAITING_UPDATE --> RECEIVE_URL:[bot] plz send me a valid URL

    state PROCCESSING_INPUT <<join>>

    RECEIVE_FILE --> PROCCESSING_INPUT
    RECEIVE_URL --> PROCCESSING_INPUT

    PROCCESSING_INPUT --> SEND_ANALYSIS

    SEND_ANALYSIS --> [*]

```

### References

- [VirusTotal](https://www.virustotal.com/)
- [PhishStats](https://phishstats.info/)
