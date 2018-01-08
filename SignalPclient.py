## Importing libraries
import sys, time, os
from pyfasta import Fasta   # Interface to easily read fasta files
import MechanicalSoup



class signalPclient:

    ## URL address of the signalP Server
    self.signalPserver_url = 'http://www.cbs.dtu.dk/services/SignalP/'

    def __init__(self,
                    input  = inputFileName,
                    output = outputFileName):

        ## Setting the input/output files
        self.inputFileName  = inputFileName
        self.outputFileName = outputFileName


        ## Setting parameters

        # Threhsold on the number of proteins per files. If a file contains more than that,
        # it will be divided into smaller files.
        self.numProteinsPerFile = 2000

        # Everything entry that is longer than the threshold below will be discarded.
        self.lineLengthThreshold = 9000



        return


    def submit( self ):

        ## Parsing and filtering the input file
        filtered_fasta = self.getFilteredFASTA( self.inputFileName )

        ## Submitting the filtered databank
        self.submit2( filtered_fasta )

        return


    ##
    ## Parsing the input file and filtering it
    ##

    # The following methods parse the input file and ensures
    # the following criteria:
    # > each protein has sequence_length < 6000
    # > total of 2000 proteins in fasta file

    #
    #
    #
    def getFilteredFASTA(self, fasta_file):
        protein_list = get_FASTA_array(fasta_file)
        submission_list = generate_submission(protein_list)
        FASTA_TO_SUBMIT = "".join(submission_list)
        return FASTA_TO_SUBMIT

    #
    #This function parses fasta file into array (each protein is one element)
    #
    def getFastaArray(fasta_file):
        #parsing FASTA
        FASTA_string= open(fasta_file, 'r').read()
        #rough list of proteins
        protein_list= FASTA_string.split(">")
        #loop to remove empty elements
        while "" in protein_list:
            protein_list.remove("")
        #add header to each protein
        new_protein_list = [">" + protein for protein in protein_list]

        return new_protein_list


    #
    # This method generates a new file ready to be submitted.
    #
    def generateSubmission( protein_list ):

        #declare submission list
        submission_list = []
        total_AA_count = 0

        #loop through each protein and count AA and add to list of submissions
        for protein in protein_list:

            #parse individual protein to get sequence
            single_protein = protein.split("\n")
            #remove blanks
            while "" in single_protein:
                single_protein.remove("")


            ## COUNTING SEQUENCE LENGTH

            sequence_array = []
            for element in single_protein[1:]:
                sequence_array.append(element)

            # get sequence length
            sequence_string =  "".join(sequence_array)
            sequence_length = len(sequence_string)
            total_AA_count = total_AA_count + sequence_length

            ## FILTERING STEPS

            if sequence_length < 6000:
                submission_list.append(protein)
            #count total AA and stop if > 200,000
            if total_AA_count > 199999:
                return submission_list
            #count the number of proteins and check if lower than 2,000
            if len(submission_list)>1999:
                return submission_list

        return -1


    ##
    ## Accessing the server and submiting the job
    ##

    def submit2( generatedFile ):

        ## Accessing signalP Server's home page
        # Creating a browser object
        self.browser = mechanicalsoup.StatefulBrowser()
        # Setting the address
        self.browser.open( 'http://www.cbs.dtu.dk/services/SignalP/' )
        # Selecting the form (nr=0 is a useless form)
        browser.select_form( nr = 1 )
        # Uploading input file
        browser['SEQSUB'] = generatedFile

        ## Submiting the file for analysis
        browser.submit_selected()

        ## Sleeping for 5min to wait for the results...
        # -- this step needs to be improved: we should check
        # for results every n seconds instead.
        time.sleep(300)

        # Open current page (becomes wait page) and
        # extract URL with the analyses' results
        resultsURL = str( browser.get_current_page().select('noscript') ).split()[7][6:-7]
        # Accessing the webpage with the results
        browser.open( resultsURL )


        ## Extracting the signal peptides

        # array to save the signal peptides found by signalP Server
        results = []

        # extract result lines, check if there is a signalling sequence, if yes, pass line to results
        for res in browser.get_current_page().select('p'):
            if 'YES' in str(res):
                results.append(str(res).splitlines()[7])


        # Save the output to file
        with open(self.outputFileName, "w") as text_file:
            text_file.write("Signal peptide positive: %s" % results)


        ### -- this is a great idea, but we need to work on it
        # # in case you are interested in all proteins
        # total = []
        # for res in browser.get_current_page().select('p'):
        #     total.append(str(res).splitlines()[7])
        #
        # with open("OutputTotal.txt", "w") as text_file:
        #     text_file.write("All: %s" % total)
        ### --

        return


## The end, my friend.
