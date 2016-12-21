import numpy as np
import h5py
import parser
import datetime
from netCDF4 import Dataset
import os.path
import matplotlib.pyplot as plt
from math import sin,cos
from scipy.interpolate import griddata, interp2d
 
def date_range(start_dt, end_dt = None):
    start_dt = datetime.datetime.strptime(start_dt, "%Y%m%d%H")
    if end_dt: end_dt = datetime.datetime.strptime(end_dt, "%Y%m%d%H")
    while start_dt <= end_dt:
        yield start_dt.strftime("%Y%m%d%H")
        start_dt += datetime.timedelta(seconds=3600)
t_range = [e for e in date_range('2014070100','2014073123')]


LAT_bilt = 52.10168
LON_bilt = 5.17834
r_earth = 6378137.
angles = [0.3, 0.4, 0.8, 1.1, 2.0, 3.0, 4.5, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0,  25.0 ]
scans = ['scan1','scan2','scan3','scan4','scan5','scan6','scan7','scan8','scan9',
             'scan10','scan11','scan12','scan13','scan14']
ZZ_sc1 = np.zeros([len(t_range),len(angles),360,240])*np.nan
lat = np.zeros([360,240])*np.nan
lon = np.zeros([360,240])*np.nan
z = np.zeros([len(angles),360,240])*np.nan
degr = np.arange(0,360,1)
r = np.arange(0,240,1)*1000  # convert from KM to M
print np.shape(z)
time = t_range #datetime.datetime.strptime(t_range, "%Y%m%d%H")

for x in range(len(scans)): 
	for i in  range(0,len(r)):
		for j in degr:
			dx = r[i]*cos(degr[j]*(np.pi/180))
			dy = r[i]*sin(degr[j]*(np.pi/180))
			lat[j,i] = LAT_bilt + (180/np.pi)*(dy/r_earth)
			lon[j,i] = LON_bilt + (180/np.pi)*(dx/r_earth)/cos(LAT_bilt*np.pi/180)
			z[x,j,i] = r[i]*sin(angles[x]*np.pi/180)

for t in range(len(t_range)):
  path= '/Volumes/extharddrive/work/ERA_URBAN/DATA/RADAR_july2014/july2014/RAD_NL60_VOL_NA_'+t_range[t]+'00.h5'
  if (os.path.exists(path)):
    files = h5py.File(path,'r')
    print files
    for x in range(len(scans)): 
        scan1 =files.get(scans[x])
        PV = np.array(scan1.get('scan_Z_data'))
        cal_sc1 = scan1.get('calibration')
        str = np.array_str(cal_sc1.attrs.get('calibration_Z_formulas')).strip("['']").split('=')
        code = parser.expr(str[1]).compile()
        Z_sc1 = eval(code)
        for i in  range(0,len(r)):
            for j in degr:
                ZZ_sc1[t,x,j,i] = Z_sc1[j,i]
  else:
    ZZ_sc1[t,:] =-999

    
ntime = len(time); nangles = len(scans); ndegr = len(degr); ndist = len(r)
ncfile = Dataset('Radar_DB_test2.nc','w',format='NETCDF4') 
ncfile.createDimension('time',ntime)
ncfile.createDimension('angles',nangles)
ncfile.createDimension('degrees',ndegr)
ncfile.createDimension('distance',ndist)

data = ncfile.createVariable('Reflectivity','f4',('time','angles','degrees','distance'))
data1 = ncfile.createVariable('Latitude','f4',('degrees','distance'))
data2 = ncfile.createVariable('Longitude','f4',('degrees','distance'))
data3 = ncfile.createVariable('Altitude','f4',('angles','degrees','distance'))
data4 = ncfile.createVariable('Time','i4',('time'))
data4.units = '%Y%m%d%H'
data3.units = 'meters'
data.units = 'dBZ'
data1.units = 'degrees_east'
data1.standard_name = 'Longitude'
data2.units = 'degrees_north'
data2.standard_name = 'Latitude'
data[:] = ZZ_sc1
data1[:] = lat
data2[:] = lon
data3[:] = z
data4[:] = time

ncfile.close()

print np.shape(ZZ_sc1)
print time
plt.figure()
plt.hexbin(lon.flatten(),lat.flatten(),C=ZZ_sc1[3,1,:,:].flatten())
plt.show()

