from django.utils import unittest
from django_toolkit.csv.unicode import UnicodeWriter, UnicodeReader, CastingUnicodeWriter
from tempfile import NamedTemporaryFile


class UnicodeWriterTestCase(unittest.TestCase):

    def test_write(self):
        f = NamedTemporaryFile(mode='w+')
        csv_writer = UnicodeWriter(f, lineterminator="\n")
        csv_writer.writerow(['NAME', 'AGE'])
        csv_writer.writerow(['foo', '12'])
        csv_writer.writerow(['bar', '16'])
        f.seek(0)
        actual = f.read()
        expected = ("NAME,AGE\n"
                    "foo,12\n"
                    "bar,16\n")
        self.assertEqual(actual, expected)


class CastingUnicodeWriterTestCase(unittest.TestCase):
 
    def test_write(self):
        f = NamedTemporaryFile(mode='w+')
        csv_writer = CastingUnicodeWriter(f, lineterminator="\n")
        csv_writer.writerow(['NAME', 'AGE', 'THINGS'])
        csv_writer.writerow(['foo', 12, 12.31])
        csv_writer.writerow(['bar', 16, 78.89])
        f.seek(0)
        actual = f.read()
        expected = ("NAME,AGE,THINGS\n"
                    "foo,12,12.31\n"
                    "bar,16,78.89\n")
        self.assertEqual(actual, expected)


class UnicodeReaderWriterTestCase(unittest.TestCase):

    def test_read(self):
        f = NamedTemporaryFile(mode='w+')
        csv_writer = UnicodeWriter(f, lineterminator="\n")
        expected = [['NAME', 'AGE'],
                    ['foo', '12'],
                    ['bar', '16']]
        csv_writer.writerows(expected)
        f.seek(0)

        csv_reader = UnicodeReader(f)
        actual = [line for line in csv_reader]

        self.assertEqual(actual, expected)
