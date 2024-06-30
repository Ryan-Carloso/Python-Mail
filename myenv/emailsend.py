import time
import pyautogui
import random
import tkinter as tk
import threading

# Global variables to keep track of the number of emails sent and start time
emails_sent_count = 0
start_time = None

# Sample lists for demonstration (replace these with your actual lists)
remetente_list = [
    "example1@gmail.com",
    "example2@gmail.com",
    "example3@gmail.com",
]
email_list = [
    "recipient1@example.com",
    "recipient2@example.com",
    "recipient3@example.com",
]

# Function to send email
def enviar_email(email, remetente):
    global emails_sent_count

    try:
        time.sleep(5)  # Give enough time to switch between windows

        # Open a new tab in the browser (change this based on your OS and browser)
        pyautogui.hotkey('command', 't')  # Assuming macOS with Chrome

        time.sleep(2)

        # Move the cursor to the address bar and click to enter the Gmail URL
        pyautogui.click(x=100, y=100)  # Change the coordinates according to your screen
        gmail_url = f'https://mail.google.com/mail/u/0/?authuser={remetente}&view=cm&to={email}&su=%5BBinance%5D%20Request%20to%20Reset%20Security%20Items%20From%2084.193.82.102'
        pyautogui.write(gmail_url)
        pyautogui.press('enter')
        time.sleep(20)  # Adjust this as necessary

        # Click on the HTML content (adjust coordinates based on your screen resolution)
        pyautogui.click(438, 767)
        time.sleep(10)

        # Click on the apply button in HTML (adjust coordinates based on your screen resolution)
        pyautogui.click(1174, 731)
        time.sleep(7)

        # Click on schedule send (adjust coordinates based on your screen resolution)
        pyautogui.click(145, 765)
        time.sleep(7)

        # Click on schedule send 2 (adjust coordinates based on your screen resolution)
        pyautogui.click(144, 731)
        time.sleep(7)

        # Click on tomorrow afternoon (adjust coordinates based on your screen resolution)
        num_tabs = random.randint(0, 2)

        # Press the "Tab" key a random number of times
        for _ in range(num_tabs):
            pyautogui.press('tab')
            time.sleep(0.2)  # Short pause between key presses

        pyautogui.press('enter')

        # Print a different message depending on the value of num_tabs
        if num_tabs == 0:
            print("Tomorrow morning.")
        elif num_tabs == 1:
            print("Tomorrow Afternoon.")
        elif num_tabs == 2:
            print("Monday or so.")

        time.sleep(6)
        pyautogui.hotkey('command', 'w')  # Close the current tab

        # Update the email count and log
        emails_sent_count += 1
        emails_sent_label.config(text=f"Emails sent: {emails_sent_count}")
        log_message = f"Sender: {remetente}\nRecipient: {email}\n"
        print(log_message)
        log_text.configure(state='normal')
        log_text.insert(tk.END, log_message + "\n")
        log_text.configure(state='disabled')
        log_text.see(tk.END)

    except Exception as e:
        print(f"An error occurred while sending email: {e}")

# Function to start the email sending process
def iniciar_envio():
    global start_time
    start_time = time.time()

    try:
        index_remetente = 0
        index_destinatario = 0

        while not stop_event.is_set():
            remetente = remetente_list[index_remetente]
            destinatario = email_list[index_destinatario]

            enviar_email(destinatario, remetente)
            time.sleep(7)  # Wait a bit between sends to avoid overload problems

            index_remetente = (index_remetente + 1) % len(remetente_list)
            index_destinatario = (index_destinatario + 1) % len(email_list)

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to start the email sending process in a separate thread
def start_thread():
    global email_thread
    stop_event.clear()
    email_thread = threading.Thread(target=iniciar_envio)
    email_thread.start()
    start_timer()

# Function to stop the email sending process
def parar_envio():
    stop_event.set()
    email_thread.join()
    stop_timer()
    # No need to destroy the main window here to keep it open

# Function to open a new window to edit remetente list
def editar_remetentes():
    global remetente_list
    edit_window = tk.Toplevel(janela)
    edit_window.title("Editar Remetentes")

    # Explanation label
    explanation_label = tk.Label(edit_window, text="Edite a lista dos remetentes:")
    explanation_label.pack(pady=10)

    # Create a text area to edit remetente list
    edit_text = tk.Text(edit_window, height=10, width=50)
    edit_text.pack(pady=10)

    # Insert current remetentes into the text area
    for remetente in remetente_list:
        edit_text.insert(tk.END, remetente + "\n")

    # Button to save changes
    def salvar():
        global remetente_list
        remetente_list = edit_text.get("1.0", tk.END).strip().split("\n")
        edit_window.destroy()
    
    save_button = tk.Button(edit_window, text="Salvar", command=salvar)
    save_button.pack(pady=10)

# Function to open a new window to edit destinatario list
def editar_destinatarios():
    global email_list
    edit_window = tk.Toplevel(janela)
    edit_window.title("Editar Destinatários")

    # Explanation label
    explanation_label = tk.Label(edit_window, text="Edite a lista dos destinatários:")
    explanation_label.pack(pady=10)

    # Create a text area to edit destinatario list
    edit_text = tk.Text(edit_window, height=10, width=50)
    edit_text.pack(pady=10)

    # Insert current destinatarios into the text area
    for destinatario in email_list:
        edit_text.insert(tk.END, destinatario + "\n")

    # Button to save changes
    def salvar():
        global email_list
        email_list = edit_text.get("1.0", tk.END).strip().split("\n")
        edit_window.destroy()
    
    save_button = tk.Button(edit_window, text="Salvar", command=salvar)
    save_button.pack(pady=10)


# Function to start the timer
def start_timer():
    global start_time
    start_time = time.time()
    update_timer()

# Function to update the timer display
def update_timer():
    if not stop_event.is_set():
        elapsed_time_seconds = int(time.time() - start_time)
        hours, remainder = divmod(elapsed_time_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text=f"Elapsed Time: {hours:02}:{minutes:02}:{seconds:02}")
        janela.after(1000, update_timer)

# Function to stop the timer
def stop_timer():
    timer_label.config(text="Timer stopped")

# Create the graphical interface
janela = tk.Tk()
janela.title("Automatic Email Sending")

# Create a start button
botao_iniciar = tk.Button(janela, text="Iniciar Envio", command=start_thread)
botao_iniciar.pack(pady=10)

# Create a stop button
botao_parar = tk.Button(janela, text="Parar Envio", command=parar_envio)
botao_parar.pack(pady=10)

# Create a button to edit remetentes
botao_editar_remetentes = tk.Button(janela, text="Editar Remetentes", command=editar_remetentes)
botao_editar_remetentes.pack(pady=10)

# Create a button to edit destinatarios
botao_editar_destinatarios = tk.Button(janela, text="Editar Destinatários", command=editar_destinatarios)
botao_editar_destinatarios.pack(pady=10)

# Create a label to display the count of emails sent
emails_sent_label = tk.Label(janela, text="Emails enviados: 0")
emails_sent_label.pack(pady=10)

# Create a label to display the timer
timer_label = tk.Label(janela, text="Tempo decorrido: 0 segundos")
timer_label.pack(pady=10)

# Create a text widget to log the sent emails
log_text = tk.Text(janela, height=10, width=50, state='disabled')
log_text.pack(pady=10)

# Event to signal stopping the email sending process
stop_event = threading.Event()

janela.mainloop()
