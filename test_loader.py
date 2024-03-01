
from pathlib import Path
from argparse import Namespace
import argparse
from typing import List

import matplotlib

import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable

import av2.geometry.polyline_utils as polyline_utils
import av2.rendering.vector as vector_plotting_utils
from av2.datasets.sensor.av2_sensor_dataloader import AV2SensorDataLoader
from av2.map.map_api import ArgoverseStaticMap, LaneSegment

#https://argoverse.github.io/user-guide/api/hd_maps.html

PURPLE_RGB = [201, 71, 245]
PURPLE_RGB_MPL = np.array(PURPLE_RGB) / 255

DARK_GRAY_RGB = [40, 39, 38]
DARK_GRAY_RGB_MPL = np.array(DARK_GRAY_RGB) / 255

def plot_lane_segments(
    ax: matplotlib.axes.Axes, lane_segments: List[LaneSegment], lane_color: np.ndarray = DARK_GRAY_RGB_MPL
) -> None:
    """

    Args:
        ax:
        lane_segments:
    """
    for ls in lane_segments:
        pts_city = ls.polygon_boundary
        ALPHA = 1.0  # 0.1
        vector_plotting_utils.plot_polygon_patch_mpl(
            polygon_pts=pts_city, ax=ax, color=lane_color, alpha=ALPHA, zorder=1
        )

        for bound_type, bound_city in zip(
            [ls.left_mark_type, ls.right_mark_type], [ls.left_lane_boundary, ls.right_lane_boundary]
        ):
            if "YELLOW" in bound_type:
                mark_color = "y"
            elif "WHITE" in bound_type:
                mark_color = "w"
            else:
                mark_color = "grey"  # "b" lane_color #

            LOOSELY_DASHED = (0, (5, 10))

            if "DASHED" in bound_type:
                linestyle = LOOSELY_DASHED
            else:
                linestyle = "solid"

            if "DOUBLE" in bound_type:
                left, right = polyline_utils.get_double_polylines(
                    polyline=bound_city.xyz[:, :2], width_scaling_factor=0.1
                )
                ax.plot(left[:, 0], left[:, 1], mark_color, alpha=ALPHA, linestyle=linestyle, zorder=2)
                ax.plot(right[:, 0], right[:, 1], mark_color, alpha=ALPHA, linestyle=linestyle, zorder=2)
            else:
                ax.plot(
                    bound_city.xyz[:, 0],
                    bound_city.xyz[:, 1],
                    mark_color,
                    alpha=ALPHA,
                    linestyle=linestyle,
                    zorder=2,
                )

dataroot = "data/logs/" 
log_id="0cfNzxkFwK3x3JB9HpcKIqoRCztSAreo__Winter_2021"
cam_name="ring_front_center"

args = Namespace(**{"dataroot": Path(dataroot), "log_id": Path(log_id)})
loader = AV2SensorDataLoader(data_dir=args.dataroot, labels_dir=args.dataroot)
cam_timestam=loader._sdb.per_log_cam_timestamps_index[log_id][cam_name]

ego_vehicle=[]
for timestamp in cam_timestam:
  ego_vehicle.append(list(loader.get_city_SE3_ego(log_id, timestamp).translation))
ego_vehicle = np.array(ego_vehicle)

fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(111)

log_map_dirpath = Path(args.dataroot) / args.log_id / "map"

avm = ArgoverseStaticMap.from_map_dir(log_map_dirpath, build_raster=False)

crosswalk_color = PURPLE_RGB_MPL
CROSSWALK_ALPHA = 0.6
for pc in avm.get_scenario_ped_crossings():
    vector_plotting_utils.plot_polygon_patch_mpl(
        polygon_pts=pc.polygon[:, :2],
        ax=ax,
        color=crosswalk_color,
        alpha=CROSSWALK_ALPHA,
        zorder=3,
    )

plot_lane_segments(ax=ax, lane_segments=avm.get_scenario_lane_segments())

# retain every pose first.
# traj_ns = loader.get_subsampled_ego_trajectory(log_id, sample_rate_hz=1e9)
# # now, sample @ 1 Hz
# traj_1hz = loader.get_subsampled_ego_trajectory(log_id, sample_rate_hz=1.0)
# med_x, med_y = np.median(traj_ns, axis=0)

# Derive plot area from trajectory (with radius defined in infinity norm).
# view_radius_m = 50
# xlims = [med_x - view_radius_m, med_x + view_radius_m]
# ylims = [med_y - view_radius_m, med_y + view_radius_m]

# ax.plot(traj_ns[:, 0], traj_ns[:, 1], color="r", zorder=4, label="Ego-vehicle pose")
# ax.scatter(
#     traj_1hz[:, 0], traj_1hz[:, 1], 100, facecolors="none", edgecolors="r", zorder=4
# )  # marker='o', color="r")
x = ego_vehicle[0,0]
y = ego_vehicle[0,1]
view_radius_m = 50
xlims = [x - view_radius_m, x + view_radius_m]
ylims = [y - view_radius_m, y + view_radius_m]
# med_x, med_y = np.median(ego_vehicle[:,:2], axis=0)
# print("med_x: ", med_x)
# print("med_y: ", med_y)
# xlims = [med_x - view_radius_m, med_x + view_radius_m]
# ylims = [med_y - view_radius_m, med_y + view_radius_m]
ax.scatter(x,y, s = 1, zorder=4, marker="x", c="red")


plt.axis("equal")
plt.xlim(xlims)
plt.ylim(ylims)
plt.title(f"Log {args.log_id}")
plt.axis("off")
plt.legend()
plt.tight_layout()
plt.show()




