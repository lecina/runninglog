import unittest
import os.path
import logging

from runninglog.constants import blockNames
from runninglog.config import config


logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


class TestConfig(unittest.TestCase):
    def test_change_output_dir(self):
        desc_dict = {blockNames.ConfigParams.output_dir: 'alternative'}

        configuration = config.Config()
        self.assertNotEqual(configuration.output_dir, 'alternative')
        configuration.load_config(desc_dict)
        self.assertEqual(configuration.output_dir, 'alternative')

    def test_change_raw_output_dir(self):
        desc_dict = {blockNames.ConfigParams.raw_output_dir: 'alternative'}

        configuration = config.Config()

        golden_val = os.path.join('data', 'alternative')
        self.assertNotEqual(configuration._raw_output_dir, golden_val)
        configuration.load_config(desc_dict)
        self.assertEqual(configuration._raw_output_dir, golden_val)

    def test_change_processed_output_dir(self):
        desc_dict = {blockNames.ConfigParams.processed_output_dir: 'alternative'}

        configuration = config.Config()

        golden_val = os.path.join('data', 'alternative')
        self.assertNotEqual(configuration._processed_output_dir, golden_val)
        configuration.load_config(desc_dict)
        self.assertEqual(configuration._processed_output_dir, golden_val)

    def test_change_input_dir(self):
        desc_dict = {blockNames.ConfigParams.input_dir: 'alternative'}

        configuration = config.Config()
        self.assertNotEqual(configuration.input_dir, 'alternative')
        configuration.load_config(desc_dict)
        self.assertEqual(configuration.input_dir, 'alternative')

    def test_change_df_name(self):
        desc_dict = {blockNames.ConfigParams.df_name: 'alternative'}

        configuration = config.Config()
        self.assertNotEqual(configuration._df_name, 'alternative')
        configuration.load_config(desc_dict)
        self.assertEqual(configuration._df_name, 'alternative')

    def test_change_df_struct_name(self):
        desc_dict = {blockNames.ConfigParams.df_struct_name: 'alternative'}

        configuration = config.Config()
        self.assertNotEqual(configuration._df_struct_name, 'alternative')
        configuration.load_config(desc_dict)
        self.assertEqual(configuration._df_struct_name, 'alternative')

    def test_change_output_fmt(self):
        desc_dict = {blockNames.ConfigParams.output_fmt: 'csv'}

        configuration = config.Config()
        self.assertNotEqual(configuration.output_format, ['csv'])
        configuration.load_config(desc_dict)
        self.assertEqual(configuration.output_format, ['csv'])

    def test_change_output_fmt_list(self):
        desc_dict = {blockNames.ConfigParams.output_fmt: ['pickle', 'csv']}

        configuration = config.Config()
        #order is reversed in default values
        self.assertNotEqual(configuration.output_format, ['pickle', 'csv'])
        configuration.load_config(desc_dict)
        self.assertEqual(
            set(configuration.output_format), set(['pickle', 'csv'])
        )

def main():
    return unittest.main(exit=False)

if __name__ == "__main__":
    main()
