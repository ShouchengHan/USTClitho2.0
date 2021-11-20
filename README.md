# USTClitho2.0
Updated Unified Seismic Tomography Models for Continental China Lithosphere (USTClitho2.0)

This is the updated unified 3-D P- and S-wave velocity models of the crust and uppermost mantle for continental China, obtained by joint inversion of body wave arrival times and surface wave dispersion curves data.

* Method: Joint inversion of body wave (P and S-wave) arrival times and Rayleigh wave dispersion curves data (Zhang et al.,2014,PAG； Han et al.,2021,SRL).

* Grid spacing: 0.5 degrees horizontally, and vertically at depths of -7, 0, 5, 10, 15, 20, 30, 40, 60, 80, 100, 120, 150, 180 km.

* We provide Vp and Vs models in two types with the depths relative to the mean sea level and the actual surface, respectively. In two model files, each line represents the Vp and Vs at each grid node with the format of Longitude, Latitude, Depth(km), Vp(km/s) and Vs(km/s).
  1) USTClitho2.0.txt: the depth of 0 km is the surface 
  2) USTClitho2.0.wrst.sea_level.txt: the depth of 0 km is the mean sea level


* Please choose appropriate model according to your purpose. For example, if you work with the surface wave problems or receiver functions, model with the depth relative to the surface (USTClitho2.0.txt) is recommended. If you are doing body wave tomography or earthquake relocations, model with depth relative to the mean sea level (USTClitho2.0.wrst.sea_level.txt) is recommended.

* We also provide models in the tomoDD format (MOD-USTClitho2.0) with a Python script (interpVel.py) with which you can use USTClitho2.0 as the initial models for regional study in China.
* Usage: 1) Modify lines 101-103 in the Python script to change the MOD coordinates; 
         2) Run the command `python interpVel.py` to generate the new model in tomoDD-format (MOD).


If you have any questions, please feel free to contact Haijiang Zhang (zhang11@ustc.edu.cn) or Shoucheng Han (hansc01@mail.ustc.edu.cn).

References:
Shoucheng Han, Haijiang Zhang, Hailiang Xin, Weisen Shen, Huajian Yao; USTClitho2.0: Updated Unified Seismic Tomography Models for Continental China Lithosphere from Joint Inversion of Body‐Wave Arrival Times and Surface‐Wave Dispersion Data. Seismological Research Letters 2021; doi: https://doi.org/10.1785/0220210122.
