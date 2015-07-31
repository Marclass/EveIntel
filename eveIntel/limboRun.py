#!/usr/bin/env python
from limbo.limbo import main
import argparse
import sys

def runSlack(token):
    parser = argparse.ArgumentParser(description="Run the limbo chatbot for Slack")
    parser.add_argument('--test', '-t', dest='test', action='store_true', required=False, help='Enter command line mode to enter a limbo repl')

    parser.add_argument('--hook', dest='hook', action='store', default='message',
                        help='Specify the hook to test. (Defaults to "message")')
    parser.add_argument('-c', dest="command", help='run a single command')
    parser.add_argument('--database', '-d', dest='database_name', default='D:\\sqlite3\\SlackBotDB\\limbo.sqlite3',
                        help="Where to store the limbo sqlite database. Defaults to limbo.sqlite")
    parser.add_argument('--pluginpath', '-pp', dest='pluginpath', default="C:\\Python27\\Lib\\limbo\\plugins",
                        help="The path where limbo should look to find its plugins")

    #if(token and token!=""):
    parser.add_argument('--token','-tk', dest='token', default=token, help="Token to use instead of environ var")


    
    args = parser.parse_args()

    main(args)

while(True):
    try:
        runSlack("")
    except Exception as e:
        #e = sys.exc_info()[0]
        print("Exception: "+str(e))
