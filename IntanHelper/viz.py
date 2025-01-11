import numpy as np
import matplotlib.pyplot as plt


def plot_overlay_pulses(obj_list):
    output_folder = obj_list[0].output_folder
    ylim = 7000
    fig, axes = plt.subplots(4, 4, figsize=(10, 15))
    axes = axes.flatten()
    # colors = ['#5f8fb7', '#6d9d74', '#9c5a61']
    colors = ['#9c5a61', '#6d9d74']
    title = f'Stimulating ch {obj_list[0].stimulation_channels}'
    category = []
    for index, color, obj in zip(range(3), colors, obj_list):
        data = obj.pulses
        ch_names = obj.recording_channels
        sample_rate = obj.sample_rate
        category.append(obj.parent_folder)
        average_data = np.mean(data, axis=0)
        for i, ax in enumerate(axes):
            if i < data.shape[1]:
                x_axis = -3 +(np.arange(0, len(data[0, i, :]))) / sample_rate * 1000
                ax.plot(x_axis, average_data[i, :], color=color, linewidth=1, alpha=1)

                if i == obj.stimulation_channels:
                    ax.set_title(f"Channel {ch_names[i]}", color='red')
                else:
                    ax.set_title(f"Channel {ch_names[i]}")

                ax.set_title(f"Channel {ch_names[i]}")
                ax.set_xlabel('Time (msec)')
                if ylim is not None:
                    ax.set_ylim(-ylim, ylim)

                # Only show x-ticks and x-labels on the last row
                if i < 12:  # Exclude last row
                    ax.set_xticks([])
                    ax.set_xticklabels([])
                else:
                    ax.set_xlabel('Time (msec)')  # Show x-label only on the last row

                # Only show y-ticks and y-labels on the first column
                if i % 4 != 0:  # Exclude first column
                    ax.set_yticks([])
                    ax.set_yticklabels([])

                # # Add the estimated impedance
                # current_a = 5 / 1e6
                # max_v = np.max(abs(average_data[i, :]) / 1e6)
                # z = (max_v / current_a) / 1e3
                #
                # ax.text(
                #     0.95, 0.05+index*0.06,  # Position in normalized axis coordinates
                #     f"{z:.2f}",  # Text to display
                #     color=color,
                #     fontsize=7,
                #     transform=ax.transAxes,  # Use axis coordinates
                #     verticalalignment='bottom',
                #     horizontalalignment='right')
            else:
                ax.axis('off')

    # Add a single-row legend below the title
    legend_handles = [
        plt.Line2D([0], [0], color=color, lw=2, label=parent)
        for color, parent in zip(colors, category)
    ]
    plt.figlegend(handles=legend_handles, loc='upper center', ncol=len(obj_list), frameon=False)
    plt.suptitle(title, y=0.95)  # Adjust title to make room for legend
    plt.tight_layout(rect=[0, 0, 1, 0.93])  # Adjust layout to fit legend and title
    plt.savefig(rf'{output_folder}/{title}.png')
    plt.close()
