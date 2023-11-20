import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
import seaborn as sns
from mpl_toolkits.mplot3d import axes3d, Axes3D
import matplotlib.cm as cmx
from matplotlib import cm


def plot_3d_scatter(df: pd.DataFrame) -> None:
    x = df['cache_size_log2'].to_numpy()
    y = df['line_size_log2'].to_numpy()
    z = df['set_size_log2'].to_numpy()
    v = df['hits'] / df['accesses'].to_numpy()

    fig = plt.figure(figsize=(6, 6))
    ax = Axes3D(fig, auto_add_to_figure=True)
    fig.add_axes(ax)

    cmap = ListedColormap(sns.color_palette("husl", 512).as_hex())

    # plot
    sc = ax.scatter(x, y, z, s=40, c=v, marker='o', cmap=cmap, alpha=1)
    ax.set_xlabel('Cache Size')
    ax.set_ylabel('Line Size')
    ax.set_zlabel('Set Size')

    plt.legend(*sc.legend_elements(), bbox_to_anchor=(1.05, 1), loc=2)
    plt.savefig("Hit Rate vs Cache Size Line Size and Set Size", bbox_inches='tight')


def plot_2d_scatter(df: pd.DataFrame, set_size: int) -> None:
    df = df[df['set_size_log2'] == set_size]

    x = df['cache_size_log2'].to_numpy()
    y = df['line_size_log2'].to_numpy()
    v = df['hits'] / df['accesses'].to_numpy()

    fig = plt.figure()
    ax = fig.add_axes((1,1,1,1))
    cmap = ListedColormap(sns.color_palette("husl", 512).as_hex())

    sc = ax.scatter(x, y, s=40, c=v, cmap=cmap, alpha=1)
    ax.set_xlabel('Cache Size')
    ax.set_ylabel('Line Size')
    ax.set_title(f'Hit Rate vs Cache Size and Line Size with Set Size {pow(2, set_size)}')
    plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    plt.yticks(np.arange(min(y), max(y)+1, 1.0))

    plt.legend(*sc.legend_elements(), bbox_to_anchor=(1.05, 1), loc=2)
    plt.savefig(f"Hit Rate vs Cache Size and Line Size with Set Size {pow(2, set_size)}", bbox_inches='tight')


def plot_3d_surface_lru_vs_fifo(df_lru: pd.DataFrame, df_fifo: pd.DataFrame, set_size: int) -> None:
    df_lru = df_lru[df_lru['set_size_log2'] == set_size]
    df_fifo = df_fifo[df_fifo['set_size_log2'] == set_size]

    cache_size_range = (min(df_lru['cache_size_log2']), max(df_lru['cache_size_log2']))
    line_size_range = (min(df_lru['line_size_log2']), max(df_lru['line_size_log2']))

    z_lru = np.empty((cache_size_range[1] - cache_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)
    z_fifo = np.empty((cache_size_range[1] - cache_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)

    x_ax = np.arange(cache_size_range[0], cache_size_range[1] + 1, 1.0)
    y_ax = np.arange(line_size_range[0], line_size_range[1] + 1, 1.0)

    for i in range(len(x_ax)):
        for j in range(len(y_ax)):
            lru_line = df_lru[(df_lru["cache_size_log2"] == x_ax[i]) & (df_lru["line_size_log2"] == y_ax[j])]
            fifo_line = df_fifo[(df_fifo["cache_size_log2"] == x_ax[i]) & (df_fifo["line_size_log2"] == y_ax[j])]

            lru_val = (lru_line["hits"] / lru_line["accesses"]).sum()
            fifo_val = (fifo_line["hits"] / fifo_line["accesses"]).sum()

            z_lru[i][j] = lru_val if lru_val != 0 else np.NaN
            z_fifo[i][j] = fifo_val if fifo_val != 0 else np.NaN

    x_ax, y_ax = np.meshgrid(x_ax, y_ax)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    cmap = ListedColormap(sns.color_palette("husl", 512).as_hex())

    print(x_ax, y_ax, z_lru)

    ax.view_init(elev=5, azim=45)

    surf_lru = ax.plot_surface(x_ax, y_ax, z_lru.T, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    surf_fifo = ax.plot_surface(x_ax, y_ax, z_fifo.T, cmap=cmap, linewidth=0, antialiased=True)

    ax.set_xlabel('Cache Size')
    ax.set_ylabel('Line Size')
    ax.set_title(f'Hit Rate vs Cache Size and Line Size with Set Size {pow(2, set_size)}')
    plt.xticks(np.arange(cache_size_range[0], cache_size_range[1]+1, 1.0))
    plt.yticks(np.arange(line_size_range[0], line_size_range[1], 1.0))

    fig.colorbar(surf_lru, shrink=0.5, aspect=5)

    plt.savefig(f"Hit Rate vs Cache Size and Line Size with Set Size {pow(2, set_size)}", bbox_inches='tight')


def plot_3d_surface_lru_vs_fifo_fixed_cache_size(df_lru: pd.DataFrame, df_fifo: pd.DataFrame, cache_size: int) -> None:
    df_lru = df_lru[df_lru['cache_size_log2'] == cache_size]
    df_fifo = df_fifo[df_fifo['cache_size_log2'] == cache_size]

    set_size_range = (min(df_lru['set_size_log2']), max(df_lru['set_size_log2']))
    line_size_range = (min(df_lru['line_size_log2']), max(df_lru['line_size_log2']))

    # z_lru = np.empty((set_size_range[1] - set_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)
    # z_fifo = np.empty((set_size_range[1] - set_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)

    x_ax = np.arange(set_size_range[0], set_size_range[1] + 1, 1.0)
    y_ax = np.arange(line_size_range[0], line_size_range[1] + 1, 1.0)

    x_ax, y_ax = np.meshgrid(x_ax, y_ax)

    z_lru = np.empty(x_ax.shape, dtype=np.float32)
    z_fifo = np.empty(x_ax.shape, dtype=np.float32)

    for i, (row1, row2) in enumerate(zip(x_ax, y_ax)):
        for j, (col1, col2) in enumerate(zip(row1, row2)):
            lru_line = df_lru[(df_lru["set_size_log2"] == col1) & (df_lru["line_size_log2"] == col2)]
            fifo_line = df_fifo[(df_fifo["set_size_log2"] == col1) & (df_fifo["line_size_log2"] == col2)]

            lru_val = (lru_line["hits"] / lru_line["accesses"]).sum()
            fifo_val = (fifo_line["hits"] / fifo_line["accesses"]).sum()

            z_lru[i][j] = lru_val if lru_val != 0 else np.NaN
            z_fifo[i][j] = fifo_val if fifo_val != 0 else np.NaN

    # for i in range(len(x_ax)):
    #     for j in range(len(y_ax)):
    #         lru_line = df_lru[(df_lru["set_size_log2"] == x_ax[i]) & (df_lru["line_size_log2"] == y_ax[j])]
    #         fifo_line = df_fifo[(df_fifo["set_size_log2"] == x_ax[i]) & (df_fifo["line_size_log2"] == y_ax[j])]
    #
    #         lru_val = (lru_line["hits"] / lru_line["accesses"]).sum()
    #         fifo_val = (fifo_line["hits"] / fifo_line["accesses"]).sum()
    #
    #         z_lru[i][j] = lru_val if lru_val != 0 else np.NaN
    #         z_fifo[i][j] = fifo_val if fifo_val != 0 else np.NaN

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    cmap = ListedColormap(sns.color_palette("husl", 512).as_hex())

    print(x_ax.shape, y_ax.shape, z_lru.shape)

    ax.view_init(elev=25, azim=225)

    surf_lru = ax.plot_surface(x_ax, y_ax, z_lru, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    surf_fifo = ax.plot_surface(x_ax, y_ax, z_fifo, cmap=cmap, linewidth=0, antialiased=True)

    ax.set_xlabel('Set Size')
    ax.set_ylabel('Line Size')
    ax.set_title(f'Hit Rate vs Cache Size and Line Size with Cache Size {pow(2, cache_size)}')
    plt.xticks(np.arange(set_size_range[0], set_size_range[1]+1, 1.0))
    plt.yticks(np.arange(line_size_range[0], line_size_range[1], 1.0))

    fig.colorbar(surf_lru, shrink=0.5, aspect=5)

    plt.savefig(f"Hit Rate vs Cache Size and Line Size with Cache Size {pow(2, cache_size)}", bbox_inches='tight')


def plot_3d_surface_lru_difference_fifo_fixed_cache_size(df_lru: pd.DataFrame, df_fifo: pd.DataFrame, cache_size: int) -> None:
    df_lru = df_lru[df_lru['cache_size_log2'] == cache_size]
    df_fifo = df_fifo[df_fifo['cache_size_log2'] == cache_size]

    set_size_range = (min(df_lru['set_size_log2']), max(df_lru['set_size_log2']))
    line_size_range = (min(df_lru['line_size_log2']), max(df_lru['line_size_log2']))

    # z_lru = np.empty((set_size_range[1] - set_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)
    # z_fifo = np.empty((set_size_range[1] - set_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)

    x_ax = np.arange(set_size_range[0], set_size_range[1] + 1, 1.0)
    y_ax = np.arange(line_size_range[0], line_size_range[1] + 1, 1.0)

    x_ax, y_ax = np.meshgrid(x_ax, y_ax)

    z_lru = np.empty(x_ax.shape, dtype=np.float32)
    z_fifo = np.empty(x_ax.shape, dtype=np.float32)

    for i, (row1, row2) in enumerate(zip(x_ax, y_ax)):
        for j, (col1, col2) in enumerate(zip(row1, row2)):
            lru_line = df_lru[(df_lru["set_size_log2"] == col1) & (df_lru["line_size_log2"] == col2)]
            fifo_line = df_fifo[(df_fifo["set_size_log2"] == col1) & (df_fifo["line_size_log2"] == col2)]

            lru_val = (lru_line["hits"] / lru_line["accesses"]).sum()
            fifo_val = (fifo_line["hits"] / fifo_line["accesses"]).sum()

            z_lru[i][j] = lru_val if lru_val != 0 else np.NaN
            z_fifo[i][j] = fifo_val if fifo_val != 0 else np.NaN

    # for i in range(len(x_ax)):
    #     for j in range(len(y_ax)):
    #         lru_line = df_lru[(df_lru["set_size_log2"] == x_ax[i]) & (df_lru["line_size_log2"] == y_ax[j])]
    #         fifo_line = df_fifo[(df_fifo["set_size_log2"] == x_ax[i]) & (df_fifo["line_size_log2"] == y_ax[j])]
    #
    #         lru_val = (lru_line["hits"] / lru_line["accesses"]).sum()
    #         fifo_val = (fifo_line["hits"] / fifo_line["accesses"]).sum()
    #
    #         z_lru[i][j] = lru_val if lru_val != 0 else np.NaN
    #         z_fifo[i][j] = fifo_val if fifo_val != 0 else np.NaN

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    cmap = ListedColormap(sns.color_palette("husl", 512).as_hex())

    print(x_ax.shape, y_ax.shape, z_lru.shape)

    ax.view_init(elev=25, azim=225)

    surf_lru = ax.plot_surface(x_ax, y_ax, z_lru-z_fifo, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    # surf_fifo = ax.plot_surface(x_ax, y_ax, z_fifo, cmap=cmap, linewidth=0, antialiased=True)

    ax.set_xlabel('Set Size')
    ax.set_ylabel('Line Size')
    ax.set_title(f'LRU Hit Rate - FIFO Hit Rate vs Cache Size and Line Size with Cache Size {pow(2, cache_size)}')
    plt.xticks(np.arange(set_size_range[0], set_size_range[1]+1, 1.0))
    plt.yticks(np.arange(line_size_range[0], line_size_range[1], 1.0))

    fig.colorbar(surf_lru, shrink=0.5, aspect=5)

    plt.savefig(f'LRU Hit Rate - FIFO Hit Rate vs Cache Size and Line Size with Cache Size {pow(2, cache_size)}', bbox_inches='tight')


def plot_3d_surface_lru_fifo_difference(df_lru: pd.DataFrame, df_fifo: pd.DataFrame, set_size: int) -> None:
    df_lru = df_lru[df_lru['set_size_log2'] == set_size]
    df_fifo = df_fifo[df_fifo['set_size_log2'] == set_size]

    cache_size_range = (min(df_lru['cache_size_log2']), max(df_lru['cache_size_log2']))
    line_size_range = (min(df_lru['line_size_log2']), max(df_lru['line_size_log2']))

    z_lru = np.empty((cache_size_range[1] - cache_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)
    z_fifo = np.empty((cache_size_range[1] - cache_size_range[0] + 1, line_size_range[1] - line_size_range[0] + 1), dtype=np.float32)

    x_ax = np.arange(cache_size_range[0], cache_size_range[1] + 1, 1.0)
    y_ax = np.arange(line_size_range[0], line_size_range[1] + 1, 1.0)

    for i in range(len(x_ax)):
        for j in range(len(y_ax)):
            lru_line = df_lru[(df_lru["cache_size_log2"] == x_ax[i]) & (df_lru["line_size_log2"] == y_ax[j])]
            fifo_line = df_fifo[(df_fifo["cache_size_log2"] == x_ax[i]) & (df_fifo["line_size_log2"] == y_ax[j])]

            lru_val = (lru_line["hits"] / lru_line["accesses"]).sum()
            fifo_val = (fifo_line["hits"] / fifo_line["accesses"]).sum()

            z_lru[i][j] = lru_val if lru_val != 0 else np.NaN
            z_fifo[i][j] = fifo_val if fifo_val != 0 else np.NaN

    x_ax, y_ax = np.meshgrid(x_ax, y_ax)

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    cmap = ListedColormap(sns.color_palette("husl", 512).as_hex())

    print(x_ax, y_ax, z_lru)

    ax.view_init(elev=27, azim=315)

    surf_lru = ax.plot_surface(x_ax, y_ax, z_lru.T-z_fifo.T, cmap=cm.coolwarm, linewidth=0, antialiased=True)

    ax.set_xlabel('Cache Size')
    ax.set_ylabel('Line Size')
    ax.set_title(f'LRU Hit Rate - FIFO Hit Rate vs Cache Size and Line Size with Set Size {pow(2, set_size)}')
    plt.xticks(np.arange(cache_size_range[0], cache_size_range[1]+1, 1.0))
    plt.yticks(np.arange(line_size_range[0], line_size_range[1], 1.0))

    # fig.colorbar(surf_lru, shrink=0.5, aspect=5)

    plt.savefig(f"LRU Hit Rate - FIFO Hit Rate vs Cache Size and Line Size with Set Size {pow(2, set_size)}", bbox_inches='tight')


def main():
    df_lru = pd.read_csv("LRUresults.csv")
    df_fifo = pd.read_csv("FIFOresults.csv")

    for i in range(min(df_lru['cache_size_log2']), max(df_lru['cache_size_log2']) + 1):
        plot_3d_surface_lru_difference_fifo_fixed_cache_size(df_lru, df_fifo, i)


if __name__ == "__main__":
    main()
