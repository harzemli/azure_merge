extends Label

# Called when the node enters the scene tree for the first time.
func _ready():
	text = get_node("/root/Navigation2D").SERVER_IP
