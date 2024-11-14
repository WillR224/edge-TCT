import time
import os
import sys



try:
    import libximc.highlevel as ximc
    print("Use libximc {} that has been found among the pip installed packages".format(ximc.ximc_version()))
except ImportError:
    print("Warning! libximc cannot be found among the pip installed packages. Did you forget to install it via pip?\n"
          "Trying to import the library using relative path: ../../../ximc/crossplatform/wrappers/python ...")
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    ximc_dir = os.path.join(cur_dir, "ximc-2.14.27","ximc")
    ximc_package_dir = os.path.join(ximc_dir, "crossplatform", "wrappers", "python")
    print(ximc_package_dir)
    sys.path.append(ximc_package_dir)
    import libximc.highlevel as ximc
    print("Success!")

print("Library version: " + ximc.ximc_version())







def move(axis: ximc.Axis, distance: int, udistance: int) -> None:
    print("\nGoing to {0} steps, {1} microsteps".format(distance, udistance))
    axis.command_move(distance, udistance)

def status(axis: ximc.Axis) -> None:
    print("\nGet status")
    status = axis.get_status()
    print("Status.Ipwr: {}".format(status.Ipwr))
    print("Status.Upwr: {}".format(status.Upwr))
    print("Status.Iusb: {}".format(status.Iusb))
    print("Status.Flags: {}".format(status.Flags))






enum_flags = ximc.EnumerateFlags.ENUMERATE_PROBE | ximc.EnumerateFlags.ENUMERATE_NETWORK

enum_hints = "addr="
devenum = ximc.enumerate_devices(enum_flags, enum_hints)
print("Device count: {}".format(len(devenum)))
print("Found devices:\n", devenum)

flag_virtual = 0

open_name = None
if len(sys.argv) > 1:
    open_name = sys.argv[1]
    print("open_name = ", open_name)
elif len(devenum) > 0:
    open_name = devenum[0]["uri"]
    print("open_name = ", open_name)
else:
    tempdir = os.path.join(os.path.expanduser('~'), "testdevice.bin")
    open_name = "xi-emu:///" + tempdir
    flag_virtual = 1
    print("The real controller is not found or busy with another app.")
    print("The virtual controller is opened to check the operation of the library.")
    print("If you want to open a real controller, connect it or close the application that uses it.")
    print("open_name = ", open_name)





axis = ximc.Axis(open_name)
print("\nOpen device " + axis.uri)
axis.open_device()




status(axis)
move(axis,10,0)
