import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["OAI"],  # This is the default and can be omitted
)

with open("data.txt", "r") as file:
    markdownplan = file


# Predefined system prompts
system_prompts = [
  {
    "name": "Prompt 1",
    "content": "Sei un nutrizionista esperto. Rispondi come tale. Devi rispondere alle domande in base al mio piano nutrizionale. Posso mangiare solo ingredienti presenti nel mio piano nutrizionale e nelle quantità indicate."
  },
  {
    "name": "Prompt 2",
    "content": """Sei un chatbot nutrizionista virtuale altamente qualificato, progettato per rispondere a domande sui piani alimentari personalizzati dei pazienti. Devi fornire risposte accurate, comprensibili e amichevoli basandoti sul piano alimentare specifico del paziente. Segui queste linee guida:

Personalizzazione: Rispondi sempre in modo personalizzato in base alle informazioni fornite sul piano alimentare del paziente.
Educazione: Se possibile, includi spiegazioni semplici per aiutare il paziente a comprendere il motivo delle raccomandazioni.
Empatia: Mostrati sempre gentile, incoraggiante e disponibile.
Limiti: Se una domanda esula dalle tue competenze o richiede l’intervento di un professionista, invita il paziente a consultare il suo nutrizionista o medico di riferimento.
Esempio di approccio:

Domanda del paziente: "Posso aggiungere zucchero al caffè?"
Risposta: \"Secondo il tuo piano alimentare, è meglio evitare lo zucchero aggiunto per gestire al meglio i tuoi livelli di glicemia. Potresti provare una piccola quantità di dolcificante naturale, ma sentiti libero di consultare il tuo nutrizionista per maggiori dettagli.\""""
  },
  {
    "name": "Prompt 3",
    "content": """Sei un nutrizionista esperto altamente qualificato. Rispondi come tale. Rispondi alle domande basandoti sui piani alimentari personalizzati dei pazienti. Devi fornire risposte accurate, comprensibili e amichevoli basandoti sul piano alimentare specifico del paziente. Segui queste linee guida:

Personalizzazione: Rispondi sempre in modo personalizzato in base alle informazioni fornite sul piano alimentare del paziente.
Educazione: Se possibile, includi spiegazioni semplici per aiutare il paziente a comprendere il motivo delle raccomandazioni.
Empatia: Mostrati sempre gentile, incoraggiante e disponibile.
Limiti: Se una domanda esula dalle tue competenze o richiede l’intervento di un professionista, invita il paziente a consultare il suo nutrizionista o medico di riferimento.
Esempio di approccio:

Domanda del paziente: "Posso aggiungere zucchero al caffè?"
Risposta: \"Secondo il tuo piano alimentare, è meglio evitare lo zucchero aggiunto per gestire al meglio i tuoi livelli di glicemia. Potresti provare una piccola quantità di dolcificante naturale, ma sentiti libero di consultare il tuo nutrizionista per maggiori dettagli.\""""
  }
]

system_prompt_dict = {item["name"]: item["content"] for item in system_prompts}

questions = [
    "Posso sostituire un alimento del piano con un altro?",
    "Quanto spesso posso fare uno strappo alla dieta?",
    "È necessario pesare sempre gli alimenti?",
    "Cosa posso mangiare se ho fame fuori pasto?",
    "Posso bere un succo di frutta al posto della frutta fresca?",
    "Posso concedermi un dolce una volta a settimana?",
    "Quali sono le alternative allo zucchero?",
    "Posso mangiare la pasta integrale invece di quella normale?",
    "Cosa posso usare al posto del burro nelle ricette?",
    "Cosa devo mangiare prima di un allenamento?",
    "Come posso gestire la dieta in una cena al ristorante?",
    "Sono intollerante al lattosio, quali alternative posso scegliere?",
    "Posso includere alimenti senza glutine nella mia dieta anche se non sono celiaco?",
    "Quanto tempo ci vuole per vedere risultati con questa dieta?",
    "Come posso aumentare la massa muscolare mantenendo il mio piano?",
    "È meglio fare colazione appena sveglio o più tardi?",
    "Posso bere tè o caffè durante il giorno?"
]

def chatbot(prompt, username = "Marco", system = "Sei un nutrizionista esperto. Rispondi come tale. Devi rispondere alle domande in base al mio piano nutrizionale. Posso mangiare solo ingredienti presenti nel mio piano nutrizionale e nelle quantità indicate."):
    try:
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"{system} Questo è il mio piano nutrizionale: {markdownplan}. Il mio nome è {username}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.1,
                n=1,
                stop=None,
                stream=False
            )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Arturo nutritionist bot POC")

# Select a system prompt
selected_prompt = st.sidebar.selectbox("Select a system prompt:", list(system_prompt_dict.keys()))

# Display suggested questions
st.markdown("### Suggested Questions")
question = st.radio("Select a question to test:", questions)

# Option for custom question
st.markdown("### Or Enter Your Own Question")
custom_question = st.text_input("Your Question:")

# Final user message
user_message = custom_question if custom_question else question

# Generate response button
if st.button("Generate Response"):
    if user_message:
        st.markdown("### Chatbot Response:")
        with st.spinner("Generating response..."):
            try:
                response = chatbot(user_message, system=system_prompt_dict[selected_prompt])
                st.success("Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error generating response: {e}")
    else:
        st.warning("Please select a question or enter your own question.")
