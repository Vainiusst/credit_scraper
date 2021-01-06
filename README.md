# credit_scraper
A tool that I created in Python to help me automate a boring and arduous task of collecting various credit-related data (such as installment size, APR, etc.) from the Web, using Selenium.

Firstly this project began as a functional piece, however it was hard to stick to the best practices and write reusable code, so I decided to re-write it into classes for ease of use, simpler logic implementation and better functionality.

The project is now complete and functional. However, nearly every month I run it there appears to be some bugs, usually caused by the changed DOM structure of the pages. As majority of the things are hardcoded (y'know, DOM is different, behaviour of JS elements is different, so I doubt there's really any way around it), the modules are suited for that page and that page only. I guess some things could be rewritten with inheritance (cookie_monster is probably the same everywhere), I couldn't be bothered, but maybe I'll do that some time in the future. I'm just happy this works for now.
