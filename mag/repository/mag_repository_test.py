import unittest
from mag.repository.mag_repository import MagRepository
from mag.domain.mag import Mag
from flask_mongoalchemy import fields


class TestMagRepository(unittest.TestCase):
    def test_create(self):
        rep = MagRepository()
        id1 = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        id2 = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        self.assertNotEqual(id1, id2)
        rep.delete(id1)
        rep.delete(id2)

    # def test_get_exists(self):
    #     rep = MagRepository()
    #     mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 5)
    #     mag1 = rep.get(mag_id)
    #     mag2 = Mag(mag_id=fields.ObjectId(mag_id), kassir_id=fields.ObjectId('5bfbacaf102bd238e0238fa5'),
    #                      date_time='01.01.2018_12:00', col=[True, True, True, True, True])
    #     self.assertEqual(mag1, mag2)
    #     rep.delete(mag_id)

    def test_get_false(self):
        rep = MagRepository()
        mag = rep.get('5bd89b59af1')
        self.assertIsNone(mag)

    def test_read_paginated(self):
        rep = MagRepository()
        mags = rep.read_paginated(1, 5)
        self.assertLessEqual(len(mags), 5)

    def test_delete(self):
        rep = MagRepository()
        mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        rep.delete(mag_id)
        self.assertFalse(rep.exists(mag_id))

    def test_get_a_seat_true(self):
        rep = MagRepository()
        mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        boolean = rep.get_a_seat(mag_id, 2)
        self.assertTrue(boolean)
        rep.delete(mag_id)

    def test_get_a_seat_false(self):
        rep = MagRepository()
        mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        rep.get_a_seat(mag_id, 2)
        boolean = rep.get_a_seat(mag_id, 2)
        self.assertFalse(boolean)
        rep.delete(mag_id)

    def test_get_a_seat_none(self):
        rep = MagRepository()
        boolean = rep.get_a_seat('5bd897f8af', 1)
        self.assertIsNone(boolean)

    def test_free_a_seat_true(self):
        rep = MagRepository()
        mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        rep.get_a_seat(mag_id, 1)
        boolean = rep.free_a_seat(mag_id, 1)
        self.assertTrue(boolean)
        rep.delete(mag_id)

    def test_free_a_seat_false(self):
        rep = MagRepository()
        mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        boolean = rep.free_a_seat(mag_id, 2)
        self.assertFalse(boolean)
        rep.delete(mag_id)

    def test_free_a_seat_none(self):
        rep = MagRepository()
        boolean = rep.free_a_seat('5bd897f8af', 2)
        self.assertIsNone(boolean)

    def test_exists(self):
        rep = MagRepository()
        mag_id = rep.create('5bd89b59af13c757e1b7f3fd', '01.01.2018_12:00', 50)
        boolean = rep.exists(mag_id)
        self.assertTrue(boolean)
        rep.delete(mag_id)


if __name__ == '__main__':
    unittest.main()
