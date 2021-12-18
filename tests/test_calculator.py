import pytest
import calculator


def test_calculate_air_friction():
    # given AIR_FRICTION_COEFFICIENT = 0.00035
    velocity = 11
    assert calculator.calculate_air_friction(velocity) == 0.021175


def test_total_force():
    # given SLIDING_FRICTION_COEFFICIENT = 0.0001
    #      AIR_FRICTION_COEFFICIENT = 0.00035
    velocity = 5
    throttle_force = 7
    assert calculator.total_force(velocity, throttle_force) == 6.994644


@pytest.mark.parametrize('old_velocity, throttle_force, expected', [
    (11, 13, 0),
    (125, 325, 447.264644)])
def test_velocity(old_velocity, throttle_force, expected):
    assert calculator.velocity(old_velocity, throttle_force) == expected


@pytest.mark.parametrize('x1, y1, x2, y2, x3, y3, expected', [
    (3, 3, 4, 4, 3, 5, 1),
    (3, 3, 5, 5, 3, 7, 2),
    (3, 3, 5, 5, 3, 6, 1.5811),
    (0, 0, 1, 2, 3, 4, 7.9057),
    (0, 0, 2, 1, 4, 3, 7.9057)])
def test_radius(x1, y1, x2, y2, x3, y3, expected):
    # expected values retrieved from https://planetcalc.com/8116/
    assert round(calculator.radius(x1, y1, x2, y2, x3, y3), 4) == expected


def test_centripetal_force():
    # value retrieved from https://www.omnicalculator.com/physics/centripetal-force
    # with car mass 1
    assert round(calculator.centripetal_force(17, 19), 2) == 15.21


@pytest.mark.parametrize('centripetal_force', [
    calculator.DERAIL_THRESHOLD + 0.0001,
    -calculator.DERAIL_THRESHOLD - 0.0001])
def test_is_derailed(centripetal_force):
    assert calculator.is_derailed(centripetal_force)


def test_is_not_derailed():
    centripetal_force = calculator.DERAIL_THRESHOLD
    assert calculator.is_derailed(centripetal_force) is False


def test_euclidean_distance():
    delta_x = 3
    delta_y = 4
    assert calculator.euclidean_distance(delta_x, delta_y) == 5


def test_calculate_deltas():
    x1, x2, y1, y2, = (0, 3, 0, 4)
    expected = (3, 4)
    assert calculator.calculate_deltas(x1, x2, y1, y2) == expected


def test_new_position():
    velocity = 11
    x1 = 1
    y1 = 2
    x2 = 4
    y2 = 6
    interval = 3
    expected_x = 20.8
    expected_y = 28.4

    assert round(calculator.new_position(velocity, x1, x2, y1, y2, interval)['x'], 1) == expected_x
    assert round(calculator.new_position(velocity, x1, x2, y1, y2, interval)['y'], 1) == expected_y
    assert calculator.new_position(velocity, x1, x2, y1, y2, interval)['coordinate_reached'] is True


def test_coordinate_reached():
    interval = 1.1
    total_time_needed = 2
    assert calculator.coordinate_reached(interval, total_time_needed)


def test_coordinate_not_reached():
    interval = 1
    total_time_needed = 2
    assert calculator.coordinate_reached(interval, total_time_needed) is False
