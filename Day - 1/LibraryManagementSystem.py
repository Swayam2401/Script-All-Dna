
class Library:

    books = {}
    members = []

    #constructor for assinging library class
    def __init__(this):
        constantBook = ("Madame Bovary","War and Peace","The Great Gatsby","Lolita","Middlemarch","Adventures of Huckleberry Finn","The Stories","Ulysses")
        this.books = {}
        this.members = []

        for book in constantBook:
            this.books.update({book : 10})

    #add book method
    def addNewBook(this,bookName,qty):
        for book in this.books.keys():
            if(book == bookName):
                print("already avaliable")
                return
            
        this.books.update({bookName : qty})
        print("added")

    #add member method
    def addMember(this,member):
        this.members.append(member)

    #borrow helper method which checks the conditions
    def canBorrow(this,member,book,reqQty,bookQty):
        if(member.limit < reqQty or bookQty < reqQty):
            return "You can not borrow this book"
        
        member.borrowedBook.update({book : reqQty})
        member.limit -= reqQty
        bookQty -= reqQty

        this.books.update({book : bookQty})

    #borrow book method
    def borrowBook(this,name,book,qty):
        curr = 0
        
        for val in this.books.keys():
            if(book == val):
                curr = this.books[book]

        for member in this.members:
            if(member.name == name):
                this.canBorrow(member,book,qty,curr)
        

#member class
class Member:

    #constructor
    def __init__(this,name,library,isPremium):
        this.name = name
        this.library = library
        this.borrowedBook = {}
        this.isPremium = isPremium

        if(isPremium):
            this.limit  = 5
        else:
            this.limit = 3

    #return book method
    def returnBook(this,bookName,qty):
        for book in this.borrowedBook:
            if(book == bookName):
                this.borrowedBook.update({book : this.borrowedBook[book] - qty})
                this.library.books.update({book : this.library.books[book] + qty})
                this.limit += qty


#implementation of all the methods
lib = Library()
print(lib.books)


#add book section
lib.addNewBook("the book",10)

# creating member 
member1 = Member("Swayam",lib,False)
member2 = Member("meet",lib,True)

lib.addMember(member1)
lib.addMember(member2)

lib.borrowBook("Swayam","the book",2)

print(member1.borrowedBook)
print(lib.books)
member1.returnBook("the book",2)
print(lib.books)






