#!/usr/bin/python3

#TODO:
# Wrap up output dialog
# Clean up TK interface

import fileinput
import sys
import os
import tkinter as tk
from tkinter import filedialog 

PRECINCT_INDICATOR = "Precinct :,"
HEADERS="PRECINCT,VOTER ID,LAST NAME,FIRST NAME,MAILING STREET ADDRESS,MAILING CITY,MAILING STATE,MAILING ZIP,PHYSICAL ADDRESS,PHYSICAL CITY,PHYSICAL STATE,PHYSICAL ZIP,STATUS,PHONE,ASSIGNMENT"

def main():
    if(len(sys.argv)>1):
        readpath = sys.argv[1]
    else:
        readpath=filedialog.askopenfilename(title="Select OCVR file",
                    filetypes=(("txt files", "*.txt"),("all files", "*.*")))
    if not os.path.isfile(readpath):
       print("File {} does not exist. Exiting.".format(readpath))
       sys.exit()

    print(HEADERS)

    with open(readpath) as fp:
        for line in fp:
            if PRECINCT_INDICATOR in line:
                precinct=line.rstrip().split(",")[1]
            if (line[0].isdigit()):
                #This is a PCP record, process accordingly
                fields=list(map(strip,line.rstrip().split(",")))
                
                pcp_id=fields[0]
                lastname=fields[1][1:] #remove starting quote
                firstname=parse_firstname(fields[2])
                (ma_adr,ma_city,ma_state,ma_zip)=parse_address(fields[3])
                (pa_adr,pa_city,pa_state,pa_zip)=parse_address(fields[4])
                the_rest=','.join(fields[5:])
                pcp_record=','.join([precinct,pcp_id,lastname,firstname,
                    ma_adr,ma_city,ma_state,ma_zip,    
                    pa_adr,pa_city,pa_state,pa_zip,
                    the_rest])
                print(pcp_record)
                

def strip(s):
    return s.strip()

def parse_firstname(candidate):
    arr=candidate.split(" ")
    if (len(arr) < 4):
        return('','','','')
    if (len(arr) == 1):
        fn=arr[0]
    else:
        fn=''.join(arr[:-1])
    return fn

def parse_address(candidate):
    if (candidate==""):
        return('','','','')
    else:
        arr=candidate.split(" ")
        zipcode=arr[-1]
        state=arr[-2]
        city=arr[-3]
        address=' '.join(map(str,arr[:-3]))
        return (address,city,state,zipcode)
    

        
if __name__ == '__main__':
    main()



#Copyright 2018-2023, Michael C Smith (Mike@MikeSmithForOregon.com)
#Chair, Gun Owners Caucus (2019-), Democratic Party of Oregon
#       (https://dpo.org/caucuses/gun-owners-caucus/)
#Rules Committee Chair (2021-), Former Second Vice-Chair (2019-21), 
#and Former Technology Officer (2017-19), Multnomah County Democrats
#       (https://multdems.org/)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is furnished
#to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
