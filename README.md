# Reading Assistant

**CS410, Fall 2020**

> Christopher Rock (cmrock2)  
> Zichun Xu (zichunx2)  
> Kevin Ros (kjros2)

<!--
### Documentation Guidelines

The documentation should consist of the following elements: 1) An overview of
the function of the code (i.e., what it does and what it can be used for). 2)
Documentation of how the software is implemented with sufficient detail so that
others can have a basic understanding of your code for future extension or any
further improvement. 3) Documentation of the usage of the software including
either documentation of usages of APIs or detailed instructions on how to
install and run a software, whichever is applicable. 4) Brief description of
contribution of each team member in case of a multi-person team.
-->

Overview
========

Problem
-------
"Information overload" is something people in today’s society are accustomed.
Most people develop methods of coping with the huge amount of information
available. We filter things through trusted sources, prioritize information that
is actionable, and change our mental model of the situation as necessary.

Earlier this year, the 2019 novel Coronavirus epidemic turned the world on its
collective head and created a flurry of information. Large volumes of text data
are expected to be consumed and acted upon in a short period of time.

For humans, initially the challenge is simply to read and understand the
documents. However the difficulty quickly becomes identifying what is new
knowledge, and remembering the source of previously seen similar knowledge. New
documents may have significant overlap with prior knowledge. Differences between
documents must be reviewed, and often the progression of changes is important.

Information retrieval, text mining, and recommender systems have developed
algorithmic strategies to identify and extract useful information from
text-based knowledge. The focus of these tools has generally been to pull
relevant documents via (search), or push potentially interesting documents (
recommender). These techniques can be modified to assist a reader in identifying
new useful information.

What is our tool?
-----------
In line with our project proposal, our overall goal was to create a reading
assistant tool that allows a user to maintain a collection of *read* documents (
reflecting the current knowledge of the user)
and then provides insight about a new *unread* document when compared to the all
read documents. Our initial idea from the project proposal was to focus on the
differences between documents, however the reality is that there were so many
ways documents could be different that this was not particularly helpful. In
this final version we instead focus on the areas of similarity betwen the unread
document from the corpus of read. This allows the user to then quickly hone in
on areas where the new document reinforce or subtly change what they had
previously discovered from the read docuements.

What can it be used for?
------------------------
Although this is created as a command line tool, as described above the initial
inspiration for this idea was the surplus of information that was being pushed
out (in our case via email) during the first months of the COVID-19 pandemic.
One way to use this tool would be to integrate it with a mail server, so that
you could forward an email or attachment and indicate that you had or had not
read the document - then the server could spit back a new email with some
analysis of the document including a list (and linke) to the other read similar
documents, as well as highlight passages (paragraphs in our case)
of particular interest.

Implementation
==============
On start-up, text documents (directory path provided by user) are loaded by the
assistant. During loading, the documents are processed and added to an inverted
index. These documents are considered to be the previously-read documents by the
user. Once the loading is complete, the assistant waits for a path to a text
file (unseen document). Given this path, the assistant ranks the previously-read
documents using the unseen document and returns the most similar read document
names to the user. We also provided methods for a user to add and remove
previously-read documents. Currently, the assistant calculates similarity using
the Okapi BM25 ranking function along with various optimization techniques,
including an inverted index. To heuristically gauge the effectiveness of this
method, each team member collected approximately 8-10 documents. These documents
were loaded as the previously-read documents, and additional documents were
provided as the unseen documents. From the preliminary examination, the results
seem promising. The code is written in a modular fashion, so that we can easily
extend the assistant to use different similarity/difference measures and
methods. In addition to document-level BM-25, we have implemented
paragraph-level BM25 which allows more detailed evaluation of unseen documents
compared to seen documents. We have also used the external library gensim to
include Latent Semantic Indexing at a document level, with document- level
similarity. This is currently a separate script and will be integrated for the
final project. Our planned extensions are discussed in the following section.

Usage
=====
We recommend using python 3.6 or 3.7, with gensim (and its dependencies), as
well as the smart_open package.

To start the reading assistant, you must first have two directories of text
files. One directory should be "read"
documents, and the other is "unread" documents. Start the program by running the
script like so:

```
python reading_assistant.py read_docs_path unread_docs_path [k1] [b]
```

`read_docs_path`   : path containing text files that have been read by the
user  
`unread_docs_path` : path containing text files that have not been read by the
user  
`[k1]`             : value for BM25. Default: 1.2 (optional)  
`[b]` : the b value for BM25. Default: 0.75

The script will load the read documents into an inverted index, and then go into
the Read-Eval-Print Loop (REPL).  
Once the REPL is running, you will be presented with a list of *Read* documents
and *Un-Read* documents. For example, you may see the following:

```
-= READ FILES: =-
    0 : covid-bhc-contact-sop-1.txt
    1 : covid-isos-brief.txt
    2 : covid-update-4.txt
    3 : covid-dod-mgmt-guide.txt
    4 : covid-update-1.txt
    5 : covid-update-3.txt
    6 : covid-bhc-pt.txt
    7 : covid-update-2.txt
    8 : covid-yoko-sop.txt
    9 : covid-fragord.txt
   10 : covid-bhc-extended-use.txt
=- UN-READ FILES: -=
    0 : covid-bhc-contact-sop-2.txt
    1 : covid-annex-1.txt
Please use one of the following commands:
  rank [unread_file_#]            --> Compares new document to previously-read documents
  read [unread_file_#]            --> add the document from the unread list to the read list
  forget [read_file_#]            --> remove a document from the read list
  view document [document name]   --> prints the document
  view paragraph [paragraph name] --> prints the paragraph
  set scope [integer]             --> only documents above this number of standard deviations above mean ranking score are returned
  exit                            --> Exits the program


```

To see the rank of the unread document **covid-annex-1.txt** you would
enter `rank 1` at the prompt.

To move a document **covid-bhc-contact-sop-2.txt** from the *unread* into the *
read* grouping, type `read 0`.

Or, to move document **covid-fragord.txt** from *read* to *unread*,
type `forget 9`.

To view the text of document **covid-yoko-sop.txt**,
type 'view document covid-yoko-sop.txt'. Note that this only works with
documents listed under READ FILES.

Similarly, to view the first paragraph of document **covid-yoko-sop.txt**,
type 'view paragraph covid-yoko-sop.txt_parag0'. Note that this only works with
documents listed under READ FILES. 

The 'set scope [integer]' command determines scope of the ranking results. As each document
and paragraph in READ FILES is given a ranking score, the [integer] determines the cut-off
of these scores. More specifically, the [integer] is the number of standard deviations above the mean
ranking score. That is, a scope of 2 means that only documents and paragraphs that are two or more
standard deviations above the mean score are returned. A scope of 0 means that all documents and paragraphs
above the mean ranking score are returned. Generally, a higher scope means fewer documents and paragraphs
returned, but these documents and paragraphs are much more relevant. 



Team Contributions
==================
All team members were active participants throughout the entire project
lifecycle process. Our team worked well together and all members contributed
meaningfully to our end result. All met via Zoom on the following days (30-60
minute meetings):

- Sep 10th: initial team meeting and plan for future meeting timeline
- Oct 3rd: draft concept of reading assistant formed
- Oct 9th: discussion of unit 1 concepts and relation to project
- Oct 21st: formalized topic and planned submission of topic to CMT
- Oct 24th: discussed status, potential roadblocks, and plan forward
- Nov 14th: reviewed TA comments and initial review of BM25 document-level
  rankings
- Nov 17th: discussed additional methods to rank articles
- Nov 29th: reviewed progress report, paragraph ranking, and formulated final
  plan for code breakdown
- Dec 6th: reviewed integration of gensim, paragraph ranking, CLI, and initial
  REPL
- Dec 11th: reviewed final product and discussed last touches necessary to
  complete project
- Dec 13th: recorded tutorial

Specific Contributions
------------------------------
All members contributed to write-ups, review of code, reviewing submission
requirements, and ensuring deadlines were met.

*Kevin Ros*:

- Created initial BM25 document-level code, with necessary ability to
  dynamically add and remove documents.
- Drafted initial documents (proposal, progress report)
- Added initial REPL interface
- Added standard deviation analysis of results to simplify interpretation of
  ranking data

*Zichun Xu*

- Created paragraph level analysis of BM25 analysis method
- Modified gensim LSI analysis for paragraph level analysis

*Christopher Rock*

- Added gensim LSI ranking methods
- Added CLI and finalized REPL

References
==========
<sup>1</sup>https://github.com/meta-toolkit/metapy

<sup>2</sup>https://tac.nist.gov/2008/summarization/update.summ.08.guidelines.html

<sup>3</sup>Andrei V, Arandjelović O. Complex temporal topic evolution
modelling using the Kullback-Leibler divergence and the Bhattacharyya distance.
EURASIP J Bioinform Syst Biol. 2016 Sep 29;2016(1):16. doi:
10.1186/s13637-016-0050-0. PMID: 27746813; PMCID: PMC5042987.

<sup>4</sup>Liu, Heng-Hui & Huang, Yi-Ting & Chiang, Jung-Hsien. (2010). A
study on paragraph ranking and recommendation by topic information retrieval
from biomedical literature. ICS 2010 - International Computer Symposium.
10.1109/COMPSYM.2010.5685393.

<sup>5</sup>https://radimrehurek.com/gensim/models/lsimodel.html