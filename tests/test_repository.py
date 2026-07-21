import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RepositoryTests(unittest.TestCase):
    def test_grants_have_required_fields(self):
        data=json.loads((ROOT/'data/current/grants.json').read_text())
        for g in data['grants']:
            for field in ('id','title','agency','category','status','url'):
                self.assertTrue(g.get(field),f'Missing {field}')
    def test_urls_are_https(self):
        data=json.loads((ROOT/'data/current/grants.json').read_text())
        self.assertTrue(all(g['url'].startswith('https://') for g in data['grants']))
    def test_unique_ids(self):
        data=json.loads((ROOT/'data/current/grants.json').read_text())
        ids=[g['id'] for g in data['grants']]; self.assertEqual(len(ids),len(set(ids)))
if __name__=='__main__': unittest.main()
