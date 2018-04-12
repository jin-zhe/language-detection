# Language-detection
*A Python language detection module for Malay, Bahasa Indonesia and phoentic Tamil*

## Running it
`$ python build_test_LM.py -b input.train.txt -t input.test.txt -o input.predict.txt`

## How it works
The module first needs to learn the langauges by building the respective 4-gram language models with add-1 smoothing. This training file is provided as **input.train.txt**. It basically comprises of lines of each language with the first word of each line indicating the correct langauge.

Provided with a test file **input.test.txt** with lines for various NL syntax, this module then predicts whether the text is Indonesian, Malaysian, phonetic Tamil, or some other language. For instance, given the following three lines:

*Semua manusia dilahirkan bebas dan samarata dari segi kemuliaan dan hak-hak.*  
*Semua orang dilahirkan merdeka dan mempunyai martabat dan hak-hak yang sama.*  
*Maitap piiviyiar cakalarum cutantiramkav piakkiaar*

The module will prepend the respective langauges predicted to each line and produce the output file **input.predict.txt** which will look like the following:

*malaysian	Semua manusia dilahirkan bebas ...*  
*indonesian	Semua orang dilahirkan merdeka ...*  
*tamil	Maitap piiviyiar cakalarum cutantiramkav piakkiaar ...

## Some notes
**The current implementation is based on character-based n-grams. Would character-based n-grams perform better?**  
I think it really depends on what we are trying to achieve. I.e. what do we mean by 'performing better'

Token-based n-gram models should perform much better when it comes to differentiating between languages which share a huge set of common vocabulary but have different usage patterns. For example, the task of differentiating between old Elizabethan English and modern English would very well require word token-based n-gram models. However, in order for a token-based n-gram model to realize its fullest potential, the training set must ideally be so large that it could exhaustively cover most if not all possible n-gram word tokens (all possible n-word permutations) in the given language. From a computational standpoint, this is not very feasible because it results in time and space complexities in the order of |V|^n where V is the immensely huge set of all normalized words in the given language. Thus, token-based n-gram models are not expected to perform well in terms of efficiency and it should be reserved for applications which are not time-sensitive.

On the other hand, for any alphabetic languages systems, character-based n-gram models will have a computational complexity of |26|^n  (assuming English alphabet size). Comparatively, this is much better in terms of feasibility. A character-based n-gram model assumes that the language structure follows certain characteristic sequences. This assumption is very sensible and valid for most if not all alphabetic languages. For character-based n-gram models, we shouldn't need too large a set of training data because characteristic alphabetic sequences in the language should be sufficiently prevalent in a smaller set of text. Hence, if we are looking at small training data and want a computationally efficient method to detect a language with reasonable accuracy, a character-based n-gram approach is the clear winner.

**The current training set comprise of equal data to build each language model. What happen if we increase it and what would happen if the distribution of training data is uneven?**  
If a larger set of training data is provided for each language model, overall performance should improve in general because of increased statistical significance in the learning process, which in turn brings about more accurate probabilities evaluated for each n-gram. I.e. we get a much more accurate probability of an n-gram appearing in the given language. The increased probabilistic granularity as a result of that would greatly help in the task of differentiating between 'close languages' such as Malaysian and Indonesian.

However if we only provided more data for a single language, for example Indonesian, the prediction performance will suffer due to add-1 smoothing because over-smoothing would result within the models of other languages. I.e. Malaysian and Tamil dictionaries would be dominated by new Indonesian n-grams which has a count of 1, which is close to their inherent average counts due to smaller training data sets. A fix for this issue is perhaps to use a smaller smoothing weight, for e.g. an add-0.01 smoothing depending on how much larger is the training set for Indonesian

**Can the n-gram size be varied? How would it affect performance?**  
Detection accuracy should greatly decrease as we approach a unigram model, where we end up predicting the language at the alphabetic level. Since the all 3 languages in the current implementation uses alphabets, using unigrams defeats the purpose by ignoring the uniqueness of the language which is characterized by the distinct sequences of letters. This is analogous to having insufficient context when we use a bigram model to predict the likelihood of a language in producing a given phrase.

However as we increase the n-gram size, we should expect detection to be more accurate as we would be able to capture the distinctiveness of the language's words very well and also have good context for prediction. The only drawback to this would be the exponential computational complexity.

## Future developments
Both **input.train.txt** and **input.test.txt** can be modified to predict different sets of langauges
