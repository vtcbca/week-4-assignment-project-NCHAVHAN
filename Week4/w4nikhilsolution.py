def connect():


    conn=sq.connect("C:\sqlite3\22bca32.db")
    cur=conn.cursor()
    conn.commit()
    return conn


#  creating table


 def createtable(conn):
     cur=conn.cursor()
     cur.execute("Create table conect(Fnmae text,Last name text,contact number,Email text,City text);")
     conn.commit()

     
#Log table creating

def cretaelog(con):
    cur=con.cursor()
    cur.execute("""Create table if not existing contect_log
        (
            Fname text,
            Lastname text,
            contect number,
            datetime text,
            operation_Performed text
            );""")
    conn.commit()

    
# creating trigger for log table 

def logTrigger(con):
    cur=con.cursor()
    cur.execute("""CREATE TRIGGER IF NOT EXISTS insertLogTrigger
                        after insert
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(new.fname,new.laname,new.contact,datetime('now','localtime'),'INSERT');
                        END;""")
    cur.execute("""CREATE TRIGGER IF NOT EXISTS deleteLogTrigger
                        after delete 
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(old.fname,old.laname,old.contact,datetime('now','localtime'),'DELETE');
                        END;""")
    cur.execute("""CREATE TRIGGER IF NOT EXISTS updateLogTrigger
                        after update
                        on contact
                        BEGIN
                            INSERT INTO CONTACT_log
                            VALUES(new.fname,new.laname,new.contact,datetime('now','localtime'),'After UPDATE');
                            INSERT INTO CONTACT_log
                            VALUES(old.fname,old.laname,old.contact,datetime('now','localtime'),'Before UPDATE');
                        END;""")
    con.commit()

# validating record 

def createTrigger(con):
    cur=con.cursor()
    con.execute("""CREATE TRIGGER validate_field 
    BEFORE INSERT
    ON CONTACT
    BEGIN
    SELECT
    CASE
    WHEN new.email NOT LIKE '%_@_%_.%' THEN
        RAISE(ABORT,'Please enter email in correct format')
    WHEN length(new.contact)<10 THEN
        RAISE(ABORT,'please enter valid contact no.')\
    END;
    END;""")           
    con.commit()

# insert record 

def insertRecords(con):
    cur=con.cursor()
    fname=input("\n\nEnter first name: ")
    lname=input("Enter last name: ")
    contact=int(input("Enter contact: "))
    email=input("Enter email:")
    city=input("Enter city: ")
    L=[fname,lname,contact,email,city]
    conn.execute("INSERT INTO CONTACT VALUES(?,?,?,?,?);",L)
    print('\n\nContact inserted sucessfully.\n')
    con.commit()

# updating record 

def updateContacts(con):
    cur=con.cursor()
    name_search=input("\n\nEnter their First name: ")
    new_contact=input("Enter New Contact No :")
    cur.execute(f"update CONTACT set contact='{new_contact}' where fname='{name_search}'")
    print("\n\nContact updated successfully.\n")
    con.commit()

#deleting record 

def deleteContacts(con):
    cur=con.cursor()
    name_search=input("\n\nEnter their First Name: ")
    cur.execute(f"delete from CONTACT where fname='{name_search}'")
    print("\n\nContact deleted successfully.\n")
    con.commit()

# searching record

def searchContacts(con):
    cur=con.cursor()
    name_search=input("\n\nEnter their First Name: ")
    cur.execute(f"select * from CONTACT where fname='{name_search}'")
    records=cur.fetchall()
    print('\n____________________________________________________________________________________')
    print('Fname\tLaname\tContact\t\tEmail\t\t\tCity')
    print('______________________________________________________________________________________')
    for rows in records:
        print('{}\t{}\t{}\t{}\t{}'.format(rows[0],rows[1],rows[2],rows[3],rows[4]))     
    print('\n\nThis are all available records\n')
    con.commit()

# def viewRecords(con):
    cur=con.cursor()
    cur.execute('select * from CONTACT')
    records=cur.fetchall()
    print('\n____________________________________________________________________________________')
    print('Fname\tLaname\tContact\t\tEmail\t\t\tCity')
    print('______________________________________________________________________________________')
    for rows in records:
        print('{}\t{}\t{}\t{}\t{}'.format(rows[0],rows[1],rows[2],rows[3],rows[4]))       
    print('\n\nThis are all available records')
    con.commit()

# operation function 

def operationFunct():
    con=createConnect()
    tablecreate(con)
    createLog(con)
    createTrigger(con)
    logTrigger(con)
    choice=1
    while choice!=0:
        print('\n-------------------------------------------------------------------------------------------------')

    print('Enter 1 For Insert Contact No')
    print('Enter 2 For Update Contact No')
    print('Enter 3 For Delete Contact No')
    print('Enter 4 For Search Contact No')
    print('5- View all records')
    print('Enter 0 For Quit')
      choice=int(input('\nEnter your choice: '))     
       if choice==1:
            insertRecords(con)      
        elif choice==2:
            updateContacts(con)     
        elif choice==3:
            deleteContacts(con)     
        elif choice==4:
            searchContacts(con)     
        elif choice==5:
            viewRecords(con)       
    con.close()
import sqlite3 as sq     
operationFunct()       
