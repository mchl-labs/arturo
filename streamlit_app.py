import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["OAI"],  # This is the default and can be omitted
)

username = ""
markdownplan = ""


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
    Se te lo chiedono la dieta si può fare bene solo con il nutrizionista. Saluta l'utente solo la prima volta. Alla fine di ogni messaggio proponi sempre consigli su altre cose da chiederti che potrebbero interessargli, non invitarlo semplicemente a chiederti altro ma dargli delle idee su cosa altro ti potrebbe chiedere.
    Esempio di approccio:
    
    Domanda del paziente: "Posso aggiungere zucchero al caffè?"
    Risposta: \"Secondo il tuo piano alimentare, è meglio evitare lo zucchero aggiunto per gestire al meglio i tuoi livelli di glicemia. Potresti provare una piccola quantità di dolcificante naturale, ma sentiti libero di consultare il tuo nutrizionista per maggiori dettagli.\""""
    }
]

pazienti = [
    {
        "name": "P. Capuano",
        "path": "data.txt"
    },
    {
        "name": "Test 2",
        "path": "data.txt"
    }
]

system_prompt_dict = {item["name"]: item["content"] for item in system_prompts}
pazienti_dict = {item["name"]: item["path"] for item in pazienti}

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

def chatbot(history, username = "Marco", system = "Sei un nutrizionista esperto. Rispondi come tale. Devi rispondere alle domande in base al mio piano nutrizionale. Posso mangiare solo ingredienti presenti nel mio piano nutrizionale e nelle quantità indicate."):
    try:
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"{system} Questo è il mio piano nutrizionale: {markdownplan}. Il mio nome è {username}"},
                    *history
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
st.title("Arturo BOT 🎈")

# Sidebar: System Prompt Selection
paziente = st.sidebar.selectbox("Seleziona un paziente:", list(pazienti_dict.keys()))

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display chat history
st.markdown("### Chat History")
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        st.markdown(f"""<div style="background-color: #e0f7fa; padding: 10px; border-radius: 10px; margin: 5px 0; color: #00796b;"><strong>Paziente:</strong> {message['content']}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="background-color: #f1f8e9; padding: 10px; border-radius: 10px; margin: 5px 0; color: #33691e;"><strong>Chatbot:</strong> {message['content']}</div>""", unsafe_allow_html=True)

# Display suggested questions
st.markdown("### Domande suggerite")
question = st.radio("Seleziona una domanda:", questions)

with st.form("my_form", clear_on_submit=True):
    # Text input field
    custom_question = st.text_input("O inserisci la tua domanda:")
    
    # Submit button
    submitted = st.form_submit_button("Send")

# Final user message
user_input = custom_question if custom_question else question

# Handle user input and update conversation history
if submitted:
    if username != paziente:
        username = paziente
        with open(pazienti_dict[paziente], "r") as file:
            markdownplan = file.read()
    if user_input:
        # Add user message to history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
        # Generate chatbot response
        with st.spinner("Generating response..."):
            response = chatbot(st.session_state.conversation_history, username=username, system=system_prompt_dict["Prompt 3"])
    
        # Add chatbot response to history
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
        # Refresh the chat display
        st.rerun()
    else:
        st.warning("Please enter a question.")

# Clear conversation
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.rerun()
