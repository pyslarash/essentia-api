import tensorflow as tf 

def detect_device():
    """
    Detect whether TensorFlow is using a GPU and print its details.
    """
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("\033[1;32mGPU detected!\033[0m")
        print("Using the following GPU(s):")
        for gpu in gpus:
            # Get detailed GPU information
            details = tf.config.experimental.get_device_details(gpu)
            device_name = details.get('device_name', 'Unknown GPU')
            print(f"\033[1m🤖 {device_name}\033[0m")
    else:
        print("\033[1;31mNo GPU detected. TensorFlow will use the CPU.\033[0m")