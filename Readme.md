# Python Client for the SignalP Server

<img src="resources/qcbCollaboratory_logo.png" height="50"/>

signalPclient is small Python module that automates the submission of a sequence databank to ServerP 4.1 Server, a web service that detects and predicts the cleavage points of signal peptides for Gram-positive prokaryotes, Gram-negative prokaryotes, and eukaryotes. SignalP Server is hosted by the Center for Biological Sequence Analysis at the Technical University of Denmark (DTU):

http://www.cbs.dtu.dk/services/SignalP/

We started developing signalPclient during the [Python Hackathon](https://github.com/thmosqueiro/UCLA-Collaboratory_Hackathon/blob/master/Materials_Resources/Problem-4/Readme.md), hosted by the [QCB Collaboratory](https://qcb.ucla.edu/collaboratory/) at UCLA. SignalP Server was originally proposed on a [Nature Methods paper](https://www.nature.com/articles/nmeth.1701) by TN Petersen, S Brunak, G von Heijne and H Nielsen.


<img src="./resources/scheme_signalPclient.png" width="600" />


## How to install and use

If you have pip, you can install signalPclient using:
```
pip install git+https://github.com/thmosqueiro/signalPclient
```
Otherwise, you can download signalPclient and use run its setup script. To download it, simply click [here](https://github.com/thmosqueiro/signalPclient/archive/master.zip). After unzipping the file, navigate to the unzipped signalPclient directory and run:
```
python setup.py install
```

If you have a fasta file ```databank.fasta``` with sequences that you want to submit to SignalP Server, run:
```
import signalPclient
signalPclient.submit(databank.fasta)
```


## Dependencies

Other than the standard Python libraries, signalPclient only requires:

* pyfasta
* Mechanize (Python 2) or MechanicalSoup (Python 3)


## People involved

* Xiaofei Lin
* Anela Tosevska
* Cheng Chen
* Thiago Mosqueiro


## License to use

Feel free to use this Python script for free, as long as you comply with the [MIT license](./LICENSE).
