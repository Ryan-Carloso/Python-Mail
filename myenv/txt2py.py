import os

def format_emails(input_file, output_file):
    input_path = os.path.join('myenv', input_file)
    output_path = os.path.join('myenv', output_file)
    
    with open(input_path, 'r') as infile:
        emails = infile.readlines()
    
    formatted_emails = ['"{}"'.format(email.strip()) + ',' for email in emails]
    
    with open(output_path, 'w') as outfile:
        outfile.write('\n'.join(formatted_emails))

# Nome dos arquivos de entrada e saída
input_file = 'emails.txt'
output_file = 'formatted_emails.txt'

# Chama a função para formatar os emails
format_emails(input_file, output_file)
