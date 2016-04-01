import visa
import time

def main():
    rm = visa.ResourceManager()
    device_name = rm.list_resources()[0]

    dev = rm.open_resource(device_name, read_termination='\r', send_end=True)

    print dev.query('*IDN?')

    with open('output.txt', 'w') as f:
        for i in range(100):
            time.sleep(0.1)
            f.write(dev.ask('READ?')+'\n')
            f.flush()


if __name__=='__main__':
    main()

