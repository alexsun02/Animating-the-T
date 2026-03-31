# Victor Li Reflection
## Question 1
Animation A shows daily average actual travel time dipping slightly on February 23, 
with the scheduled travel time dipping as well but slightly less. This is misleading 
because the dip actually reflects fewer stop segments surviving the cleaning process 
per trip during the storm, which lowers the summed travel time rather than indicating faster trains. 
Animation B's heatmap is more insightful, showing the northern above-ground stops (Malden Center, Wellington)
and both terminal stations 
(Oak Grove, Forest Hills) warming noticeably on February 23, while the underground downtown core 
(State, Downtown Crossing, Chinatown) barely changed. Stony Brook also spiked on the 23rd. 
This pattern makes sense: above-ground and terminal stations are more exposed to snow and wind. 
By February 25, the heatmap columns return to their typical color pattern.
This all suggests service recovered within about two days.

## Question 2
The scheduled_travel_time field is null when LAMP can't match a real-time trip to a planned GTFS schedule. 
This happens more on storm days when the MBTA runs non-standard service. In the acquisition layer, 
these nulls are dropped before summing scheduled segment times per trip. This means the scheduled average on 
storm days is based on fewer and potentially non-representative trips. The chart reflects data completeness 
as much as actual performance, which is important context for interpreting it.

## Question 3
Layer separation was most helpful when debugging the heatmap pivot table. 
I could run model.py standalone, print travel_by_stop_and_day, and verify station ordering and values without 
launching any animation or waiting for frames to render. One annoyance was passing three separate DataFrames 
into the model felt redundant since they all derive from the same source, but computing trip aggregations inside 
the model would have violated the layer boundary.

## Question 4
I primarily used Claude as a debugging assistant, not as a primary programming agent. I'd write out most of what I
wanted to do, leaving a couple blanks for Claude to fill if I was unsure or unconfident on implementation. 
This method of programming was largely successful and I mostly didn't need to change Claude's output. The only 
time it was necessary was for the heatmap coloring as there was a massive outlier on the 8th of February throwing off
the entire color scale. I solved this by using a lower/top percentile instead of a min/max.
Additionally, Claude was used to write some comments/documentation after everything was done.

# Alex Sun Reflection
## Question 1
Animation A shows that the storm around February 23–24 affected the Orange Line, but the effect is a little hard to interpret from the line chart alone. The actual travel time stays somewhat elevated around that period, but it does not spike as dramatically as someone might expect from a storm. Part of that is because the average is being taken across available trips, so the line does not capture every kind of disruption equally. Animation B makes the impact much clearer. The stops that seem most affected are near the ends of the line, especially Oak Grove, Malden Center, and Forest Hills, where the colors become warmer around February 23–24. Stony Brook also stands out as more affected than many of the downtown stops. In contrast, stations like State, Downtown Crossing, and Chinatown look more stable. By around February 25–27, most of the heatmap colors move back toward their usual pattern, so it looks like service recovered within a couple of days.

## Question 2
The scheduled_travel_time field has missing values on storm days because the MBTA was running non-standard service, so some real trips no longer matched the normal planned schedule. In the acquisition layer, I kept those rows when cleaning the data overall because they were still valid for actual travel-time analysis. However, when computing scheduled trip totals, I dropped rows where scheduled_travel_time was null before summing by trip. This means the scheduled average in Animation A is based only on the subset of trips that still had schedule information. Because of that, the scheduled line during the storm is not a complete picture of the system and should be interpreted more cautiously than the actual line.

## Question 3
Layer separation helped a lot when I was building the acquisition layer and later testing Animation A. Once acquire.py was working, we could run model.py separately and verify the dates, stop list, and aggregated values before touching any animation code. That made debugging much easier because it was clearer whether a problem was coming from the data pipeline or from Matplotlib. One part that felt slightly annoying was dealing with both station IDs and readable station names. The raw data used parent station IDs, but the assignment wanted station names, so we had to be careful about which representation belonged in which layer.

## Question 4
I used ChatGPT to help with code structure, debugging steps, and some of the animation setup. Overall it was useful, especially for helping me move through errors faster and think about how to organize the acquisition layer. However, I still had to test everything myself, fix environment issues like missing pyarrow and ffmpeg, and make sure the outputs actually matched the assignment requirements. I also had to correct details such as station naming and Git issues with generated files.
