import mysql.connector

def getConnection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root"
    )
    return mydb

def createDB():
    myconn = getConnection()
    mycurr = myconn.cursor()
    mycurr.execute("DROP DATABASE IF EXISTS Test")
    mycurr.execute("CREATE DATABASE Test")
    myconn.close()

def createQueryBuilder():
    object = {
        "user" : """CREATE TABLE User(
                    userID INTEGER NOT NULL,
                    userName VARCHAR(255),
                    password VARCHAR(255),
                    PRIMARY KEY(userID))""",
        "blog" : """CREATE TABLE Blog(
                    blogID INTEGER NOT NULL,
                    blogName VARCHAR(255),
                    content VARCHAR(255),
                    authorID INTEGER,
                    upVoteCount INTEGER,
                    downVoteCount INTEGER, 
                    PRIMARY KEY(blogID),
                    FOREIGN KEY(authorID) REFERENCES User(userID) ON DELETE CASCADE)""",
        "comment" : """CREATE TABLE Comment(
                    comID INTEGER NOT NULL,
                    comDesc VARCHAR(255),
                    upCount INTEGER,
                    downCount INTEGER,
                    postID INTEGER, 
                    PRIMARY KEY(comID),
                    FOREIGN KEY(postID) REFERENCES Blog(blogID) ON DELETE CASCADE)""",
        "tag" : """CREATE TABLE Tag(
                    tagID INTEGER NOT NULL,
                    tagName VARCHAR(255), 
                    PRIMARY KEY(tagID))""",
        "tagmap" : """CREATE TABLE TagMap(
                    blogID INTEGER NOT NULL,
                    tagID INTEGER NOT NULL,
                    FOREIGN KEY(blogID) REFERENCES Blog(blogID) ON DELETE CASCADE,
                    FOREIGN KEY(tagID) REFERENCES Tag(tagID) ON DELETE CASCADE)"""
    }
    return object


def createNewTable(queryObj,table):
    myconn = getConnection()
    mycurr = myconn.cursor()
    mycurr.execute("USE Test")
    create_table = queryObj[table]
    mycurr.execute(create_table)
    myconn.close()

def executeQuery(queries):
    myconn = getConnection()
    mycurr = myconn.cursor()
    for query in queries:
        mycurr.execute(query)

def create():
    createDB()
    queryObj = createQueryBuilder()
    preprocessList = ["USE Test","DROP TABLE IF EXISTS TagMap","DROP TABLE IF EXISTS Comment",
    "DROP TABLE IF EXISTS Tag","DROP TABLE IF EXISTS Blog","DROP TABLE IF EXISTS User"]
    executeQuery(preprocessList)
    tableList = ["user","blog","comment","tag","tagmap"]
    for table in tableList:
        createNewTable(queryObj,table)