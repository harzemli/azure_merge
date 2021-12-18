""" main module for the race. Run this program
    Create a car class, check if it is accelerating or if it will derail
    Display lap times, number of laps completed"""
import calculator as calculate
import coordinates
import godot_communicator
import json
import time

""" Godot communication """
GODOT_IP = '127.0.0.1'
LISTENER_PORT = 4242
UPDATE_INTERVAL = 1 / 60

VELOCITY_MODIFIER = 70                      # Throttle force
INNER_TRACK = True                          
OUTER_TRACK = False
LAST_LANE_CHANGE_REQUEST_POINT = 25         # Last point in the segment 1 of the track.


class Car:
    """define the car class here"""
    def __init__(self, track, cpu_controlled):
        """ initialize as player or cpu car and provide coordinates and other properties """
        if cpu_controlled:
            self.name = "cpuCar"
            self.current_track = INNER_TRACK
        else:
            self.name = "playerCar"
            self.current_track = OUTER_TRACK
        self.velocity = 0
        self.track = track
        # print(len(track))
        self.x, self.y = coordinates.extract_x_and_y_values_lists(track)
        # self.x=[float(item) for item in (x[1:])]
        # self.y=[float(item) for item in (y[1:])]
        # print(self.x)
        self.coordinateIndex = 0
        self.coordinate = {'x': self.x[self.coordinateIndex],
                           'y': self.y[self.coordinateIndex],
                           'coordinate_reached': True}
        self.position = 1
        self.position_percentage = 0
        self.CpuControlled = cpu_controlled
        self.derailed = False
        self.best_lap = 0
        self.last_lap = 0
        self.lap_start_time = 0
        self.progress = 0
        self.ready_to_lane_change = False
        self.derail_start_time = 0

    def is_accelerating(self, data):
        """ Check if space bar is being pressed by player """
        if self.CpuControlled:
            return True if b'enter' in data else False
        else:
            return True if b'space' in data else False

    def check_for_reset(self, data):
        """ check if the reset button is pressed """
        if data:
            if self.CpuControlled:
                if b'cpu_reset' in data:
                    return True
                else:
                    return False
            else:
                if b'player_reset' in data:
                    return True
                else:
                    return False

    def check_lane_change(self, data):
        """ To check if lane change button is pressed and invoke the lane change \
            function if it is pressed before the permissible coordinate """
        if data and self.coordinateIndex < LAST_LANE_CHANGE_REQUEST_POINT:
            if (self.CpuControlled and b'lane_change_cpu' in data) or \
                    (not self.CpuControlled and b'lane_change_player' in data):
                self.lane_change_pre()

    def lane_change_pre(self):
        """ changes the 2nd and 3rt part of the track accordingly """
        if self.current_track == INNER_TRACK:
            self.x, self.y = coordinates.extract_x_and_y_values_lists(inner_to_outer_track)
            self.track = inner_to_outer_track
        else:
            self.x, self.y = coordinates.extract_x_and_y_values_lists(outer_to_inner_track)
            self.track = outer_to_inner_track
        self.ready_to_lane_change = True                                # Flag for lane change button

    def lane_change_post(self):
        """ Changes the 1st and 2nd part of the track after the car passes 2nd part(link) of the track """
        if self.current_track == INNER_TRACK:
            self.current_track = OUTER_TRACK
            self.x, self.y = coordinates.extract_x_and_y_values_lists(all_outer_track)
            self.track = all_outer_track
        else:
            self.current_track = INNER_TRACK
            self.x, self.y = coordinates.extract_x_and_y_values_lists(all_inner_track)
            self.track = all_inner_track

        self.ready_to_lane_change = False

    def is_derailed(self):
        """ calculate the centripetal force and check if it is greater than the threshold for derailing"""
        i = self.coordinateIndex
        if i < 1:
            return False
        radius = calculate.radius(self.x[i], self.y[i], self.x[i - 1], self.y[i - 1], self.x[i - 2], self.y[i - 2])
        centripetal_force = calculate.centripetal_force(self.velocity, radius)
        return calculate.is_derailed(centripetal_force)
    
    def derail(self):
        """ if derailed, change the status of variable derailed and the velocity to zero"""
        print("DERAILED")
        self.velocity = 0
        self.derailed = True
        self.derail_start_time = time.time()
        return 'derailed'

    def set_lap_start_time(self):
        """ begin the stopwatch for the race lap"""
        if not self.lap_start_time:
            self.lap_start_time = time.time()

    def reset_initial(self):
        """ to reset car in its initial track """
        if self.CpuControlled:
            self.track = all_inner_track
            self.x, self.y = coordinates.extract_x_and_y_values_lists(all_inner_track)
            self.current_track = INNER_TRACK
        else:
            self.track = all_outer_track
            self.x, self.y = coordinates.extract_x_and_y_values_lists(all_outer_track)
            self.current_track = OUTER_TRACK 

    def reset(self):
        """ if reset by user, reset the car to initial position and the lap time """
        self.reset_initial()
        self.coordinate = {'x': self.x[0], 'y': self.y[0], 'coordinate_reached': True}
        self.velocity = 0
        self.coordinateIndex = 0
        self.lap_start_time = 0
        self.ready_to_lane_change = False
        self.best_lap = 0
        self.last_lap = 0
        self.progress = 0


    def update_velocity(self, new_data):
        """ update car velocity"""
        # self.velocity = get_new_velocity(self.velocity, self.is_accelerating(new_data) if new_data else False)
        if self.CpuControlled:
            if new_data:
                self.velocity = calculate.velocity(self.velocity,
                                                   VELOCITY_MODIFIER if self.is_accelerating(new_data) else 0)
            else:
                self.velocity = calculate.velocity(self.velocity, 1)
        else:
            if new_data:
                self.velocity = calculate.velocity(self.velocity,
                                                   VELOCITY_MODIFIER if self.is_accelerating(new_data) else 0)
            else:
                self.velocity = calculate.velocity(self.velocity, 0)

    def calculate_position(self):
        """ calculate next coordinate"""
        i = self.coordinateIndex
        next_coord = i + 1 if i + 1 < len(self.track) else 0
        self.coordinate = calculate.new_position(self.velocity,
                                                 self.coordinate['x'],
                                                 self.x[next_coord],
                                                 self.coordinate['y'],
                                                 self.y[next_coord],
                                                 UPDATE_INTERVAL)
        if self.coordinate['coordinate_reached']:
            self.coordinateIndex = next_coord
            print(next_coord)
            if self.coordinateIndex == 0:
                self.lap_complete()

    def lap_complete(self):
        """ if lap is completed, update the count"""
        self.progress += 1
        self.set_last_lap()
        print("Laps completed: " + str(self.progress))

    def set_best_lap(self, lap_time):
        """ check lowest lap time and update"""
        if lap_time < self.best_lap or self.best_lap == 0:
            self.best_lap = lap_time

    def set_last_lap(self):
        """ check the last lap time and update required variables"""
        lap_time = round((time.time() - self.lap_start_time) * 1000)
        self.last_lap = lap_time
        self.lap_start_time = time.time()
        self.set_best_lap(lap_time)

    def set_position_percentage(self):
        """ calculate position percentage"""
        self.position_percentage = 100 * (self.coordinateIndex / len(self.track))

    def get_dictionary(self):
        """ create dictionary for car and add key-value pairs"""
        dictionary = {
            "name": self.name,
            "velocity": self.velocity,
            "last_lap": self.last_lap,
            "best_lap": self.best_lap,
            "derailed": self.derailed,
            "coordinate": self.coordinate,
            "race_position": self.position,
            "progress": self.progress
        }
        return dictionary


def set_cars_position():
    """ Function to see which car is leading the race"""
    if len(cars) > 1:
        cars[0].position_percentage = ((cars[0].coordinateIndex)/ len(cars[0].track))*100
        cars[1].position_percentage = ((cars[1].coordinateIndex)/ len(cars[1].track))*100
        if cars[0].progress > cars[1].progress:
            cars[0].position = "1st"
            cars[1].position = "2nd"
        elif cars[0].progress == cars[1].progress and cars[0].position_percentage >= cars[1].position_percentage:
            cars[0].position = "1st"
            cars[1].position = "2nd"
        else:
            cars[0].position = "2nd"
            cars[1].position = "1st"


def game_loop(cars):
    """ the main loop where all functions act and the race keeps running"""
    # set up communicator
    communicator = godot_communicator.Connection(GODOT_IP, LISTENER_PORT)
    communicator.start_sending(UPDATE_INTERVAL)

    while True:
        new_data = communicator.receive_data()

        message_dictionary = {}
        for car in cars:
            car.check_lane_change(new_data)
            if car.check_for_reset(new_data):
                # reset this car
                cars[0].reset()
                cars[1].reset()
            if car.is_derailed():
                car.derail()
            else:
                if not car.derailed:
                    car.update_velocity(new_data)
                else:
                    if time.time() - car.derail_start_time > 3:
                        car.derailed = False

                if car.velocity > 0:
                    car.set_lap_start_time()
                    set_cars_position()
                    car.calculate_position()

            if car.ready_to_lane_change: 
                if car.track == inner_to_outer_track and car.coordinateIndex == 30:         
                    """ 30 and 33 are the coordinate index for the end of part 2 of inner and outer track. \
                        the lane_change_post() function is only to be invoked after the car \
                        reaches these points """
                    car.lane_change_post()
                    car.coordinateIndex = 31
                elif car.track == outer_to_inner_track and car.coordinateIndex == 33:
                    car.lane_change_post()    
            message_dictionary[car.name] = car.get_dictionary()
        json_message: str = json.dumps(message_dictionary)
        communicator.set_data(json_message)


if __name__ == "__main__":
    all_inner_track, all_outer_track, inner_to_outer_track, outer_to_inner_track = coordinates.load_tracks()
    # print(coordinates.load_tracks())
    # outer_track.insert(0,'q,q')
    # print(inner_track)
    playerCar = Car(all_outer_track, False)
    cpuCar = Car(all_inner_track, True)
    # print(playerCar)
    cars = [playerCar, cpuCar]
    # add CpuCar
    game_loop(cars)
    # run_simulation(outer_track)
