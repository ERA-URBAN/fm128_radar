import os
from os.path import dirname, abspath
import unittest
from fm128_radar.write_fm128_radar import write_fm128_radar
from datetime import datetime
import numpy as np
import filecmp


class end2endtest(unittest.TestCase):
    def setUp(self):
        '''
        setup test environment
        '''
        # define test data
        self.radar_name = 'radar'
        self.lat0 = 50.3
        self.lon0 = 10.6
        self.elv0 = 11.4
        self.time = datetime(2002, 2, 2)
        self.latitude = 51.2 * np.ones((3, 4))
        self.longitude = 11.2 * np.ones((3, 4))
        self.altitude = 422 * np.ones((2, 3, 4))
        self.rf = 4.2 * np.ones((2, 3, 4))
        self.rf_qc = 0 * np.ones((2, 3, 4))
        self.rf_err = 1.3 * np.ones((2, 3, 4))
        self.rv = 7 * np.ones((2, 3, 4))
        self.rv_qc = 0 * np.ones((2, 3, 4))
        self.rv_err = 2 * np.ones((2, 3, 4))
        self.outputfile = 'fm128_radar.out'
        # define test_data location
        self.test_data = os.path.join(dirname(abspath(__file__)), '..',
                                      'test_data')

    def test_01(self):
        '''
        Test single radar with 2 vertical levels
        '''
        # write observation to ascii file
        write_fm128_radar(self.radar_name, self.lat0, self.lon0, self.elv0,
                          self.time, self.latitude, self.longitude,
                          self.altitude, self.rf, self.rf_qc, self.rf_err,
                          self.rv, self.rv_qc, self.rv_err,
                          outfile=self.outputfile, single=True)
        # test if output file exists
        self.assertEqual(os.path.exists(self.outputfile), 1)
        # check if output is same as sample file
        testfile = os.path.join(self.test_data, 'fm128_radar.single')
        self.assertEqual(filecmp.cmp(self.outputfile,  testfile), 1)

    def test_02(self):
        ''':
        Test two radars with two vertical levels each
        '''
        self.radar_name = ['radar1', 'radar2']
        self.time = [datetime(2002, 2, 2), datetime(2002, 2, 2)]
        self.latitude = 51.2 * np.ones((2, 3, 4))
        self.longitude = 11.2 * np.ones((2, 3, 4))
        self.altitude = 422 * np.ones((2, 2, 3, 4))
        self.lat0 = [50.3, 41.2]
        self.lon0 = [10.6, 9.4]
        self.elv0 = [11.4, 12.2]
        self.rf = 4.2 * np.ones((2, 2, 3, 4))
        self.rf_qc = 0 * np.ones((2, 2, 3, 4))
        self.rf_err = 1.3 * np.ones((2, 2, 3, 4))
        self.rv = 7 * np.ones((2, 2, 3, 4))
        self.rv_qc = 0 * np.ones((2, 2, 3, 4))
        self.rv_err = 2 * np.ones((2, 2, 3, 4))
        # write observation to ascii file
        write_fm128_radar(self.radar_name, self.lat0, self.lon0, self.elv0,
                          self.time, self.latitude, self.longitude,
                          self.altitude, self.rf, self.rf_qc, self.rf_err,
                          self.rv, self.rv_qc, self.rv_err,
                          outfile=self.outputfile, single=True)
        # test if output file exists
        self.assertEqual(os.path.exists(self.outputfile), 1)
        # check if output is same as sample file
        testfile = os.path.join(self.test_data, 'fm128_radar.multiple')
        self.assertEqual(filecmp.cmp(self.outputfile,  testfile), 1)

    def test_03(self):
        ''':
        Test two radars with two vertical levels each
        '''
        self.radar_name = ['radar1', 'radar2']
        self.time = [datetime(2002, 2, 2), datetime(2002, 2, 2)]
        self.latitude = 51.2 * np.ones((2, 2, 3, 4))
        self.longitude = 11.2 * np.ones((2, 2, 3, 4))
        self.altitude = 422 * np.ones((2, 2, 3, 4))
        self.lat0 = [50.3, 41.2]
        self.lon0 = [10.6, 9.4]
        self.elv0 = [11.4, 12.2]
        self.rf = 4.2 * np.ones((2, 2, 3, 4))
        self.rf_qc = 0 * np.ones((2, 2, 3, 4))
        self.rf_err = 1.3 * np.ones((2, 2, 3, 4))
        self.rv = 7 * np.ones((2, 2, 3, 4))
        self.rv_qc = 0 * np.ones((2, 2, 3, 4))
        self.rv_err = 2 * np.ones((2, 2, 3, 4))
        # write observation to ascii file
        write_fm128_radar(self.radar_name, self.lat0, self.lon0, self.elv0,
                          self.time, self.latitude, self.longitude,
                          self.altitude, self.rf, self.rf_qc, self.rf_err,
                          self.rv, self.rv_qc, self.rv_err,
                          outfile=self.outputfile, single=False)
        # test if output file exists
        self.assertEqual(os.path.exists(self.outputfile), 1)
        # check if output is same as sample file
        testfile = os.path.join(self.test_data, 'fm128_radar.multiple2')
        self.assertEqual(filecmp.cmp(self.outputfile,  testfile), 1)

if __name__ == "__main__":
    unittest.main()
