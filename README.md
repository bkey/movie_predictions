Prediction Domestic Movie Box Office with Wikipedia Page View
=================

In this project I am trying to decide which actor/actress to cast in a hypothetical film that will most help the film to make money. Specifically, is there a better way to choose actors than based solely on their previous box office totals. In previous studies, it has been found that an actor or actress' previous box office success is a predicitive factor in a film's box office. (http://digitalcommons.iwu.edu/cgi/viewcontent.cgi?article=1109&context=econ_honproj, http://pages.stern.nyu.edu/~jsimonof/movies/movies.pdf) But can we quantify "star power" in a different way? In the age of the Internet, we can track users' interest in an actor/actress by more methods that box office receipts.

I am using all films from 2012-2013 except animated films and documentaries taken from the list of US films on boxofficemojo.com. Additonally, I have taken page view statistics of every actor in one of the said movies (as listed on boxofficemojo) for the years 2013 and 2013 taken from http://stats.grok.se/

I tried several models, the one that worked best was a linear regression using average page views for the 30 days leading up to a film’s release, budget and rating The prediction using the wikipedia page views performed slightly worse than the previous box office totals with r-squareds 0.614 and 0.64 respectively. However, the page views are signifcant and future work could be done to improve the model.
