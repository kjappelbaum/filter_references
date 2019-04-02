# filter_references

*Warning* Still buggy, still bad style, still experimental. 

experimental project to find relevant articles from a list of references using ChemRefResolver.

## Why? 
If you do a literature review and have to check a lot of references for a particular concept, it takes a lot of time, this is an attempt to do a bit of filtering to only look at the references that really contain the concept of interest. 

## How? 
The script takes a list of references you can copy and paste from an article. Mabye you have to do some simple list-comprehension-like pre-processing to remove copying artifacts. 

Then, the script uses Chemrefresolver to lookup the reference and then the script parses the website 
chemrefresolver redirects us to. Often this is only the abstract or another landing page. 
Hence, I try to implement how to get from these pages to the HTML fulltext. 

## ToDo:
- [ ] use more features of scrapy
- [ ] go to fulltext for more publishers than ACS
- [ ] save a bit more context in output
- [ ] better way of writing output, e.g. using the items in scrapy 
