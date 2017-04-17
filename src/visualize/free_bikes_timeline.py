#!/usr/bin/env python3

import colorsys
import csv
import os
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np

from utils import print_progressbar, clear_progressbar, get_csv


def main():
    station_ids_to_plot = None  # [508, 509, 510, 101, 102]
    stations = {}
    timestamps = []
    last_timestamp = None
    station_names = {}
    for row in get_csv('stations.csv'):
        station_id = int(row['station_id:ID(Station)'])
        station_names[station_id] = row['name'].replace('/', '/\n')
    for row in get_csv('extra/free_bikes_at_station.csv'):
        if last_timestamp != row['timestamp:INT']:
            last_timestamp = row['timestamp:INT']
            timestamps.append(datetime.fromtimestamp(float(row['timestamp:INT'])))
        station_id = int(row['station_id:INT'])
        if station_ids_to_plot and station_id not in station_ids_to_plot:
            continue
        if not station_id in stations:
            stations[station_id] = []
        station = stations[station_id]
        station.append(int(row['free_bikes:INT']))
    plot(timestamps, stations, station_names)


def get_colors(n):
    colors = [colorsys.hsv_to_rgb(x / n, 1, 1) for x in range(n)]
    return colors


def plot(x, stations, station_names, output_filename='timeline.png', step='post'):
    fig, axes = plt.subplots(len(stations), 1, sharex=True)
    fig.set_size_inches(19.20, 1.5 * len(stations))  # Those are pixels: 1920 width, 150 height for each station
    station_ids = list(stations.keys())
    station_ids.sort(key=lambda x: station_names[x])
    for ax, station_id, color in zip(axes, station_ids, get_colors(len(axes))):
        station_values = stations[station_id]
        station_name = station_names[station_id]
        ax.fill_between(x, 0, station_values, step=step)
        ax.set_ylabel(station_name, rotation=0, horizontalalignment='right', verticalalignment='center')
        ax.grid(True)
    plt.savefig(output_filename)
    plt.clf()