import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from model import build_model


def update(frame, im, heatmap_full, heatmap_display, ax, dates):
    """Reveal one more column (day) of the heatmap."""
    # copy the next day's column into the display array
    heatmap_display[:, frame] = heatmap_full[:, frame]
    im.set_array(heatmap_display)
    ax.set_title(f"Orange Line — Travel Time by Stop\n{dates[0]} to {dates[frame]}")
    return [im]


def main():
    # build the model
    model = build_model("Orange", "Orange Line")

    # get the pivot table (stops × dates) from the model
    pivot = model.travel_by_stop_and_day
    stops = model.stops
    dates = model.dates

    # convert to numpy array for set_array()
    heatmap_full = pivot.to_numpy().copy()

    # initialize display array with NaN (will appear as blank)
    heatmap_display = np.full_like(heatmap_full, np.nan)

    # set consistent color scale from the full dataset
    # using percentile because the february 8th outliers would otherwise make the graph unreadable
    vmin = np.nanpercentile(heatmap_full, 2)
    vmax = np.nanpercentile(heatmap_full, 99.7)

    # create figure and initial heatmap
    fig, ax = plt.subplots(figsize=(14, 8))

    im = ax.imshow(
        heatmap_display,
        aspect="auto",
        cmap="plasma",
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest"
    )

    # label axes
    ax.set_yticks(range(len(stops)))
    ax.set_yticklabels(stops, fontsize=8)

    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels([d[5:] for d in dates], rotation=45, ha="right", fontsize=7)
    ax.set_xlabel("Date")
    ax.set_ylabel("Station")
    ax.set_title(f"Orange Line — Travel Time by Stop")

    cbar = fig.colorbar(im, ax=ax, label="Mean Travel Time (seconds)")

    fig.tight_layout()

    # animate: one frame per day
    anim = FuncAnimation(
        fig,
        update,
        frames=len(dates),
        fargs=(im, heatmap_full, heatmap_display, ax, dates),
        interval=500,
        blit=False,
        repeat=False
    )

    anim.save("mbta_orange_animation_b.mp4", fps=2)
    print("Saved mbta_orange_animation_b.mp4")
    plt.show()


if __name__ == "__main__":
    main()