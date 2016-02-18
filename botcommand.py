import json
import pickle


def parse(bot, command_string):
    arglist = command_string.split(' ')
    if arglist[0] == '@favequotesbot':
        arglist[0] = arglist[0][len('@favequotesbot '):]
    if arglist[0][0] == '/':
        arglist[0] = arglist[0][1:]
    if not arglist[0] in commands:
        return 'I didn\'t understand that command!'
    return commands[arglist[0]](bot, arglist)


def addquote(bot, args):
    username = args[1]
    del args[0]
    del args[0]
    quote_string = " ".join(args)
    if not username in bot.quotes:
        bot.quotes[username] = []
    bot.quotes[username].append(quote_string)
    savequotedict(bot.quotes)
    return 'Added the new quote!'


def removeQuote(bot, args):
    username = args[1]
    index = int(args[2])
    msg = ""
    if not username in bot.quotes:
        return "User does not exist!"
    try:
        del bot.quotes[username][index]
        savequotedict(bot.quotes)
        msg = "Removed quote successfully!"
    except IndexError:
        msg = "That quote does not exist!"
        pass
    return msg


def removeuser(bot, args):
    username = args[1]
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
        quote = 'That index is out of range!'
        pass
    return quote


def showUsers(bot, args):
    userlist = "Users in quote book: \n"
    keyList = list(bot.quotes.keys())
    for x in range(0,len(keyList)):
        userlist = userlist + keyList[x] + "\n"
    return userlist


def showAll(bot, args):
    if not args[1] in bot.quotes:
        return "User does not exist!"
    quotelist = "Quotes shown by index number first:\n"
    for x in range(0, len(bot.quotes[args[1]])):
        quotelist = quotelist + str(x) + " : " + bot.quotes[args[1]][x] + "\n"
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