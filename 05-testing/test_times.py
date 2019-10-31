from times import overlap_time, time_range
import datetime

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
    result = overlap_time(first, second) 
    for i in range (len(overlap_time(first, second))):
        t0_s = datetime.datetime.strptime(overlap_time(first, second)[i][0], "%Y-%m-%d %H:%M:%S")
        t1_s = datetime.datetime.strptime(overlap_time(first, second)[i][1], "%Y-%m-%d %H:%M:%S")
        result = (t1_s - t0_s).total_seconds()
        assert result == 1200

# Dont overlap at all
# If the two times are the same 
# Different lengths of overlap
# Overlapping times but different days 
# If your gap is too long for your time - error
# If your time is not divisable how the gaps are defined 
