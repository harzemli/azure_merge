import pytest
import coordinates

TEST_TRACK_DICT = {
    'inner_track': {
        'part_1': ['1,1'],
        'part_2': ['2,4', '3,9'],
        'part_3': ['4,10', '5,15']},
    'outer_track': {
        'part_1': ['10,1'],
        'part_2': ['11,11', '12,111'],
        'part_3': ['13,1111', '14,11111']},
    'links': {
        'inner_to_outer_track': ['10,100', '50,50', '100,10'],
        'outer_to_inner_track': ['100,10', '50,50', '10,100']}}
TEST_INNER_TRACK = ['1,1', '2,4', '3,9', '4,10', '5,15']
TEST_OUTER_TRACK = ['10,1', '11,11', '12,111', '13,1111', '14,11111']

# Test track 1 order:
# -> inner_1, inner_2, inner_3, inner_1
# -> links_in_to_out
# -> outer_3, outer_1
# -> links_out_to_in
# -> inner_3
TEST_TRACK_1 = ['1,1', '2,4', '3,9', '4,10', '5,15', '1,1',
                '10,100', '50,50', '100,10',
                '13,1111', '14,11111', '10,1',
                '100,10', '50,50', '10,100',
                '4,10', '5,15']
TEST_TRACK_1_X = [1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 10.0, 50.0, 100.0,
                  13.0, 14.0, 10.0, 100.0, 50.0, 10.0, 4.0, 5.0]
TEST_TRACK_1_Y = [1.0, 4.0, 9.0, 10.0, 15.0, 1.0, 100.0, 50.0, 10.0,
                  1111.0, 11111.0, 1.0, 10.0, 50.0, 100.0, 10.0, 15.0]
# Test track 2 order:
# -> outer_1
# -> links_out_to_in
# -> inner_3, inner_1, inner_2, inner_3, inner_1
# -> links_in_to_out
# -> outer_3
TEST_TRACK_2 = ['10,1',
                '100,10', '50,50', '10,100',
                '4,10', '5,15', '1,1', '2,4', '3,9', '4,10', '5,15', '1,1',
                '10,100', '50,50', '100,10',
                '13,1111', '14,11111']
TEST_TRACK_2_X = [10.0, 100.0, 50.0, 10.0, 4.0, 5.0, 1.0, 2.0, 3.0,
                  4.0, 5.0, 1.0, 10.0, 50.0, 100.0, 13.0, 14.0]
TEST_TRACK_2_Y = [1.0, 10.0, 50.0, 100.0, 10.0, 15.0, 1.0, 4.0, 9.0,
                  10.0, 15.0, 1.0, 100.0, 50.0, 10.0, 1111.0, 11111.0]


def test_create_tracks():
    t1, t2 = coordinates.create_tracks(TEST_TRACK_DICT)
    assert t1 == TEST_INNER_TRACK
    assert t2 == TEST_OUTER_TRACK


@pytest.mark.parametrize('test_track, expected_x, expected_y', [
    (TEST_TRACK_1, TEST_TRACK_1_X, TEST_TRACK_1_Y),
    (TEST_TRACK_2, TEST_TRACK_2_X, TEST_TRACK_2_Y)])
def test_extract_x_and_y_values_lists(test_track, expected_x, expected_y):
    x, y = coordinates.extract_x_and_y_values_lists(test_track)
    assert x == expected_x
    assert y == expected_y
