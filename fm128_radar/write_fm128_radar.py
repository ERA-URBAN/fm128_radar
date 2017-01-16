'''
description:    Python library to write WRFDA fm128_radar ascii files
license:        APACHE 2.0
author:         Ronald van Haren, NLeSC (r.vanharen@esciencecenter.nl)
'''

import numpy


class write_fm128_radar:
  def __init__(self, radar_name, lat0, lon0, elv0, date, lat,
               lon, elv, rf, rf_qc, rf_err,
               rv, rv_qc, rv_err, outfile='fm128_radar.out'):
    if (numpy.shape(radar_name) == True and numpy.shape(radar_name)>1):
      # multiple radars in output file
      nrad = numpy.shape(radar_name)
      self.init_file(nrad, outfile)
      for r_int in range(0, nrad):
        max_levs = numpy.shape(elv[r_int])[0]
        # number of points: degrees * distance
        np = numpy.shape(elv[r_int])[1] * numpy.shape(elv[r_int])[2]
        self.write_header(radar_name[r_int], lon0[r_int], lat0[r_int],
                          elv0[r_int], date[r_int], np[r_int], max_levs[r_int])
        self.write_data(date[r_int], lat[r_int], lon[r_int], elv0[r_int],
                        max_levs[r_int], elv[r_int], rv[r_int], rv_qc[r_int],
                        rv_err[r_int], rf[r_int], rf_qc[r_int], rf_err[r_int])
    else:
      # one radar in output file
      self.init_file(1, outfile)
      max_levs = numpy.shape(elv)[0]
      # number of points: degrees * distance
      np = numpy.shape(elv)[1] * numpy.shape(elv)[2]
      self.write_header(radar_name, lon0, lat0, elv0, date, np, max_levs)
      self.write_data(date, lat, lon, elv0, max_levs, elv, rv, rv_qc, rv_err,
                      rf, rf_qc, rf_err)
    self.close_file()

  def init_file(self, nrad, outfile):
    '''
    Initialize output file
      - input:
        * nrad: number of radars
        * outfile: name of output file
    '''
    self.f = open(outfile, 'w')
    fmt = "%14s%3i"
    self.f.write(fmt % ("TOTAL RADAR = ", nrad))
    self.f.write("\n")
    self.f.write("%s" % ("#-----------------------------#"))
    self.f.write("\n")

  def close_file(self):
    '''
    Close output file
    '''
    self.f.close()

  def write_header(self, radar_name, lon0, lat0, elv0, date, np, max_levs):
    '''
    Write the radar specific header to the output file
    '''
    # define header format
    fmt = "%5s%2s%12s%8.3f%2s%8.3f%2s%8.1f%2s%19s%6i%6i"
    # add temporary test data
    name='RADAR'
    hor_spacing=''
    self.f.write(fmt % (name, hor_spacing, radar_name, lon0, hor_spacing,
                        lat0, hor_spacing, elv0, hor_spacing, date,
                        np, max_levs))
    self.f.write("\n")
    self.f.write("%s" % (
      '#---------------------------------------------------------#'))
    self.f.write("\n")

  def write_data(self, date, lat, lon, elv0, levs, elv, rv_data, rv_qc, rv_err,
                 rf_data, rf_qc, rf_err):
    '''
    Write radar measurements to the output file
    '''
    fmt = "%12s%3s%19s%2s%12.3f%2s%12.3f%2s%8.1f%2s%6i"
    fmt_2 = "%3s%12.1f%12.3f%4i%12.3f%2s%12.3f%4i%12.3f%2s"
    hor_spacing = ''
    # loop over horizontal data points
    for i in range(0, numpy.shape(lat)[0]):
      for j in range(0, numpy.shape(lat)[1]):
        self.f.write(fmt % ('FM-128 RADAR', hor_spacing, date, hor_spacing,
                            lat[i,j], hor_spacing, lon[i,j], hor_spacing, elv0,
                            hor_spacing, levs))
        self.f.write("\n")
        # loop over vertical elevations for each radar
        for m in range(0, numpy.shape(elv)[0]): # count_nz(i)):
          self.f.write(fmt_2 % (hor_spacing, elv[m,i,j],
                                rv_data[m,i,j], rv_qc[m,i,j], rv_err[m,i,j],
                                hor_spacing,
                                rf_data[m,i,j], rf_qc[m,i,j], rf_err[m,i,j],
                                hor_spacing))
          self.f.write("\n")

