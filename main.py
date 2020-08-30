import mysql.connector
import CreateTable,PopulateTable
    
def getConnection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root"
    )
    return mydb    

def executeQuery(query):
    myconn = getConnection()
    mycurr = myconn.cursor()
    mycurr.execute("USE Test")
    mycurr.execute(query)
    myconn.commit()
    myconn.close()

def displayResult(query):
    myconn = getConnection()
    mycurr = myconn.cursor()
    mycurr.execute("USE Test")
    mycurr.execute(query)
    for x in mycurr:
        print(x)
    myconn.close()

def main():
    PopulateTable.populate()
    queryObj = PopulateTable.createQueryBuilder()
    # Testcase 1 : Unkonown user tries to write a blog
    value = (4,"Introduction_new","This is first blog of user3",3,1,0)
    PopulateTable.insertIntoTable(queryObj,"blog",value)

    # Testcase 2 : Inserting NULL to PK
    value = (None,"Introduction_new","This is first blog of user3",3,1,0)
    PopulateTable.insertIntoTable(queryObj,"blog",value)

    # Testcase 3 : Get blogs based on upvotes
    sql = "SELECT blogName,upVoteCount,downVoteCount FROM Blog ORDER BY upVoteCount DESC"
    displayResult(sql)
    print('\n')
    update_sql = "UPDATE Blog SET upVoteCount = 4 WHERE blogID = 3"
    executeQuery(update_sql)
    displayResult(sql)

    # Testcase 4 : Get comments for a particular post
    sql = "SELECT * FROM Comment WHERE postID = 1"
    displayResult(sql)

    # Testcase 5 : Search blog based on tag value
    sql = """SELECT * FROM Blog WHERE blogID IN(
            SELECT DISTINCT blogID FROM TagMap WHERE tagID IN(
            SELECT tagID FROM Tag WHERE tagName = 'CS'  
            ))"""
    displayResult(sql)

    # TestCase 6 : Deleting user will delete all posts made by the user
    sql = "DELETE FROM User where userID = 1"
    executeQuery(sql)
    tables = ["User","Blog","Comment","Tag","TagMap"]
    sql_list = ["SELECT * FROM User","SELECT * FROM Blog", "SELECT * FROM Comment","SELECT * FROM Tag",
                "SELECT * FROM TagMap"]
    for sql,table in zip(sql_list,tables):
        print(table)
        displayResult(sql)
        print('\n')

main()