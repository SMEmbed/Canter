import filecmp
import canter


def test_load_properties():
    pipeline_a = canter.Pipeline('videotestsrc pattern=snow num-buffers=2 ! filesink locaion=a.bin')
    pipeline_a.play()
    pipeline_b = canter.Pipeline('videotestsrc num-buffers=2 ! filesink locaion=b.bin', 'pattern.json')
    pipeline_b.play()

    assert filecmp.cmp('a.bin', 'b.bin')
