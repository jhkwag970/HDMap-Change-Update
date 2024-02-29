
from av2.map.map_api import ArgoverseStaticMap
from pathlib import Path

# #https://argoverse.github.io/user-guide/api/hd_maps.html
path="logs/0cfNzxkFwK3x3JB9HpcKIqoRCztSAreo__Winter_2021/map"
log_map_dirpath = Path(path)
avm = ArgoverseStaticMap.from_map_dir(log_map_dirpath=log_map_dirpath, build_raster=False)
