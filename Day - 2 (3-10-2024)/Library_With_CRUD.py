import mysql.connector as connector


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
        constantBook = ("Madame Bovary","War and Peace","The Great Gatsby","Lolita","Middlemarch","Adventures of Huckleberry Finn","The Stories","Ulysses")
        
        for book in constantBook:
            this.addNewBook(book,10)

    #show avalible book
    def showBooks(this):
        cursor.execute("Select * from Book;")
        books = cursor.fetchall()

        for book in books:
            print(book[0],book[1])
        

    #add book method
    def addNewBook(this,bookName,qty):
        cursor.execute("SELECT * FROM Book WHERE book = %s;",(bookName,))
        fetched = cursor.fetchone()

        if(fetched):
            print(f"{bookName} book is already exist")
            return
        
        cursor.execute("Insert Into Book(book,qty) values (%s,%s);",(bookName,qty))
        connection.commit()
        

    #add member method
    def addMember(this,name,isPremium):
        cursor.execute("select * from Member;")
        members = cursor.fetchall()
        newId = len(members) + 1

        cursor.execute("Insert into Member (id,name,isPremium) values (%s,%s,%s)",(newId,name,isPremium))
        connection.commit()

    #remove member
    def removeMember(this,id):
        cursor.execute("select 1 from Member where id = %s",(id,))
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

        cursor.execute("select * from Borrow where id = %s",(member[0],))
        borrowed = cursor.fetchall()

        for b in borrowed:
            qtyBorrowed += b[2]

        if(reqQty > limit - qtyBorrowed):
            print(f"{member[1]}, your borrow limit is full!!")
            return
        
        cursor.execute("select * from Book where book = %s",(book,))
        bookObj = cursor.fetchone()

        if(bookObj == None or reqQty > bookObj[1]):
            print("Stock of the book is not available")
            return
        
        cursor.execute("select * from Borrow where id = %s and bookName = %s;",(member[0],book))
        isExist = cursor.fetchone()


        if(isExist):
            cursor.execute("Update Borrow set qty = %s where bookName = %s;",(isExist[2] + reqQty,book))
        else:
            cursor.execute("Insert Into Borrow (id,bookName,qty) values (%s,%s,%s);",(member[0],book,reqQty))

        cursor.execute("Update Book Set qty = %s where book = %s;",(bookQty - reqQty,book))

        connection.commit()
        


    #borrow book method
    def borrowBook(this,id,book,qty):
        cursor.execute("select * from Member where id = %s",(id,))
        member = cursor.fetchone()

        if(member):
            this.__canBorrow(member,book,qty)
            return
        
        print(f"{id} Id not exist!!")
    
    #return Book method
    def returnBook(this,id,book,returnQty):
        cursor.execute("Select * from Member where id = %s",(id,))
        member = cursor.fetchone()


        if(member):
            cursor.execute("select * from Borrow where id = %s and bookName = %s;",(id,book))
            borrowed = cursor.fetchone()

            if(borrowed and returnQty <= borrowed[2]):
                cursor.execute("Update Borrow set qty = %s where id = %s and bookName = %s",(borrowed[2] - returnQty,id,book))
                cursor.execute("select qty from Book where book = %s",(book,))
                currQty = cursor.fetchone()

                cursor.execute("Update Book set qty = %s where book = %s",(currQty[0] + returnQty,book))
                connection.commit()
                return
            
            print("book does not exsits!!")
            return
        
        print("User not Found")

    #show members
    def showMembers(this):
        cursor.execute("select * from Member;")
        members = cursor.fetchall()

        for member in members:
            print(member[0],member[1],member[2])

        


#implementation of all the methods
lib = Library()
lib.showBooks()
lib.showMembers()






