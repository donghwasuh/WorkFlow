import socket, threading, select
from EventFlow.ThreadDaemon import ThreadDaemon
from EventFlow.MiddleInterface import MiddleInterface

name = 'ConsoleListener'
version = '0.2'
last_fix = 'Wonchul Kang'

import EventFlow.Log as Log
Log.Init()

def debugLog(msg):
    __LOG__.Trace("D : %s : %s" % (name, msg))

def normalLog(msg):
    __LOG__.Trace("L : %s : %s" % (name, msg))

def exceptionLog(msg):
    __LOG__.Trace("E : %s : %s" % (name, msg))
    __LOG__.Exception()

class ConsoleListener(ThreadDaemon):
    def __init__(self, main_process, debugMode=False):
        ThreadDaemon.__init__(self, main_process, debugMode=debugMode)
        # sock storage init
        self.sock_list = []
        self.client_hash = {}
        self.middle_interface = MiddleInterface(self.main_p, web=False)

        # listen socket init
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.bind( (self.main_p.host, self.main_p.port) )

    # override shutdown function for close all socket
    def shutdown(self):
        normalLog("close all connected socket")
        # close all connected socket
        for sock in self.sock_list:
            self.close(sock)
        if self.debugMode: debugLog("%s daemon shutdown called" % self.__class__.__name__)
        # set shutdown flag to true
        self.shutdownFlag = True
        normalLog("%s daemon shutdown flag setted" % self.__class__.__name__)
    
    # do loop this function
    def loop(self):
        self.listen_sock.listen(100)
        if self.listen_sock not in self.sock_list: self.sock_list.append(self.listen_sock)

        while True:
            if self.shutdownFlag: break
            
            # listen for incoming message
            try: in_data, out_data, except_data = select.select(self.sock_list, [], [], 1)
            except Exception, e:
                exceptionLog("Exception in socket selelct : %s" % str(e))
                continue

            # if message size 0, ignore
            if len(in_data) == 0: continue

            for sock in in_data:
                # detected socket == listen_sock, create new socket
                if (sock == self.listen_sock):
                    client, addr = self.listen_sock.accept()
                    normalLog( "%s client connected" % str(addr) )
                    self.sock_list.append(client)
                    self.client_hash[client] = client.makefile()
                else:
                    try:
                        # read line from socket
                        in_line = self.client_hash[sock].readline()
                    except Exception, e:
                        exceptionLog("Exception in socket read : " + str(e))
                        continue
                    
                    try:
                        # parsing from read line
                        close_flag, shutdown_flag, response = self._call_command(in_line.strip())
                        if response:
                            sock.sendall(response)
                        if close_flag:
                            self.close(sock)
                        if shutdown_flag:
                            self.main_p.shutdown()
                    except Exception, e:
                        exceptionLog("Exception in socket write : " + str(e))
                        self.close(sock)
                        continue

    # parse command type, quit, kill, hlp, else
    def _call_command(self, line):
        shutdown_flag = False
        close_flag = False
        message = ''
        if len(line.strip()) == 0: line = 'hlp'

        if line.strip().split()[0].lower() in [ 'q', 'quit', 'k', 'kill', 'kil' ]:
            close_flag = True
            message = 'BYE\n'
            if line.strip().split()[0].lower() in [ 'k', 'kill', 'kil' ]:
                shutdown_flag = True
        else:
            message = self.middle_interface.command(line)
        if self.debugMode: debugLog( (close_flag, shutdown_flag, message ) )
        return (close_flag, shutdown_flag, message)
                        
    def close(self, sock):
        try: self.client_hash[sock].close()
        except: pass
        try: del self.client_hash[sock]
        except: pass
        try: self.sock_list.remove(sock)
        except: pass
        try: sock.close()
        except: pass
    
