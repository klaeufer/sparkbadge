import unittest
import yaml
from os.path import join, dirname

class TestMetrics(unittest.TestCase):
    """Tests metrics."""

    def test_changes(self):

        spark_dir = join(dirname(__file__), "../../.sparkbadge")
        with open(spark_dir + "/" + "spark.yml", 'r') as file:
            cfg = file.read()
        meta = yaml.safe_load(cfg)
        # metric = meta["metrics"][source][metric_type] 
        for source in meta["metrics"]:
            for metric_type in source:
                print("SOURCE IS ", source)
                self.assertEqual(url, 
                     sparkbadge.sparkbadge(
                         uep, date, metric_type, source, "spark.yml"))


if __name__ == '__main__':
    unittest.main()
