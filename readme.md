## stoxsnschulz Readme

Stox S.N. Schulz presents data from the Amsterdam Stock Exchange in a way not found elsewhere. For more information, see \templates\about_content.html. 

Stox S.N. Schulz is not a person, as far as I know. It's just a peculiar way of spelling 'stocks essentials'. 

The project is mainly intended to learn-by-doing Python-for-web, in particular screenscraping, Flask, Ninja, HMTL, CSS, and whatever comes up getting it working like I want to. It also presents an overview that I wanted to see regularly, and couldn't find anywhere else. 

The project has two sections: 

1. a screenscraper/data reshuffler, to run once each working day after about 17:20 CET. 

    - `ud.py` (for **U**ps and **D**owns) reads all 75 AEX, AMC, AScX stocks, and a few interesting numbers about them, from various public web pages. `ud.py` calls `hilo.py`
    - `hilo.py` reads 52 week **HI**gh and **LO**w from each individual stock page, also from various public web pages. A few extra parameters are calculated for each stock. 
    - When all data is collected, five shortlists are computed, and then stored as pickles. They can also be output to the console, nicely formatted (or to a file if redirected). 
    
2. a minimal Flask app that reads the pickles and presents them on a web site. The site has just two pages: 

    - a page with the shortlists
    - an about page. 
    
### License

The following license applies to the entire Stox S.N. Schulz project 

Copyright 2016 Rolf Blijleven

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

