import visa
import time

def main():
    rm = visa.ResourceManager()
    device_name = rm.list_resources()[0]

    dev = rm.open_resource(device_name, read_termination='\r', send_end=True)

    print dev.query('*IDN?')


if __name__=='__main__':
    main()

