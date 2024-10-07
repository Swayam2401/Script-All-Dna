from flask import Flask,render_template,url_for,request
import mysql.connector as connector

connection = connector.connect(
        host='localhost',
        user='root',
        password='@Modi2401',
        database='Library_Management',
        auth_plugin = "mysql_native_password"
    )

cursor = connection.cursor()

#######################################################

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

    
    #get all borrowed book
    def getAllBorrowed(this,id):
        cursor.execute("select * from Borrow where userId = %s",(id,))
        
        return cursor.fetchall()

    
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

lib = Library()

#######################################

#Flask starts here


app = Flask(__name__)


@app.route("/signUp",methods = ["GET","POST"])
def signUp():
    print(request.method)
    if(request.method == "POST"):
        userId = request.form['userId']
        name = request.form['name']
        isPremium = bool(int(request.form["radioBtn"]))

        if(userId == None or name == None):
            return render_template("Login.html")
        
        #new member added
        lib.addMember(name,userId,isPremium)

        #fetch all borrowed books
        borrowed = lib.getAllBorrowed(userId)

        return render_template("home.html",books = borrowed)
    else:
        return render_template("Login.html")

if(__name__ == "__main__"):
    app.run(debug=True)


        







