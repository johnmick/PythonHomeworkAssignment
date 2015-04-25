Backend Python Engineer homework
--------------------------------

####Task: 
Design and develop a program that robustly processes site operator/visitor data into site activity summary.

----------

####Input: 
A '\n' delimited, JSON Encoded, log file of two types.

####Output:
A sorted summary of the **number of unique visitors and operators** along with the **number of chat messages and e-mails** per site on **stdout**.

----------

####Requirements:
**JSON encoded input data** ([format details](https://gist.github.com/jzellner/856fd143323f3cba4773)) and **Python**.

----------

####Usage Example:
Process "**input_data/big_input"** site data into summaries and validate output using **"output_data/big_output"** as comparison:

*Instructions relative to root directory of repository, assuming data files are available at given paths.*

**Direct single-threaded approach implementation (stable):**
 
     python single_threaded_approach/main.py      \
              -f input_data/big_input             \
            > output_data/big_output;             \
     python test_scripts/validate.py
 
**Extendable pipeline approach implementation (experimental):**
 
     python pipeline_approach/main.py             \
              -f input_data/big_input             \
            > output_data/big_output;             \
     python test_scripts/validate.py
 
*Note: Pipeline implementation currently provides no fault recovery.*
 
 ----------
 
####Command line help:
 
     python single_threaded_approach/main.py -h
     python pipeline_approach/main.py -h

----------

####Currently tested with: 
OSX Yosemite and Fedora using Python 2.7 

----------

####Thoughts:

**Problem domain:**  The idea of reading input streams over various protocols, decoding formats, and processing data to support customer informational awareness is a really fun issue to consider as the solutions find endless domains of data to explore.
 
**Requirements:**  The process begins by understanding both the exact customer requirements as well as the theme of the [assignment ](https://gist.github.com/jzellner/856fd143323f3cba4773).  Repeated readings and brief sketches and outlines of your own aide in reducing the risk of not capturing the requirements in full.  While capturing requirements, developers establish a shared understanding of expectations (which developers plan for exceeding) and requirements.
 
**Drafting:**  With the problem well understood software designs are sketched on paper representing module components with their roles and information flow.  Considerations for both the direct problem requiring a solution and generalizations are kept in mind.  

**Some state at some time:**  With a satisfying draft diagram, attention may now be directed to customer specific data and informational needs.  How do these needs relate to the data available as an input to the system?  Each customer data requirement is a function of some data available from the input system; otherwise some new input must be formulated or need re-evaluated.  

 For each given customer need, once identified, the behavior of the input parameters is considered.

 - Each site stores timestamped buckets of **messages** along with a unique set of visitor ids.

 - Each site contains a time indexed list of **operator actions** recording operator ids and online/offline actions by time.
 
Due to the unordered nature of the input stream the software must maintain data to determine the website state for any given point.  With the state of the website known by time we look at the two message types possible:

 - A new visitor message may be evaluated against the existing state
   system of a given site.  Online sites receive chats, offline sites send e-mails.

 - A new operator message is used to update the state system of a site.  If the state system changes  data reductions dependent on site state are adjusted.


**Whelp, time to code:**
 A single threaded implementation is produced where emphasis is placed on defining each small problem of the task into contained function definitions.  Clearer identification of functional data contracts and tests are formed in this phase.  The program is brought to a point of the target output but need not be correct in all test cases yet.
 
**Testing:**
 A simple validation script is written to compare generated outputs against target output.  Small individual site data files are used first.  Once correct, the largest dataset available is passed through the system to identify failing edge cases.  Test failures are examined individually by creating new input/output test cases which capture only the observed pattern to cause the failure.  Reiteration and reconsideration of code / identification of bugs drives the implementation to a more correct form.
 
**Robustness:**
 The user may control the frequency in which the software stores binary data allowing resumption on in the event of failure.  Currently this may defined as:
 `number of messages processed between each save state`
 
 When the time comes to save:
  
  1. The software pauses processing and writes a new binary file to a temp folder **".homeworktmp"**
  2. Once written the file is used to replace any existing old save state.
  3. Lastly the seek play-head on the input_stream is saved in a separate **".last_processed"**
 
In the event of subsequent starts, from either an abnormal shutdown or successful execution, the software first attempts to resume state by using these temporary files. The temporary files may be cleared using the **clear_cache** flag.
 
**Stress Testing Robustness:**
To test software robustness a stress script is developed which initializes the software with pseudorandom save frequencies and terminates the process pseudorandomly.


**How to Stress Test:** Remember to clear the cache directory if you wish to start a fresh test.
 
 `./test_scripts/stress-test-single-threaded-approach.sh`
 
  

----------

####Closing Thoughts:
   

 Inspired by logstash and distributed systems, the framework of breaking problems into generalized pipelines of **inputs -> processors -> outputs** motivated my curiosity to implement a Pipeline framework in Python.
 
 The Pipelining chain was something I previously explored and was familiar with putting together.

 The homework assignment was a perfect excuse to try a pipeline approach out.  The pipeline approach provides a flexible approach towards manipulating the data while coming at the cost of some additional processing time.  

 Continued efforts would look towards optimizing this model and distributing it between machines using configurable protocols for transport.  By providing distribution methods, scaling designs could be tested.
 
 This was a really fun assignment with a nice set of it items on the table for consideration!  
 
 All the best!
   - John Mick
