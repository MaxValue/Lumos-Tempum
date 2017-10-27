#!/usr/bin/env python3
# coding: utf-8

import os, importlib, configparser, csv, time, datetime, shutil, subprocess

technology_names = os.walk(os.path.join(os.getcwd(),"technologies")).__next__()[1]
technologies = {}
for technology in technology_names:
	if technology != "__pycache__":
		technologies[technology] = importlib.import_module("technologies."+technology+".adapter")

def get_time():
	utc_offset = config.getint("GENERAL", "utc_offset", fallback=0)
	current_time = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=utc_offset)))
	return time_to_percent(current_time.hour, current_time.minute)

def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)
	return float( rightMin + (valueScaled * rightSpan) )

def time_to_percent(hours, minutes):
	return ((float(hours) * 60 * 60) + (float(minutes) * 60)) / 86400.0

def get_light_setting():
	current_time = get_time()

	next_day = 0.0
	for i, this_time in enumerate(times):
		if this_time["Start"] > current_time:
			interval_end = this_time
			end_index = i
			break
	else:
		interval_end = times[0]
		next_day = 1.0
		end_index = 0

	for i in range(end_index, -1, -1):
		if times[i]["Start"] <= current_time:
			interval_start = times[i]
			break
	else:
		interval_start = times[-1]
		next_day = 1.0

	brightness = translate(
							current_time,
							interval_start["Start"],
							interval_end["Start"]+next_day,
							interval_start["Brightness"],
							interval_end["Brightness"]
						)
	temperature = translate(
							current_time,
							interval_start["Start"],
							interval_end["Start"]+next_day,
							interval_start["Temperature"],
							interval_end["Temperature"]
						)

	return (brightness, temperature)

def log_this(msg):
	print(msg, flush=True)

log_this("loading vars and configs")

config_folder = os.path.join(os.path.expanduser("~"),".config/lumostempum")
if not os.path.exists(config_folder):
	os.makedirs(config_folder)
if not os.path.exists(os.path.join(config_folder,"settings.ini")):
	shutil.copy(os.path.join(os.getcwd(),"settings.ini"),os.path.join(config_folder,"settings.ini"))

config = configparser.ConfigParser(default_section="DO NOT USE THIS SECTION", empty_lines_in_values=False)
config.read(os.path.join(config_folder,"settings.ini"))

for technology in technologies.keys():
	technologies[technology].init(config)

times = []
with open(os.path.expanduser(config.get("GENERAL","schedule_file")), encoding="utf-8") as schedule_file:
	schedule_file_reader = csv.DictReader(schedule_file, delimiter=';')
	for keyframe in schedule_file_reader:
		times.append({
						"Start":time_to_percent(keyframe["Hour"],keyframe["Minute"]),
						"Brightness":float(keyframe["Brightness"]),
						"Temperature":float(keyframe["Temperature"])
					})
times = sorted(times, key=lambda keyframe: keyframe["Start"])

heartbeat_time = config.getint("GENERAL", "heartbeat_time")

error_occured = False

log_this("entering loop")

while 1:
	if os.path.exists(os.path.join(config_folder,"LUMOSTEMPUM.STOP")):
		log_this("quitting!")
		os.remove(os.path.join(config_folder,"LUMOSTEMPUM.STOP"))
		quit()

	target_brightness, target_temperature = get_light_setting()
	#subprocess.call(["systemd-notify","--status=Brightness: {:.2%} Temperature: {:.0f}K".format(target_brightness,target_temperature)])

	for technology in technologies.keys():
		if not technologies[technology].set_both(target_brightness, target_temperature):
			error_occured = True
			break
	else:
		error_occured = False

	if error_occured:
		time.sleep(10)
	else:
		time.sleep(heartbeat_time)
