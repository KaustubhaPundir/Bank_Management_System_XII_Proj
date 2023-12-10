def startup():
    import  mysql.connector as sql
    global usrn
    global pasw
    usrn=input("Enter your sql username ")
    pasw=input("Enter your sql password ")
    conn=sql.connect(host='localhost',user=usrn,passwd=pasw)
    cur = conn.cursor()
    cur.execute("create database if not exists bank")
    cur.execute("use bank")
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='user_table'")
    if cur.fetchone()[0]==0:
        cur.execute('create table user_table(username varchar(25), password varchar(25))')
    startup2()    
def startup2():
    import  mysql.connector as sql
    conn=sql.connect(host='localhost',user=usrn,passwd=pasw,database='bank')
    cur = conn.cursor()
    print('1.REGISTER')
    print('2.LOGIN')
    n=int(input('enter your choice='))
    if n== 1:
        name=input('Enter a Username=')
        passwd=input('Enter a 4 DIGIT Password=')
        V_SQLInsert="INSERT  INTO user_table (password,username)values(" +  str (passwd) + ",' " + name + " ') "
        cur.execute(V_SQLInsert)
        conn.commit()
        print('USER created succesfully')
        startup2()
    if  n==2 :
        name=input('Enter your Username=')
        passwd=input('Enter your 4 DIGIT Password=')
        V_Sql_Sel="select * from user_table where password='"+str (passwd)+"' and username=  ' " +name+ " ' "
        cur.execute(V_Sql_Sel)
        if cur.fetchone() is  None:
            print('Invalid username or password')
            startup2()
        else:
            cur.execute('CREATE TABLE IF NOT EXISTS customer_details(acct_no integer, acct_name varchar(25), phone_no integer, adress varchar(60), cr_amt float)');
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='customer_details'")
            menu()
def menu():
    import datetime as dt
    import  mysql.connector as sql
    conn=sql.connect(host='localhost',user=usrn,password=pasw,database='bank')
    cur = conn.cursor()
    
    conn.autocommit = True
    print('1.CREATE BANK ACCOUNT')
    print('2.TRANSACTION')
    print('3.CUSTOMER DETAILS')
    print('4.TRANSACTION DETAILS')
    print('5.DELETE DETAILS')
    print('6.QUIT')
    
    n=int(input('Enter your CHOICE='))
    if n == 1:
        acc_no=int(input('Enter your ACCOUNT NUMBER='))
        acc_name=input('Enter your ACCOUNT NAME=')
        ph_no=int(input('Enter your PHONE NUMBER='))
        add=(input('Enter your place='))
        cr_amt=float(input('Enter your credit amount='))
        V_SQLInsert="INSERT  INTO customer_details values (" +  str (acc_no) + ",' " + acc_name + " ',"+str(ph_no) + ",' " +add + " ',"+ str (cr_amt) + " ) "
        cur.execute(V_SQLInsert)
        print('Account Created Succesfully!!!!!')
        conn.commit()
        menu()
    if n == 2:
        acct_no=int(input('Enter Your Account Number='))
        cur.execute('select * from customer_details where acct_no='+str(acct_no))
        data=cur.fetchall()
        count=cur.rowcount
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='transactions'")
        if cur.fetchone()[0]==0:
            cur.execute('CREATE TABLE IF NOT EXISTS transactions(acct_no integer, date DATE, Amount_withdrawn float, Amount_added float)');
        if count == 0:
            print('Account Number Invalid Sorry Try Again Later')
        else:
            print('1.WITHDRAW AMOUNT')
            print('2.ADD AMOUNT')
            x=int(input('Enter your CHOICE='))
            if x==1:
                current_time=dt.datetime.now()
                current_time=current_time.strftime('%y/%m/%d')
                amt=float(input('Enter withdrawl amount='))
                cur.execute('update customer_details set    cr_amt=cr_amt-'+str(amt) +  ' where acct_no=' +str(acct_no) )
                conn.commit()
                print('Account Updated Succesfully!!!!!')
                cur.execute("insert into transactions values ({},'{}',{},{})".format(acct_no,current_time,amt,0))
                conn.commit()
            if x==2:
                current_time=dt.datetime.now()
                current_time=current_time.strftime('%y/%m/%d')
                amt=float(input('Enter amount to be added='))
                cur.execute('update customer_details set      cr_amt=cr_amt+'+str(amt) +  ' where acct_no=' +str(acct_no) )
                conn.commit()
                cur.execute("insert into transactions values ({},'{}',{},{})".format(acct_no,current_time,0,amt))
                conn.commit()
                print('Account Updated Succesfully!!!!!')
        menu()
    
    if n == 3:
        acct_no=int(input('Enter your account number='))
        cur.execute('select * from customer_details where acct_no='+str(acct_no))
        if cur.fetchone() is  None:
            print('Invalid Account number')
        else:
            cur.execute('select * from customer_details where acct_no='+str(acct_no))
            data=cur.fetchall()
            for row in data:
                print('ACCOUNT NO=',acct_no)
                print('ACCOUNT NAME=',row[1])
                print('PHONE NUMBER=',row[2])
                print('ADDRESS=',row[3])
                print('cr_amt=',row[4])
        menu()
    if n== 4:
        acct_no=int(input('Enter your account number='))
        print()
        cur.execute('select * from customer_details                where  acct_no='+str(acct_no) )
        if cur.fetchone() is  None:
            print()
            print('Invalid Account number')
        else:
            cur.execute('select * from transactions where acct_no='+str(acct_no) )
            data=cur.fetchall()
            for row in data:
                print('ACCOUNT NO=',acct_no)
                print()
                print('DATE=',row[1])
                print()
                print('WITHDRAWAL AMOUNT=',row[2])
                print()
                print('AMOUNT ADDED=',row[3])
                print()
            conn.commit()
        menu()
    
    if n == 5:
        print('DELETE YOUR ACCOUNT')
        acct_no=int(input('Enter your account number='))
        cur.execute('delete from customer_details where acct_no='+str(acct_no) )
        print('ACCOUNT DELETED SUCCESFULLY')
        menu()
    
    if n == 6:
        quit()
    else:
        print("invalid choice")
        menu()
def quit():
    print("exited")
startup()

