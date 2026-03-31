
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
The scheduled_travel_time field is null when LAMP can't match a real-time trip to a planned GTFS schedule/ 
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