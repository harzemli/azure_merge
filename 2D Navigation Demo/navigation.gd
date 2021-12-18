extends Navigation2D

var path = []
var communicator
var thread
var start_tick
var close_game
var cars

var SERVER_IP ="127.0.0.1"
var PORT = 4242
var CHARACTER_SPEED = 10000000

var ExampleJSON: String = '{"playerCar": {"name": "playerCar", '\
+ '"race_position": 1, "velocity": 12, "last_lap": "undefined", "best_lap": '\
+ '"undefined", "derailed": false, "coordinate": "1,1"}, "cpuCar": {"name": '\
+ '"cpuCar", "race_position": 2, "velocity": 13, "last_lap": "undefined", '\
+ '"best_lap": "undefined", "derailed": false, "coordinate": "2,2"}}'

class Communication:
	var server_ip
	var port
	var socket
	
	func _init(server_ip = "127.0.0.1", port=4242):
		self.server_ip = server_ip
		self.port = port
	
	func start_communication():
		self.socket = PacketPeerUDP.new()
		self.socket.set_dest_address(self.server_ip, self.port)
		self.socket.put_packet("Started socket. Port 4242".to_ascii())


class Car:
	var name
	var velocity
	var derailed
	var coordinate
	var race_position
	var best_lap
	var last_lap
	var progress
	var path = []
	
	func _init(name="Car", velocity=0, race_position=0):
		self.name = name
		self.velocity = velocity
		self.race_position = race_position


func _physics_process(delta):
	# delta is 1/60th second
	# walk distance gives pixels / frame
	var walk_distance = CHARACTER_SPEED * delta
	move_along_path(walk_distance)
	
	send_throttle_on_space()
	
	update_timer()


func thread_check_incoming(userdata):
	while true:
		if close_game:
			return # close thread upon closing of game
		var data = get_data()
		if data:
			data = JSON.parse(data).result
			
			update_car_classes(data)
			update_info_grid()

			$Derailed.visible = cars[0].derailed
			$Derailedcpu.visible = cars[1].derailed
			drive_cars()


func _input(event):
	# events are defined in: Project > Project Settings > Input Map tab
	if event.is_action_pressed("r"):
		#$Derailed.visible = false
		reset_timer()
		communicator.socket.put_packet("cpu_reset".to_ascii())
		communicator.socket.put_packet("player_reset".to_ascii())
	
	if event.is_action_pressed("esc"):
		communicator.socket.close()
		close_game = true # ensures thread to close
		get_tree().quit()
		
	if event.is_action_pressed("l"):
		communicator.socket.put_packet("lane_change_player".to_ascii())

	if event.is_action_pressed("c"):
		communicator.socket.put_packet("lane_change_cpu".to_ascii())


func send_throttle_on_space():
	if Input.is_key_pressed(KEY_SPACE):
		if not start_tick:
			# only start timer if not yet started
			start_timer()
		communicator.socket.put_packet("space".to_ascii())
	
	if Input.is_key_pressed(KEY_ENTER):
		communicator.socket.put_packet("enter".to_ascii())


func get_data():
	return communicator.socket.get_packet().get_string_from_ascii()


func update_car_classes(data):
	# print(cars[0].velocity)
	# car classes should be updated with data in JSON format
	for car in cars:
		for variable in car.get_property_list():
			if variable.usage == 8192 && variable.name in data[car.name]:
				# All properties are given, but only properties with usage 8192
				# are variables of the class.
				# Variable is only updated if it present in JSON message
				car[variable.name] = data[car.name][variable.name]


func update_info_grid():
	# pushes the information from car classes into the grid container
	for car in cars:
		get_node("GridContainer/Panel" + car.name + "/Name" + car.name).text = str(car.name)
		get_node("GridContainer/Position" + car.name).text = str(car.race_position)
		get_node("GridContainer/Velocity" + car.name).text = str(round(car.velocity))
		var last_lap = ms_To_mm_ss_msmsms(car.last_lap)
		var best_lap = ms_To_mm_ss_msmsms(car.best_lap)
		get_node("GridContainer/LastLap" + car.name).text = str(last_lap)
		get_node("GridContainer/BestLap" + car.name).text = str(best_lap)
		get_node("GridContainer/Progress" + car.name).text = str(car.progress)


func drive_cars():
	for car in cars:
		var x = car.coordinate.x
		var y = car.coordinate.y
		# print(String(x) + " " + String(y))
		update_navigation_path(get_node(car.name).position, Vector2(x, y), car)
		set_physics_process(true)


func split_coordinate_string(string):
	return string.rsplit(",", true, 6)


func is_derailed(data):
	for car in cars:
		if data[car.name]['derailed'] == true:
			return true
	return false


func start_timer():
	start_tick = OS.get_ticks_msec()


func update_timer():
	if start_tick: # only start showing the time if the timer started
		var current_time = OS.get_ticks_msec() - start_tick
		$Control/Legend2/PanelContainer/Timerlabel.text = ms_To_mm_ss_msmsms(current_time)


func reset_timer():
	start_tick = 0


func ms_To_mm_ss_msmsms(time):
	var digits = []
	var minutes = "%02d" % [time / 60000]
	digits.append(minutes)
	var seconds = "%02d" % [time / 1000]
	digits.append(seconds)
	var milliseconds = "%03d" % [int(ceil(time)) % 1000]
	digits.append(milliseconds)
	var formatted = String()
	var colon = ":"
	for digit in digits:
		formatted += digit + colon
	if not formatted.empty():
		formatted = formatted.rstrip(colon)
	return formatted


func move_along_path(distance): # Distance is pixels required to be traversed in this frame
	for car in cars:
		if car.path:
			var new_point = car.path[car.path.size()-1]
			get_node(car.name).position = new_point
	set_physics_process(false)


func update_navigation_path(start_position, end_position, car):
	# get_simple_path returns a PoolVector2Array of points that lead you
	# from the start_position to the end_position.
	car.path = get_simple_path(start_position, end_position, true)
	# The first point is always the start_position.
	# We don't need it in this example as it corresponds to the character's position.
	car.path.remove(0)


func _init():
	# setup UDP communication
	communicator = Communication.new(SERVER_IP, PORT)
	communicator.start_communication()
	print("A new thread for communication is created ", communicator.socket)
	
	# initialize two car classes
	cars = [Car.new("playerCar", 0, 0), Car.new("cpuCar", 0, 1)]


func _on_Port_text_entered(new_text):
	pass # Replace with function body.


func _ready():
	thread = Thread.new()
	# Third argument is optional userdata, it can be any variable.
	# Thread is used to asynchronously check incoming data
	thread.start(self, "thread_check_incoming", "sogeti")

