# kinda-sorta
Kinda-Sorta is an alternative approach to resource discovery within a museum's collection. Rather than ask users what they are looking for, it starts with a single object and asks the user what aspects of that object are important to them. They can adjust how important those facets are and it will then suggest similar objects using those criteria (the algorithm is still under development). 

The inspiration for this project came from previous work on Serendip-o-matic as well as discussions with colleagues about 'user driven relevancy''. 

Many museums provide some mechanism for users to see 'related' objects from an object page. These are valuable because they allow users to click through and explore the collection further. However, these approaches has several limitations which kinda-sorta seeks to solve. 


Issues with existing approaches
--------------------------------
1. They are one-dimensional. The Walters provides several ways to explore objects which have in common a single data point (creator, medium, geography, location)
2. They don't reflect *my* values
3. They are a black box
4. They are static **

Improvements from kinda-sorta
------------------------------
1. Multi-dimensional 
2. Reflect the relative importance of one aspect over another
3. Dynamic 

# Status
The project on not currently running on heroku because I needed to take the Solr server offline 
