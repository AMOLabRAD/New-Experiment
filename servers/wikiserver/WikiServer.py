"""
### BEGIN NODE INFO
[info]
name = WikiServer
version = 1.0
description = 
instancename = WikiServer

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

import os, re, sys
import labrad
from labrad.server import LabradServer, setting, Signal
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

class WikiServer(LabradServer):
    """
    WikiServer for pushing data to wiki
    """
    name = 'WikiServer'
    
    @inlineCallbacks
    def initServer(self):
        try:
            yield self.client.registry.cd(['','Servers', 'wikiserver'])
        except:
            try:
                print 'Could not load repository location from registry.'
                print 'Please enter Wiki directory or hit enter to use the current directory:'
                DATADIR = raw_input( '>>>' )
                if DATADIR == '':
                    DATADIR = os.path.join( os.path.split( __file__ )[0], '__data__' )
                if not os.path.exists( DATADIR ):
                    os.makedirs( DATADIR )
                # set as default and for this node
                print DATADIR, "is being used",
                print "as the data location."
                print "To permanently set this, stop this server,"
                print "edit the registry keys"
                print "and then restart."
            except Exception, E:
                print
                print E
                print
                print "Press [Enter] to continue..."
                raw_input()
                sys.exit()
        self.maindir = yield self.client.registry.get('wikipath')
        self.maindir = self.maindir[0] + '/'

    @setting(21, 'Update Wiki', sourcefile='s', destinationfile='s', returns='')
    def update_wiki(self, c, sourcefile, destinationfile):
        yield os.system("cp " + (self.datadir + sourcefile).replace(" ","\ ") + " " + (self.maindir + self.wikidir + destinationfile).replace(" ","\ "))
        yield os.chdir(self.maindir)
        print os.getcwd()
        yield os.system("bash updatewiki.sh")
        
    @setting(22, 'Add wiki directory', wikidir='s',returns='')    
    def set_wiki_dir(self, c, wikidir):
        self.wikidir = wikidir 
     
    @setting(23, 'Add data directory', datadir='s',returns='')    
    def set_data_dir(self, c, datadir):
        self.datadir = datadir + '/'


if __name__ == "__main__":
    from labrad import util
    util.runServer(WikiServer())