# Copyright 2017 Adrian-Ioan Garovat, Emanuel Covaci, Sebastian-Valeriu Males
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from authentication.tests import ExtendedUser
from config.settings import BASE_DIR
from event.forms import EventCreationFormAdmin
from event.models import Event


class EventTestCase(TestCase):

    def setUp(self):
        """ Create user for tests """
        self.user = ExtendedUser.objects.create_user(first_name="test",
                                                     last_name="forthewin",
                                                     username="kek",
                                                     password="cevaparola")
        self.event = Event.objects.create(name="de test",
                                          text="ca sa fie",
                                          address="Something",
                                          geolocation="4,20",
                                          author=self.user)

    def test_create_event(self):
        """ Test if event is created correctly"""
        obj = self.event

        self.assertTrue(isinstance(obj, Event))
        self.assertEqual(obj.__unicode__(), obj.name)


class EventCreationFormAdminTestCase(TestCase):

    def setUp(self):
        self.post_dict = {
            "name": "Testing event",
            "text": "Such text much wow",
            "date_0": (datetime.datetime.today() +
                    datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "date_1": (datetime.datetime.now() +
                       datetime.timedelta(hours=9)).strftime('%H:%M:%S'),
            "address": "Dayton, OH, USA",
            "geolocation": "39.7589478,-84.19160690000001"
        }

    def get_file(sef, filepath):
        uploadedfile = open(BASE_DIR + filepath, "rb")
        file_dict = {
            'file': SimpleUploadedFile(uploadedfile.name, uploadedfile.read())

        }
        return file_dict

    def test_big_file_validation(self):
        """Tests if form is valid with a big file"""
        form = EventCreationFormAdmin(
            self.post_dict, self.get_file("/static/test_files/big_file"))
        self.assertFalse(form.is_valid())

    def test_wrong_mime_type(self):
        """Tests if form is valid with the wrong mime type file"""
        form = EventCreationFormAdmin(
            self.post_dict, self.get_file("/static/test_files/good_file"))
        self.assertFalse(form.is_valid())

    def test_wrong_date(self):
        inp = self.post_dict
        inp["date_0"] = (datetime.datetime.now() +
                         datetime.timedelta(days=-2)).strftime('%Y-%m-%d')
        form = EventCreationFormAdmin(
            inp, self.get_file("/static/assets/counter-bg.jpg"))
        self.assertFalse(form.is_valid())

    def test_correct_form_validation(self):
        """Tests if form is valid with correct info"""
        form = EventCreationFormAdmin(
            self.post_dict, self.get_file("/static/assets/counter-bg.jpg"))
        print self.post_dict
        print form.errors
        self.assertTrue(form.is_valid())
