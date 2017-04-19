# Data Visualization: Titanic Survivors

* Udacity Data Analyst Nanodegree: Project 6
* Author: Ke Zhang
* Submission Date: 2017-04-18 (Revision 2)

## Changes in Revision 2

* added chart explanations for each selected combinations and for distribution and survival rate charts
* distribution charts are hidden by default
* removed total frequency from the tooltip
* removed chart details from the first page.


## Final Version Website

* [Titanic Survivors (final version)](https://www.2cn.de/titanic)


## Summary

The underlying titanic data set contains demographics and passenger information from 891 of the 2224 passengers and crew on board the Titanic which was already analyzed in the [Intro to data analysis project](https://classroom.udacity.com/nanodegrees/nd002) earlier. Here in this project we want visualize the 714 data records after removing outliers and utilize the findings from the previous project and illustrate how great the influence of features 'Pclass', 'Sex' and 'Age' had on the survival chance. The attached single page application 'index_final.html' tries with several animated charts to visualize these findings.


## File Listing

- ./README.md (this file): a description of the submission
- ./index_1.html: first working version of the visualization
- ./index_final.html: final version of the visualization
- ./css/: contains css files for the visualization
- ./css/main_1.css: first version of the main project css file
- ./css/main_final.css: first version of the main project css file
- ./js/: contains javascript files for the visualization
- ./data/: data directory containing json files
	
	
## Design

This web application applies three opensource libraries to create its ui elements, construct dynamic tables and plot interactive charts. It also follows stringent discipline 
of rules taught in the udacity lecture and described on [the story telling with data](http://www.storytellingwithdata.com) website.

- As chart framework we chose solely [_dimple.js_](http://dimplejs.org) as it is powerful and flexible enough to fulfill our tasks. 
- The [semantic-ui](https://semantic-ui.com) framework defines the color scheme, design and layout of all the ui components.
- To display the data records in a table enriched with sorting and filtering options we used the [dynatable](https://www.dynatable.com) library.

At the beginning we considered using a great variety of chart types such as scatter plot, bar chart and pie chart all together on the same page. But after some thinking and discussions on the first ui mockups with friends we made the decision keep everything simple and to use bar charts only to highlight the survivorship data. 

The page has a three-part vertical layout made up of header, main and footer sections. The page navigation is attached aside the title in the header section. It allows readers to go forward or switch back in the story line. The footer lists useful information the links. In the main part the story line itself is again divided into three steps:

- The first step introduces the readers the background story and describes the underlying data.
- The visualization is in the second step. In the center of the page are bar charts representing the distribution and survival rates of the selected categories such as sex, age and ticket class. The selection bar for categories is placed above the charts. In the charts, the _x_-axis represents the different categories of passenger information and depending on the selected scenario its _y_-axis displays either the relative fequencies or the survival ratio of the chosen categories. The _y_-axis was omitted since points are labeled directly. And the chart contains when necessary a legend explaining the color coding and explanation of the groups. 
- In the last step readers can dig into the simplified data and search or validate the data themselves.


## Feedback & Changes

Feedbacks are made during the various stages of the web application from the sketch phase to the final review. In the following we lists three of them and documents the subsequent changes made the implementation.

**Feedback 1** (Sketch Phase):

> The story line isn't made clear in the writeup. There are too many chart types and features used in the visualization. Readers spend to much time just try to understand what the different chart types are representing.

Changes made after first feedback:

- uses bar chart consequently and standardized color coding to fixed colors
- only use the three main features: sex, age and ticket class
- simplified the csv data and reduced columns on the dynamic table

**Feedback 2** (First Version):

> The web application looks nice and is interactive. But there could be a bug. Sometimes I didn't see any changes after selecting the categories. Maybe there's an update problem. It's preferable to not only have the title in the single charts but also a main title above all charts describing which categories are actually selected.

Changes after feedback 2:

- refactored code and moved all chart related functions to a separate javascript file.
- added a chart title below the selection box

** Feedback 3** (First Version):

> I think readers are actually more interested in ratios than in absolute numbers. I would like to see percentages of survival or at least in the tooltips. Another issue are the colors for 'survived' and 'died'. The aim of the story is to find out which group had more chance to survive. I would emphasize and hightlight **'survived'** and weaken the number of passengers 'died' by changing the colors. And if it's possible I want more lively fonts in the charts to compensate the tragic story.

Changes after the third feedback:

- changed the scaling of the y-axis from absolute to relative ratios
- added tooltip to show the absolute and total frequencies
- changed colors for 'survived' and 'died' to 'lime green' and 'light grey'
- changed font type used in the charts to 'Shadows Into Light'


** Feedbacks after final version and future works ** (Final Version):

> I played with several combinations of categories. Sometime more than 6 charts are displayed vertically rather than plotted in a matrix layout like usually utilized in the matplotlib.
> I changed the categories and all previous charts disappeared suddenly and the new charts were then created afterwards. A better user experience would be a more smooth transition between these changes by reusing existing visuals and advocating more animations instead of creating the new chart objects every time.

Open issues on the final version and future works:

- It was too time consuming to add the multi plots feature. All plot functions, font sizes and svg elements had to adjusted to fit into a matrix layout. I have tried to implement like in the _dimplejs_ [advanced trellis bar exmaple](http://dimplejs.org/advanced_examples_viewer.html?id=advanced_trellis_bar). Unfortunately it didn't work due to some layout problems like placing the on-screen ratios and legends. I'll embed this feature when _dimplejs_ has better matrix layout support later.
- The reuse of existing charts was also hindered by the dimplejs update issues. There was too little benefit to make a clean solution for reusing charts with different scales and categories. The simplest way to refresh the charts was to create a new one.
- In the current version I used prepared static csv files to load the survival data. On the market there are lots of serverside and even clientside data filtering/querying/grouping libraries like python pandas. 


## Resources

- [Udacity Website](https://www.udacity.com)
- [Story telling with data Website](http://www.storytellingwithdata.com)
- [Dimple.js Documentation](http://dimplejs.org) (MIT License)
- [Semantic-UI Documentation](https://semantic-ui.com) (MIT License)
- [Dynatable Documentation](https://www.dynatable.com) (LGPL)
- [Titanic Dataset](https://www.kaggle.com/c/titanic)


