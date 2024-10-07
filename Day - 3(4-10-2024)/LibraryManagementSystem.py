import mysql.connector as connector

#added command line iterface and updated naming

connection = connector.connect(
        host='localhost',
        user='root',
        password='@Modi2401',
        database='Library_Management',
        auth_plugin = "mysql_native_password"
    )

cursor = connection.cursor()

class Library:

    #constructor for assinging library class
    def __init__(this):
        return

    #show avalible book
    def showBooks(this):
        cursor.execute("Select * from Book;")
        books = cursor.fetchall()

        for book in books:
            print(book[0],book[1])
        

    #add book method
    def addNewBook(this,bookName,qty):
        cursor.execute("SELECT * FROM Book WHERE bookName = %s;",(bookName,))
        fetched = cursor.fetchone()

        if(fetched):
            print(f"{bookName} book is already exist")
            return
        
        cursor.execute("Insert Into Book(bookName,qty) values (%s,%s);",(bookName,qty))
        connection.commit()
        

    #add member method
    def addMember(this,name,id,isPremium):
        member = this.fetchMember(id)

        if(member):
            print("This id is already exist please,enter new id!!")
            return False
        
        print("Member added successfully!!")
        cursor.execute("Insert into Member (id,name,isPremium) values (%s,%s,%s)",(id,name,isPremium))
        connection.commit()

        return True

    #remove member
    def removeMember(this,id):
        cursor.execute("select * from Member where id = %s",(id,))
        member = cursor.fetchone()

        if(member):
            cursor.execute("delete from Member Where id = %s",(id,))
            print("member removed successfully")
            connection.commit()
            return
        
        print(f"Id {id} is not exist")
        

    #borrow helper method which checks the conditions
    def __canBorrow(this,member,book,reqQty):

        limit = 5 if member[2] else 3
        qtyBorrowed = 0

        cursor.execute("select * from Borrow where userId = %s",(member[0],))
        borrowed = cursor.fetchall()

        for b in borrowed:
            qtyBorrowed += b[2]

        if(reqQty > limit - qtyBorrowed):
            print(f"{member[1]}, your borrow limit is full!!")
            return
        
        cursor.execute("select * from Book where bookName = %s",(book,))
        bookObj = cursor.fetchone()

        if(bookObj == None or reqQty > bookObj[1]):
            print("Stock of the book is not available")
            return
        
        cursor.execute("select * from Borrow where userId = %s and bookName = %s;",(member[0],book))
        isExist = cursor.fetchone()


        if(isExist):
            cursor.execute("Update Borrow set qty = %s where bookName = %s;",(isExist[2] + reqQty,book))
        else:
            cursor.execute("Insert Into Borrow (userId,bookName,qty) values (%s,%s,%s);",(member[0],book,reqQty))

        cursor.execute("Update Book Set qty = %s where bookName = %s;",(bookObj[1] - reqQty,book))

        connection.commit()
        


    #borrow book method
    def borrowBook(this,id,book,qty):
        cursor.execute("select * from Member where id = %s",(id,))
        member = cursor.fetchone()

        if(member):
            this.__canBorrow(member,book,qty)
    
    #return Book method
    def returnBook(this,id,book,returnQty):

            cursor.execute("select * from Borrow where userId = %s and bookName = %s;",(id,book))
            borrowed = cursor.fetchone()

            if(borrowed and returnQty <= borrowed[2]):
                cursor.execute("Update Borrow set qty = %s where userId = %s and bookName = %s",(borrowed[2] - returnQty,id,book))
                cursor.execute("select qty from Book where bookName = %s",(book,))
                currQty = cursor.fetchone()

                cursor.execute("Update Book set qty = %s where bookName = %s",(currQty[0] + returnQty,book))
                connection.commit()
                print("You successfully borrowed ")
                return
            
            print("book does not exsits!!")


    #show members
    def showMembers(this):
        cursor.execute("select * from Member;")
        members = cursor.fetchall()

        for member in members:
            print(member[0],member[1],member[2])

    #Fetch member for authentication
    def fetchMember(this,id):
        cursor.execute("select * From Member where id = %s;",(id,))
        member = cursor.fetchone()

        if(member):
            return True
        
        return False


        


#implementation of all the methods
lib = Library()

print("welcom, Back to Library !!")

flag = False
while(flag == False):
    isNew = int(input("Are you new member ? enter (1 or 0): "))

    if(isNew):

        print("let's create new Account")

        name = str(input("enter your name: "))
        id = int(input("enter unique id: (id should be 4 length and only number): "))
        isPremium = int(input("do you want premium membership ?(1 or 0): "))

        res = lib.addMember(name,id,isPremium)

        if(res == False):
            print("Try again something went wrong !!")
            continue
    
    userId = int(input("enter your id: "))
    member = lib.fetchMember(userId)

    if(member):
        print("what do you want to do in Library")
        print("Want to see available Book press 1")
        print("Want to Borrow Book press 2")
        print("want to return book press 3")
        print("want to remove account press 4")
        print("want to leave library press 5")

        option = int(input("enter your answer: "))

        if(option == 1):
            lib.showBooks()
    
        elif(option == 2):
            bookName = str(input("Enter book name: "))
            reqQty = int(input("enter qty to borrow: "))

            lib.borrowBook(userId,bookName,reqQty)
        
        elif(option == 3):
            bookName = str(input("Enter book name: "))
            returnQty = int(input("enter qty to return: "))

            lib.returnBook(userId,bookName,returnQty)
        
        elif(option == 4):
            lib.removeMember(userId)
        
        elif(option == 5):
            print("Thank you for visiting")
            break

        else:
            print("Try again something went wrong !!")
    else:
        print("user id not found try again !!")
    
    
    






