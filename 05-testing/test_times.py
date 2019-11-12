from times import overlap_time, time_range
import datetime
import pytest

@pytest.mark.parametrize('test_input, expected', [
     # no overlap
     ([["2019-01-01 00:00:00", "2019-01-01 23:50:00"], ["2019-01-02 00:30:00", "2019-01-02 23:55:00"]], []),
     # touching edges
     ([["2019-10-31 00:00:00", "2019-10-31 00:50:00", 3, 600], ["2019-10-31 00:10:00", "2019-10-31 01:00:00", 3, 600]], []),
 ])

def test_many(test_input, expected):
     large = time_range(*test_input[0])
     short = time_range(*test_input[1])
     result = overlap_time(large, short)
     assert result == expected

def test_range_backwards():
     with pytest.raises(ValueError, match=r"End date should be after the start date for the interval"):
         time_range("2019-10-31 00:00:00", "2019-10-30 00:50:00", 3, 600)

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = overlap_time(large, short) 
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    assert result == expected

def test_class_time():
    large = time_range("2010-10-31 10:00:00", "2010-10-31 13:00:00")
    short = time_range("2010-10-31 10:05:00", "2010-10-31 12:55:00", 3, 600)
    result = overlap_time(large, short) 
    assert result == short

def test_20min():
    first = time_range("2010-10-31 00:00:00", "2010-10-31 23:50:00", 24, 10*60)
    second = time_range("2010-10-31 00:30:00", "2010-10-31 23:55:00", 24, 35*60)
    for i in range (len(overlap_time(first, second))):
        t0_s = datetime.datetime.strptime(overlap_time(first, second)[i][0], "%Y-%m-%d %H:%M:%S")
        t1_s = datetime.datetime.strptime(overlap_time(first, second)[i][1], "%Y-%m-%d %H:%M:%S")
        result_t = (t1_s - t0_s).total_seconds()
        assert result_t == 1200

   # assert all([(datetime.datetime.strptime(t0, "%Y-%m-%d %H:%M:%S")-datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")).total_seconds()==20*60 for t0, t1 in overlap_time(first, second)])
   # use a debugger

## Ideas for testing 

# Dont overlap at all
# If the two times are the same 
# Different lengths of overlap
# Overlapping times but different days 
# If your gap is too long for your time - error
# If your time is not divisable how the gaps are defined 
