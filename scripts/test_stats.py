"""Offline tests for the statistics transformation and error handling."""
from __future__ import annotations
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import refresh_stats as stats

class StatsTests(unittest.TestCase):
    def test_filters_private_and_forks_and_deduplicates(self):
        repos=[
            {'id':1,'language':'Python','stargazers_count':3},
            {'id':2,'language':'TypeScript','stargazers_count':5,'archived':True},
            {'id':3,'language':'Python','stargazers_count':50,'fork':True},
            {'id':4,'language':'Python','stargazers_count':90,'private':True},
            {'id':1,'language':'Python','stargazers_count':3},
            {'id':5,'language':None},
        ]
        d=stats.summarize({'login':'example','followers':7},repos)
        self.assertEqual(d['original_public_repositories'],3)
        self.assertEqual(d['stars_on_original_public_repositories'],8)
        self.assertEqual(d['primary_language_counts'],{'Python':1,'TypeScript':1})
        self.assertEqual(d['followers'],7)

    def test_svg_is_valid_and_escaped(self):
        d=stats.summarize({'login':'example','followers':0},[{'id':1,'language':'A&B <test>'}])
        svg=stats.render(d)
        ET.fromstring(svg)
        self.assertIn('A&amp;B &lt;test&gt;',svg)
        self.assertNotIn('<script',svg)

    def test_zero_repositories(self):
        d=stats.summarize({'login':'example','followers':0},[])
        self.assertEqual(d['original_public_repositories'],0)
        self.assertIn('No primary-language data',stats.render(d))

    def test_failure_keeps_previous_asset(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'card.svg'; p.write_text('previous-good-card')
            with patch('sys.argv',['refresh_stats.py','--output',str(p)]),patch.object(stats,'fetch_summary',side_effect=RuntimeError('offline test')):
                self.assertEqual(stats.main(),1)
            self.assertEqual(p.read_text(),'previous-good-card')

if __name__=='__main__':
    unittest.main()
