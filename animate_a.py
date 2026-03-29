"""
animate_a.py

Animation A for MBTA subway line analysis

This animation shows two lines building day by day across February 2026:
- daily mean actual travel time
- daily mean scheduled travel time

The animation takes only computed fields from the SubwayLine model
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from model import build_model

def update(frame, x_values, dates, actual_values, scheduled_values, actual_line, scheduled_line, title_text):
    """Update both lines up to the current frame"""
    current_x = x_values[:frame + 1]
    current_actual = actual_values[:frame + 1]
    current_scheduled = scheduled_values[:frame + 1]
    # Update lines
    actual_line.set_data(current_x, current_actual)
    scheduled_line.set_data(current_x, current_scheduled)
    # Update the title in each frame
    title_text.set_text(
        f"Orange Line Travel Time Through February 2026\nThrough {dates[frame]}"
    )
    return actual_line, scheduled_line, title_text

def main():
    """Build the model and create Animation A"""
    line = build_model("Orange", "Orange Line")
    # Get dates from model
    dates = line.dates
    # Get actual and scheduled travel times
    actual_values = [line.daily_avg_travel[date] for date in dates]
    scheduled_values = [line.daily_avg_scheduled.get(date, float("nan")) for date in dates]
    # Set range for x values
    x_values = list(range(len(dates)))
    fig, ax = plt.subplots(figsize=(11, 6))
    # Create the two lines
    actual_line, = ax.plot([], [], label="Actual Travel Time", linewidth=2)
    scheduled_line, = ax.plot([], [], label="Scheduled Travel Time", linewidth=2)
    # Mark the storm window
    ax.axvspan(22, 23, alpha=0.2, label="Blizzard (Feb 23–24)")
    # Set range for y values
    y_max = max(
        max(actual_values),
        max(value for value in scheduled_values if value == value)
    ) * 1.1
    ax.set_xlim(0, len(dates) - 1)
    ax.set_ylim(0, y_max)
    ax.set_xticks(x_values)
    ax.set_xticklabels([date[5:] for date in dates], rotation=45)
    ax.set_xlabel("Date in February 2026")
    ax.set_ylabel("Average Travel Time (seconds)")
    title_text = ax.set_title("Orange Line Travel Time Through February 2026")
    ax.legend()
    ax.grid(True, alpha=0.3)
    # Create the animation
    anim = FuncAnimation(
        fig,
        update,
        frames=len(dates),
        fargs=(x_values, dates, actual_values, scheduled_values, actual_line, scheduled_line, title_text),
        interval=400,
        blit=False,
        repeat=False
    )
    # Save the animation to mp4 file
    anim.save("mbta_orange_animation_a.mp4", fps=2)
    plt.show()

if __name__ == "__main__":
    main()