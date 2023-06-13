import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('contacts.db')
c = conn.cursor()

# Create the contacts table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        category TEXT
    )
''')

# Function to add a new contact
def add_contact(name, phone, email, category):
    c.execute('INSERT INTO contacts (name, phone, email, category) VALUES (?, ?, ?, ?)', (name, phone, email, category))
    conn.commit()
    print('Contact added successfully.')

# Function to edit an existing contact
def edit_contact(contact_id, name, phone, email, category):
    c.execute('UPDATE contacts SET name=?, phone=?, email=?, category=? WHERE id=?', (name, phone, email, category, contact_id))
    conn.commit()
    print('Contact updated successfully.')

# Function to search contacts by name or category
def search_contacts(search_term):
    c.execute('SELECT * FROM contacts WHERE name LIKE ? OR category LIKE ?', (f'%{search_term}%', f'%{search_term}%'))
    contacts = c.fetchall()
    if contacts:
        print('Search results:')
        for contact in contacts:
            print(f'ID: {contact[0]}')
            print(f'Name: {contact[1]}')
            print(f'Phone: {contact[2]}')
            print(f'Email: {contact[3]}')
            print(f'Category: {contact[4]}')
            print('---')
    else:
        print('No matching contacts found.')

# Function to export contacts to a CSV file
def export_contacts(filename):
    c.execute('SELECT * FROM contacts')
    contacts = c.fetchall()
    if contacts:
        with open(filename, 'w') as file:
            file.write('Name,Phone,Email,Category\n')
            for contact in contacts:
                file.write(','.join(contact[1:]) + '\n')
        print('Contacts exported successfully.')
    else:
        print('No contacts found to export.')

# Function to import contacts from a CSV file
def import_contacts(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(',')
            add_contact(*data)
    print('Contacts imported successfully.')

# Main program loop
while True:
    print('1. Add a new contact')
    print('2. Search contacts')
    print('3. Exit')
    choice = input('Enter your choice (1-3): ')

    if choice == '1':
        name = input('Enter contact name: ')
        phone = input('Enter contact phone number: ')
        email = input('Enter contact email address: ')
        category = input('Enter contact category: ')
        add_contact(name, phone, email, category)
        export_contacts('contacts.csv')

    elif choice == '2':
        search_term = input('Enter search term: ')
        import_contacts('contacts.csv')
        search_contacts(search_term)

    elif choice == '3':
        break

# Close the database connection
conn.close()