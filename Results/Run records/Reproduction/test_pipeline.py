"""Meaningful boundary checks for the report publication and archive paths."""
import hashlib,json,pathlib,tempfile,unittest,zipfile
from unittest.mock import patch
import pipeline
from pipeline import extract,safe_publish,sha
class PipelineTests(unittest.TestCase):
    def test_changed_frozen_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);file=root/'input.csv';file.write_text('0,1')
            (root/'package-manifest.json').write_text(json.dumps(dict(Files=[dict(Path='input.csv',Sha256=sha(file))])))
            with patch.object(pipeline,'PACKAGE',root):
                pipeline.check_package();file.write_text('1,0')
                with self.assertRaises(ValueError):pipeline.check_package()
    def test_existing_work_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);work=root/'existing';work.mkdir();sentinel=work/'keep';sentinel.write_text('preserve')
            with patch('sys.argv',['pipeline.py','--output',str(root/'Results'),'--work',str(work)]):
                with self.assertRaises(FileExistsError):pipeline.main()
            self.assertEqual(sentinel.read_text(),'preserve')
    def test_refuse_archive_escape(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);z=root/'bad.zip'
            with zipfile.ZipFile(z,'w') as a:a.writestr('../outside.txt','bad')
            with self.assertRaises(ValueError):extract(z,root/'inside')
            self.assertFalse((root/'outside.txt').exists())
    def test_archive_replaced_files_and_preserve_unrelated(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);src=root/'stage';dst=root/'Results';src.mkdir();dst.mkdir()
            (src/'report.csv').write_text('new');(dst/'report.csv').write_text('old');(dst/'unrelated.txt').write_text('keep')
            changed=safe_publish(src,dst,root/'archive')
            self.assertEqual((dst/'report.csv').read_text(),'new');self.assertEqual((dst/'unrelated.txt').read_text(),'keep')
            self.assertEqual((root/'archive/report.csv').read_text(),'old');self.assertEqual(len(changed),1)
            self.assertEqual(safe_publish(src,dst,root/'unused'),[])
    def test_compilation_logs_stay_in_work_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);src=root/'stage';folder=src/'Individual simulations/case';folder.mkdir(parents=True)
            (folder/'strategy.pdf').write_bytes(b'pdf');(folder/'strategy.aux').write_text('aux');(folder/'strategy.log').write_text('log')
            changed=safe_publish(src,root/'Results',root/'archive')
            self.assertEqual(len(changed),1);self.assertTrue((root/'Results/Individual simulations/case/strategy.pdf').exists())
            self.assertFalse((root/'Results/Individual simulations/case/strategy.log').exists());self.assertTrue((folder/'strategy.log').exists())
if __name__=='__main__':unittest.main()
