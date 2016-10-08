## stoxsnschulz Readme

Stox S.N. Schulz presents data from the Amsterdam Stock Exchange in a way not found elsewhere. For more information, see \templates\about_content.html. 

Stox S.N. Schulz is not a person, as far as I know. It's just a peculiar way of spelling 'stocks essentials'. 

The project is mainly intended to learn-by-doing Python-for-web, in particular screenscraping, Flask, Ninja, HMTL, CSS, and whatever comes up getting it working like I want to.  

The project has two sections: 

1. a screenscraper/data reshuffler, to run once each working day after about 17:20 CET. 

    - ud.py (for *U*ps and Downs) reads all 75 AEX, AMC, AScX stocks, plus couple of interesting numbers about them, from three tables on www.beleggen.nl.   
    - hilo.py reads 52 week _HI_gh and _LO_w from each individual stock page, also on www.beleggen.nl. A few extra parameters are calculated for each stock. 
    - ud.py calls hilo.py, and then outputs five shortlists as pickles in the pickles-directory; it also writes the shortlists, nicely formatted, to the console (or to a file if redirected). 
    
2. a minimal Flask app that reads the pickles and presents them on a web site. The site has just two pages: 

    - a page with the shortlists
    - an about page. 
    
### License

The software in this project is in the public domain. Anyone can use it, in part or as a whole, to do whatever you want with it - except for commercial purposes. 

### todo?

- auto-tweet facility to announce updates
- views counter
- determine how to let response come in
