import serial
from adafruit_fingerprint import Adafruit_Fingerprint

class FingerprintScanner:
    def __init__(self, port="/dev/ttyS0", baudrate=57600, timeout=1):
        try:
            # Set up serial communication with the fingerprint sensor
            self.uart = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            # Initialize the fingerprint sensor with the serial connection
            self.fingerprint_sensor = Adafruit_Fingerprint(self.uart)

            if self.fingerprint_sensor.read_templates() < 0:
                raise RuntimeError("Failed to read fingerprint templates from the sensor.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize fingerprint scanner: {e}")

    def capture_fingerprint(self):
        """Capture a fingerprint and return the template."""
        try:
            print("Waiting for finger...")

            while self.fingerprint_sensor.get_image() != Adafruit_Fingerprint.OK:
                pass

            if self.fingerprint_sensor.image_2_tz(1) != Adafruit_Fingerprint.OK:
                print("Error: Could not convert image to template.")
                return None

            # Check if fingerprint already exists in the sensor memory
            if self.fingerprint_sensor.finger_search() != Adafruit_Fingerprint.NOTFOUND:
                print(f"Fingerprint already exists.")
                return None

            # Store the fingerprint in the sensor memory
            if self.fingerprint_sensor.store_model(1) != Adafruit_Fingerprint.OK:
                print("Error: Could not store fingerprint template.")
                return None

            # Download the characteristics (template) from the sensor
            fingerprint_template = self.fingerprint_sensor.get_fpdata("char", 1)
            return fingerprint_template

        except Exception as e:
            print(f"Failed to capture fingerprint: {e}")
            return None

    def compare_fingerprint(self, stored_fingerprint):
        """Compare a captured fingerprint against a stored template."""
        try:
            print("Waiting for finger...")

            while self.fingerprint_sensor.get_image() != Adafruit_Fingerprint.OK:
                pass

            if self.fingerprint_sensor.image_2_tz(1) != Adafruit_Fingerprint.OK:
                print("Error: Could not convert image to template.")
                return False

            # Upload the stored fingerprint template to the sensor
            if self.fingerprint_sensor.upload_fpdata(stored_fingerprint, "char", 2) != Adafruit_Fingerprint.OK:
                print("Error: Could not upload fingerprint template.")
                return False

            # Compare the stored template with the newly captured template
            if self.fingerprint_sensor.compare_templates() == 0:
                print("Fingerprints match!")
                return True
            else:
                print("Fingerprints do not match.")
                return False

        except Exception as e:
            print(f"Failed to compare fingerprints: {e}")
            return False
