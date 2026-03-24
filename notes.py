notes = []
from datetime import datetime

while True:
    print("\n1. Add Note")
    print("2. View Notes")
    print("3. Delete Notes")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        note = input("Enter your note: ")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notes.append(note)

        with open("notes.txt", "a") as file:
         file.write(f"[{timestamp}] {note}\n")

         print("Note saved.")

    elif choice == "2":
        try:
            file = open("notes.txt", "r")
            for line in file:
                print(line.strip())
            file.close()
        except:
            print("No notes yet.")

    elif choice == "3":
     with open("notes.txt", "r") as file:
        notes = file.readlines()

     for i, note in enumerate(notes, start=1):
        print(i, note.strip())

     delete = int(input("Enter note number to delete: "))

     if 1 <= delete <= len(notes):
        notes.pop(delete - 1)

        with open("notes.txt", "w") as file:
            file.writelines(notes)

        print("Note deleted.")
     else:
        print("Invalid number.")        

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")