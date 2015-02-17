# Language-detection
*A Python language detection module for Malay, Bahasa Indonesia and phoentic Tamil*

##Running it
`$ python build_test_LM.py -b input.train.txt -t input.test.txt -o input.predict.txt`

##How it works
The module first needs to learn the langauges by building the respective 4-gram language models. This training file is provided as **input.train.txt**. It basically comprises of lines of each language with the first word of each line indicating the correct langauge.

Provided with a test file **input.test.txt** with lines for various NL syntax, this module then predicts whether the text is Indonesian, Malaysian, phonetic Tamil, or some other language. For instance, given the following three lines:

*Semua manusia dilahirkan bebas dan samarata dari segi kemuliaan dan hak-hak.*  
*Semua orang dilahirkan merdeka dan mempunyai martabat dan hak-hak yang sama.*  
*Maitap piiviyiar cakalarum cutantiramkav piakkiaar*

The module will prepend the respective langauges predicted to each line and produce the output file **input.predict.txt** which will look like the following:

*malaysian	Semua manusia dilahirkan bebas ...*  
*indonesian	Semua orang dilahirkan merdeka ...*  
*tamil	Maitap piiviyiar cakalarum cutantiramkav piakkiaar ...

##Future developments
Both **input.train.txt** and **input.test.txt** can be modified to predict different sets of langauges. Work is currently in the pipeline to collect training data which would cover most languages represented in Unicode 
