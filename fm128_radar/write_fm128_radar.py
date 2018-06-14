'''
description:    Python library to write WRFDA fm128_radar ascii files
license:        APACHE 2.0
author:         Ronald van Haren, NLeSC (r.vanharen@esciencecenter.nl)
'''

import numpy


class write_fm128_radar:
    '''
    Class module that writes write radar data to FM128_RADAR ascii
    format that can be used in WRFDA data assimiliation

    :param radar_name: name of radar
    :param lat0: latitude of radar station [deg]
    :param lon0: longitude of radar station [deg]
    :param elv0: elevation of radar station [m]
    :param date: date of observation
    :param lat: latitude of measurement point [deg]
    :param lon: longitude of measurement point [deg]
    :param elv: elevation of measurement point [m]
    :param rf: reflectivity
    :param rf_qc: quality control flag reflectivity
    :param rf_err: error on reflectivity measurement
    :param rv: radial velocity
    :param rv_qc: quality control flag radial velocity
    :param rv_err: error on radial velocity
    :param outfile: output filename of FM128_RADAR ascii file
    :param single: has reflection angle its own distinct lon/lat grid?
    :type radar_name: str
    :type lat0: float
    :type lon0: float
    :type elv0: float
    :type date:  datetime.datetime
    :type lat: numpy.ndarray
    :type lon: numpy.ndarray
    :type elv: numpy.ndarray
    :type rf: numpy.ndarray
    :type rf_qc: numpy.ndarray
    :type rf_err: numpy.ndarray
    :type rv: numpy.ndarray
    :type rv_qc: numpy.ndarray
    :type rv_err: numpy.ndarray
    :type outfile: str
    :type single: bool
    '''
    def __init__(self, radar_name, lat0, lon0, elv0, date, lat,
                 lon, elv, rf, rf_qc, rf_err,
                 rv, rv_qc, rv_err, outfile='fm128_radar.out', single=True):
        if ((isinstance(radar_name, (list, numpy.ndarray))
             and (len(radar_name) > 1))):
            # multiple radars in output file
            nrad = len(radar_name)
            # convert date to string
            dstring = [d.strftime('%Y-%m-%d %H:%M:%S') for d in date]
            self.init_file(nrad, outfile)
            for r_int in range(0, nrad):
                if single:
                    max_levs = numpy.shape(elv[r_int])[0]
                else:
                    max_levs = 1
                np = self.get_number_of_points(rf[r_int])
                # number of points: degrees * distance
                self.write_header(radar_name[r_int], lon0[r_int], lat0[r_int],
                                  elv0[r_int], dstring[r_int], np,
                                  max_levs)
                if single:
                    self.write_data_single(dstring[r_int], lat[r_int],
                                           lon[r_int], elv0[r_int], elv[r_int],
                                           rv[r_int], rv_qc[r_int],
                                           rv_err[r_int], rf[r_int],
                                           rf_qc[r_int], rf_err[r_int])
                else:
                    self.write_data(dstring[r_int], lat[r_int], lon[r_int],
                                    elv0[r_int], elv[r_int], rv[r_int],
                                    rv_qc[r_int], rv_err[r_int], rf[r_int],
                                    rf_qc[r_int], rf_err[r_int])
        else:
            # one radar in output file
            self.init_file(1, outfile)
            if single:
                max_levs = numpy.shape(elv)[0]
            else:
                max_levs = 1
            np = self.get_number_of_points(rf)
            dstring = date.strftime('%Y-%m-%d %H:%M:%S')
            self.write_header(radar_name, lon0, lat0, elv0, dstring, np,
                              max_levs)
            if single:
                self.write_data_single(dstring, lat, lon, elv0, elv, rv, rv_qc,
                                       rv_err, rf, rf_qc, rf_err)
            else:
                self.write_data(dstring, lat, lon, elv0, elv, rv, rv_qc,
                                rv_err, rf, rf_qc, rf_err)
        self.close_file()

    def init_file(self, nrad, outfile):
        '''
        Initialize output file

        :param nrad: number of radars in output file
        :param outfile: name of output file
        :type nrad: int
        :type outfile: str
        '''
        self.f = open(outfile, 'w')
        fmt = "%14s%3i"
        self.f.write(fmt % ("TOTAL RADAR = ", nrad))
        self.f.write("\n")
        self.f.write("%s" % ("#-----------------------------#"))
        self.f.write("\n")
        self.f.write("\n")

    def close_file(self):
        '''
        Close output file
        '''
        self.f.close()

    def write_header(self, radar_name, lon0, lat0, elv0, date, np, max_levs):
        '''
        Write the radar specific header to the output file

        :param radar_name: name of radar
        :param lat0: latitude of radar station [deg]
        :param lon0: longitude of radar station [deg]
        :param elv0: elevation of radar station [m]
        :param date: date of observation
        :param np: total number of measurement points for the radar
        :param max_levs: number of vertical levels
        :type radar_name: str
        :type lat0: float
        :type lon0: float
        :type elv0: float
        :type date:  datetime.datetime
        :type np: int
        :type max_levs: int
        '''
        # define header format
        fmt = "%5s%2s%12s%8.3f%2s%8.3f%2s%8.1f%2s%19s%6i%6i"
        # add temporary test data
        name = 'RADAR'
        hor_spacing = ''
        self.f.write(fmt % (name, hor_spacing, radar_name, lon0, hor_spacing,
                            lat0, hor_spacing, elv0, hor_spacing, date,
                            np, max_levs))
        self.f.write("\n")
        self.f.write("%s" % (
            '#---------------------------------------------------------#'))
        self.f.write("\n")
        self.f.write("\n")

    @staticmethod
    def get_number_of_points(rf):
        '''
        Return the total number of points for a radar:
            - For a masked array this all all points that are not masked
            - For a normal array this is all points
 
        :param rf: (masked) array of reflectivity measurements
        :type rf: numpy.ndarray
        :returns: total number of measurement points of the radar
        :rtype: int
        '''
        try:
            # masked array
            return len(rf.count(axis=0).flatten().nonzero()[0])
        except AttributeError:
            # Fallback for a non-masked array
            return len(rf[0, :].flatten())

    @staticmethod
    def get_levs_point(rf_data_point):
        '''
        Return the number of levels for a data point
        - For a masked array this all all points that are not masked
        - For a normal array this is all points

        :param rf_data_point: (masked) array of reflectivity data points
        :type rf_data_point: numpy.ndarray
        :returns: number of levels for a data point
        :rtype: int
        '''
        try:
            return rf_data_point.count()
        except AttributeError:
            try:
                return len(rf_data_point)
            except TypeError:
                return 1

    def write_data(self, date, lat, lon, elv0, elv, rv_data, rv_qc, rv_err,
                   rf_data, rf_qc, rf_err):
        '''
        Write radar measurements to the output file

        :param date: date of observation
        :param lat: latitude of measurement point [deg]
        :param lon: longitude of measurement point [deg]
        :param elv0: elevation of radar station [m]
        :param elv: elevation of measurement point [m]
        :param rv_data: radial velocity
        :param rv_qc: quality control flag radial velocity
        :param rv_err: error on radial velocity
        :param rf_data: reflectivity
        :param rf_qc: quality control flag reflectivity
        :param rf_err: error on reflectivity measurement
        :type date:  datetime.datetime
        :type lat: numpy.ndarray
        :type lon: numpy.ndarray
        :type elv0: float
        :type elv: numpy.ndarray
        :type rv_data: numpy.ndarray
        :type rv_qc: numpy.ndarray
        :type rv_err: numpy.ndarray
        :type rf_data: numpy.ndarray
        :type rf_qc: numpy.ndarray
        :type rf_err: numpy.ndarray
        '''
        fmt = "%12s%3s%19s%2s%12.3f%2s%12.3f%2s%8.1f%2s%6i"
        hor_spacing = ''
        # loop over horizontal data points
        for m in range(0, numpy.shape(lat)[0]):  # vertical levels
            for i in range(0, numpy.shape(lat)[1]):
                for j in range(0, numpy.shape(lat)[2]):
                    levs = self.get_levs_point(rf_data[m, i, j])
                    if levs > 0:
                        # Only write the output data if there is
                        # at least 1 vertical level
                        # with reflectivity data
                        self.f.write(fmt % ('FM-128 RADAR', hor_spacing, date,
                                            hor_spacing, lat[m, i, j],
                                            hor_spacing, lon[m, i, j],
                                            hor_spacing, elv0, hor_spacing,
                                            levs))
                        self.f.write("\n")
                        # loop over vertical elevations for each radar
                        if hasattr(rf_data, 'mask'):
                            if rf_data.mask[m, i, j]:
                                continue
                        else:
                            self.write_measurement_line(hor_spacing,
                                                        elv[m,i,j],
                                                        rv_data[m,i,j],
                                                        rv_qc[m,i,j],
                                                        rv_err[m,i,j],
                                                        rf_data[m,i,j],
                                                        rf_qc[m,i,j],
                                                        rf_err[m,i,j])

    def write_data_single(self, date, lat, lon, elv0, elv, rv_data, rv_qc,
                          rv_err, rf_data, rf_qc, rf_err):
        '''
        Write radar measurements to the output file

        :param date: date of observation
        :param lat: latitude of measurement point [deg]
        :param lon: longitude of measurement point [deg]
        :param elv0: elevation of radar station [m]
        :param elv: elevation of measurement point [m]
        :param rv_data: radial velocity
        :param rv_qc: quality control flag radial velocity
        :param rv_err: error on radial velocity
        :param rf_data: reflectivity
        :param rf_qc: quality control flag reflectivity
        :param rf_err: error on reflectivity measurement
        :type date:  datetime.datetime
        :type lat: numpy.ndarray
        :type lon: numpy.ndarray
        :type elv0: float
        :type elv: numpy.ndarray
        :type rv_data: numpy.ndarray
        :type rv_qc: numpy.ndarray
        :type rv_err: numpy.ndarray
        :type rf_data: numpy.ndarray
        :type rf_qc: numpy.ndarray
        :type rf_err: numpy.ndarray
        '''
        fmt = "%12s%3s%19s%2s%12.3f%2s%12.3f%2s%8.1f%2s%6i"
        hor_spacing = ''
        # loop over horizontal data points
        for i in range(0, numpy.shape(lat)[0]):
            for j in range(0, numpy.shape(lat)[1]):
                levs = self.get_levs_point(rf_data[:, i, j])
                if levs > 0:
                    # Only write the output data if there is
                    # at least 1 vertical level
                    # with reflectivity data
                    self.f.write(fmt %
                                 ('FM-128 RADAR', hor_spacing, date,
                                  hor_spacing, lat[i, j], hor_spacing,
                                  lon[i, j], hor_spacing, elv0, hor_spacing,
                                  levs))
                    self.f.write("\n")
                    # loop over vertical elevations for each radar
                    for m in range(0, numpy.shape(elv)[0]):
                        if hasattr(rf_data, 'mask'):
                            if rf_data.mask[m, i, j]:
                                continue
                        else:
                            self.write_measurement_line(hor_spacing,
                                                        elv[m,i,j],
                                                        rv_data[m,i,j],
                                                        rv_qc[m,i,j],
                                                        rv_err[m,i,j],
                                                        rf_data[m,i,j],
                                                        rf_qc[m,i,j],
                                                        rf_err[m,i,j])

    def write_measurement_line(self, hor_spacing, elv,
                               rv_data, rv_qc, rv_err,
                               rf_data, rf_qc, rf_err):
        '''
        Write measurement line to output file

        :param hor_spacing: horizontal spacing
        :param elv: elevation of measurement point [m]
        :param rv_data: radial velocity
        :param rv_qc: quality control flag radial velocity
        :param rv_err: error on radial velocity
        :param rf_data: reflectivity
        :param rf_qc: quality control flag reflectivity
        :param rf_err: error on reflectivity measurement
        :type elv: float
        :type rv_data: float
        :type rv_qc: float
        :type rv_err: float
        :type rf_data: float
        :type rf_qc: float
        :type rf_err: float
        '''
        fmt_2 = "%3s%12.1f%12.3f%4i%12.3f%2s%12.3f%4i%12.3f%2s"
        self.f.write(fmt_2 % (hor_spacing, elv,
                              rv_data, rv_qc,
                              rv_err, hor_spacing,
                              rf_data, rf_qc,
                              rf_err, hor_spacing))
        self.f.write("\n")
