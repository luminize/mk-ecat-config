#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree


os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser(description='Extract OD values from EtherCAT slave')
parser.add_argument('-c', '--config', help='Give the name of the EtherCAT XML file to use', action='store')
parser.add_argument('-n', '--node', help='Slave node to use', action='store')
parser.add_argument('-o', '--output', help='Output filename', action='store')


args = parser.parse_args()

root = xml.etree.ElementTree.parse(os.path.curdir+'/'+args.config).getroot()

# etherlab:
# bool,
# int8, int16, int32, int64,
# uint8, uint16, uint32, uint64,
# float, double,
# string, octet_string, unicode_string.

stdtypes = {'BIT2': (2, 'bit2'),
            'BOOL': (1, 'bool'),
            'DINT': (32, 'int32'),
            'INT': (16, 'int16'),
            'UDINT': (32, 'uint32'),
            'UINT': (16, 'uint16'),
            'USINT': (8, 'uint8'),
            'SINT': (8, 'int8'),
            'STRING(31)': (248, 'string'),
            'STRING(4)': (32, 'string')}

print ('Settings in drives for slave nr %s' % args.node)
for dictobjects in root.iter('Objects'):
    # traverse all objects in the OD
    for dictobj in dictobjects:
        #for child in dictobj:
        idx = dictobj.find('Index').text
        idx = idx.replace('#', '0')
        objtype = dictobj.find('Type').text
        if type(objtype) != 'NoneType':
            #if objtype == 'Type':
                dtype = objtype
                if dtype in stdtypes :
                    # this is standard, so we know the amount of bytes
                    # do something here
                    # print ('standard type: %s' % dtype)
                    indexnamename = dictobj.find('Name')
                    if indexnamename is not None:
                        indexnamenametext = indexnamename.text
                    else:
                        indexnamenametext = 'NONAME'
                    (t, ecattype) = stdtypes[dtype]
                    print ("%s:00 - %s" % (idx, indexnamenametext))
                    command = "ethercat -p %s upload --type %s %s 0x00" % (args.node, ecattype, idx)
                    p = subprocess.Popen([ 'ethercat', '-p', args.node, 'upload', '--type', ecattype, idx, '0x00' ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    value = ""
                    errorl = ""
                    for line in p.stdout:
                        value = value + line
                    #print (command)
                    print (value)
                    for line in p.stderr:
                        errorl = errorl + line
                    #print(errorl)



                else:
                    # we have subindexes because this is not a standard type
                    #print ('non standard type: %s' % dtype)
                    print('Subindexes :')
                    for datatype in root.iter('DataType'):
                        # find the name and compare
                        dataname = datatype.find('Name')
                        if dataname is not None:
                            datanametext = dataname.text
                            if datanametext == dtype: #<Name>DT1C00</Name>
                                #print("we found a match, now traverse further")
                                for subitem in datatype.findall('SubItem'):
                                    # first see if there is a SubIdx
                                    subidx = subitem.find('SubIdx')
                                    if subidx is not None:
                                        subidx = subidx.text
                                        # there is another subindex
                                        # print(subidx)
                                        subname = subitem.find('Name').text
                                        # print(subname)
                                        subtype = subitem.find('Type').text
                                        # print(subtype)
                                        #print("%s:%s" % (idx, subidx))
                                        #st = int('11')
                                        #print("test %02x" % st)
                                        if subtype in stdtypes :
                                            # this is standard, so we know the amount of bytes
                                            # do something here
                                            # print ('standard type: %s' % dtype)
                                            (t, ecattype) = stdtypes[subtype]
                                            print ("%s:%02x - %s" % (idx, int(subidx), subname))
                                            #print ("ethercat -p 3 upload --type %s %s 0x%02x" % (ecattype, idx, int(subidx)))
                                            command = "ethercat -p %s upload --type %s %s 0x%02x" % (args.node, ecattype, idx, int(subidx))
                                            subidxstring = '0x%02x' % int(subidx)
                                            p = subprocess.Popen([ 'ethercat', '-p', args.node, 'upload', '--type', ecattype, idx, subidxstring ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                            value = ""
                                            errorl = ""
                                            for line in p.stdout:
                                                value = value + line
                                            #print (command)
                                            print (value)
                                            for line in p.stderr:
                                                errorl = errorl + line
                                            #print (errorl)



                                        else:
                                            print ("%s:0x%02x unknown type %s" % (idx, int(subidx), subtype))
                                        #
                                    else:
                                        # there is no new subindex, but there might be an array of elements
                                        # so check of there is a <Name>Elements</Name>
                                        # get the <BaseType>
                                        # find the datatype
                                        # get value of <Arrayinfo> <Elements>
                                        subitemname = subitem.find('Name')
                                        if subitemname is not None:
                                            # <Name> exist
                                            if subitemname.text == "Elements":
                                                # find the type
                                                elemtype = subitem.find('Type').text
                                                # no traverse the Datatypes again
                                                for arraytype in root.iter('DataType'):
                                                    # find the name tag and compare
                                                    dataname2 = arraytype.find('Name')
                                                    # check it exists
                                                    if dataname2 is not None:
                                                        datanametext2 = dataname2.text
                                                        # exists, now compare
                                                        if datanametext2 == elemtype:
                                                            # found it, get the Basetype, Arrayinfo and Elements
                                                            basetype = arraytype.find('BaseType').text
                                                            (u, ecatbasetype) = stdtypes[basetype]
                                                            arrayinfo = arraytype.find('ArrayInfo')
                                                            nrelements = arrayinfo.find('Elements').text
                                                # now we have the first subindex and nr of elements in the array
                                                # get the names from the array in <Object> tag
                                                for i in range (0, int(nrelements)):
                                                    #print('Printing subindex array')
                                                    # <Object>
                                                    #   <Info>
                                                    #     <Subitem>
                                                    #       <Name>
                                                    infosection = dictobj.find('Info')
                                                    subindexname = infosection[i+1][0].text
                                                    print ("%s:%02x - %s" % (idx, i+1, subindexname))
                                                    #print ("ethercat -p 3 upload --type %s %s 0x%02x" % (ecatbasetype, idx, i+1))
                                                    command = "ethercat -p %s upload --type %s %s 0x%02x" % (args.node, ecatbasetype, idx, i+1)
                                                    subidxstring = '0x%02x' % (i+1)
                                                    p = subprocess.Popen([ 'ethercat', '-p', args.node, 'upload', '--type', ecatbasetype, idx, subidxstring ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                                    value = ""
                                                    errorl = ""
                                                    for line in p.stdout:
                                                        value = value + line
                                                    #print (command)
                                                    print (value)
                                                    for line in p.stderr:
                                                        errorl = errorl + line
                                                    #print (errorl)


