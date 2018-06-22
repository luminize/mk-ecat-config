start the configuration by giving an XML file to show the LCEC component the network topology and setup:
`./run.py -c ethercat-config-test-joint6.xml`

for extracting data from devices you need to have the XML file with types and object dictionary.
`./extract-OD-values.py -c=IS620N-Ecat_v2.3.xml -n=4 > out4.txt 2>&1`