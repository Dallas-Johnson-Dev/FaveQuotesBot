import json
import pickle


def parse(bot, command_string):
    arglist = command_string.split(' ')
    if arglist[0] == '@favequotesbot':
        del arglist[0]
    if arglist[0][0] == '/':
        arglist[0] = arglist[0][1:]
    if not arglist[0] in commands:
        return 'I didn\'t understand that command!'
    return commands[arglist[0]](bot, arglist)


def addquote(bot, args):
    username = ""
    try:
        username = args[1]
    except IndexError:
        return "Please enter a user!"
        pass
    del args[0]
    del args[0]
    quote_string = " ".join(args)
    if not username in bot.quotes:
        bot.quotes[username] = []
    bot.quotes[username].append(quote_string)
    savequotedict(bot.quotes)
    return 'Added \"{0}\" to the quote book!'.format(quote_string)


def removeQuote(bot, args):
    username = ""
    index = 0
    temp = ""
    try:
        username = args[1]
        index = int(args[2])
    except IndexError:
        return "Please enter a user and an index!"
        pass
    msg = ""
    if not username in bot.quotes:
        return "User does not exist!"
    try:
        temp = bot.quotes[username][index]
        del bot.quotes[username][index]
        savequotedict(bot.quotes)
        msg = "Removed the quote \"{0}\" successfully!".format(temp)
    except IndexError:
        msg = "That quote does not exist!"
        pass
    return msg


def removeuser(bot, args):
    username = ""
    try:
        username = args[1]
    except IndexError:
        return "Please enter a user to remove!"
        pass
    if not username in bot.quotes:
        return "User does not exist!"
    bot.quotes.pop(args[1])
    savequotedict(bot.quotes)
    return "Removed {0} from the quote book!".format(args[1])


def query(bot, args):
    username = args[1]
    quote = ""
    if not username in bot.quotes:
        return "User does not exist!"
    try:
        quote = bot.quotes[username][int(args[2])]
    except IndexError:
        quote = 'That quote does not exist!'
        pass
    return quote


def showUsers(bot, args):
    userlist = "Users in quote book: \n"
    keyList = list(bot.quotes.keys())
    index = 0
    #I have no idea why the for loop is fucked here.
    #Yay hackjobs!
    while True:
        if index == len(keyList):
            break
        userlist = userlist + keyList[index] + "\n"
        index = index + 1
    return userlist


def showAll(bot, args):
    index = 0
    if not args[1] in bot.quotes:
        return "User does not exist!"
    quotelist = "Quotes shown by index number first:\n"
    while True:
        if index == len(bot.quotes[args[1]]):
            break
        quotelist = quotelist + str(index) + " : " + bot.quotes[args[1]][index] + "\n"
        index = index + 1
    return quotelist


def printhelp(bot, args):
    helpmsg = 'list of commands:\n /add @username quote\n /remove @username index\n /showusers\n /showall @username\n /query @username index\n /help\n'
    return helpmsg


def savequotedict(quote_dict):
    with open('quotelist.qt', 'wb') as filedescriptor:
        try:
            pickle.dump(quote_dict, filedescriptor)
        except IOError:
            pass


#Forward declare all of the methods. Just go with it.
#This won't work otherwise.
commands = {'add':addquote,
            'remove':removeQuote,
            'removeuser':removeuser,
            'query':query,
            'help':printhelp,
            'showusers':showUsers,
            'showall':showAll}