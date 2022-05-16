# #!/usr/bin/python
# import os
# import sys
# import cv2 as CV2
# import sqlite3
# from sqlite3 import Connection, Cursor
# from sys import stdout
# import unittest
# from motiondetect import dataBase, MotionDetect
# from datetime import datetime, timedelta


# class DatabaseTest(unittest.TestCase):
#     '''
#         > to run test on this class, do:
#         tests/motiondetect_database_test.py
#         > python -m unittest tests/motiondetect_database_test.py
#     '''
#     test_video = '/home/kcdouglass/Desktop/SoftwareEngineering/open-source-security-camera/open-source-security-camera/osCam/videos/funny_monkeys.avi'
#     USER_CONFIG_SETTING = {
#         'recordToDevice':0,
#             'filePath':'/home/pi/open-source-security-camera/osCam/videos/',
#             'maxSpace': 100, 
#             'timeToLive':60,
#             'lengthOfRecordings': 10,
#     }
    
#     def setUp(self) -> None:
#         # For Database Class
#         self.TEST_DB_FILE_NAME = r"osCam.test/db.sqlite3"
#         self.db_file_name = r"osCam/db.sqlite3"
#         self.userconfig_name = 'userconfig_storage'
#         self._db = dataBase
#         self.connection = dataBase.create_connection(self.db_file_name)
#         self.cursor = self.connection.cursor()
#         self.motion_detect = MotionDetect()

#     def tearDown(self) -> None:
#         """
#             Delete any Test database/ Entries on Treadown
#         """
#         tear_down_file_name = self.db_file_name 
#         if self.connection and self.cursor == self.connection:
#             # if there was a valid connection we should roll-back any potential changes on tear-down
#             self.connection.cursor.close()
#             self.connection.close()
#             if self.db_file_name is None:
#                 os.remove(self.TEST_DB_FILE_NAME)
#             else:
#                 os.remove(self.db_file_name)
#         else:
#             print("No {} Connections to Close.".format(self.db_file_name))

#     def test_smoke_test(self):
#         self.assertEqual(1,1)

#     def test_valid_userconfig_setting_entry_list(self):
#         # Ensure the lists are the same and data had been saved
#         self.db_file_name = r"osCam/db.sqlite3"
#         _connection = self._db.create_connection(self.db_file_name)
#         selected_items = self._db.GetSettingsFromDB(_connection)
#         self.assertIsNotNone((selected_items))
      
#     def test_has_valid_db_entry(self):
#         """
#         ENTRY RETURN VALUE EXAMPLE
#             [1, 0, '/home/pi/open-source-security-camera/osCam/videos/', 100, 60, 10]
#         """
#         self.db_file_name=r"osCam/db.sqlite3"
#         self.connection = dataBase.create_connection(self.db_file_name)
#         self.cursor = self.connection.cursor()
#         userconf_storage = self.cursor.execute('SELECT * FROM userconfig_storage').fetchall()
#         original_items = [1, 0, '/home/pi/open-source-security-camera/osCam/videos/', 100, 60, 10]
#         _storage = []
#         for record in userconf_storage:
#             for data in record:
#                 _storage.append(data)
#         # ENSURE SAMENESS
#         self.assertListEqual(
#                 original_items,
#                 _storage,
#             )

#     def test_create_connection(self):
#         '''Sqlit3 returns instance-of *Connection* on successfull connection'''
#         is_connected = dataBase.create_connection(r"osCam/db.sqlite3")
#         self.assertIsInstance(is_connected, sqlite3.Connection)
#         self.assertTrue(isinstance(is_connected, sqlite3.Connection))

#     def test_create_invalid_connection_exeption(self):
#         """Ensure that database is not created Every time by checking when invalid connection"""
#         try:
#             is_connected = dataBase.create_connection("file:testtemplate.db?mode=ro")
#             self.assertTrue(is_connected is None)
#         except sqlite3.Error:
#             self.assertTrue(is_connected is None)
#             self.fail()

#     def test_motiondetect_smoke_test(self):
#         self.assertTrue(self.motion_detect.capture)

#     def handle_open_video(self, capture, frame, isReading):
#         count = 0
#         while(capture.isOpened() and count < 20):
#             if isReading:
#                 CV2.imshow('FRAME', frame)
#                 count += 1
#             else:
#                 break

#     def test_detect_invalid(self):
#         self.motion_detect = MotionDetect()
#         self.motion_detect.capture = CV2.VideoCapture(self.test_video)
#         capture = self.motion_detect.capture
#         isDetect, frame = capture.read() 
#         self.handle_open_video(capture, frame, isDetect )
#         self.assertEqual(isDetect,  True)

#     def test_rescale_frame(self):
#         self.motion_detect = MotionDetect()
#         self.motion_detect.capture = CV2.VideoCapture(self.test_video)
#         capture = self.motion_detect.capture
#         isReading, frame = capture.read()
#         self.handle_open_video(capture,frame, isReading)  
#         self.motion_detect.actions(self.motion_detect.rescaleFrame(frame))
#         self.assertTrue(isReading != None)

#     def test_motiondetect_init_then_cleanup(self):
#         self.motion_detect = MotionDetect()
#         captured_video = CV2.VideoCapture(self.test_video)
#         isReading, frame = self.motion_detect.capture.read()
#         self.motion_detect.cleanUp()
#         self.assertEqual(isReading, False)


# if __name__ == '__main__':
#     unittest.main()

