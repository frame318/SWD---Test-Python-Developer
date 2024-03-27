"""
เขียนโปรแกรมอะไรก็ได้ที่อยาก present Python's skill set เจ๋ง ๆ ของตัวเอง
ข้อนี้ไม่ต้องทำก็ได้ ไม่มีผลลบกับการให้คะแนน แต่ถ้าทำมาเเล้วเจ๋งจริง ก็จะพิจารณาเป็นพิเศษ

"""


"""
เป็นตัวอย่าง code ที่เคยเขียนไว้ในโปรเจค iot เพื่อส่งข้อมูลจาก MQTT ไปที่ InfluxDB
"""


def send_rpi_info(rpi_data):

    json_body = [{
        'measurement': "rpi_data",
        'tags': {
            'device_serial_number': rpi_data['device_serial_number'],
        },
        'fields': {
            # "cmd": "info",
            "cpu_temp": float(rpi_data['cpu_temp'].replace("'C", "")),
            "cpu_freq": float(rpi_data['cpu_freq'].replace("'C", "")),
            "voltage": float(rpi_data['voltage'].replace("V", "")),
            "arm_memory": int(rpi_data['arm_memory'].replace("M", "")),
            "cpu_memory": int(rpi_data['cpu_memory'].replace("M", "")),
            "cpu_serial_number": rpi_data['cpu_serial_number'],
            # "device_serial_number": rpi_data['device_serial_number'],
            "hardware": rpi_data['hardware'],
            "rtl_sdr": rpi_data['rtl_sdr'],
            "mac_address": rpi_data['mac_address'],
            # "time": rpi_data['time'],
        }
    }]
    write_api.write(bucket=bucket, org=org, record=json_body)


def send_nbtc_data(sound, device_serial_number):
    json_body = [{
        'measurement': "nbtc_data",
        'tags': {
            'device_serial_number': device_serial_number,
            'type': 'nbtc',
            # 'pk': sound[-19:-4],
        },
        'fields': {
            'device_serial_number': device_serial_number,
            "file": sound,
            # "time": datetime,
        },
    }]
    write_api.write(bucket=bucket, org=org, record=json_body)
    response = requests.get(
        f'https://fm-mon.nbtc.go.th/monitoring/api/send-notification/{device_serial_number}', 
    )


def send_carrier_data(sound, device_serial_number):
    json_body = [{
        'measurement': "nbtc_data",
        'tags': {
            'device_serial_number': device_serial_number,
            'type': 'carrier',
            # 'pk': sound[-19:-4],
        },
        'fields': {
            'device_serial_number': device_serial_number,
            "file": sound,
            # "time": datetime,
        },
    }]
    write_api.write(bucket=bucket, org=org, record=json_body)

def send_screenshots_data(sound, device_serial_number):
    json_body = [{
        'measurement': "nbtc_data",
        'tags': {
            'device_serial_number': device_serial_number,
            'type': 'img',
            # 'pk': sound[-19:-4],
        },
        'fields': {
            'device_serial_number': device_serial_number,
            "file": sound,
            # "time": datetime,
        },
    }]
    write_api.write(bucket=bucket, org=org, record=json_body)


def send_record_carrier_data(sound, device_serial_number):
    json_body = [{
        'measurement': "record_carrier",
        'tags': {
            'device_serial_number': device_serial_number,
            'type': 'carrier',
            # 'pk': sound[-19:-4],
        },
        'fields': {
            'device_serial_number': device_serial_number,
            "file": sound,
            # "time": datetime,
        },
    }]
    write_api.write(bucket=bucket, org=org, record=json_body)


def send_carrier_screenshots_data(sound, device_serial_number):
    json_body = [{
        'measurement': "record_carrier",
        'tags': {
            'device_serial_number': device_serial_number,
            'type': 'img',
            # 'pk': sound[-19:-4],
        },
        'fields': {
            'device_serial_number': device_serial_number,
            "file": sound,
            # "time": datetime,
        },
    }]
    write_api.write(bucket=bucket, org=org, record=json_body)

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("/nbtc/aero-radio-monitor/cmd-response/#")
    # self.subscribe("/nbtc/aero-radio-monitor/set-frequency/#")

def process_info_message(data):
    try:
        time.sleep(1)
        send_rpi_info(data)
    except:
        print("Error sending rpi info to influxdb")

def process_record(msg, sound, device_serial_number):
    try:
        with open("../monitoring/media/sound/record/{}".format(sound), "wb") as f:
             f.write(msg.payload)
        send_nbtc_data(sound, device_serial_number)
    except:
        print("Error sending nbtc data to influxdb")

def process_carrier(msg, sound, device_serial_number):
    try:
        with open("../monitoring/media/sound/carrier/{}".format(sound), "wb") as f:
                f.write(msg.payload)
        send_carrier_data(sound, device_serial_number)
    except:
        print("Error sending nbtc data to influxdb")

def process_screenshots(msg, sound, device_serial_number):
    try:
        with open("../monitoring/media/img/screenshots/{}".format(sound), "wb") as f:
                f.write(msg.payload.replace(sound.encode(), b''))
        send_screenshots_data(sound, device_serial_number)
    except:
        print("Error sending nbtc data to influxdb")


def process_record_carrier(msg, sound, device_serial_number):
    try:
        with open("../monitoring/media/sound/carrier/{}".format(sound), "wb") as f:
            f.write(msg.payload)
        send_record_carrier_data(sound, device_serial_number)
    except:
        print("Error sending nbtc data to influxdb")

def process_carrier_screenshots(msg, sound, device_serial_number):
    try:
        with open("../monitoring/media/img/screenshots/{}".format(sound), "wb") as f:
                f.write(msg.payload.replace(sound.encode(), b''))
        send_carrier_screenshots_data(sound, device_serial_number)
    except:
        print("Error sending nbtc data to influxdb")

def on_message(client, userdata,msg):
    # print(msg.payload.decode("utf-8", "strict"))
    print(msg.topic)

    if msg.topic == "/nbtc/aero-radio-monitor/cmd-response/info/":
        data = json.loads(msg.payload)
        thread = threading.Thread(target=process_info_message, args=(data,))
        thread.start()

    if msg.topic == "/nbtc/aero-radio-monitor/cmd-response/record/":
        sound = msg.payload[:55].decode("utf-8", "strict")
        device_serial_number = msg.payload[-21:].decode("utf-8", "strict")
        thread = threading.Thread(target=process_record, args=(msg, sound,device_serial_number))
        thread.start()
        
    if msg.topic == "/nbtc/aero-radio-monitor/cmd-response/carrier/":
        sound = msg.payload[:41].decode("utf-8", "strict")
        device_serial_number = msg.payload[-21:].decode("utf-8", "strict")
        thread = threading.Thread(target=process_carrier, args=(msg, sound,device_serial_number))
        thread.start()
    
    if msg.topic == "/nbtc/aero-radio-monitor/cmd-response/screenshots/":
        sound = msg.payload[:41].decode("utf-8", "strict")
        device_serial_number = msg.payload[-21:].decode("utf-8", "strict")
        thread = threading.Thread(target=process_screenshots, args=(msg, sound,device_serial_number))
        thread.start()
    
    if msg.topic == "/nbtc/aero-radio-monitor/cmd-response/record-carrier/":
        sound = msg.payload[:41].decode("utf-8", "strict")
        device_serial_number = msg.payload[-21:].decode("utf-8", "strict")
        thread = threading.Thread(target=process_record_carrier, args=(msg, sound,device_serial_number))
        thread.start()
    
    if msg.topic == "/nbtc/aero-radio-monitor/cmd-response/carrier-screenshots/":
        sound = msg.payload[:41].decode("utf-8", "strict")
        device_serial_number = msg.payload[-21:].decode("utf-8", "strict")
        thread = threading.Thread(target=process_carrier_screenshots, args=(msg, sound,device_serial_number))
        thread.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()