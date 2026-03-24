contact = {}

while True:
    print("\n1. Add new contact ")
    print("2. View saved contact ")
    print("3. Delete contact ")
    print("4. Search ")
    print("5. exit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Enter a name: ")
        phone = input("Enter phone number: ")

        contact[name] = phone

    elif choice == "2":
     for name, phone in contact.items():
        print(name, ":", phone)  

    elif choice == "3":
       name = input("Type number you want to delete?: ")

       if name in contact:
          del contact[name]
          print ("Contact deleted")
       else:
          print("Contact not FOUND")  

    elif choice == "4":
     search = input("Enter name or number to search: ").lower()

     found = False

     for name, phone in contact.items():
        if search in name.lower() or search in phone:
            print(name, ":", phone)
            found = True

     if not found:
        print("No matching contact found.")       
          
            

    elif choice == "4":
        print("THANK YOU, GOODBYE")
        break

    else:
        print("INVALID ENTRY")    
