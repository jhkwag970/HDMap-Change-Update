
from av2.map.map_api import ArgoverseStaticMap
import av2.utils.io as io_utils
from pathlib import Path
import matplotlib.pyplot as plt
from av2.geometry.sim2 import Sim2

# #https://argoverse.github.io/user-guide/api/hd_maps.html
# path="logs/0cfNzxkFwK3x3JB9HpcKIqoRCztSAreo__Winter_2021"
# log_map_dirpath = Path(path) / "map"
# vector_data_fnames = sorted(log_map_dirpath.glob("log_map_archive_*.json"))
# avm = ArgoverseStaticMap.from_map_dir(log_map_dirpath=log_map_dirpath, build_raster=False)
# #print(avm)

# vehicel_pose = io_utils.read_feather(path+"/city_SE3_egovehicle.feather")
# print(vehicel_pose)

path="logs/"
resource="resources/"
log_dirs = sorted(Path(path).glob("*"))
for dir in log_dirs:
    log_id = dir.name
    ego_vehicle = sorted(dir.glob("city_SE3_egovehicle.feather"))
    vehicel_pose = io_utils.read_feather(ego_vehicle[0])
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(vehicel_pose.tx_m.values, vehicel_pose.ty_m.values, label="vehicle pose", marker=".")
    ax.grid()
    ax.legend()
    plt.savefig(resource+log_id+".png")
    plt.close
