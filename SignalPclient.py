##
## Usage:
## python SignalPclient.py <File.fast>
##

## Importing libraries
import sys, time, math
from pyfasta import Fasta   # Interface to easily read fasta files
from twill import commands  # This will make possible go through the web


## Setting parameters

# Threhsold on the number of proteins per files. If a file contains more than that,
# it will be divided into smaller files.
numProteinsPerFile = 5

# Everything entry that is longer than the threshold below will be discarded.
lineLengthThreshold = 9000


## Get the fasta name file from the command-line
inputfilename = sys.argv[1]
print 'Input fasta file: ', inputfilename

# Parsing the prefix of the input file to use it later
parsedInputFile_prefix = inputfilename.split('.fast')[0]

## Reading the input file
print 'Loading fasta file...'
f = Fasta(inputfilename)

## Getting all keys
KEYS = sorted( f.keys() )

records2Discard = {}
goodRecords     = {}


# We now split them into two dictionaries depedinding on their
# size.
for j in KEYS:
    print len( f[j] )
    if len( f[j] ) > lineLengthThreshold:
        records2Discard[ j ] = f[j]
    else:
        goodRecords[ j ] = f[j]

# Writing back to hard disk our results
filewLongRecords = open(parsedInputFile_prefix + '_discarded_longLines.fasta', 'w')
for j in sorted(records2Discard.keys()):
    filewLongRecords.write('>' + j + '\n')
    filewLongRecords.write(str(records2Discard[j]) + '\n')
filewLongRecords.close()


# Since there's this limitation of 2000 proteins per file in
# the server, we'll equaly distribute them into several files

# Number of proteins
numProteins = len( sorted(goodRecords.keys()) )

# number of files
numFiles    = int( math.ceil(
                    float(numProteins) / float(numProteinsPerFile) )
                    )

print 'Number of auxiliary files: ', numFiles

resultingFileNames = []

# Creating each of the files
for k in range(0, numFiles):

    # Specific file name
    resultingFileNames.append( parsedInputFile_prefix + '_SignalPclient_auxiliary_' + str(k) + '.fasta' )

    # Creating the file
    print 'Creating file ' + resultingFileNames[-1]
    currFile = open( resultingFileNames[-1] , 'w')

    # Iterating through the proteins that will be stored in currFile
    for j in sorted(goodRecords.keys())[ numProteinsPerFile*k : numProteinsPerFile*(k+1) - 1 ]:
        currFile.write('>' + j + '\n')
        currFile.write(str(goodRecords[j]) + '\n')

    # Closing the file
    currFile.close()



## Sending over the internet

# For each file created in the last step, we want to submit to
# the SignalP web app, wait for the results and save it in our
# hard drive.

# for fastafilename in resultfilenames:
#
#     inputfile = open( fastafilename , 'r' )
#     inforead = inputfile.read()
#
#
#     # First steps...
#     print 'Accessing the web app and filling the form...'
#
#     # Going to the web app page
#     commands.go('http://www.cbs.dtu.dk/services/SignalP/')
#
#     # Setting up a few options
#     commands.fv('2','SEQPASTE',inforead)
#     commands.fv('2','graphmode',[''])
#
#
#     # Submiting the appropriate form
#     print 'Submiting the form'
#     commands.submit('13')
#
#
#     # Guessing now the job id
#     a = commands.show()
#     b = a.split('\n')[2]
#     jobid = b.split('of')[1].split('</span')[0].strip()
#
#     # Constructing the url with the results...
#     url2go = 'http://www.cbs.dtu.dk//cgi-bin/webface2.fcgi?jobid=' + jobid
#     print 'Our results are in ' + url2go + '\n\n'
#
#     # Waiting a bit for the results...
#     print 'Waiting some moments for the server to complete our request!'
#     time.sleep(5*60)
#
#     # This timing has actually two purposes: while the results are being
#     # calculated, the script will be quiet. But also, there will be some
#     # time after the results are ready so that the server won't go overloaded.
#     # Please, do not overload the server using this script!!
#
#     # Going after the results...
#     commands.go(url2go)
#
#
#     # Following the link for the result file
#     commands.follow('processed fasta entries')
#
#     # Saving the result in the hard drive
#     commands.save_html( fastafilename.split('.fasta')[0] + '_RESULT.fasta' )
#
#
#
#
# # The end, my friend.
